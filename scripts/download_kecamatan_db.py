#!/usr/bin/env python3
"""
Download Complete Kecamatan Database from GitHub
Source: https://github.com/cahyadsn/wilayah
"""

import requests
import json
import re
import os

# GitHub raw URLs for kecamatan data
GITHUB_BASE = "https://raw.githubusercontent.com/cahyadsn/wilayah/master"

# SQL files with coordinates
SQL_FILES = [
    "db/wilayah_level_3.sql",  # Kecamatan level
]

OUTPUT_FILE = "datasets/kecamatan_full.json"

def download_sql_file(url):
    """Download SQL file from GitHub"""
    print(f"Downloading: {url}")
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"Error: {e}")
    return None

def parse_kecamatan_from_sql(sql_content):
    """Parse kecamatan data from SQL INSERT statements"""
    kecamatan_db = {}
    
    # Pattern for INSERT INTO kecamatan VALUES
    pattern = r"INSERT INTO `kecamatan` VALUES \((.*?)\);"
    matches = re.findall(pattern, sql_content, re.DOTALL)
    
    for match in matches:
        # Parse values
        values = match.split(',')
        if len(values) >= 6:
            code = values[0].strip().strip("'`")
            name = values[1].strip().strip("'`")
            city_code = values[2].strip().strip("'`")
            lat = values[3].strip().strip("'`")
            lon = values[4].strip().strip("'`")
            
            # Try to get city/province name (would need to join with other tables)
            # For now, use placeholder
            location_key = f"{name}, {city_code}"
            
            try:
                lat_float = float(lat) if lat else 0
                lon_float = float(lon) if lon else 0
                
                if -15 < lat_float < 10 and 95 < lon_float < 142:  # Indonesia bounds
                    kecamatan_db[location_key] = {
                        "code": code,
                        "city_code": city_code,
                        "lat": lat_float,
                        "lon": lon_float
                    }
            except:
                continue
    
    return kecamatan_db

def merge_with_geokeo_data():
    """Merge with data from geokeo.com"""
    # This would require scraping geokeo.com pages
    # For now, use GitHub data
    pass

def save_to_json(data, output_file):
    """Save to JSON file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved {len(data)} kecamatan to {output_file}")

def main():
    print("=" * 60)
    print("🇮🇩 Download Kecamatan Database")
    print("=" * 60)
    
    all_kecamatan = {}
    
    for sql_file in SQL_FILES:
        url = f"{GITHUB_BASE}/{sql_file}"
        sql_content = download_sql_file(url)
        
        if sql_content:
            kecamatan = parse_kecamatan_from_sql(sql_content)
            all_kecamatan.update(kecamatan)
            print(f"  Parsed {len(kecamatan)} kecamatan from {sql_file}")
    
    if all_kecamatan:
        save_to_json(all_kecamatan, OUTPUT_FILE)
        print(f"\n✅ Complete! Total: {len(all_kecamatan)} kecamatan")
    else:
        print("\n❌ No data found")

if __name__ == "__main__":
    main()
