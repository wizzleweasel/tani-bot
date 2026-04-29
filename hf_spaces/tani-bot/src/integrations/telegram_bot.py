#!/usr/bin/env python3
"""TaniBot Telegram Bot Integration"""

import requests
import json
from typing import Optional, Dict

class TaniBotTelegram:
    """Telegram bot for TaniBot agricultural assistant"""
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        
    def send_message(self, chat_id: str, text: str, parse_mode: str = "Markdown") -> Dict:
        """Send text message to chat"""
        url = f"{self.base_url}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            return response.json()
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def get_me(self) -> Dict:
        """Get bot info"""
        url = f"{self.base_url}/getMe"
        try:
            response = requests.get(url, timeout=10)
            return response.json()
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def send_welcome(self, chat_id: str) -> Dict:
        """Send welcome message"""
        welcome_text = """
🌾 *Welcome to TaniBot!*

I'm your agricultural AI assistant for Indonesia. I can help you with:

📊 *Crop Recommendations*
- Best crops for your location
- Planting season optimization
- Expected yield predictions

🌤️ *Weather Insights*
- Current weather conditions
- 7-day forecasts
- Climate analysis

📈 *Yield Predictions*
- ML-powered estimates
- Historical comparisons
- Optimization tips

*Currently in Beta* - Phase 1 Development

To get started, try:
- "What crops grow well in Jawa Barat?"
- "Weather forecast for Jakarta"
- "Predict rice yield"
"""
        return self.send_message(chat_id, welcome_text)
    
    def send_weather_update(self, chat_id: str, location: str, weather_data: Dict) -> Dict:
        """Send weather update"""
        current = weather_data.get('current', {})
        temp = current.get('temperature_2m', 'N/A')
        humidity = current.get('relative_humidity_2m', 'N/A')
        rain = current.get('precipitation', 'N/A')
        
        text = f"""
🌤️ *Weather Update - {location}*

🌡️ Temperature: {temp}°C
💧 Humidity: {humidity}%
🌧️ Rainfall: {rain}mm

_Data from Open-Meteo API_
"""
        return self.send_message(chat_id, text)
    
    def send_crop_recommendation(self, chat_id: str, crop: str, recommendation: str) -> Dict:
        """Send crop recommendation"""
        text = f"""
🌾 *Crop Recommendation: {crop}*

{recommendation}

_Would you like more details?_
"""
        return self.send_message(chat_id, text)
    
    def send_error(self, chat_id: str, error_message: str) -> Dict:
        """Send error message"""
        text = f"""
⚠️ *Error*

{error_message}

Please try again or contact support.
"""
        return self.send_message(chat_id, text)


# Test the bot
if __name__ == "__main__":
    # Token from user
    TOKEN = "8693067374:AAEGnQrRfIXMvWf7wwhn8ELo_IiaOcBNKS0"
    
    bot = TaniBotTelegram(TOKEN)
    
    print("=" * 60)
    print("🤖 TESTING TANIBOT TELEGRAM BOT")
    print("=" * 60)
    
    # Get bot info
    print("\n1. Getting bot info...")
    bot_info = bot.get_me()
    if bot_info.get('ok'):
        result = bot_info.get('result', {})
        print(f"   ✅ Bot name: @{result.get('username', 'N/A')}")
        print(f"   ✅ Bot ID: {result.get('id', 'N/A')}")
        print(f"   ✅ Can join groups: {result.get('can_join_groups', False)}")
    else:
        print(f"   ❌ Error: {bot_info}")
    
    print("\n✅ Bot test complete!")
    print("\nNext: Send test message to your Telegram")
