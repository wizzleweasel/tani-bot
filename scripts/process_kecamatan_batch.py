#!/usr/bin/env python3
"""
Process Kecamatan in Batches
Reads CSV, outputs queries for web search
Saves results incrementally
"""

import csv
import json
import os
from typing import List, Dict

# Configuration
CSV_FILE = "datasets/kecamatan_raw.csv"
OUTPUT_FILE = "datasets/kecamatan_with_coords.json"
PROGRESS_FILE = "datasets/coords_progress.json"

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

def load_csv() -> List[Dict]:
    """Load kecamatan from CSV"""
    data = []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def load_progress() -> Dict:
    """Load progress file"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {'processed': [], 'results': {}}

def save_progress(progress: Dict):
    """Save progress"""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def save_results(results: Dict):
    """Save final results"""
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

def generate_batch_queries(start: int, end: int) -> List[str]:
    """Generate web search queries for a batch"""
    data = load_csv()
    queries = []
    
    for i in range(start, min(end, len(data))):
        row = data[i]
        name = row['name']
        province = PROVINCE_MAP.get(row['id'][:2], '')
        query = f"latitude longitude Kecamatan {name} Indonesia coordinates"
        queries.append(query)
    
    return queries

def main():
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python3 process_kecamatan_batch.py <start> <end>")
        print("Example: python3 process_kecamatan_batch.py 0 100")
        sys.exit(1)
    
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    
    print(f"Generating queries for batch {start}-{end}...")
    queries = generate_batch_queries(start, end)
    
    print(f"\nGenerated {len(queries)} queries:")
    for i, q in enumerate(queries[:10]):  # Show first 10
        print(f"  {start+i+1}. {q}")
    if len(queries) > 10:
        print(f"  ... and {len(queries)-10} more")
    
    print(f"\n✅ Ready for web search processing")

if __name__ == "__main__":
    main()
