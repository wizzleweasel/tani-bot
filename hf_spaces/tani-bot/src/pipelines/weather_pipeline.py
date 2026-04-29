"""Weather Data Pipeline - Open-Meteo + NASA POWER"""

import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import json


class WeatherPipeline:
    """Pipeline for fetching weather data from Open-Meteo and NASA POWER"""
    
    OPEN_METEO_BASE = "https://api.open-meteo.com/v1"
    NASA_POWER_BASE = "https://power.larc.nasa.gov/api"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        
    def fetch_current_weather(self, latitude: float, longitude: float) -> Dict:
        """Fetch current weather for a location"""
        url = f"{self.OPEN_METEO_BASE}/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m",
            "timezone": "auto"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching weather: {e}")
            return {}
    
    def fetch_forecast(self, latitude: float, longitude: float, days: int = 7) -> Dict:
        """Fetch weather forecast"""
        url = f"{self.OPEN_METEO_BASE}/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,sunshine_duration,weather_code",
            "timezone": "auto",
            "forecast_days": days
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching forecast: {e}")
            return {}
    
    def fetch_nasa_power(self, latitude: float, longitude: float, start_date: str, end_date: str) -> Dict:
        """Fetch solar radiation and other data from NASA POWER"""
        url = f"{self.NASA_POWER_BASE}/temporal/daily"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start": start_date,
            "end": end_date,
            "parameters": "T2M_MAX,T2M_MIN,PRECTOT_CORR,T2M",
            "format": "json",
            "lonLat": "true",
            "sources": "MERRA2"
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching NASA POWER data: {e}")
            return {}
    
    def get_weather_for_location(self, latitude: float, longitude: float, 
                                   location_name: str = "Unknown") -> Dict:
        """Get comprehensive weather data for a location"""
        current = self.fetch_current_weather(latitude, longitude)
        forecast = self.fetch_forecast(latitude, longitude)
        extended = self.generate_extended_forecast(latitude, longitude, historical_days=90)
        
        return {
            "location": location_name,
            "coordinates": {"lat": latitude, "lon": longitude},
            "current": current.get("current", {}),
            "forecast_7day": forecast.get("daily", {}),
            "forecast_30day": extended,
            "timestamp": datetime.now().isoformat()
        }
    
    def calculate_ema(self, values: list, period: int = 3) -> list:
        """Calculate Exponential Moving Average for weather forecast"""
        if not values or len(values) < period:
            return values
        
        ema = [values[0]]
        alpha = 2 / (period + 1)
        
        for i in range(1, len(values)):
            ema_val = ema[-1] * (1 - alpha) + values[i] * alpha
            ema.append(ema_val)
        
        return ema
    
    def generate_extended_forecast(self, lat: float, lon: float, historical_days: int = 90) -> Dict:
        """Generate extended forecast using historical data + EMA"""
        import math
        from datetime import datetime, timedelta
        
        # Get historical data from NASA POWER
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=historical_days)).strftime("%Y-%m-%d")
        
        historical = self.fetch_nasa_power(lat, lon, start_date, end_date)
        
        if not historical or 'properties' not in historical:
            # Fallback: generate synthetic extended forecast
            return self._generate_synthetic_extended_forecast(lat, lon, historical_days)
        
        properties = historical['properties']
        dates = properties.get('time', [])
        temps_max = properties.get('T2M_MAX', [])
        temps_min = properties.get('T2M_MIN', [])
        precip = properties.get('PRECTOT_CORR', [])
        
        # Calculate EMA for next 30 days
        if temps_max and len(temps_max) >= 7:
            ema_max = self.calculate_ema(temps_max[-7:], period=3)
            ema_min = self.calculate_ema(temps_min[-7:], period=3)
            ema_precip = self.calculate_ema([p if p else 0 for p in precip[-7:]], period=3)
        else:
            # Use simple average if not enough data
            ema_max = [sum(temps_max[-7:]) / 7] * 30 if temps_max else [28.0] * 30
            ema_min = [sum(temps_min[-7:]) / 7] * 30 if temps_min else [22.0] * 30
            ema_precip = [sum([p if p else 0 for p in precip[-7:]]) / 7] * 30 if precip else [5.0] * 30
        
        # Generate 30-day forecast
        extended_forecast = {
            'time': [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 31)],
            'temperature_2m_max': [round(e, 1) for e in ema_max[:30]],
            'temperature_2m_min': [round(e, 1) for e in ema_min[:30]],
            'precipitation_sum': [round(e, 1) for e in ema_precip[:30]]
        }
        
        return extended_forecast
    
    def _generate_synthetic_extended_forecast(self, lat: float, lon: float, days: int) -> Dict:
        """Generate synthetic extended forecast based on climate normals"""
        from datetime import datetime, timedelta
        
        # Approximate climate normals for Indonesia (tropical)
        base_temp_max = 30.0 + (lat * 0.1)  # Slightly cooler at higher latitudes
        base_temp_min = 23.0 + (lat * 0.1)
        base_precip = 5.0  # Tropical rainfall
        
        forecast = {
            'time': [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, days + 1)],
            'temperature_2m_max': [round(base_temp_max + (math.sin(i/7) * 2), 1) for i in range(1, days + 1)],
            'temperature_2m_min': [round(base_temp_min + (math.sin(i/7) * 1.5), 1) for i in range(1, days + 1)],
            'precipitation_sum': [round(base_precip + (math.sin(i/3) * 3), 1) for i in range(1, days + 1)]
        }
        
        return forecast
    
    def save_weather_data(self, weather_data: Dict, db_client: Optional[any] = None):
        """Save weather data to database (if client provided)"""
        if db_client:
            # TODO: Implement database save
            pass
        else:
            print(f"Weather data for {weather_data.get('location')}:")
            print(json.dumps(weather_data, indent=2))


# Example usage
if __name__ == "__main__":
    pipeline = WeatherPipeline()
    
    # Example: Jakarta coordinates
    weather = pipeline.get_weather_for_location(-6.2088, 106.8456, "Jakarta")
    print(json.dumps(weather, indent=2))
