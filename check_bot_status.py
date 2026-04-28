#!/usr/bin/env python3
"""Check Assistant Bot Status"""

import requests

TOKEN = "8676588212:AAGs9wKmvdf4zfdHPFqwua5CXMA_9o7E1Nw"

print("=" * 60)
print("🤖 CHECKING @usualclaw_bot STATUS")
print("=" * 60)

# Get bot info
url = f"https://api.telegram.org/bot{TOKEN}/getMe"
response = requests.get(url)

if response.status_code == 200:
    bot_info = response.json().get('result', {})
    print(f"\n✅ Bot Username: @{bot_info.get('username', 'N/A')}")
    print(f"✅ Bot ID: {bot_info.get('id', 'N/A')}")
    print(f"✅ Bot Name: {bot_info.get('first_name', 'N/A')}")
    print(f"✅ Can join groups: {bot_info.get('can_join_groups', False)}")
    print(f"✅ Can read messages: {bot_info.get('can_read_all_group_messages', False)}")
    print(f"✅ Supports inline: {bot_info.get('supports_inline_queries', False)}")
    
    # Get updates (check if bot received messages)
    print("\n📬 Checking recent updates...")
    updates_url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    updates_response = requests.get(updates_url)
    
    if updates_response.status_code == 200:
        updates = updates_response.json().get('result', [])
        if updates:
            print(f"✅ Found {len(updates)} recent message(s)")
            for update in updates[-3:]:
                if 'message' in update:
                    msg = update['message']
                    print(f"  - From: {msg.get('from', {}).get('first_name', 'Unknown')}")
                    print(f"    Text: {msg.get('text', 'N/A')}")
        else:
            print("⚠️ No recent messages received")
            print("\n💡 Possible issues:")
            print("  1. Bot not started yet (send /start)")
            print("  2. Chat ID not saved")
            print("  3. Bot blocked by user")
    else:
        print(f"❌ Updates check failed: {updates_response.json()}")
else:
    print(f"❌ Bot check failed: {response.json()}")

print("\n" + "=" * 60)
