#!/usr/bin/env python3
"""
Complete Kecamatan Database Builder
Downloads all 7k+ kecamatan, fetches coordinates via web search,
saves to JSON with GitHub CDN storage
"""

import requests
import json
import re
import time
import os
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# Configuration
CSV_URL = "https://raw.githubusercontent.com/coll-j/indonesia-locations-data/main/kecamatan.csv"
OUTPUT_FILE = "datasets/kecamatan_full.json"
GITHUB_REPO = "wizzleweasel/tani-bot"
GITHUB_BRANCH = "main"

def download_csv() -> List[Dict]:
    """Download kecamatan CSV from GitHub"""
    print("📥 Downloading kecamatan CSV...")
    try:
        response = requests.get(CSV_URL, timeout=30)
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
            print(f"✅ Downloaded {len(data)} kecamatan")
            return data
    except Exception as e:
        print(f"❌ Error: {e}")
    return []

def search_coordinates(kecamatan_name: str, city_code: str) -> Optional[Tuple[float, float]]:
    """
    Search for coordinates using web search
    Returns (lat, lon) or None
    """
    # Use web_search tool
    from web_search import web_search
    
    query = f"latitude longitude {kecamatan_name} kecamatan Indonesia"
    
    try:
        result = web_search(query=query, count=3)
        content = result.get('content', '')
        
        # Extract coordinates
        coords = extract_coordinates(content)
        if coords:
            return coords
    except Exception as e:
        print(f"  Error: {e}")
    
    return None

def extract_coordinates(text: str) -> Optional[Tuple[float, float]]:
    """Extract lat/lon from text"""
    import re
    
    patterns = [
        r'(-?\d+\.?\d*)\s*,?\s*(-?\d+\.?\d*)',
        r'Latitude:\s*(-?\d+\.?\d*).*?Longitude:\s*(-?\d+\.?\d*)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                lat = float(match[0])
                lon = float(match[1])
                
                # Validate Indonesia bounds
                if -15 < lat < 10 and 95 < lon < 142:
                    return lat, lon
            except:
                continue
    
    return None

def get_province_from_code(code: str) -> str:
    """Extract province name from kecamatan code"""
    province_map = {
        '11': 'Aceh',
        '12': 'Sumatera Utara',
        '13': 'Sumatera Barat',
        '14': 'Riau',
        '15': 'Jambi',
        '16': 'Sumatera Selatan',
        '17': 'Bengkulu',
        '18': 'Lampung',
        '19': 'Kepulauan Bangka Belitung',
        '21': 'Kepulauan Riau',
        '31': 'DKI Jakarta',
        '32': 'Jawa Barat',
        '33': 'Jawa Tengah',
        '34': 'DI Yogyakarta',
        '35': 'Jawa Timur',
        '36': 'Banten',
        '51': 'Bali',
        '52': 'Nusa Tenggara Barat',
        '53': 'Nusa Tenggara Timur',
        '61': 'Kalimantan Barat',
        '62': 'Kalimantan Tengah',
        '63': 'Kalimantan Selatan',
        '64': 'Kalimantan Timur',
        '65': 'Kalimantan Utara',
        '71': 'Sulawesi Utara',
        '72': 'Sulawesi Tengah',
        '73': 'Sulawesi Selatan',
        '74': 'Sulawesi Tenggara',
        '75': 'Gorontalo',
        '76': 'Sulawesi Barat',
        '81': 'Maluku',
        '82': 'Maluku Utara',
        '91': 'Papua Barat',
        '94': 'Papua',
    }
    return province_map.get(code[:2], 'Unknown')

def build_location_db(kecamatan_list: List[Dict]) -> Dict:
    """Build location database with coordinates"""
    location_db = {}
    processed = 0
    found = 0
    not_found = []
    
    print("\n🔍 Searching for coordinates...")
    print("This will take a while (rate limited to 3s per query)\n")
    
    for i, kec in enumerate(kecamatan_list):
        processed += 1
        
        # Build full location name
        province = get_province_from_code(kec['id'])
        location_name = f"{kec['name']}, {kec['city_code']}, {province}"
        
        # Skip if already exists
        if location_name in location_db:
            continue
        
        # Search for coordinates
        print(f"[{processed}/{len(kecamatan_list)}] 🔍 {kec['name']}")
        coords = search_coordinates(kec['name'], kec['city_code'])
        
        if coords:
            lat, lon = coords
            location_db[location_name] = {
                "lat": lat,
                "lon": lon,
                "code": kec['id'],
                "city_code": kec['city_code'],
                "source": "web_search",
                "timestamp": datetime.now().isoformat()
            }
            found += 1
            print(f"  ✅ {lat}, {lon}")
        else:
            not_found.append(kec['name'])
            print(f"  ❌ Not found")
        
        # Rate limiting
        time.sleep(3)
        
        # Save progress periodically
        if processed % 100 == 0:
            save_progress(location_db, not_found, processed, len(kecamatan_list))
            print(f"\n💾 Saved progress: {len(location_db)} locations\n")
    
    return location_db

def save_progress(db: Dict, not_found: List, processed: int, total: int):
    """Save progress to file"""
    data = {
        'locations': db,
        'not_found': not_found,
        'processed': processed,
        'total': total,
        'last_updated': datetime.now().isoformat()
    }
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_final_results(db: Dict):
    """Save final results"""
    data = {
        'locations': db,
        'total': len(db),
        'completed_at': datetime.now().isoformat()
    }
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Saved {len(db)} locations to {OUTPUT_FILE}")

def main():
    print("=" * 60)
    print("🇮🇩 Kecamatan Database Builder")
    print("=" * 60)
    
    # Download CSV
    kecamatan_list = download_csv()
    if not kecamatan_list:
        print("❌ Failed to download data")
        return
    
    # Build database
    location_db = build_location_db(kecamatan_list)
    
    # Save final results
    save_final_results(location_db)
    
    print("\n" + "=" * 60)
    print("✅ Complete!")
    print(f"Total: {len(location_db)} locations")
    print("=" * 60)

if __name__ == "__main__":
    main()
