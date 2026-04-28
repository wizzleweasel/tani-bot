#!/usr/bin/env python3
"""Test Bot Message"""

import requests

BOT_TOKEN = "8676588212:AAGs9wKmvdf4zfdHPFqwua5CXMA_9o7E1Nw"
CHAT_ID = "8689301832"

print("Testing bot message...")

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data = {
    "chat_id": CHAT_ID,
    "text": "🤖 *Assistant Bot Test*\n\n✅ Bot is deployed and running!\n\n*HF Spaces*: baguswicak/usual-bot\n\nReady to help with general tasks!",
    "parse_mode": "Markdown"
}

response = requests.post(url, json=data, timeout=10)

if response.status_code == 200:
    print("✅ Message sent successfully!")
    print("Check Telegram for the message from @usualclaw_bot")
else:
    print(f"❌ Failed: {response.json()}")
