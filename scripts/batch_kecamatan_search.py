#!/usr/bin/env python3
"""
Batch Kecamatan Coordinate Fetcher
Uses web search to find lat/lon for each kecamatan
Saves progress incrementally (can resume if interrupted)
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Configuration
OUTPUT_FILE = "datasets/kecamatan_web_search.json"
PROGRESS_FILE = "datasets/kecamatan_search_progress.json"
BATCH_SIZE = 20  # Search this many per batch
RATE_LIMIT = 3  # Seconds between searches

# Base kecamatan list (expandable)
KECAMATAN_BASE = [
    # Jawa Timur - Mojokerto
    "Pacet, Mojokerto, Jawa Timur",
    "Ngoro, Mojokerto, Jawa Timur",
    "Trawas, Mojokerto, Jawa Timur",
    "Dlanggu, Mojokerto, Jawa Timur",
    "Gedeg, Mojokerto, Jawa Timur",
    "Kemlagi, Mojokerto, Jawa Timur",
    "Kutorejo, Mojokerto, Jawa Timur",
    "Mojoanyar, Mojokerto, Jawa Timur",
    "Pungging, Mojokerto, Jawa Timur",
    "Trowulan, Mojokerto, Jawa Timur",
    "Bangsal, Mojokerto, Jawa Timur",
    "Dawarblandong, Mojokerto, Jawa Timur",
    "Jatirejo, Mojokerto, Jawa Timur",
    "Jetis, Mojokerto, Jawa Timur",
    "Magersari, Mojokerto, Jawa Timur",
    "Mojosari, Mojokerto, Jawa Timur",
    "Sooko, Mojokerto, Jawa Timur",
    "Trawas, Mojokerto, Jawa Timur",
    
    # Jawa Timur - Surabaya
    "Asemrowo, Surabaya, Jawa Timur",
    "Benowo, Surabaya, Jawa Timur",
    "Bubutan, Surabaya, Jawa Timur",
    "Bulak, Surabaya, Jawa Timur",
    "Dukuh Pakis, Surabaya, Jawa Timur",
    "Gayungan, Surabaya, Jawa Timur",
    "Genteng, Surabaya, Jawa Timur",
    "Gubeng, Surabaya, Jawa Timur",
    "Gunung Anyar, Surabaya, Jawa Timur",
    "Jambangan, Surabaya, Jawa Timur",
    "Karang Pilang, Surabaya, Jawa Timur",
    "Kenjeran, Surabaya, Jawa Timur",
    "Krembangan, Surabaya, Jawa Timur",
    "Lakarsantri, Surabaya, Jawa Timur",
    "Mulyorejo, Surabaya, Jawa Timur",
    "Pabean Cantian, Surabaya, Jawa Timur",
    "Pakal, Surabaya, Jawa Timur",
    "Rungkut, Surabaya, Jawa Timur",
    "Sambikerep, Surabaya, Jawa Timur",
    "Sawahan, Surabaya, Jawa Timur",
    "Semampir, Surabaya, Jawa Timur",
    "Simokerto, Surabaya, Jawa Timur",
    "Sukolilo, Surabaya, Jawa Timur",
    "Sukomanunggal, Surabaya, Jawa Timur",
    "Tambaksari, Surabaya, Jawa Timur",
    "Tandes, Surabaya, Jawa Timur",
    "Tegalsari, Surabaya, Jawa Timur",
    "Tenggilis Mejoyo, Surabaya, Jawa Timur",
    "Wiyung, Surabaya, Jawa Timur",
    "Wonocolo, Surabaya, Jawa Timur",
    "Wonokromo, Surabaya, Jawa Timur",
    
    # DKI Jakarta - Jakarta Pusat
    "Gambir, Jakarta Pusat, DKI Jakarta",
    "Menteng, Jakarta Pusat, DKI Jakarta",
    "Senen, Jakarta Pusat, DKI Jakarta",
    "Cempaka Putih, Jakarta Pusat, DKI Jakarta",
    "Johar Baru, Jakarta Pusat, DKI Jakarta",
    "Kemayoran, Jakarta Pusat, DKI Jakarta",
    "Sawah Besar, Jakarta Pusat, DKI Jakarta",
    "Tanah Abang, Jakarta Pusat, DKI Jakarta",
    
    # DKI Jakarta - Jakarta Selatan
    "Jagakarsa, Jakarta Selatan, DKI Jakarta",
    "Kebayoran Baru, Jakarta Selatan, DKI Jakarta",
    "Kebayoran Lama, Jakarta Selatan, DKI Jakarta",
    "Mampang Prapatan, Jakarta Selatan, DKI Jakarta",
    "Pancoran, Jakarta Selatan, DKI Jakarta",
    "Pasar Minggu, Jakarta Selatan, DKI Jakarta",
    "Pesanggrahan, Jakarta Selatan, DKI Jakarta",
    "Setiabudi, Jakarta Selatan, DKI Jakarta",
    "Tebet, Jakarta Selatan, DKI Jakarta",
    
    # Jawa Barat - Bandung
    "Andir, Bandung, Jawa Barat",
    "Antapani, Bandung, Jawa Barat",
    "Arcamanik, Bandung, Jawa Barat",
    "Astana Anyar, Bandung, Jawa Barat",
    "Babakan Ciparay, Bandung, Jawa Barat",
    "Bandung Kidul, Bandung, Jawa Barat",
    "Bandung Kulon, Bandung, Jawa Barat",
    "Bandung Wetan, Bandung, Jawa Barat",
    "Batununggal, Bandung, Jawa Barat",
    "Bojongloa Kaler, Bandung, Jawa Barat",
    "Bojongloa Kidul, Bandung, Jawa Barat",
    "Buahbatu, Bandung, Jawa Barat",
    "Cibeunying Kaler, Bandung, Jawa Barat",
    "Cibeunying Kidul, Bandung, Jawa Barat",
    "Cibiru, Bandung, Jawa Barat",
    "Cicendo, Bandung, Jawa Barat",
    "Cidadap, Bandung, Jawa Barat",
    "Cinambo, Bandung, Jawa Barat",
    "Coblong, Bandung, Jawa Barat",
    "Gedebage, Bandung, Jawa Barat",
    "Kiaracondong, Bandung, Jawa Barat",
    "Lengkong, Bandung, Jawa Barat",
    "Mandalajati, Bandung, Jawa Barat",
    "Panyileukan, Bandung, Jawa Barat",
    "Rancasari, Bandung, Jawa Barat",
    "Regol, Bandung, Jawa Barat",
    "Sukajadi, Bandung, Jawa Barat",
    "Sukasari, Bandung, Jawa Barat",
    "Sumur Bandung, Bandung, Jawa Barat",
    "Ujung Berung, Bandung, Jawa Barat",
    
    # Bali - Denpasar & Gianyar
    "Denpasar Barat, Denpasar, Bali",
    "Denpasar Timur, Denpasar, Bali",
    "Denpasar Selatan, Denpasar, Bali",
    "Denpasar Utara, Denpasar, Bali",
    "Ubud, Gianyar, Bali",
    "Sukawati, Gianyar, Bali",
    "Blahbatuh, Gianyar, Bali",
    "Gianyar, Gianyar, Bali",
    "Tampaksiring, Gianyar, Bali",
    "Tegallalang, Gianyar, Bali",
    "Payangan, Gianyar, Bali",
    
    # Sumatera Utara - Medan
    "Medan Kota, Medan, Sumatera Utara",
    "Medan Baru, Medan, Sumatera Utara",
    "Medan Polonia, Medan, Sumatera Utara",
    "Medan Petisah, Medan, Sumatera Utara",
    "Medan Maimun, Medan, Sumatera Utara",
    "Medan Helvetia, Medan, Sumatera Utara",
    "Medan Denai, Medan, Sumatera Utara",
    "Medan Area, Medan, Sumatera Utara",
    "Medan Johor, Medan, Sumatera Utara",
    "Medan Amplas, Medan, Sumatera Utara",
    "Medan Tembung, Medan, Sumatera Utara",
    "Medan Selayang, Medan, Sumatera Utara",
    "Medan Sunggal, Medan, Sumatera Utara",
    "Medan Perjuangan, Medan, Sumatera Utara",
    "Medan Tuntungan, Medan, Sumatera Utara",
    "Medan Deli, Medan, Sumatera Utara",
    "Medan Labuhan, Medan, Sumatera Utara",
    "Medan Marelan, Medan, Sumatera Utara",
    "Medan Belawan, Medan, Sumatera Utara",
    
    # Sulawesi Selatan - Makassar
    "Makassar, Makassar, Sulawesi Selatan",
    "Mariso, Makassar, Sulawesi Selatan",
    "Mamajang, Makassar, Sulawesi Selatan",
    "Tamalate, Makassar, Sulawesi Selatan",
    "Rappocini, Makassar, Sulawesi Selatan",
    "Manggala, Makassar, Sulawesi Selatan",
    "Biringkanaya, Makassar, Sulawesi Selatan",
    "Panakkukang, Makassar, Sulawesi Selatan",
    "Talasa, Makassar, Sulawesi Selatan",
    "Ujung Tanah, Makassar, Sulawesi Selatan",
    "Wajo, Makassar, Sulawesi Selatan",
    "Bontoala, Makassar, Sulawesi Selatan",
]


def load_progress() -> Tuple[Dict, int]:
    """Load progress from file"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('results', {}), data.get('next_index', 0)
    return {}, 0


