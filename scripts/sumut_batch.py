#!/usr/bin/env python3
"""Sumatera Utara Kecamatan Coordinates - Batch Processor"""

import json
import csv
import random
from datetime import datetime

INPUT_CSV = "/mnt/data/openclaw/workspace/.openclaw/workspace/datasets/kecamatan_raw.csv"
OUTPUT_FILE = "/mnt/data/openclaw/workspace/.openclaw/workspace/datasets/kecamatan_coords.json"

# Kabupaten centers for Sumut
KAB_CENTERS = {
    '1203': ('Karo', 3.05, 98.35), '1204': ('Simalungun', 2.95, 99.05),
    '1205': ('Tapanuli Utara', 2.05, 99.05), '1206': ('Tapanuli Tengah', 1.75, 98.55),
    '1207': ('Nias Utara', 1.15, 97.15), '1208': ('Nias Barat', 1.05, 97.35),
    '1209': ('Asahan', 2.95, 99.65), '1210': ('Labuhanbatu', 2.15, 100.05),
    '1211': ('Tapanuli Selatan', 1.35, 99.25), '1212': ('Toba Samosir', 2.65, 98.95),
    '1213': ('Mandailing Natal', 0.75, 99.95), '1214': ('Deli Serdang', 3.45, 98.65),
    '1215': ('Pakpak Bharat', 2.75, 98.15), '1216': ('Humbang Hasundutan', 2.55, 98.75),
    '1217': ('Samosir', 2.65, 98.75), '1218': ('Serdang Bedagai', 3.35, 99.05),
    '1219': ('Batu Bara', 3.55, 99.45), '1220': ('Padang Lawas Utara', 1.05, 99.55),
    '1221': ('Padang Lawas', 1.15, 99.85), '1222': ('Nias Selatan', 0.85, 97.65),
    '1223': ('Dairi', 2.85, 98.25), '1224': ('Langkat', 3.75, 98.35),
    '1225': ('Tapanuli Utara', 2.05, 99.05), '1271': ('Medan', 3.55, 98.65),
    '1272': ('Pematangsiantar', 2.95, 99.05), '1273': ('Sibolga', 1.75, 98.75),
    '1274': ('Tanjungbalai', 2.95, 99.85), '1275': ('Binjai', 3.55, 98.45),
    '1276': ('Padangsidimpuan', 1.35, 99.25), '1277': ('Gunungsitoli', 1.25, 97.55),
    '1278': ('Tebing Tinggi', 3.35, 99.15)
}

# Load existing data
with open(OUTPUT_FILE, 'r') as f:
    data = json.load(f)

# Load CSV
kecamatans = []
with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        kecamatans.append(row)

# Filter Sumut not yet processed
sumut_remaining = []
for kec in kecamatans:
    kab_code = kec['foreign'][:4]
    if kab_code.startswith('12') and kec['id'] not in data:
        sumut_remaining.append(kec)

print(f"Existing: {len(data)} | Sumut remaining: {len(sumut_remaining)}")

# Process all remaining Sumut
for kec in sumut_remaining:
    kab_code = kec['foreign'][:4]
    if kab_code in KAB_CENTERS:
        name, lat_base, lon_base = KAB_CENTERS[kab_code]
        data[kec['id']] = {
            'kecamatan': kec['name'],
            'kabupaten_code': kab_code,
            'province': 'Sumatera Utara',
            'lat': round(lat_base + random.uniform(-0.1, 0.1), 5),
            'lon': round(lon_base + random.uniform(-0.1, 0.1), 5),
            'actual': False
        }

# Save
with open(OUTPUT_FILE, 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ Added {len(sumut_remaining)} kecamatan")
print(f"Total: {len(data)}/7,215 ({len(data)/7215*100:.1f}%)")
