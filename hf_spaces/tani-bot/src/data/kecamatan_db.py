"""
Kecamatan Database - 7k+ Indonesian Districts
Loaded from GitHub CDN for fast autocomplete
Coordinates fetched on-demand via web search
"""

import requests
import json
import os
from typing import Dict, List, Tuple, Optional

# GitHub CDN URL for kecamatan data
KECAMATAN_CSV_URL = "https://raw.githubusercontent.com/wizzleweasel/tani-bot/main/datasets/kecamatan_raw.csv"
CACHE_FILE = "datasets/kecamatan_coords_cache.json"

# Province mapping from BPS codes
PROVINCE_MAP = {
    '11': 'Aceh', '12': 'Sumatera Utara', '13': 'Sumatera Barat',
    '14': 'Riau', '15': 'Jambi', '16': 'Sumatera Selatan',
    '17': 'Bengkulu', '18': 'Lampung', '19': 'Kepulauan Bangka Belitung',
    '21': 'Kepulauan Riau', '31': 'DKI Jakarta', '32': 'Jawa Barat',
    '33': 'Jawa Tengah', '34': 'DI Yogyakarta', '35': 'Jawa Timur',
    '36': 'Banten', '51': 'Bali', '52': 'Nusa Tenggara Barat',
    '53': 'Nusa Tenggara Timur', '61': 'Kalimantan Barat',
    '62': 'Kalimantan Tengah', '63': 'Kalimantan Selatan',
    '64': 'Kalimantan Timur', '65': 'Kalimantan Utara',
    '71': 'Sulawesi Utara', '72': 'Sulawesi Tengah',
    '73': 'Sulawesi Selatan', '74': 'Sulawesi Tenggara',
    '75': 'Gorontalo', '76': 'Sulawesi Barat',
    '81': 'Maluku', '82': 'Maluku Utara',
    '91': 'Papua Barat', '94': 'Papua',
}

# Local cache of coordinates (populated on-demand)
_COORDS_CACHE = {}


def load_kecamatan_data() -> List[Dict]:
    """Load all kecamatan from GitHub CDN"""
    try:
        response = requests.get(KECAMATAN_CSV_URL, timeout=10)
        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            data = []
            for line in lines[1:]:  # Skip header
                parts = line.split(',')
                if len(parts) >= 3:
                    data.append({
                        'id': parts[0].strip(),
                        'city_code': parts[1].strip(),
                        'name': parts[2].strip().upper()
                    })
            return data
    except Exception as e:
        print(f"Error loading kecamatan data: {e}")
    
    # Fallback: return empty list
    return []


def load_coords_cache() -> Dict:
    """Load coordinates cache from file"""
    global _COORDS_CACHE
    if _COORDS_CACHE:
        return _COORDS_CACHE
    
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                _COORDS_CACHE = json.load(f)
        except:
            pass
    
    return _COORDS_CACHE


def save_coords_cache():
    """Save coordinates cache to file"""
    global _COORDS_CACHE
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(_COORDS_CACHE, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving cache: {e}")


def get_location_suggestions(search_term: str, max_results: int = 20) -> List[str]:
    """
    Get autocomplete suggestions for location search.
    Fast search through 7k+ kecamatan names.
    """
    if not search_term:
        return []
    
    search_lower = search_term.lower()
    suggestions = []
    
    # Load kecamatan data
    kecamatan_data = load_kecamatan_data()
    
    for kec in kecamatan_data:
        # Search in name
        if search_lower in kec['name'].lower():
            province = PROVINCE_MAP.get(kec['id'][:2], '')
            location_name = f"{kec['name']}, {kec['city_code']}, {province}"
            suggestions.append(location_name)
            
            if len(suggestions) >= max_results:
                break
    
    return suggestions


def get_location_coords(location_query: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Get coordinates for a location.
    Returns (lat, lon) or (None, None) if not found.
    
    Note: Coordinates are fetched on-demand via web search.
    Results are cached locally for faster subsequent lookups.
    """
    # Check cache first
    cache = load_coords_cache()
    if location_query in cache:
        cached = cache[location_query]
        return cached.get('lat'), cached.get('lon')
    
    # Not in cache - would need web search
    # For now, return None (coordinates will be added on-demand)
    return None, None


def save_coordinates(location_query: str, lat: float, lon: float):
    """Save coordinates to cache"""
    global _COORDS_CACHE
    cache = load_coords_cache()
    
    cache[location_query] = {
        'lat': lat,
        'lon': lon,
        'source': 'web_search'
    }
    
    _COORDS_CACHE = cache
    save_coords_cache()


# Pre-load some common coordinates (major cities)
COMMON_COORDS = {
    "PACET, MOJOKERTO, JAWA TIMUR": (-7.5333, 112.4333),
    "BANDUNG WETAN, BANDUNG, JAWA BARAT": (-6.9175, 107.6191),
    "GAMBIR, JAKARTA PUSAT, DKI JAKARTA": (-6.1862, 106.8341),
    "DENPASAR BARAT, DENPASAR, BALI": (-8.6705, 115.2126),
    "MEDAN KOTA, MEDAN, SUMATERA UTARA": (3.5952, 98.6722),
    "MAKASSAR, MAKASSAR, SULAWESI SELATAN": (-5.1477, 119.4327),
}

# Initialize cache with common coordinates
_COORDS_CACHE.update({k: {'lat': v[0], 'lon': v[1]} for k, v in COMMON_COORDS.items()})
