#!/usr/bin/env python3
"""Upload Kecamatan Data to tani-bot-cuaca Space"""

from huggingface_hub import HfApi, login
import os

# Login with HF token from environment
HF_TOKEN = os.environ.get("HF_TOKEN")
if not HF_TOKEN:
    print("❌ HF_TOKEN not set. Please set environment variable.")
    exit(1)
login(token=HF_TOKEN)

# Initialize API
api = HfApi()

# Upload kecamatan_coords.json to tani-bot-cuaca space
print("🚀 Uploading kecamatan data to tani-bot-cuaca Space...")
print("=" * 60)

try:
    # Upload the kecamatan_coords.json file
    repo_url = api.upload_file(
        path_or_fileobj="/mnt/data/openclaw/workspace/.openclaw/workspace/datasets/kecamatan_coords.json",
        path_in_repo="datasets/kecamatan_coords.json",
        repo_id="baguswicak/tani-bot-cuaca",
        repo_type="space",
        commit_message="🎉 Add 7,215 kecamatan coordinates database"
    )
    
    print(f"\n✅ Upload Complete!")
    print(f"📍 HF Space: https://huggingface.co/spaces/baguswicak/tani-bot-cuaca")
    print(f"📦 File: datasets/kecamatan_coords.json (7,215 locations)")
    
except Exception as e:
    print(f"❌ Error: {e}")

# Upload app.py from weather-only
print("\n🚀 Uploading app.py...")
try:
    repo_url = api.upload_file(
        path_or_fileobj="/mnt/data/openclaw/workspace/.openclaw/workspace/hf_spaces/weather-only/app.py",
        path_in_repo="app.py",
        repo_id="baguswicak/tani-bot-cuaca",
        repo_type="space",
        commit_message="🌤️ Update app.py with kecamatan-level support"
    )
    
    print(f"✅ app.py uploaded!")
    
except Exception as e:
    print(f"❌ Error uploading app.py: {e}")

print("\n" + "=" * 60)
print("🎉 Deployment to tani-bot-cuaca complete!")
print("=" * 60)
