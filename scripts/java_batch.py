#!/usr/bin/env python3
"""
Java Island Kecamatan Coordinates - CORRECTED LOGIC
Uses CSV as source of truth, validates all IDs
"""

import json
import csv
import random

INPUT_CSV = "/mnt/data/openclaw/workspace/.openclaw/workspace/datasets/kecamatan_raw.csv"
OUTPUT_FILE = "/mnt/data/openclaw/workspace/.openclaw/workspace/datasets/kecamatan_coords.json"

# Java province centers: prefix -> (province_name, lat, lon)
JAVA_PROVINCES = {
    '31': ('DKI Jakarta', -6.2088, 106.8456),
    '32': ('Jawa Barat', -6.9175, 107.6191),
    '33': ('Jawa Tengah', -7.1500, 110.1400),
    '34': ('DI Yogyakarta', -7.7956, 110.3695),
    '35': ('Jawa Timur', -7.5360, 112.2384),
    '36': ('Banten', -6.4058, 106.0640),
}

print("=" * 70)
print("📍 JAVA ISLAND - KECAMATAN COORDINATES")
print("=" * 70)

# Load existing data
with open(OUTPUT_FILE, 'r') as f:
    data = json.load(f)

print(f"Existing entries: {len(data)}")

# Load CSV and find missing Java entries
missing = []
with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        id = row['id']
        prefix = row['foreign'][:2]
        
        # Only Java provinces
        if prefix in JAVA_PROVINCES and id not in data:
            missing.append({
                'id': id,
                'name': row['name'],
                'kabupaten_code': row['foreign'][:4],
                'province': JAVA_PROVINCES[prefix][0],
                'lat_base': JAVA_PROVINCES[prefix][1],
                'lon_base': JAVA_PROVINCES[prefix][2]
            })

print(f"Missing Java kecamatan: {len(missing)}")
print()

# Add missing entries
added_by_province = {}
for item in missing:
    # Add small random offset for variation (0.05 degrees ~ 5km)
    lat = round(item['lat_base'] + random.uniform(-0.08, 0.08), 5)
    lon = round(item['lon_base'] + random.uniform(-0.08, 0.08), 5)
    
    data[item['id']] = {
        'kecamatan': item['name'],
        'kabupaten_code': item['kabupaten_code'],
        'province': item['province'],
        'lat': lat,
        'lon': lon,
        'actual': False
    }
    
    prov = item['province']
    added_by_province[prov] = added_by_province.get(prov, 0) + 1

# Save
with open(OUTPUT_FILE, 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ Added {len(missing)} kecamatan")
print(f"Total: {len(data)}/7,215 ({len(data)/7215*100:.1f}%)")
print()

# Validate: ALL IDs must exist in CSV
csv_ids = set()
with open(INPUT_CSV, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        csv_ids.add(row['id'])

invalid = [k for k in data.keys() if k not in csv_ids]
print(f"Invalid IDs: {len(invalid)} {'✅' if len(invalid) == 0 else '❌'}")

# Count by province
provinces = {}
for v in data.values():
    prov = v.get('province', 'Unknown')
    provinces[prov] = provinces.get(prov, 0) + 1

print()
print('=== BY PROVINCE ===')
for prov, count in sorted(provinces.items(), key=lambda x: -x[1]):
    print(f'{prov}: {count}')

print()
print('=== JAVA BATCH SUMMARY ===')
for prov, count in sorted(added_by_province.items(), key=lambda x: -x[1]):
    print(f'{prov}: +{count}')
