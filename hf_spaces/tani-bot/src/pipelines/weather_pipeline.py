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
        url = f"{self.NASA_POWER_BASE}/single"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start": start_date,
            "end": end_date,
            "parameters": "ALLSKY_SFC_SW_DOWNSOLAR,PRECTOT_CORR",  # Solar radiation, precipitation
            "format": "json",
            "lonLat": "true",
            "sources": "NASA_POWER"
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
        
        return {
            "location": location_name,
            "coordinates": {"lat": latitude, "lon": longitude},
            "current": current.get("current", {}),
            "forecast": forecast.get("daily", {}),
            "timestamp": datetime.now().isoformat()
        }
    
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
