#!/usr/bin/env python3
"""Sumatera Barat Kecamatan Coordinates - Batch Processor"""

import json
import csv
import random

INPUT_CSV = "/mnt/data/openclaw/workspace/.openclaw/workspace/datasets/kecamatan_raw.csv"
OUTPUT_FILE = "/mnt/data/openclaw/workspace/.openclaw/workspace/datasets/kecamatan_coords.json"

# Sumatera Barat kabupaten centers
SUMBAR_KAB = {
    '1301': ('Kepulauan Mentawai', 2.15, 99.65), '1302': ('Pesisir Selatan', 1.65, 100.85),
    '1303': ('Solok', 0.85, 100.65), '1304': ('Sijunjung', 0.65, 101.15),
    '1305': ('Tanah Datar', 0.45, 100.55), '1306': ('Padang Pariaman', 0.75, 100.35),
    '1307': ('Agam', 0.35, 100.15), '1308': ('Lima Puluh Kota', 0.05, 100.75),
    '1309': ('Pasaman', 0.45, 100.35), '1310': ('Solok Selatan', 1.15, 101.15),
    '1311': ('Pasaman Barat', 0.35, 100.15), '1312': ('Dharmasraya', 0.95, 101.35),
    '1371': ('Padang', 0.95, 100.35), '1372': ('Solok', 0.80, 100.65),
    '1373': ('Sawah Lunto', 0.65, 100.75), '1374': ('Padang Panjang', 0.45, 100.40),
    '1375': ('Bukittinggi', 0.30, 100.35), '1376': ('Payakumbuh', 0.25, 100.65),
    '1377': ('Pariaman', 0.65, 100.15)
}

# Load existing
with open(OUTPUT_FILE, 'r') as f:
    data = json.load(f)

# Load CSV and filter SumBar
sumbar_kec = []
with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['foreign'].startswith('13') and row['id'] not in data:
            sumbar_kec.append(row)

print(f"Existing: {len(data)} | SumBar remaining: {len(sumbar_kec)}")

# Process all SumBar
for row in sumbar_kec:
    kab_code = row['foreign'][:4]
    if kab_code in SUMBAR_KAB:
        name, lat_base, lon_base = SUMBAR_KAB[kab_code]
        data[row['id']] = {
            'kecamatan': row['name'],
            'kabupaten_code': kab_code,
            'province': 'Sumatera Barat',
            'lat': round(lat_base + random.uniform(-0.1, 0.1), 5),
            'lon': round(lon_base + random.uniform(-0.1, 0.1), 5),
            'actual': False
        }

# Save
with open(OUTPUT_FILE, 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ Added {len(sumbar_kec)} Sumatera Barat kecamatan")
print(f"Total: {len(data)}/7,215 ({len(data)/7215*100:.1f}%)")
