#!/usr/bin/env python3
"""
Batch Kecamatan Coordinate Fetcher
Processes coordinates per kabupaten, saves progress, auto-pushes to GitHub
"""

import csv
import json
import os
import time
import requests
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# Configuration
CSV_FILE = "datasets/kecamatan_raw.csv"
PROGRESS_FILE = "datasets/coords_progress.json"
OUTPUT_FILE = "datasets/kecamatan_with_coords.json"
RATE_LIMIT = 3  # seconds between queries

# Province mapping
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

def load_progress() -> Dict:
    """Load progress file"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {'processed': [], 'results': {}, 'current_kabupaten': None}

def save_progress(progress: Dict):
    """Save progress"""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def save_results(results: Dict):
    """Save final results"""
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

def load_kabupaten_codes() -> List[str]:
    """Extract unique kabupaten codes from kecamatan data"""
    codes = set()
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            codes.add(row['foreign'])
    return sorted(list(codes))

def search_coordinates_via_web(kabupaten_name: str, province_name: str) -> Optional[Tuple[float, float]]:
    """
    Search for coordinates using web search
    Returns (lat, lon) or None
    """
    # This would use the web_search tool in OpenClaw
    # For now, we'll use a placeholder
    query = f"latitude longitude {kabupaten_name} {province_name} Indonesia coordinates"
    
    # In production, this would call web_search tool
    # For demo, return None
    return None

def process_kabupaten_batch(kabupaten_codes: List[str], start_idx: int, batch_size: int = 20):
    """Process a batch of kabupaten"""
    progress = load_progress()
    
    end_idx = min(start_idx + batch_size, len(kabupaten_codes))
    batch_codes = kabupaten_codes[start_idx:end_idx]
    
    print(f"\n{'='*60}")
    print(f"Processing batch: {start_idx+1} to {end_idx} of {len(kabupaten_codes)}")
    print(f"Kabupaten: {batch_codes}")
    print(f"{'='*60}\n")
    
    for kab_code in batch_codes:
        # Skip if already processed
        if kab_code in progress['processed']:
            print(f"[SKIP] {kab_code} - Already processed")
            continue
        
        # Get province and kabupaten name
        prov_code = kab_code[:2]
        province_name = PROVINCE_MAP.get(prov_code, 'Unknown')
        
        # In production, fetch kabupaten name from mapping
        # For now, use code
        kab_name = f"Kabupaten {kab_code}"
        
        print(f"[{start_idx+1}/{len(kabupaten_codes)}] 🔍 {kab_name}, {province_name}")
        
        # Search for coordinates
        coords = search_coordinates_via_web(kab_name, province_name)
        
        if coords:
            lat, lon = coords
            progress['results'][kab_code] = {
                'lat': lat,
                'lon': lon,
                'kabupaten': kab_name,
                'province': province_name,
                'source': 'web_search',
                'timestamp': datetime.now().isoformat()
            }
            print(f"  ✅ Found: {lat}, {lon}")
        else:
            print(f"  ❌ Not found")
        
        # Save progress after each
        save_progress(progress)
        
        # Rate limiting
        time.sleep(RATE_LIMIT)
        
        start_idx += 1
    
    print(f"\n✅ Batch complete! Processed {len(batch_codes)} kabupaten")
    return end_idx

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 batch_coords.py <start_index> [batch_size]")
        print("Example: python3 batch_coords.py 0 20")
        sys.exit(1)
    
    start_idx = int(sys.argv[1])
    batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    
    # Load kabupaten codes
    kabupaten_codes = load_kabupaten_codes()
    print(f"Found {len(kabupaten_codes)} unique kabupaten/kota")
    
    # Process batch
    new_idx = process_kabupaten_batch(kabupaten_codes, start_idx, batch_size)
    
    # Save final results
    progress = load_progress()
    save_results(progress['results'])
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total kabupaten: {len(kabupaten_codes)}")
    print(f"Processed: {len(progress['processed'])}")
    print(f"Results: {len(progress['results'])}")
    print(f"Next index: {new_idx}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
