#!/usr/bin/env python3
"""
Automated Kecamatan Coordinates Fetcher
Uses web search to find latitude/longitude for all kecamatan in Indonesia
"""

import requests
import json
import time
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Configuration
OUTPUT_FILE = "datasets/kecamatan_full.json"
RATE_LIMIT_DELAY = 2  # seconds between requests
BATCH_SIZE = 10  # process in batches
SAVE_INTERVAL = 50  # save every N results

# Base list of kecamatan (will be expanded)
KECAMATAN_LIST = [
    # Jawa Timur
    "Pacet, Mojokerto, Jawa Timur",
    "Ngoro, Mojokerto, Jawa Timur",
    "Trawas, Mojokerto, Jawa Timur",
    "Dlanggu, Mojokerto, Jawa Timur",
    "Gedeg, Mojokerto, Jawa Timur",
    "Kemlagi, Mojokerto, Jawa Timur",
    "Kutorejo, Mojokerto, Jawa Timur",
    "Mojoanyar, Mojokerto, Jawa Timur",
    "Pungging, Mojokerto, Jawa Timur",
    "Trowulan, Mojokerto, Jawa Timur",
    
    # Jawa Barat
    "Bandung Wetan, Bandung, Jawa Barat",
    "Sumur Bandung, Bandung, Jawa Barat",
    "Cicendo, Bandung, Jawa Barat",
    "Coblong, Bandung, Jawa Barat",
    "Sukajadi, Bandung, Jawa Barat",
    
    # DKI Jakarta
    "Gambir, Jakarta Pusat, DKI Jakarta",
    "Menteng, Jakarta Pusat, DKI Jakarta",
    "Tanah Abang, Jakarta Pusat, DKI Jakarta",
    "Kebayoran Baru, Jakarta Selatan, DKI Jakarta",
    "Tebet, Jakarta Selatan, DKI Jakarta",
    
    # Jawa Tengah
    "Semarang Tengah, Semarang, Jawa Tengah",
    "Banyumanik, Semarang, Jawa Tengah",
    "Candisari, Semarang, Jawa Tengah",
    "Gajahmungkur, Semarang, Jawa Tengah",
    
    # Bali
    "Denpasar Barat, Denpasar, Bali",
    "Denpasar Timur, Denpasar, Bali",
    "Denpasar Selatan, Denpasar, Bali",
    "Denpasar Utara, Denpasar, Bali",
    "Ubud, Gianyar, Bali",
    
    # Sumatera Utara
    "Medan Kota, Medan, Sumatera Utara",
    "Medan Baru, Medan, Sumatera Utara",
    "Medan Polonia, Medan, Sumatera Utara",
    "Medan Petisah, Medan, Sumatera Utara",
    
    # Sulawesi Selatan
    "Makassar, Makassar, Sulawesi Selatan",
    "Mariso, Makassar, Sulawesi Selatan",
    "Mamajang, Makassar, Sulawesi Selatan",
    "Tamalate, Makassar, Sulawesi Selatan",
]


def search_coordinates(kecamatan_name: str) -> Optional[Tuple[float, float]]:
    """
    Search for coordinates using web search
    Returns (latitude, longitude) or None if not found
    """
    query = f"latitude and longitude of {kecamatan_name} kecamatan Indonesia"
    
    try:
        # Use web search API
        from web_search import web_search
        result = web_search(query=query, count=3)
        
        # Parse coordinates from results
        for content in result.get('content', []):
            coords = extract_coordinates(content)
            if coords:
                return coords
        
        return None
    
    except Exception as e:
        print(f"Error searching {kecamatan_name}: {e}")
        return None


def extract_coordinates(text: str) -> Optional[Tuple[float, float]]:
    """Extract latitude/longitude from text"""
    import re
    
    # Pattern for decimal coordinates
    pattern = r'(-?\d+\.?\d*)\s*,?\s*(-?\d+\.?\d*)'
    matches = re.findall(pattern, text)
    
    for match in matches:
        try:
            lat = float(match[0])
            lon = float(match[1])
            
            # Validate coordinates (Indonesia bounds)
            if -15 < lat < 10 and 95 < lon < 142:
                return lat, lon
        except:
            continue
    
    return None


def fetch_all_kecamatan(kecamatan_list: List[str], start_index: int = 0) -> Dict:
    """
    Fetch coordinates for all kecamatan
    Resumes from start_index if interrupted
    """
    
    # Load existing data if resuming
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            location_db = json.load(f)
        print(f"Loaded {len(location_db)} existing entries")
    else:
        location_db = {}
    
    total = len(kecamatan_list)
    processed = 0
    found = 0
    not_found = []
    
    print(f"Fetching coordinates for {total - start_index} kecamatan...")
    
    for i in range(start_index, total):
        kecamatan = kecamatan_list[i]
        processed += 1
        
        # Skip if already exists
        if kecamatan in location_db:
            print(f"[{i+1}/{total}] ✓ {kecamatan} (cached)")
            continue
        
        # Search for coordinates
        print(f"[{i+1}/{total}] 🔍 Searching: {kecamatan}")
        coords = search_coordinates(kecamatan)
        
        if coords:
            lat, lon = coords
            location_db[kecamatan] = {
                "lat": lat,
                "lon": lon,
                "source": "web_search",
                "timestamp": datetime.now().isoformat()
            }
            found += 1
            print(f"  ✅ Found: {lat}, {lon}")
        else:
            not_found.append(kecamatan)
            print(f"  ❌ Not found")
        
        # Rate limiting
        time.sleep(RATE_LIMIT_DELAY)
        
        # Save periodically
        if processed % SAVE_INTERVAL == 0:
            save_progress(location_db, not_found, processed, total)
            print(f"💾 Saved progress: {len(location_db)} locations")
    
    # Final save
    save_progress(location_db, not_found, total, total)
    
    return location_db


def save_progress(location_db: Dict, not_found: List, processed: int, total: int):
    """Save progress to file"""
    data = {
        "locations": location_db,
        "not_found": not_found,
        "processed": processed,
        "total": total,
        "last_updated": datetime.now().isoformat()
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    print("=" * 60)
    print("🇮🇩 Kecamatan Coordinates Automation")
    print("=" * 60)
    print(f"Output: {OUTPUT_FILE}")
    print(f"Rate Limit: {RATE_LIMIT_DELAY}s between requests")
    print(f"Batch Size: {BATCH_SIZE}")
    print()
    
    # Fetch coordinates
    location_db = fetch_all_kecamatan(KECAMATAN_LIST)
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Complete!")
    print(f"Total: {len(location_db)} locations")
    print(f"Saved to: {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
