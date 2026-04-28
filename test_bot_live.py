#!/usr/bin/env python3
"""Test Assistant Bot Live"""

import requests

BOT_TOKEN = "8676588212:AAGs9wKmvdf4zfdHPFqwua5CXMA_9o7E1Nw"
CHAT_ID = "8689301832"

print("=" * 60)
print("🤖 TESTING ASSISTANT BOT (LIVE)")
print("=" * 60)

# Send test message
print("\n📤 Sending test message to Telegram...")
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data = {
    "chat_id": CHAT_ID,
    "text": "🎉 **Bot Deployment Test!**\n\n✅ If you receive this, the bot is working!\n\n*Assistant Bot on HF Spaces*",
    "parse_mode": "Markdown"
}

response = requests.post(url, json=data, timeout=10)

if response.status_code == 200:
    print("✅ Test message sent successfully!")
    print("\n📱 Check your Telegram:")
    print("   - You should receive a message from @usualclaw_bot")
    print("   - If yes, bot is working!")
    print("\n✅ Next: Make space private in settings")
else:
    print(f"❌ Send failed: {response.json()}")
    print("\n⚠️ Bot might still be building")
    print("   Wait 2-3 minutes and try again")

print("\n" + "=" * 60)
