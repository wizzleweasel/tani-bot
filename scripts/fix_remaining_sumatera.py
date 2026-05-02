#!/usr/bin/env python3
"""
Fix remaining Sumatera kecamatan - uses CSV as source of truth
"""

import json
import csv
import random

INPUT_CSV = "/mnt/data/openclaw/workspace/.openclaw/workspace/datasets/kecamatan_raw.csv"
OUTPUT_FILE = "/mnt/data/openclaw/workspace/.openclaw/workspace/datasets/kecamatan_coords.json"

# Province centers for coordinate approximation
PROV_CENTERS = {
    '11': ('Aceh', 4.15, 96.95),
    '12': ('Sumatera Utara', 2.75, 99.35),
    '13': ('Sumatera Barat', 0.55, 100.65),
    '14': ('Riau', 0.75, 101.45),
    '15': ('Jambi', 1.45, 102.45),
    '16': ('Sumatera Selatan', 3.55, 103.95),
    '17': ('Bengkulu', 3.75, 102.25),
    '18': ('Lampung', 5.25, 105.15),
    '19': ('Kepulauan Bangka Belitung', 2.75, 106.35),
    '21': ('Kepulauan Riau', 2.95, 104.85),
}

# Load existing data
with open(OUTPUT_FILE, 'r') as f:
    data = json.load(f)

# Load CSV and find missing Sumatera entries
missing = []
with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        id = row['id']
        prefix = row['foreign'][:2]
        
        # Only Sumatera provinces
        if prefix in PROV_CENTERS and id not in data:
            missing.append({
                'id': id,
                'name': row['name'],
                'kabupaten_code': row['foreign'][:4],
                'province': PROV_CENTERS[prefix][0],
                'lat_base': PROV_CENTERS[prefix][1],
                'lon_base': PROV_CENTERS[prefix][2]
            })

print(f"Existing entries: {len(data)}")
print(f"Missing Sumatera: {len(missing)}")
print()

# Add missing entries
for item in missing:
    # Add small random offset for variation
    lat = round(item['lat_base'] + random.uniform(-0.15, 0.15), 5)
    lon = round(item['lon_base'] + random.uniform(-0.15, 0.15), 5)
    
    data[item['id']] = {
        'kecamatan': item['name'],
        'kabupaten_code': item['kabupaten_code'],
        'province': item['province'],
        'lat': lat,
        'lon': lon,
        'actual': False
    }

# Save
with open(OUTPUT_FILE, 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ Added {len(missing)} kecamatan")
print(f"Total: {len(data)}/7,215 ({len(data)/7215*100:.1f}%)")

# Verify all IDs are valid
csv_ids = set()
with open(INPUT_CSV, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        csv_ids.add(row['id'])

invalid = [k for k in data.keys() if k not in csv_ids]
print(f"Invalid IDs after fix: {len(invalid)}")

# Count by province
provinces = {}
for v in data.values():
    prov = v.get('province', 'Unknown')
    provinces[prov] = provinces.get(prov, 0) + 1

print()
print('=== BY PROVINCE ===')
for prov, count in sorted(provinces.items(), key=lambda x: -x[1]):
    print(f'{prov}: {count}')
