#!/usr/bin/env python3
"""Deploy Assistant Bot to Railway"""

import subprocess
import os

BOT_PATH = "/mnt/data/openclaw/workspace/assistant-bot"

print("=" * 60)
print("🚂 DEPLOYING TO RAILWAY")
print("=" * 60)

# Check if Railway CLI is installed
print("\n1. Checking Railway CLI...")
try:
    result = subprocess.run(["railway", "--version"], capture_output=True, text=True)
    print(f"✅ Railway CLI installed: {result.stdout.strip()}")
except FileNotFoundError:
    print("❌ Railway CLI not found")
    print("\nInstall it:")
    print("  npm install -g @railway/cli")
    print("  Or: https://railway.app/cli")
    exit(1)

# Navigate to bot directory
print(f"\n2. Navigating to bot directory...")
os.chdir(BOT_PATH)
print(f"   {BOT_PATH}")

# Login to Railway
print("\n3. Railway login...")
print("   Opening browser for login...")
subprocess.run(["railway", "login"])

# Initialize project
print("\n4. Initializing Railway project...")
print("   This will create a new project on Railway")
subprocess.run(["railway", "init"])

# Add environment variables
print("\n5. Adding environment variables...")
subprocess.run(["railway", "variables", "set", "BOT_TOKEN=8676588212:AAGs9wKmvdf4zfdHPFqwua5CXMA_9o7E1Nw"])
subprocess.run(["railway", "variables", "set", "CHAT_ID=8689301832"])

# Deploy
print("\n6. Deploying to Railway...")
print("   This will take 2-5 minutes...")
subprocess.run(["railway", "up"])

# Open dashboard
print("\n7. Opening Railway dashboard...")
subprocess.run(["railway", "open"])

print("\n" + "=" * 60)
print("🎉 DEPLOYMENT COMPLETE!")
print("=" * 60)
print("\n✅ Bot is now running on Railway!")
print("\n📱 Test: Message @usualclaw_bot on Telegram")
print("   Send: /start")
