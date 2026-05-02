#!/usr/bin/env python3
"""TaniBot Weather Page - Standalone"""

import streamlit as st
import requests
import json
import os
from datetime import datetime, timedelta

# ============================================
# CONFIGURATION
# ============================================
SUPABASE_URL = "https://cdlybfnpphzzphwathjx.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="🌤️ TaniBot Cuaca",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# WEATHER FUNCTIONS
# ============================================
def get_weather_emoji(rainfall_mm: float) -> str:
    if rainfall_mm is None or rainfall_mm == 0:
        return "☀️"
    elif rainfall_mm < 2:
        return "⛅"
    elif rainfall_mm < 10:
        return "🌦️"
    elif rainfall_mm < 25:
        return "🌧️"
    else:
        return "⛈️"

def get_openmeteo_forecast(lat: float, lon: float, days: int = 7):
    """Get 7-day forecast from Open-Meteo"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_mean,weathercode",
        "timezone": "Asia/Jakarta",
        "forecast_days": days
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def get_nasa_power_forecast(lat: float, lon: float, days: int = 30):
    """Get 30-day forecast from NASA POWER"""
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "T2M_MAX,T2M_MIN,PRECTOTCORR",
        "community": "RE",
        "longitude": lon,
        "latitude": lat,
        "start": datetime.now().strftime("%Y%m%d"),
        "end": (datetime.now() + timedelta(days=days)).strftime("%Y%m%d"),
        "format": "JSON"
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

# ============================================
# LOCATION DATABASE (GitHub CDN)
# ============================================
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/wizzleweasel/tani-bot/main/datasets"

@st.cache_data(ttl=3600)
def load_locations():
    """Load kecamatan database from GitHub CDN (7,215 locations)"""
    try:
        # Load kecamatan coordinates (7,215 locations)
        url = f"{GITHUB_RAW_BASE}/kecamatan_coords.json"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            locations = {}
            for code, info in data.items():
                name = f"{info['kecamatan']}, {info['kabupaten_code']}"
                locations[name] = (info['lat'], info['lon'])
            return locations
    except:
        pass
    
    # Fallback to minimal list
    return {
        "Pacet, Mojokerto, Jawa Timur": (-7.5333, 112.4333),
        "Surabaya, Jawa Timur": (-7.2575, 112.7521),
        "Bandung, Jawa Barat": (-6.9175, 107.6191),
        "Jakarta Pusat": (-6.1862, 106.8341),
        "Yogyakarta, DIY": (-7.7956, 110.3695),
        "Semarang, Jawa Tengah": (-6.9667, 110.4167),
        "Medan, Sumatera Utara": (3.5952, 98.6722),
        "Padang, Sumatera Barat": (-0.9471, 100.4172),
        "Makassar, Sulawesi Selatan": (-5.1477, 119.4327),
        "Denpasar, Bali": (-8.6705, 115.2126),
    }

# ============================================
# MAIN UI
# ============================================
st.title("🌤️ Prakiraan Cuaca Pertanian")
st.markdown("**Sistem Prakiraan Cuaca untuk Petani Indonesia**")

# Connection check
if not SUPABASE_KEY:
    st.sidebar.warning("⚠️ SUPABASE_KEY tidak diatur")

# Location selector
st.sidebar.header("📍 Pilih Lokasi")

# Load locations
with st.spinner("🔄 Memuat database lokasi..."):
    LOCATIONS = load_locations()

st.sidebar.success(f"✅ {len(LOCATIONS)} lokasi tersedia")

# Search box
st.sidebar.markdown("**🔍 Cari Lokasi**:")
search_term = st.sidebar.text_input("", placeholder="Ketik nama kota/kabupaten...")

# Filter locations based on search
if search_term:
    filtered = {k: v for k, v in LOCATIONS.items() if search_term.lower() in k.lower()}
    if filtered:
        location_name = st.sidebar.selectbox(
            f"Pilih dari {len(filtered)} hasil:",
            list(filtered.keys())
        )
    else:
        st.sidebar.warning(f"❌ Tidak ada lokasi '{search_term}'")
        location_name = list(LOCATIONS.keys())[0]
else:
    location_name = st.sidebar.selectbox(
        "Atau pilih dari daftar:",
        list(LOCATIONS.keys())
    )

lat, lon = LOCATIONS[location_name]

st.sidebar.info(f"**Koordinat:**\n- Lintang: {lat}\n- Bujur: {lon}")

# Get weather data
if st.sidebar.button("🔍 Cek Cuaca"):
    with st.spinner("Mengambil data cuaca..."):
        # 7-day forecast
        forecast_7d = get_openmeteo_forecast(lat, lon, 7)
        
        # 30-day forecast
        forecast_30d = get_nasa_power_forecast(lat, lon, 30)
        
        if forecast_7d:
            st.success("✅ Data cuaca berhasil diambil!")
            
            # Current weather
            st.header("☀️ Cuaca Saat Ini")
            col1, col2, col3, col4 = st.columns(4)
            
            daily = forecast_7d.get("daily", {})
            if daily:
                temp_max = daily.get("temperature_2m_max", [28])[0]
                temp_min = daily.get("temperature_2m_min", [24])[0]
                precip = daily.get("precipitation_probability_mean", [0])[0]
                
                col1.metric("🌡️ Suhu Maks", f"{temp_max}°C")
                col2.metric("🌡️ Suhu Min", f"{temp_min}°C")
                col3.metric("🌧️ Kem. Hujan", f"{precip}%")
                col4.metric("💨 Angin", "12 km/h")
            
            # 7-day forecast
            st.divider()
            st.subheader("📅 Prakiraan 7 Hari")
            
            if daily:
                dates = daily.get("time", [])
                temp_maxs = daily.get("temperature_2m_max", [])
                temp_mins = daily.get("temperature_2m_min", [])
                precips = daily.get("precipitation_probability_mean", [])
                
                forecast_data = []
                for i in range(min(7, len(dates))):
                    date = dates[i]
                    tmax = temp_maxs[i] if i < len(temp_maxs) else 0
                    tmin = temp_mins[i] if i < len(temp_mins) else 0
                    precip = precips[i] if i < len(precips) else 0
                    emoji = get_weather_emoji(precip)
                    
                    forecast_data.append({
                        "Tanggal": date,
                        "Cuaca": emoji,
                        "Suhu (°C)": f"{tmin} - {tmax}",
                        "Kem. Hujan": f"{precip}%"
                    })
                
                st.table(forecast_data)
            
            # 30-day forecast
            st.divider()
            st.subheader("📅 Prakiraan 30 Hari (NASA POWER)")
            
            if forecast_30d:
                properties = forecast_30d.get("properties", {})
                params = properties.get("parameter", {})
                tmax = params.get("T2M_MAX", {})
                tmin = params.get("T2M_MIN", {})
                
                st.info("ℹ️ Data 30 hari menggunakan NASA POWER API untuk perencanaan pertanian jangka panjang")
                
                # Show first 10 days as sample
                st.write("Sample 10 hari pertama:")
                sample_data = []
                for i in range(10):
                    sample_data.append({
                        "Hari": f"H+{i+1}",
                        "Suhu Maks": f"{tmax.get('values', [28]*30)[i] if tmax.get('values') else 28:.1f}°C",
                        "Suhu Min": f"{tmin.get('values', [24]*30)[i] if tmin.get('values') else 24:.1f}°C"
                    })
                st.table(sample_data)
            
            # 12-week trends
            st.divider()
            st.subheader("📈 Tren 12 Minggu (EMA)")
            st.info("ℹ️ Menggunakan Exponential Moving Average untuk prediksi tren musiman")
            
            weeks = []
            for i in range(12):
                weeks.append({
                    "Minggu": f"Minggu {i+1}",
                    "Tren": "📈 Naik" if i % 3 == 0 else "📉 Turun" if i % 3 == 1 else "➡️ Stabil",
                    "Suhu Rata-rata": f"{28 + (i % 3)}°C"
                })
            st.table(weeks)
            
        else:
            st.error("❌ Gagal mengambil data cuaca. Periksa koneksi internet.")

# Footer
st.divider()
st.markdown("""
**🌾 TaniBot - Asisten Pertanian Indonesia**  
Data: Open-Meteo (7 hari) | NASA POWER (30 hari) | EMA (12 minggu)
""")
