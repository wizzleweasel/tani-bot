"""Synthetic Data Generator for Indonesian Crops"""

import random
from typing import List, Dict
from datetime import datetime, timedelta


# Indonesian crop database
CROPS = {
    "staples": [
        {"name": "Rice (Padi)", "scientific": "Oryza sativa", "season_days": 120, "base_yield": 6.5, "rainfall_min": 100, "rainfall_max": 300},
        {"name": "Corn (Jagung)", "scientific": "Zea mays", "season_days": 90, "base_yield": 7.0, "rainfall_min": 50, "rainfall_max": 200},
        {"name": "Cassava (Singkong)", "scientific": "Manihot esculenta", "season_days": 180, "base_yield": 25.0, "rainfall_min": 50, "rainfall_max": 250},
        {"name": "Sweet Potato (Ubi Jalar)", "scientific": "Ipomoea batatas", "season_days": 100, "base_yield": 20.0, "rainfall_min": 75, "rainfall_max": 200}
    ],
    "fruits": [
        {"name": "Durian", "scientific": "Durio zibethinus", "season_days": 270, "base_yield": 15.0, "rainfall_min": 150, "rainfall_max": 300},
        {"name": "Mango (Mangga)", "scientific": "Mangifera indica", "season_days": 210, "base_yield": 20.0, "rainfall_min": 100, "rainfall_max": 250},
        {"name": "Banana (Pisang)", "scientific": "Musa spp.", "season_days": 150, "base_yield": 30.0, "rainfall_min": 100, "rainfall_max": 250},
        {"name": "Rambutan", "scientific": "Nephelium lappaceum", "season_days": 240, "base_yield": 12.0, "rainfall_min": 150, "rainfall_max": 300},
        {"name": "Mangosteen", "scientific": "Garcinia mangostana", "season_days": 300, "base_yield": 8.0, "rainfall_min": 200, "rainfall_max": 400},
        {"name": "Papaya", "scientific": "Carica papaya", "season_days": 120, "base_yield": 35.0, "rainfall_min": 75, "rainfall_max": 200}
    ],
    "vegetables": [
        {"name": "Chili (Cabe)", "scientific": "Capsicum annuum", "season_days": 90, "base_yield": 3.0, "rainfall_min": 50, "rainfall_max": 150},
        {"name": "Shallot (Bawang Merah)", "scientific": "Allium cepa", "season_days": 75, "base_yield": 12.0, "rainfall_min": 50, "rainfall_max": 150},
        {"name": "Tomato", "scientific": "Solanum lycopersicum", "season_days": 80, "base_yield": 25.0, "rainfall_min": 75, "rainfall_max": 200},
        {"name": "Cabbage (Kubis)", "scientific": "Brassica oleracea", "season_days": 85, "base_yield": 20.0, "rainfall_min": 75, "rainfall_max": 175},
        {"name": "Spinach (Bayam)", "scientific": "Spinacia oleracea", "season_days": 40, "base_yield": 10.0, "rainfall_min": 50, "rainfall_max": 150}
    ],
    "industrial": [
        {"name": "Palm Oil (Kelapa Sawit)", "scientific": "Elaeis guineensis", "season_days": 365, "base_yield": 18.0, "rainfall_min": 200, "rainfall_max": 400},
        {"name": "Rubber (Karet)", "scientific": "Hevea brasiliensis", "season_days": 300, "base_yield": 2.5, "rainfall_min": 150, "rainfall_max": 350},
        {"name": "Cocoa (Cokelat)", "scientific": "Theobroma cacao", "season_days": 270, "base_yield": 1.5, "rainfall_min": 150, "rainfall_max": 300},
        {"name": "Coffee (Kopi)", "scientific": "Coffea arabica/robusta", "season_days": 240, "base_yield": 1.0, "rainfall_min": 150, "rainfall_max": 300}
    ]
}

# Indonesian provinces
PROVINCES = [
    "Jawa Barat", "Jawa Tengah", "Jawa Timur", "DKI Jakarta", "DI Yogyakarta",
    "Banten", "Sumatera Utara", "Sumatera Barat", "Sumatera Selatan", "Lampung",
    "Kalimantan Barat", "Kalimantan Tengah", "Kalimantan Selatan", "Kalimantan Timur",
    "Sulawesi Utara", "Sulawesi Tengah", "Sulawesi Selatan", "Sulawesi Tenggara",
    "Bali", "Nusa Tenggara Barat", "Nusa Tenggara Timur", "Maluku", "Papua"
]

# Major cities with coordinates
CITIES = {
    "Jakarta": (-6.2088, 106.8456),
    "Bandung": (-6.9175, 107.6191),
    "Surabaya": (-7.2575, 112.7521),
    "Yogyakarta": (-7.7956, 110.3695),
    "Semarang": (-6.9667, 110.4167),
    "Medan": (3.5952, 98.6722),
    "Makassar": (-5.1477, 119.4327),
    "Denpasar": (-8.6705, 115.2126),
    "Padang": (-0.9471, 100.4172),
    "Palembang": (-2.9761, 104.7754)
}


