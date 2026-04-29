#!/usr/bin/env python3
"""
Fetch all Kecamatan/Kelurahan in Indonesia from BPS Data
Stores as JSON with coordinates
"""

import requests
import json
from typing import List, Dict

# BPS Indonesia API for wilayah data
BPS_API_URL = "https://api.bps.go.id"

# Alternative: Use public dataset
# https://github.com/fajar2402/indonesia-geography

def fetch_kecamatan_from_github() -> Dict:
    """Fetch kecamatan data from public GitHub repository"""
    
    # Public dataset with coordinates
    url = "https://raw.githubusercontent.com/fajar2402/indonesia-geography/master/data/kecamatan.json"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching from GitHub: {e}")
    
    return {}

def fetch_provinces() -> List[Dict]:
    """Fetch all provinces"""
    url = "https://raw.githubusercontent.com/fajar2402/indonesia-geography/master/data/provinsi.json"
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.json()
    except:
        return []

def fetch_cities(prov_id: str) -> List[Dict]:
    """Fetch all cities/regencies for a province"""
    url = f"https://raw.githubusercontent.com/fajar2402/indonesia-geography/master/data/kota.json"
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            all_cities = response.json()
            return [c for c in all_cities if c['id_provinsi'] == prov_id]
    except:
        return []

def fetch_districts(kota_id: str) -> List[Dict]:
    """Fetch all districts (kecamatan) for a city"""
    url = f"https://raw.githubusercontent.com/fajar2402/indonesia-geography/master/data/kecamatan.json"
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            all_districts = response.json()
            return [d for d in all_districts if d['id_kota'] == kota_id]
    except:
        return []

def build_comprehensive_db():
    """Build comprehensive kecamatan database with coordinates"""
    
    print("Fetching province data...")
    provinces = fetch_provinces()
    
    location_db = {}
    total_kecamatan = 0
    
    for province in provinces:
        prov_id = province['id_provinsi']
        prov_name = province['nama']
        
        print(f"Processing {prov_name} ({prov_id})...")
        
        cities = fetch_cities(prov_id)
        
        for city in cities:
            kota_id = city['id_kota']
            kota_name = city['nama']
            
            districts = fetch_districts(kota_id)
            
            for district in districts:
                kec_name = district['nama']
                lat = district.get('latitude', 0)
                lon = district.get('longitude', 0)
                
                # Format: "kecamatan, city, province"
                location_key = f"{kec_name}, {kota_name}, {prov_name}"
                
                location_db[location_key] = {
                    "lat": lat,
                    "lon": lon
                }
                
                total_kecamatan += 1
                
                if total_kecamatan % 1000 == 0:
                    print(f"  Processed {total_kecamatan} kecamatan...")
    
    print(f"\n✅ Total: {total_kecamatan} kecamatan")
    return location_db

def save_to_json(db: Dict, output_file: str = "datasets/kecamatan_database.json"):
    """Save database to JSON file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved to {output_file}")

def main():
    print("=" * 60)
    print("🇮🇩 Fetching All Kecamatan in Indonesia")
    print("=" * 60)
    
    db = build_comprehensive_db()
    save_to_json(db)
    
    # Also save as Python module
    save_as_python(db, "hf_spaces/tani-bot/src/data/kecamatan_db_full.py")

if __name__ == "__main__":
    main()
