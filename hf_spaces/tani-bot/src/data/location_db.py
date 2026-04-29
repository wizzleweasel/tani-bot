"""Indonesian Location Database - Kecamatan Level"""

# Comprehensive list of kecamatan in Indonesia
# Format: "kecamatan, kabupaten/kota, provinsi": {"lat": ..., "lon": ...}
# Source: BPS Indonesia (simplified for practical use)

LOCATION_DB = {
    # === JAWA TIMUR ===
    "Pacet, Mojokerto, Jawa Timur": {"lat": -7.5333, "lon": 112.4333},
    "Ngoro, Mojokerto, Jawa Timur": {"lat": -7.4167, "lon": 112.7333},
    "Puri, Mojokerto, Jawa Timur": {"lat": -7.4000, "lon": 112.6833},
    "Trawas, Mojokerto, Jawa Timur": {"lat": -7.5167, "lon": 112.5167},
    "Dlanggu, Mojokerto, Jawa Timur": {"lat": -7.5167, "lon": 112.6167},
    "Kedungadem, Mojokerto, Jawa Timur": {"lat": -7.3833, "lon": 112.6500},
    "Gudo, Gresik, Jawa Timur": {"lat": -7.1333, "lon": 112.6333},
    "Bangkalan, Bangkalan, Jawa Timur": {"lat": -7.0667, "lon": 112.8167},
    "Sampang, Sampang, Jawa Timur": {"lat": -6.9000, "lon": 112.7667},
    "Pamekasan, Pamekasan, Jawa Timur": {"lat": -7.1667, "lon": 113.5000},
    "Sumenep, Sumenep, Jawa Timur": {"lat": -6.9000, "lon": 113.9167},
    "Kediri, Kediri, Jawa Timur": {"lat": -7.8167, "lon": 112.0167},
    "Nganjuk, Nganjuk, Jawa Timur": {"lat": -7.6000, "lon": 111.9000},
    "Madiun, Madiun, Jawa Timur": {"lat": -7.6333, "lon": 111.5333},
    "Magetan, Magetan, Jawa Timur": {"lat": -7.6833, "lon": 111.3333},
    "Ngawi, Ngawi, Jawa Timur": {"lat": -7.1167, "lon": 111.5500},
    "Bojonegoro, Bojonegoro, Jawa Timur": {"lat": -7.1000, "lon": 112.1667},
    "Tuban, Tuban, Jawa Timur": {"lat": -6.8833, "lon": 112.0333},
    "Lamongan, Lamongan, Jawa Timur": {"lat": -7.0167, "lon": 112.4333},
    "Gresik, Gresik, Jawa Timur": {"lat": -7.1500, "lon": 112.6500},
    "Bangkalan, Bangkalan, Jawa Timur": {"lat": -7.0833, "lon": 112.8333},
    "Sidoarjo, Sidoarjo, Jawa Timur": {"lat": -7.4500, "lon": 112.7167},
    "Pasuruan, Pasuruan, Jawa Timur": {"lat": -7.6333, "lon": 112.9000},
    "Probolinggo, Probolinggo, Jawa Timur": {"lat": -7.7500, "lon": 113.2167},
    "Lumajang, Lumajang, Jawa Timur": {"lat": -8.1333, "lon": 113.2167},
    "Jember, Jember, Jawa Timur": {"lat": -8.1667, "lon": 113.7000},
    "Banyuwangi, Banyuwangi, Jawa Timur": {"lat": -8.2167, "lon": 114.3667},
    "Bondowoso, Bondowoso, Jawa Timur": {"lat": -7.9167, "lon": 113.8167},
    "Situbondo, Situbondo, Jawa Timur": {"lat": -7.7000, "lon": 114.0000},
    "Jember, Jember, Jawa Timur": {"lat": -8.1833, "lon": 113.7000},
    "Malang, Malang, Jawa Timur": {"lat": -7.9833, "lon": 112.6333},
    "Blitar, Blitar, Jawa Timur": {"lat": -8.1000, "lon": 112.1667},
    "Batu, Batu, Jawa Timur": {"lat": -7.8667, "lon": 112.5333},
    
    # === JAWA TENGAH ===
    "Semarang, Semarang, Jawa Tengah": {"lat": -6.9667, "lon": 110.4167},
    "Solo, Surakarta, Jawa Tengah": {"lat": -7.5667, "lon": 110.8167},
    "Magelang, Magelang, Jawa Tengah": {"lat": -7.5833, "lon": 110.2000},
    "Salatiga, Salatiga, Jawa Tengah": {"lat": -7.3333, "lon": 110.5000},
    "Cilacap, Cilacap, Jawa Tengah": {"lat": -7.7167, "lon": 109.0167},
    "Pekalongan, Pekalongan, Jawa Tengah": {"lat": -6.8833, "lon": 109.6667},
    "Tegal, Tegal, Jawa Tengah": {"lat": -6.8667, "lon": 109.1500},
    "Kebumen, Kebumen, Jawa Tengah": {"lat": -7.6667, "lon": 109.6500},
    "Purworejo, Purworejo, Jawa Tengah": {"lat": -7.7500, "lon": 110.0333},
    "Wonosobo, Wonosobo, Jawa Tengah": {"lat": -7.3667, "lon": 109.9000},
    "Temanggung, Temanggung, Jawa Tengah": {"lat": -7.3000, "lon": 110.1667},
    "Kendal, Kendal, Jawa Tengah": {"lat": -6.9167, "lon": 110.2000},
    "Batang, Batang, Jawa Tengah": {"lat": -6.9000, "lon": 109.7667},
    "Pemalang, Pemalang, Jawa Tengah": {"lat": -6.8833, "lon": 109.3833},
    "Brebes, Brebes, Jawa Tengah": {"lat": -6.8667, "lon": 109.0167},
    
    # === DAERAH ISTIMEWA YOGYAKARTA ===
    "Yogyakarta, Yogyakarta, DIY": {"lat": -7.7956, "lon": 110.3695},
    "Sleman, Sleman, DIY": {"lat": -7.7000, "lon": 110.3500},
    "Bantul, Bantul, DIY": {"lat": -7.8833, "lon": 110.3333},
    "Kulon Progo, Kulon Progo, DIY": {"lat": -7.8000, "lon": 110.1667},
    "Gunung Kidul, Gunung Kidul, DIY": {"lat": -7.9833, "lon": 110.6833},
    
    # === JAWA BARAT ===
    "Bandung, Bandung, Jawa Barat": {"lat": -6.9175, "lon": 107.6191},
    "Bekasi, Bekasi, Jawa Barat": {"lat": -6.2333, "lon": 106.9833},
    "Depok, Depok, Jawa Barat": {"lat": -6.4000, "lon": 106.8167},
    "Bogor, Bogor, Jawa Barat": {"lat": -6.5833, "lon": 106.8000},
    "Cirebon, Cirebon, Jawa Barat": {"lat": -6.7000, "lon": 108.5500},
    "Tasikmalaya, Tasikmalaya, Jawa Barat": {"lat": -7.3500, "lon": 108.2167},
    "Sukabumi, Sukabumi, Jawa Barat": {"lat": -6.9333, "lon": 106.9333},
    "Garut, Garut, Jawa Barat": {"lat": -7.2000, "lon": 107.9000},
    "Cianjur, Cianjur, Jawa Barat": {"lat": -6.8167, "lon": 107.1333},
    "Subang, Subang, Jawa Barat": {"lat": -6.5833, "lon": 107.7000},
    "Purwakarta, Purwakarta, Jawa Barat": {"lat": -6.5500, "lon": 107.4333},
    "Karawang, Karawang, Jawa Barat": {"lat": -6.3000, "lon": 107.3000},
    "Indramayu, Indramayu, Jawa Barat": {"lat": -6.3333, "lon": 108.3167},
    "Kuningan, Kuningan, Jawa Barat": {"lat": -7.0167, "lon": 108.4833},
    "Ciamis, Ciamis, Jawa Barat": {"lat": -7.3333, "lon": 108.3333},
    "Banjar, Banjar, Jawa Barat": {"lat": -7.3667, "lon": 108.5333},
    "Pangandaran, Ciamis, Jawa Barat": {"lat": -7.6833, "lon": 108.6500},
    
    # === JAKARTA ===
    "Jakarta Pusat, DKI Jakarta": {"lat": -6.1862, "lon": 106.8341},
    "Jakarta Utara, DKI Jakarta": {"lat": -6.1300, "lon": 106.8700},
    "Jakarta Barat, DKI Jakarta": {"lat": -6.1684, "lon": 106.7593},
    "Jakarta Selatan, DKI Jakarta": {"lat": -6.2615, "lon": 106.8106},
    "Jakarta Timur, DKI Jakarta": {"lat": -6.2146, "lon": 106.9004},
    
    # === BALI ===
    "Denpasar, Denpasar, Bali": {"lat": -8.6705, "lon": 115.2126},
    "Badung, Badung, Bali": {"lat": -8.5333, "lon": 115.1667},
    "Gianyar, Gianyar, Bali": {"lat": -8.5333, "lon": 115.3167},
    "Tabanan, Tabanan, Bali": {"lat": -8.5167, "lon": 115.1333},
    "Klungkung, Klungkung, Bali": {"lat": -8.5333, "lon": 115.4000},
    "Bangli, Bangli, Bali": {"lat": -8.4500, "lon": 115.3500},
    "Karangasem, Karangasem, Bali": {"lat": -8.4333, "lon": 115.6000},
    "Ubud, Gianyar, Bali": {"lat": -8.5167, "lon": 115.2667},
    "Nusa Dua, Badung, Bali": {"lat": -8.8000, "lon": 115.1667},
    "Sanur, Denpasar, Bali": {"lat": -8.7000, "lon": 115.2667},
    
    # === SUMATERA ===
    "Medan, Medan, Sumatera Utara": {"lat": 3.5952, "lon": 98.6722},
    "Binjai, Binjai, Sumatera Utara": {"lat": 3.6000, "lon": 98.4833},
    "Pematang Siantar, Pematang Siantar, Sumatera Utara": {"lat": 2.9500, "lon": 99.0667},
    "Tebing Tinggi, Tebing Tinggi, Sumatera Utara": {"lat": 3.3333, "lon": 99.1667},
    "Tanjung Balai, Tanjung Balai, Sumatera Utara": {"lat": 2.9667, "lon": 99.8167},
    "Padang, Padang, Sumatera Barat": {"lat": -0.9471, "lon": 100.4172},
    "Bukittinggi, Bukittinggi, Sumatera Barat": {"lat": -0.3056, "lon": 100.3667},
    "Payakumbuh, Payakumbuh, Sumatera Barat": {"lat": -0.2167, "lon": 100.6333},
    "Solok, Solok, Sumatera Barat": {"lat": -0.5667, "lon": 100.6500},
    "Palembang, Palembang, Sumatera Selatan": {"lat": -2.9761, "lon": 104.7754},
    "Prabumulih, Prabumulih, Sumatera Selatan": {"lat": -3.4333, "lon": 104.2333},
    "Pagar Alam, Pagar Alam, Sumatera Selatan": {"lat": -4.0167, "lon": 103.2500},
    "Lubuklinggau, Lubuklinggau, Sumatera Selatan": {"lat": -3.3000, "lon": 102.8667},
    "Jambi, Jambi, Jambi": {"lat": -1.6101, "lon": 103.6131},
    "Bandar Lampung, Bandar Lampung, Lampung": {"lat": -5.4292, "lon": 105.2619},
    "Metro, Metro, Lampung": {"lat": -5.1000, "lon": 105.3000},
    
    # === KALIMANTAN ===
    "Pontianak, Pontianak, Kalimantan Barat": {"lat": -0.0263, "lon": 109.3425},
    "Singkawang, Singkawang, Kalimantan Barat": {"lat": 0.9167, "lon": 108.9833},
    "Banjarmasin, Banjarmasin, Kalimantan Selatan": {"lat": -3.3194, "lon": 114.5908},
    "Banjarbaru, Banjarbaru, Kalimantan Selatan": {"lat": -3.4500, "lon": 114.8000},
    "Palangkaraya, Palangkaraya, Kalimantan Tengah": {"lat": -2.2000, "lon": 113.9167},
    "Balikpapan, Balikpapan, Kalimantan Timur": {"lat": -1.2379, "lon": 116.8529},
    "Samarinda, Samarinda, Kalimantan Timur": {"lat": -0.5022, "lon": 117.1536},
    "Tenggarong, Kutai Kartanegara, Kalimantan Timur": {"lat": -0.4167, "lon": 117.0167},
    "Sukamara, Sukamara, Kalimantan Tengah": {"lat": -1.9833, "lon": 113.4167},
    "Tanjung Selor, Bulungan, Kalimantan Utara": {"lat": 2.7500, "lon": 117.3667},
    
    # === SULAWESI ===
    "Makassar, Makassar, Sulawesi Selatan": {"lat": -5.1477, "lon": 119.4327},
    "Parepare, Parepare, Sulawesi Selatan": {"lat": -4.0167, "lon": 119.6333},
    "Palopo, Palopo, Sulawesi Selatan": {"lat": -2.9833, "lon": 120.1833},
    "Pare-pare, Parepare, Sulawesi Selatan": {"lat": -4.0167, "lon": 119.6333},
    "Palu, Palu, Sulawesi Tengah": {"lat": -0.8917, "lon": 119.8707},
    "Poso, Poso, Sulawesi Tengah": {"lat": -1.3833, "lon": 120.7667},
    "Gorontalo, Gorontalo, Gorontalo": {"lat": 0.5435, "lon": 123.0618},
    "Tomohon, Tomohon, Sulawesi Utara": {"lat": 1.3333, "lon": 124.8333},
    "Bitung, Bitung, Sulawesi Utara": {"lat": 1.4333, "lon": 125.1667},
    "Kotamobagu, Kotamobagu, Sulawesi Utara": {"lat": 0.7333, "lon": 124.3167},
    "Manado, Manado, Sulawesi Utara": {"lat": 1.4703, "lon": 124.8453},
    "Tahuna, Tahuna, Sulawesi Utara": {"lat": 3.6167, "lon": 126.1667},
    
    # === NUSA TENGGARA ===
    "Mataram, Mataram, Nusa Tenggara Barat": {"lat": -8.5833, "lon": 116.1167},
    "Bima, Bima, Nusa Tenggara Barat": {"lat": -8.4667, "lon": 118.7167},
    "Sumbawa Besar, Sumbawa, Nusa Tenggara Barat": {"lat": -8.4833, "lon": 117.4167},
    "Kupang, Kupang, Nusa Tenggara Timur": {"lat": -10.1707, "lon": 123.6073},
    "Ende, Ende, Nusa Tenggara Timur": {"lat": -8.8333, "lon": 121.6500},
    "Maumere, Sikka, Nusa Tenggara Timur": {"lat": -8.6167, "lon": 122.1667},
    "Labuan Bajo, Manggarai Barat, Nusa Tenggara Timur": {"lat": -8.4833, "lon": 119.8833},
    "Ruteng, Manggarai, Nusa Tenggara Timur": {"lat": -8.5333, "lon": 120.5000},
    
    # === PAPUA ===
    "Jayapura, Jayapura, Papua": {"lat": -2.5333, "lon": 140.7167},
    "Timika, Mimika, Papua": {"lat": -4.5333, "lon": 136.8833},
    "Merauke, Merauke, Papua": {"lat": -8.4833, "lon": 140.4000},
    "Nabire, Nabire, Papua": {"lat": -3.3667, "lon": 135.4833},
    "Wamena, Jayawijaya, Papua": {"lat": -4.0833, "lon": 138.9500},
    
    # === MALUKU ===
    "Ambon, Ambon, Maluku": {"lat": -3.6954, "lon": 128.1814},
    "Tual, Tual, Maluku": {"lat": -5.6167, "lon": 132.5833},
    "Saumlaki, Tanimbar, Maluku": {"lat": -8.1667, "lon": 131.3333},
    
    # === KEPULAUAN BANGKA BELITUNG ===
    "Pangkal Pinang, Pangkal Pinang, Bangka Belitung": {"lat": -2.1333, "lon": 106.1167},
    "Belinyu, Bangka, Bangka Belitung": {"lat": -2.3000, "lon": 106.3000},
    "Muntok, Bangka Barat, Bangka Belitung": {"lat": -2.5167, "lon": 105.6833},
    
    # === KEPULAUAN RIAU ===
    "Tanjung Pinang, Tanjung Pinang, Kepulauan Riau": {"lat": 0.9167, "lon": 104.4500},
    "Ranai, Natuna, Kepulauan Riau": {"lat": 3.7333, "lon": 108.3167},
}

# Add more kecamatan if needed
# This database can be expanded with more specific locations


def get_location_coords(location_query: str) -> tuple:
    """
    Get latitude and longitude for a location query.
    Returns (lat, lon) or (None, None) if not found.
    """
    location_query = location_query.strip()
    
    # Try exact match
    if location_query in LOCATION_DB:
        loc = LOCATION_DB[location_query]
        return loc["lat"], loc["lon"]
    
    # Try partial match
    for loc_name, coords in LOCATION_DB.items():
        if location_query.lower() in loc_name.lower():
            return coords["lat"], coords["lon"]
    
    return None, None


def get_location_suggestions(search_term: str) -> list:
    """
    Get autocomplete suggestions for location search.
    Returns list of location names matching the search term.
    """
    if not search_term:
        return []
    
    suggestions = []
    search_lower = search_term.lower()
    
    for loc_name in LOCATION_DB.keys():
        if search_lower in loc_name.lower():
            suggestions.append(loc_name)
    
    return sorted(suggestions, key=lambda x: x.split(',')[0])  # Sort by kecamatan