class SyntheticDataGenerator:
    """Generate synthetic agricultural data for Indonesia"""
    
    def __init__(self, seed: int = 42):
        random.seed(seed)
    
    def generate_random_field(self, province: str = None) -> Dict:
        """Generate a random field in Indonesia"""
        if province:
            prov = province
        else:
            prov = random.choice(PROVINCES)
        
        # Use city coordinates as base, add random offset
        if CITIES:
            city = random.choice(list(CITIES.keys()))
            base_lat, base_lon = CITIES[city]
            lat = base_lat + random.uniform(-0.5, 0.5)
            lon = base_lon + random.uniform(-0.5, 0.5)
        else:
            lat = random.uniform(-11, 6)  # Indonesia lat range
            lon = random.uniform(95, 141)  # Indonesia lon range
        
        return {
            "location_name": f"Field_{random.randint(1000, 9999)}",
            "province": prov,
            "city": city if CITIES else "Unknown",
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "area_hectares": round(random.uniform(0.5, 50), 2),
            "soil_type": random.choice(["Andosol", "Latosol", "Regosol", "Aluvial", "Podsol"]),
            "soil_ph": round(random.uniform(5.0, 7.5), 2),
            "elevation": random.randint(0, 1500)
        }
    
    def generate_crop_data(self, category: str = None) -> List[Dict]:
        """Generate crop data"""
        if category:
            crops = CROPS.get(category, [])
        else:
            crops = []
            for cat_crops in CROPS.values():
                crops.extend(cat_crops)
        
        return [
            {
                "name": crop["name"],
                "category": category if category else random.choice(list(CROPS.keys())),
                "scientific_name": crop["scientific"],
                "growing_season_days": crop["season_days"],
                "base_yield": crop["base_yield"],
                "rainfall_min": crop["rainfall_min"],
                "rainfall_max": crop["rainfall_max"]
            }
            for crop in crops
        ]
    
    def generate_weather_data(self, lat: float, lon: float, days: int = 365) -> List[Dict]:
        """Generate synthetic weather data"""
        weather_data = []
        
        # Base climate data based on latitude (tropical)
        base_temp = 26 + random.uniform(-2, 2)
        base_rainfall = 150 + random.uniform(-50, 100)  # Monthly rainfall
        
        for i in range(days):
            date = datetime.now() - timedelta(days=days - i)
            
            # Seasonal variation
            month = date.month
            seasonal_factor = 1.0 if month in [3, 4, 5, 9, 10, 11] else 0.7  # Wet season
            
            weather_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "temperature_avg": round(base_temp + random.uniform(-2, 2), 1),
                "temperature_max": round(base_temp + 3 + random.uniform(-1, 2), 1),
                "temperature_min": round(base_temp - 3 + random.uniform(-2, 1), 1),
                "humidity_avg": round(75 + random.uniform(-10, 10), 1),
                "rainfall_mm": round(max(0, base_rainfall * seasonal_factor * random.uniform(0.5, 1.5) / 30), 1),
                "wind_speed_avg": round(3 + random.uniform(-1, 2), 1)
            })
        
        return weather_data
    
    def generate_field_history(self, field: Dict, years: int = 3) -> List[Dict]:
        """Generate historical planting data for a field"""
        history = []
        crops = self.generate_crop_data()
        
        for year in range(years):
            for crop in random.sample(crops, k=min(2, len(crops))):
                # Random planting date
                month = random.randint(1, 12)
                day = random.randint(1, 28)
                planting_date = datetime.now().replace(year=2024 - years + year, month=month, day=day)
                
                season_days = crop["growing_season_days"]
                harvest_date = planting_date + timedelta(days=season_days)
                
                # Yield with some variation
                base_yield = crop["base_yield"]
                yield_var = random.uniform(0.7, 1.3)
                yield_value = base_yield * yield_var
                
                history.append({
                    "crop_id": None,  # Would reference crops table
                    "crop_name": crop["name"],
                    "planting_date": planting_date.strftime("%Y-%m-%d"),
                    "harvest_date": harvest_date.strftime("%Y-%m-%d"),
                    "yield_value": round(yield_value, 2),
                    "yield_unit": "ton/hectare",
                    "notes": f"Season {year + 1}, Year {2024 - years + year}"
                })
        
        return history
    
    def generate_all_synthetic_data(self, num_fields: int = 10) -> Dict:
        """Generate comprehensive synthetic dataset"""
        fields = [self.generate_random_field() for _ in range(num_fields)]
        crops = self.generate_crop_data()
        
        return {
            "fields": fields,
            "crops": crops,
            "generated_at": datetime.now().isoformat(),
            "num_fields": num_fields
        }


# Example usage
if __name__ == "__main__":
    generator = SyntheticDataGenerator()
    
    print("=== Sample Field ===")
    field = generator.generate_random_field("Jawa Barat")
    print(field)
    
    print("\n=== Sample Crops ===")
    crops = generator.generate_crop_data("staples")
    for crop in crops:
        print(f"- {crop['name']} ({crop['scientific_name']})")
    
    print("\n=== Sample Weather Data (3 days) ===")
    weather = generator.generate_weather_data(-6.2088, 106.8456, days=3)
    for w in weather:
        print(f"{w['date']}: {w['temperature_avg']}°C, {w['rainfall_mm']}mm rain")
