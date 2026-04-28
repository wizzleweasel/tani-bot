#!/usr/bin/env python3
"""Check Bot Updates"""

import requests

BOT_TOKEN = "8676588212:AAGs9wKmvdf4zfdHPFqwua5CXMA_9o7E1Nw"

print("=" * 60)
print("🤖 CHECKING BOT UPDATES")
print("=" * 60)

# Get recent updates
url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
response = requests.get(url, timeout=10)

if response.status_code == 200:
    updates = response.json().get('result', [])
    
    if updates:
        print(f"\n✅ Found {len(updates)} recent message(s):\n")
        for update in updates[-5:]:
            if 'message' in update:
                msg = update['message']
                print(f"From: {msg.get('from', {}).get('first_name', 'Unknown')}")
                print(f"Text: {msg.get('text', 'N/A')}")
                print(f"Date: {msg.get('date', 'N/A')}")
                print("-" * 40)
    else:
        print("\n⚠️ No recent messages received")
        print("\nPossible issues:")
        print("1. Bot not started (send /start)")
        print("2. User blocked bot")
        print("3. Bot code not running on HF")
else:
    print(f"❌ Failed: {response.json()}")

print("\n" + "=" * 60)
