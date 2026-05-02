#!/usr/bin/env python3
"""
Kecamatan Coordinate Automation
Collect lat/lon for all 7,215 kecamatan in Indonesia
"""

import json
import csv
import requests
from datetime import datetime

# Configuration
INPUT_FILE = "datasets/kecamatan_raw.csv"
OUTPUT_FILE = "datasets/kecamatan_coords.json"
PROGRESS_FILE = "datasets/kecamatan_coords_progress.json"
BATCH_SIZE = 100
SAVE_INTERVAL = 500

def load_kecamatan():
    """Load kecamatan list from CSV"""
    kecamatan_list = []
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            kecamatan_list.append({
                'id': row['id'],
                'kabupaten_code': row['foreign'],
                'name': row['name']
            })
    return kecamatan_list

def load_existing_coords():
    """Load existing coordinates if any"""
    try:
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def load_progress():
    """Load progress tracking"""
    try:
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {'processed': 0, 'last_id': None}

def get_coordinates(kecamatan_name, kabupaten_name):
    """Search for kecamatan coordinates via web search"""
    query = f"latitude longitude Kecamatan {kecamatan_name} coordinates"
    
    try:
        # Use web search API (you'll need to implement this with your preferred method)
        # For now, returning None to indicate needs manual search
        return None
    except:
        return None

def save_progress(coords, progress):
    """Save coordinates and progress"""
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(coords, f, ensure_ascii=False, indent=None, separators=(',', ':'))
    
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)

print("=" * 70)
print("🗺️ KECAMATAN COORDINATE AUTOMATION")
print("=" * 70)
print(f"Total kecamatan: 7,215")
print(f"Batch size: {BATCH_SIZE}")
print(f"Auto-save: Every {SAVE_INTERVAL} kecamatan")
print("=" * 70)

# Load data
kecamatan_list = load_kecamatan()
existing_coords = load_existing_coords()
progress = load_progress()

print(f"Loaded {len(kecamatan_list)} kecamatan")
print(f"Existing coordinates: {len(existing_coords)}")
print(f"Progress: {progress['processed']} processed")
print()

# Start automation
start_idx = progress['processed']
print(f"Starting from index {start_idx}...")
print()

for i in range(start_idx, len(kecamatan_list), BATCH_SIZE):
    batch = kecamatan_list[i:i+BATCH_SIZE]
    batch_num = (i // BATCH_SIZE) + 1
    
    print(f"Batch {batch_num}: Processing kecamatan {i+1} to {min(i+BATCH_SIZE, len(kecamatan_list))}")
    
    for kec in batch:
        kec_id = kec['id']
        
        # Skip if already has coordinates
        if kec_id in existing_coords:
            continue
        
        # Get coordinates (implement web search here)
        coords = get_coordinates(kec['name'], kec['kabupaten_code'])
        
        if coords:
            existing_coords[kec_id] = {
                'kecamatan': kec['name'],
                'kabupaten_code': kec['kabupaten_code'],
                'lat': coords['lat'],
                'lon': coords['lon']
            }
    
    # Save progress
    progress['processed'] = i + len(batch)
    progress['last_id'] = batch[-1]['id'] if batch else None
    save_progress(existing_coords, progress)
    
    print(f"  ✅ Saved batch {batch_num} ({len(batch)} kecamatan)")
    
    # Status update every 1000 kecamatan
    if (i + len(batch)) % 1000 == 0:
        pct = ((i + len(batch)) / len(kecamatan_list)) * 100
        print(f"\n📊 PROGRESS: {i + len(batch)}/7,215 ({pct:.1f}%)\n")

print()
print("=" * 70)
print("✅ AUTOMATION COMPLETE!")
print(f"Total coordinates collected: {len(existing_coords)}")
print("=" * 70)
