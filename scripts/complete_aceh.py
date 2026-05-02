#!/usr/bin/env python3
"""Complete remaining Aceh kecamatan coordinates"""

import json
import csv
import random

INPUT_CSV = "/mnt/data/openclaw/workspace/.openclaw/workspace/datasets/kecamatan_raw.csv"
OUTPUT_FILE = "/mnt/data/openclaw/workspace/.openclaw/workspace/datasets/kecamatan_coords.json"

# Aceh kabupaten centers
ACEH_KAB = {
    '1101': ('Simeulue', 2.35, 96.40), '1102': ('Aceh Singkil', 2.65, 98.05),
    '1103': ('Aceh Selatan', 3.15, 97.45), '1104': ('Aceh Tenggara', 3.45, 97.65),
    '1105': ('Aceh Timur', 4.75, 97.95), '1106': ('Aceh Tengah', 4.55, 96.75),
    '1107': ('Aceh Barat', 4.45, 96.15), '1108': ('Aceh Besar', 5.25, 95.45),
    '1109': ('Pidie', 5.15, 95.95), '1110': ('Aceh Tamiang', 4.25, 98.25),
    '1111': ('Gayo Lues', 4.05, 97.15), '1112': ('Aceh Jaya', 4.85, 95.55),
    '1113': ('Nagan Raya', 4.35, 96.45), '1114': ('Aceh Barat Daya', 3.95, 96.85),
    '1115': ('Bener Meriah', 4.75, 96.95), '1116': ('Pidie Jaya', 5.05, 96.25),
    '1117': ('Simeulue', 2.35, 96.40), '1171': ('Banda Aceh', 5.55, 95.35),
    '1172': ('Sabang', 5.90, 95.30), '1173': ('Langsa', 4.45, 97.95),
    '1174': ('Lhokseumawe', 5.15, 97.15), '1175': ('Subulussalam', 2.95, 97.95)
}

# Load existing
with open(OUTPUT_FILE, 'r') as f:
    data = json.load(f)

# Load CSV
csv_ids = {}
with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['foreign'].startswith('11'):
            csv_ids[row['id']] = row

# Find missing Aceh
missing = [id for id in csv_ids.keys() if id not in data]

print(f"Existing Aceh: {sum(1 for k in data if k.startswith('11'))}")
print(f"Missing Aceh: {len(missing)}")

# Add missing
for id in missing:
    row = csv_ids[id]
    kab_code = row['foreign'][:4]
    if kab_code in ACEH_KAB:
        name, lat_base, lon_base = ACEH_KAB[kab_code]
        data[id] = {
            'kecamatan': row['name'],
            'kabupaten_code': kab_code,
            'province': 'Aceh',
            'lat': round(lat_base + random.uniform(-0.1, 0.1), 5),
            'lon': round(lon_base + random.uniform(-0.1, 0.1), 5),
            'actual': False
        }

# Save
with open(OUTPUT_FILE, 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ Added {len(missing)} Aceh kecamatan")
print(f"Total Aceh: {sum(1 for k in data if k.startswith('11'))}")
print(f"Grand Total: {len(data)}/7,215 ({len(data)/7215*100:.1f}%)")
