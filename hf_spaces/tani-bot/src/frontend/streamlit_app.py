#!/usr/bin/env python3
"""TaniBot Streamlit Dashboard MVP"""

import streamlit as st
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipelines.weather_pipeline import WeatherPipeline
from data.synthetic_data import SyntheticDataGenerator
from llm.groq_client import TaniBotLLM
from ml.yield_predictor import YieldPredictor

# Page config
st.set_page_config(
    page_title="TaniBot - Agricultural AI Assistant",
    page_icon="🌾",
    layout="wide"
)

# Initialize session state
if 'weather_pipeline' not in st.session_state:
    st.session_state.weather_pipeline = WeatherPipeline()
if 'synthetic_gen' not in st.session_state:
    st.session_state.synthetic_gen = SyntheticDataGenerator()
if 'llm' not in st.session_state:
    st.session_state.llm = None  # Will initialize with API key
if 'predictor' not in st.session_state:
    st.session_state.predictor = None

# Sidebar
st.sidebar.title("🌾 TaniBot")
st.sidebar.markdown("**Agricultural AI Assistant for Indonesia**")

# Initialize LLM with environment variable (HF Spaces secrets)
import os
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY", "")

if groq_api_key:
    st.session_state.llm = TaniBotLLM(groq_api_key)
    st.sidebar.success("✅ LLM Connected")
else:
    st.sidebar.warning("⚠️ GROQ_API_KEY not set")

# Main navigation
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "🌤️ Weather", "🌾 Crop Advisor", "📊 Yield Prediction", "💬 Chat"]
)

# Home Page
if page == "🏠 Home":
    st.title("🌾 Welcome to TaniBot")
    st.markdown("""
    ### Agricultural AI Assistant for Indonesia
    
    TaniBot combines machine learning and large language models to help Indonesian farmers with:
    
    - 🌤️ **Weather Insights** - Current conditions and forecasts
    - 🌾 **Crop Recommendations** - Best crops for your location
    - 📊 **Yield Predictions** - ML-powered estimates
    - 💬 **Conversational AI** - Ask questions in Indonesian or English
    
    ---
    
    ### Phase 1 Features (Ready!)
    
    ✅ Weather pipeline (Open-Meteo API)  
    ✅ Synthetic agricultural data  
    ✅ XGBoost yield predictor  
    ✅ Groq LLM integration  
    ✅ Telegram bot (@tani_pintar_bot)  
    
    ---
    
    ### Quick Stats
    
    - **Crops in Database:** 19 (staples, fruits, vegetables, industrial)
    - **Sample Fields:** 20 across Indonesia
    - **Weather Data:** 365 days historical
    - **Model Accuracy:** R² = 0.96 (training), 0.66 (test)
    """)
    
    # Show sample data
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Crops", "19")
    with col2:
        st.metric("Fields", "20")
    with col3:
        st.metric("Model R²", "0.96")

# Weather Page
elif page == "🌤️ Weather":
    st.title("🌤️ Weather Insights")
    
    # Location input
    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input("Location", "Jakarta")
    with col2:
        lat = st.number_input("Latitude", value=-6.2088, format="%.4f")
        lon = st.number_input("Longitude", value=106.8456, format="%.4f")
    
    if st.button("Get Weather"):
        with st.spinner("Fetching weather data..."):
            weather = st.session_state.weather_pipeline.get_weather_for_location(lat, lon, location)
            
            # Current weather
            st.subheader(f"Current Weather in {location}")
            current = weather.get('current', {})
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Temperature", f"{current.get('temperature_2m', 'N/A')}°C")
            with col2:
                st.metric("Humidity", f"{current.get('relative_humidity_2m', 'N/A')}%")
            with col3:
                st.metric("Rainfall", f"{current.get('precipitation', 'N/A')}mm")
            with col4:
                st.metric("Wind Speed", f"{current.get('wind_speed_10m', 'N/A')} km/h")
            
            # 7-day forecast
            st.subheader("7-Day Forecast")
            forecast = weather.get('forecast', {})
            if forecast:
                dates = forecast.get('time', [])
                temps_max = forecast.get('temperature_2m_max', [])
                temps_min = forecast.get('temperature_2m_min', [])
                
                forecast_data = {
                    'Date': dates[:7],
                    'Max Temp (°C)': temps_max[:7],
                    'Min Temp (°C)': temps_min[:7]
                }
                st.dataframe(forecast_data, use_container_width=True)

