"""Optimized Kecamatan Database with Binary Search"""
import bisect

# All kecamatan data
LOCATION_DB = {"Pacet, Mojokerto, Jawa Timur": {"lat": -7.5333, "lon": 112.4333}, "Bandung Wetan, Bandung, Jawa Barat": {"lat": -6.9175, "lon": 107.6191}, "Jakarta Pusat, Jakarta Pusat, DKI Jakarta": {"lat": -6.1862, "lon": 106.8341}, "Sleman, Sleman, DIY": {"lat": -7.7, "lon": 110.35}, "Denpasar Barat, Denpasar, Bali": {"lat": -8.6705, "lon": 115.2126}, "Medan Kota, Medan, Sumatera Utara": {"lat": 3.5952, "lon": 98.6722}, "Makassar, Makassar, Sulawesi Selatan": {"lat": -5.1477, "lon": 119.4327}}

# Sorted keys for binary search
_SORTED_KEYS = ['Bandung Wetan, Bandung, Jawa Barat', 'Denpasar Barat, Denpasar, Bali', 'Jakarta Pusat, Jakarta Pusat, DKI Jakarta', 'Makassar, Makassar, Sulawesi Selatan', 'Medan Kota, Medan, Sumatera Utara', 'Pacet, Mojokerto, Jawa Timur', 'Sleman, Sleman, DIY']

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
