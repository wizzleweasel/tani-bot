#!/usr/bin/env python3
"""Add 'actual' boolean field to existing kecamatan_coords.json"""

import json

# High precision coordinates (5+ decimals) = likely actual
# Low precision (2 decimals) = likely estimated

PRECISION_THRESHOLD = 4  # decimal places

with open('datasets/kecamatan_coords.json', 'r') as f:
    data = json.load(f)

updated = 0
actual_count = 0

for code, entry in data.items():
    if 'actual' not in entry:
        # Check precision of lat/lon
        lat_str = str(entry['lat'])
        lon_str = str(entry['lon'])
        
        # Count decimal places
        lat_decimals = len(lat_str.split('.')[-1]) if '.' in lat_str else 0
        lon_decimals = len(lon_str.split('.')[-1]) if '.' in lon_str else 0
        
        # High precision = actual, low precision = estimated
        is_actual = (lat_decimals >= PRECISION_THRESHOLD or lon_decimals >= PRECISION_THRESHOLD)
        
        entry['actual'] = is_actual
        updated += 1
        
        if is_actual:
            actual_count += 1

with open('datasets/kecamatan_coords.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ Updated {updated} entries")
print(f"   - actual: true: {actual_count}")
print(f"   - actual: false: {updated - actual_count}")
