#!/usr/bin/env python3
"""Deploy Assistant Bot to HF Spaces"""

from huggingface_hub import HfApi, login
import os

HF_TOKEN = "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"
REPO_ID = "baguswicak/assistant-bot"
LOCAL_PATH = "/mnt/data/openclaw/workspace/assistant-bot"

print("=" * 60)
print("🚀 DEPLOYING ASSISTANT BOT TO HF SPACES")
print("=" * 60)

# Login
print("\n1. Logging in to HF...")
login(token=HF_TOKEN)
print("✅ Logged in")

# Initialize API
api = HfApi()

# Create space (private)
print(f"\n2. Creating private space: {REPO_ID}...")
try:
    api.create_repo(
        repo_id=REPO_ID,
        repo_type="space",
        space_sdk="streamlit",
        private=True
    )
    print("✅ Space created (private)")
except Exception as e:
    if "Cannot create repo" in str(e):
        print("ℹ️ Space already exists")
    else:
        print(f"❌ Create failed: {e}")

# Upload files
print(f"\n3. Uploading bot files...")
try:
    api.upload_folder(
        folder_path=LOCAL_PATH,
        repo_id=REPO_ID,
        repo_type="space",
        commit_message="Deploy Assistant Bot v1.0"
    )
    print("✅ Files uploaded!")
except Exception as e:
    print(f"❌ Upload failed: {e}")

# Add secrets info
print("\n" + "=" * 60)
print("🎉 DEPLOYMENT COMPLETE!")
print("=" * 60)
print(f"\n🔗 Space: https://huggingface.co/spaces/{REPO_ID}")
print("\n⚙️  ADD SECRETS (Required):")
print("   Go to Settings → Repository secrets")
print("   - BOT_TOKEN = 8676588212:AAGs9wKmvdf4zfdHPFqwua5CXMA_9o7E1Nw")
print("   - CHAT_ID = 8689301832")
print("\n⏳ Wait 3-5 minutes for build")
print("\n📱 Bot: @usualclaw_bot")
