#!/usr/bin/env python3
"""
Send Telegram Update - Kecamatan Automation Progress
"""

import requests
import json
from datetime import datetime

# Telegram Bot Configuration
BOT_TOKEN = "8693067374:AAEGnQrRfIXMvWf7wwhn8ELo_IiaOcBNKS0"
CHAT_ID = "8689301832"

def send_telegram_update(message):
    """Send message to Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Telegram update sent!")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    # Test message
    msg = """
🗺️ **KECAMATAN AUTOMATION STARTED**

📊 **Progress**: 10/7,215 (0.1%)
⏱️ **Started**: 2026-04-29 14:54 UTC
🎯 **Target**: All 7,215 kecamatan

📍 **Current Batch**:
- Aceh (Simeulue): 10 kecamatan ✅
- Next: Remaining Aceh districts

⚠️ **Note**: This is a 3-4 day automation process
    """
    
    send_telegram_update(msg)
