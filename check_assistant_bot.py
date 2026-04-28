#!/usr/bin/env python3
"""Check Assistant Bot Deployment"""

from huggingface_hub import HfApi, login
import requests

HF_TOKEN = "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"
REPO_ID = "baguswicak/usual-bot"

print("=" * 60)
print("🤖 CHECKING ASSISTANT BOT DEPLOYMENT")
print("=" * 60)

# Login
login(token=HF_TOKEN)
api = HfApi()

# Get space info
print(f"\n📊 Space: {REPO_ID}")
try:
    # Check via API
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    runtime_url = f"https://huggingface.co/api/spaces/{REPO_ID}/runtime"
    response = requests.get(runtime_url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        runtime = response.json()
        state = runtime.get('state', 'Unknown')
        print(f"✅ State: {state}")
        
        if state == 'RUNNING':
            print("\n🎉 BOT IS RUNNING!")
            print("\n📱 Test: Message @usualclaw_bot on Telegram")
            print("   Send: /start")
        elif state == 'BUILDING':
            print("\n⏳ Building... (wait 2-3 min)")
        else:
            print(f"\n⚠️ State: {state}")
    else:
        print(f"⚠️ Could not get runtime: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