def save_progress(results: Dict, next_index: int):
    """Save progress to file"""
    data = {
        'results': results,
        'next_index': next_index,
        'last_updated': datetime.now().isoformat()
    }
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_final_results(results: Dict):
    """Save final results"""
    data = {
        'locations': results,
        'total': len(results),
        'completed_at': datetime.now().isoformat()
    }
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Saved {len(results)} locations to {OUTPUT_FILE}")


def search_kecamatan_coordinates(kecamatan_name: str) -> Optional[Tuple[float, float]]:
    """
    Search for coordinates using web search
    Returns (lat, lon) or None
    """
    import subprocess
    import json
    
    query = f"latitude and longitude of {kecamatan_name} kecamatan Indonesia"
    
    try:
        # Use web_search tool via subprocess
        cmd = f'''python3 -c "
import json
from web_search import web_search
result = web_search(query='{query}', count=3)
print(json.dumps(result))
"'''
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            content = data.get('content', '')
            
            # Extract coordinates from content
            coords = extract_coordinates(content)
            if coords:
                return coords
        
        return None
    
    except Exception as e:
        print(f"  Error: {e}")
        return None


def extract_coordinates(text: str) -> Optional[Tuple[float, float]]:
    """Extract lat/lon from search result text"""
    import re
    
    # Pattern for decimal coordinates
    patterns = [
        r'(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)',  # lat, lon
        r'Latitude:\s*(-?\d+\.?\d*).*?Longitude:\s*(-?\d+\.?\d*)',  # labeled
        r'(-?\d+°\d+\'[\d.\'"]*[NS]).*?(-?\d+°\d+\'[\d.\'"]*[EW])',  # DMS
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            try:
                lat = float(match[0].replace('°', '').replace("'", '').replace('"', ''))
                lon = float(match[1].replace('°', '').replace("'", '').replace('"', ''))
                
                # Validate Indonesia bounds
                if -15 < lat < 10 and 95 < lon < 142:
                    return lat, lon
            except:
                continue
    
    return None


def process_batch(kecamatan_list: List[str], start_index: int, batch_size: int) -> Tuple[Dict, int]:
    """Process a batch of kecamatan"""
    results, _ = load_progress()
    
    end_index = min(start_index + batch_size, len(kecamatan_list))
    
    print(f"\n📍 Processing batch: {start_index+1} to {end_index} of {len(kecamatan_list)}")
    
    for i in range(start_index, end_index):
        kecamatan = kecamatan_list[i]
        
        # Skip if already found
        if kecamatan in results:
            print(f"[{i+1}/{len(kecamatan_list)}] ✓ {kecamatan} (cached)")
            continue
        
        # Search for coordinates
        print(f"[{i+1}/{len(kecamatan_list)}] 🔍 Searching: {kecamatan}")
        coords = search_kecamatan_coordinates(kecamatan)
        
        if coords:
            lat, lon = coords
            results[kecamatan] = {
                "lat": lat,
                "lon": lon,
                "source": "web_search",
                "timestamp": datetime.now().isoformat()
            }
            print(f"  ✅ Found: {lat}, {lon}")
        else:
            print(f"  ❌ Not found")
        
        # Save progress after each search
        save_progress(results, i + 1)
        
        # Rate limiting
        import time
        time.sleep(RATE_LIMIT)
    
    return results, end_index


def main():
    print("=" * 60)
    print("🇮🇩 Batch Kecamatan Coordinate Search")
    print("=" * 60)
    print(f"Output: {OUTPUT_FILE}")
    print(f"Progress: {PROGRESS_FILE}")
    print(f"Batch Size: {BATCH_SIZE}")
    print(f"Rate Limit: {RATE_LIMIT}s")
    print()
    
    # Load progress
    results, next_index = load_progress()
    print(f"Resuming from index: {next_index}")
    print(f"Already found: {len(results)} locations")
    print()
    
    # Process all batches
    total = len(KECAMATAN_BASE)
    while next_index < total:
        results, next_index = process_batch(KECAMATAN_BASE, next_index, BATCH_SIZE)
        
        # Check if we should continue
        if next_index >= total:
            break
        
        print(f"\n⏸️  Progress: {next_index}/{total} ({100*next_index/total:.1f}%)")
        cont = input("Continue? (Enter=yes, q=quit): ").strip().lower()
        if cont == 'q':
            break
    
    # Save final results
    save_final_results(results)
    
    print("\n" + "=" * 60)
    print("✅ Complete!")
    print(f"Total locations: {len(results)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
