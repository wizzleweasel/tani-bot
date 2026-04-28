#!/usr/bin/env python3
"""Test Assistant Bot"""

import requests

TOKEN = "8676588212:AAGs9wKmvdf4zfdHPFqwua5CXMA_9o7E1Nw"
CHAT_ID = "8689301832"

print("=" * 60)
print("🤖 TESTING ASSISTANT BOT")
print("=" * 60)

# Get bot info
url = f"https://api.telegram.org/bot{TOKEN}/getMe"
response = requests.get(url)

if response.status_code == 200:
    bot_info = response.json().get('result', {})
    print(f"\n✅ Bot Name: @{bot_info.get('username', 'N/A')}")
    print(f"✅ Bot ID: {bot_info.get('id', 'N/A')}")
    print(f"✅ Can join groups: {bot_info.get('can_join_groups', False)}")
    
    # Send test message
    print("\n📤 Sending test message...")
    send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": "✅ Assistant Bot Active!\n\nI'm your general-purpose assistant (separate from TaniBot dev).\n\nUse me for:\n- General questions\n- Unrelated tasks\n- Random requests\n- Daily assistance\n\nTaniBot dev stays in @tani_pintar_bot 🌾"
    }
    
    send_response = requests.post(send_url, json=data)
    if send_response.status_code == 200:
        print("✅ Test message sent!")
    else:
        print(f"❌ Send failed: {send_response.json()}")
else:
    print(f"❌ Bot test failed: {response.json()}")

print("\n" + "=" * 60)