# Crop Advisor Page
elif page == "🌾 Crop Advisor":
    st.title("🌾 Crop Advisor")
    
    crop = st.selectbox(
        "Select Crop",
        ["Rice (Padi)", "Corn (Jagung)", "Cassava (Singkong)", "Durian", "Mango (Mangga)", 
         "Banana (Pisang)", "Chili (Cabe)", "Coffee (Kopi)", "Palm Oil (Kelapa Sawit)"]
    )
    
    location = st.text_input("Location/Province", "Jawa Barat")
    
    if st.button("Get Advice") and st.session_state.llm:
        with st.spinner("Getting crop advice..."):
            result = st.session_state.llm.get_crop_advice(crop, location)
            
            if result.get('success'):
                st.success("✅ Advice generated!")
                st.markdown(result['content'])
                st.info(f"Tokens used: {result['usage']['total_tokens']}")
            else:
                st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    elif not st.session_state.llm:
        st.warning("⚠️ Please enter Groq API key in sidebar to use LLM features")

# Yield Prediction Page
elif page == "📊 Yield Prediction":
    st.title("📊 Yield Prediction")
    
    st.markdown("""
    ### XGBoost Yield Predictor
    
    Our ML model predicts crop yields based on:
    - Growing season duration
    - Base yield potential
    - Rainfall requirements
    - Temperature conditions
    - Soil pH
    
    **Model Performance:**
    - Training R²: 0.96
    - Test R²: 0.66
    - MAE: 1.34 ton/hectare
    """)
    
    # Simple prediction form
    col1, col2 = st.columns(2)
    with col1:
        crop_name = st.text_input("Crop Name", "Rice (Padi)")
        temp = st.number_input("Avg Temperature (°C)", value=27.0)
        rainfall = st.number_input("Avg Rainfall (mm)", value=150.0)
    
    with col2:
        growing_days = st.number_input("Growing Season (days)", value=120)
        base_yield = st.number_input("Base Yield (ton/ha)", value=6.5)
    
    if st.button("Predict Yield"):
        # Load predictor
        if st.session_state.predictor is None:
            with st.spinner("Loading model..."):
                st.session_state.predictor = YieldPredictor()
                # Train on synthetic data (in production, load pre-trained model)
                st.session_state.predictor.train()
        
        # Make prediction
        result = st.session_state.predictor.predict(
            crop_name, temp, rainfall, growing_days, base_yield
        )
        
        if 'error' not in result:
            st.success(f"### Predicted Yield: {result['predicted_yield']:.2f} ton/hectare")
            st.info(f"Conditions: {temp}°C, {rainfall}mm rainfall")
        else:
            st.error(f"Error: {result['error']}")

# Chat Page
elif page == "💬 Chat":
    st.title("💬 Chat with TaniBot")
    
    if not st.session_state.llm:
        st.warning("⚠️ Please enter Groq API key in sidebar to use chat")
    else:
        # Initialize chat history
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # User input
        if prompt := st.chat_input("Ask about Indonesian agriculture..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    result = st.session_state.llm.ask_agriculture(prompt)
                    
                    if result.get('success'):
                        response = result['content']
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.info(f"Tokens: {result['usage']['total_tokens']}")
                    else:
                        st.error(f"Error: {result.get('error', 'Unknown error')}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**TaniBot v0.1.0**")
st.sidebar.markdown("Phase 1 - MVP")
