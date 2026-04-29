"""Indonesian Location Database - Kecamatan Level (7,215 locations)

Complete coverage of all Indonesia kecamatan with:
- GitHub CDN integration for full 7k+ database
- Local cache for fast access
- Efficient autocomplete with fuzzy matching
- Data quality tracking (actual vs. approximated coordinates)
"""

import requests
import json
import os
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta

# Configuration
GITHUB_REPO = "wizzleweasel/tani-bot"
GITHUB_BRANCH = "main"
GITHUB_RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}"

KECAMATAN_FILE = "datasets/kecamatan_coords.json"
CACHE_FILE = "datasets/kecamatan_cache.json"
CACHE_DURATION = timedelta(hours=6)  # Cache for 6 hours

# Global cache for kecamatan data
_kecamatan_cache = None
_cache_timestamp = None


def load_kecamatan_data() -> Dict:
    """Load all 7,215 kecamatan from GitHub CDN with local caching"""
    global _kecamatan_cache, _cache_timestamp
    
    # Check in-memory cache first
    if _kecamatan_cache and _cache_timestamp:
        if datetime.now() - _cache_timestamp < CACHE_DURATION:
            return _kecamatan_cache
    
    # Try file cache
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            cache_time = datetime.fromisoformat(cache_data.get('timestamp', '2000-01-01'))
            if datetime.now() - cache_time < CACHE_DURATION:
                _kecamatan_cache = cache_data.get('locations', {})
                _cache_timestamp = cache_time
                return _kecamatan_cache
        except:
            pass
    
    # Fetch from GitHub CDN
    url = f"{GITHUB_RAW_BASE}/{KECAMATAN_FILE}"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            _kecamatan_cache = response.json()
            _cache_timestamp = datetime.now()
            
            # Save to file cache
            try:
                with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                    json.dump({
                        'timestamp': _cache_timestamp.isoformat(),
                        'locations': _kecamatan_cache
                    }, f, ensure_ascii=False, indent=2)
            except:
                pass
            
            return _kecamatan_cache
    except Exception as e:
        print(f"Error fetching kecamatan data: {e}")
    
    # Fallback to empty dict
    return {}


def get_location_coords(location_query: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Get latitude and longitude for a location query.
    Searches kecamatan name, kabupaten name, or kode.
    """
    location_query = location_query.strip().upper()
    
    kecamatan_data = load_kecamatan_data()
    
    # Search by kecamatan code (exact match)
    if location_query in kecamatan_data:
        entry = kecamatan_data[location_query]
        return entry.get('lat'), entry.get('lon')
    
    # Search by kecamatan name or kabupaten name
    for code, entry in kecamatan_data.items():
        kecamatan_name = entry.get('kecamatan', '').upper()
        kab_code = entry.get('kabupaten_code', '')
        
        # Match kecamatan name
        if location_query in kecamatan_name:
            return entry.get('lat'), entry.get('lon')
        
        # Match kabupaten code
        if location_query == kab_code:
            return entry.get('lat'), entry.get('lon')
    
    return None, None


def get_location_suggestions(search_term: str, max_results: int = 50) -> List[str]:
    """
    Get autocomplete suggestions for location search.
    Returns formatted location names for dropdown.
    """
    if not search_term:
        return []
    
    search_lower = search_term.lower()
    kecamatan_data = load_kecamatan_data()
    suggestions = []
    
    # Search through all kecamatan
    for code, entry in kecamatan_data.items():
        kecamatan_name = entry.get('kecamatan', '')
        kab_code = entry.get('kabupaten_code', '')
        
        # Check if search term matches
        if (search_lower in kecamatan_name.lower() or 
            search_lower in kab_code or
            search_lower in code.lower()):
            
            # Format: "Kecamatan Name, Kabupaten Code"
            suggestions.append({
                'name': kecamatan_name,
                'code': code,
                'kab_code': kab_code,
                'display': f"{kecamatan_name} ({kab_code})"
            })
        
        if len(suggestions) >= max_results * 2:  # Get extra for filtering
            break
    
    # Sort by relevance (kecamatan name starts with search term first)
    suggestions.sort(key=lambda x: (
        0 if x['name'].lower().startswith(search_lower) else 1,
        x['name']
    ))
    
    # Return formatted display names
    return [s['display'] for s in suggestions[:max_results]]


def get_all_kecamatan_count() -> int:
    """Get total number of kecamatan in database"""
    kecamatan_data = load_kecamatan_data()
    return len(kecamatan_data)


def get_data_quality_stats() -> Dict:
    """Get data quality statistics"""
    kecamatan_data = load_kecamatan_data()
    
    actual_true = sum(1 for v in kecamatan_data.values() if v.get('actual') == True)
    actual_false = sum(1 for v in kecamatan_data.values() if v.get('actual') == False)
    
    return {
        'total': len(kecamatan_data),
        'actual_true': actual_true,
        'actual_false': actual_false,
        'quality_percent': round(actual_true / len(kecamatan_data) * 100, 2) if kecamatan_data else 0
    }


# Legacy compatibility - keep old function signatures
def get_all_locations() -> List[str]:
    """Get all location names (for backward compatibility)"""
    kecamatan_data = load_kecamatan_data()
    return [f"{v.get('kecamatan', '')} ({v.get('kabupaten_code', '')})" 
            for v in kecamatan_data.values()]
