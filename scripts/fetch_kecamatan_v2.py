#!/usr/bin/env python3
"""
Fetch all Kecamatan/Kelurahan in Indonesia
Using multiple fallback sources
"""

import requests
import json
from typing import List, Dict, Optional

def fetch_from_alternate_source() -> Optional[Dict]:
    """Try alternative GitHub source"""
    
    sources = [
        "https://raw.githubusercontent.com/rahasia/data-kecamatan-indonesia/master/kecamatan.json",
        "https://raw.githubusercontent.com/fajar2402/indonesia-geography/master/data/kecamatan.json",
        "https://raw.githubusercontent.com/lapov/indonesia-geography/master/kecamatan.json",
    ]
    
    for url in sources:
        try:
            print(f"Trying: {url}")
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    print(f"✅ Success! Got {len(data)} entries")
                    return data
        except Exception as e:
            print(f"  Failed: {e}")
    
    return None

def normalize_data(data: List[Dict]) -> Dict:
    """Normalize different data formats to unified format"""
    
    location_db = {}
    
    for item in data:
        # Try different field names
        name = item.get('nama', item.get('name', item.get('kecamatan', '')))
        lat = item.get('latitude', item.get('lat', 0))
        lon = item.get('longitude', item.get('lon', 0))
        prov = item.get('provinsi', item.get('province', ''))
        kota = item.get('kabupaten', item.get('city', ''))
        
        if name:
            # Format: "kecamatan, city, province"
            location_key = f"{name}, {kota}, {prov}"
            
            location_db[location_key] = {
                "lat": float(lat) if lat else 0,
                "lon": float(lon) if lon else 0
            }
    
    return location_db

def generate_sample_data() -> Dict:
    """Generate sample data if API fails"""
    print("⚠️ Using sample data (API failed)")
    
    # Sample data for major cities
    return {
        "Pacet, Mojokerto, Jawa Timur": {"lat": -7.5333, "lon": 112.4333},
        "Bandung Wetan, Bandung, Jawa Barat": {"lat": -6.9175, "lon": 107.6191},
        "Jakarta Pusat, Jakarta Pusat, DKI Jakarta": {"lat": -6.1862, "lon": 106.8341},
        "Sleman, Sleman, DIY": {"lat": -7.7000, "lon": 110.3500},
        "Denpasar Barat, Denpasar, Bali": {"lat": -8.6705, "lon": 115.2126},
        "Medan Kota, Medan, Sumatera Utara": {"lat": 3.5952, "lon": 98.6722},
        "Makassar, Makassar, Sulawesi Selatan": {"lat": -5.1477, "lon": 119.4327},
    }

def save_to_json(db: Dict, output_file: str = "datasets/kecamatan_database.json"):
    """Save database to JSON file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved to {output_file}")
    print(f"📊 Total: {len(db)} locations")

def save_as_python(db: Dict, output_file: str):
    """Save as Python module with optimized lookup"""
    
    # Create optimized version with binary search
    sorted_keys = sorted(db.keys())
    
    content = f'''"""Optimized Kecamatan Database with Binary Search"""
import bisect

# All kecamatan data
LOCATION_DB = {json.dumps(db, ensure_ascii=False)}

# Sorted keys for binary search
_SORTED_KEYS = {sorted_keys}

def get_location_coords(location_query: str):
    """Get coordinates using binary search"""
    location_query = location_query.strip().lower()
    index = bisect.bisect_left(_SORTED_KEYS, location_query)
    
    # Check exact match
    if index < len(_SORTED_KEYS) and _SORTED_KEYS[index].lower() == location_query:
        loc = LOCATION_DB[_SORTED_KEYS[index]]
        return loc["lat"], loc["lon"]
    
    # Check partial match (first character)
    if index < len(_SORTED_KEYS):
        key = _SORTED_KEYS[index]
        if key.lower().startswith(location_query[:3]):
            loc = LOCATION_DB[key]
            return loc["lat"], loc["lon"]
    
    return None, None

def get_location_suggestions(search_term: str, max_results: int = 20):
    """Get autocomplete suggestions"""
    if not search_term:
        return []
    
    search_lower = search_term.lower()
    suggestions = []
    
    for key in _SORTED_KEYS:
        if search_lower in key.lower():
            suggestions.append(key)
            if len(suggestions) >= max_results:
                break
    
    return suggestions
'''
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Saved optimized Python module to {output_file}")

def main():
    print("=" * 60)
    print("🇮🇩 Fetching All Kecamatan in Indonesia")
    print("=" * 60)
    
    # Try to fetch from API
    data = fetch_from_alternate_source()
    
    if data:
        location_db = normalize_data(data)
    else:
        # Generate sample data
        location_db = generate_sample_data()
    
    # Save to JSON
    save_to_json(location_db)
    
    # Save as optimized Python module
    save_as_python(location_db, "hf_spaces/tani-bot/src/data/kecamatan_db_full.py")
    
    print("\n✅ Complete!")

if __name__ == "__main__":
    main()
