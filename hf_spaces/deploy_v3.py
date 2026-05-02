#!/usr/bin/env python3
"""Deploy TaniBot V3.0 to HF Space - Clean Deployment"""

from huggingface_hub import HfApi, login
import os

# Get token from environment
HF_TOKEN = os.environ.get("HF_TOKEN")
if not HF_TOKEN:
    print("❌ Error: HF_TOKEN not set")
    exit(1)

login(token=HF_TOKEN)
api = HfApi()

print("=" * 70)
print("🚀 DEPLOYING TaniBot V3.0 - ALL 5 PAGES")
print("=" * 70)

try:
    repo_url = api.upload_folder(
        folder_path="./",
        repo_id="baguswicak/tani-bot",
        repo_type="space",
        commit_message="🚀 TaniBot V3.0 - All 5 Pages Ready\n\n- Home, Weather, Crop Advisor, Yield, RAG Chat\n- GitHub CDN integration\n- 784KB clean deployment",
        create_pr=False,
        ignore_patterns=[
            "__pycache__/",
            "*.pyc",
            ".git/",
            "composio-venv/",
            "checkpoints/",
            ".ipynb_checkpoints/",
        ]
    )
    
    print("\n✅ DEPLOYMENT SUCCESSFUL!")
    print(f"\n📍 HF Space: https://huggingface.co/spaces/baguswicak/tani-bot")
    print(f"📦 GitHub: https://github.com/wizzleweasel/tani-bot")
    print(f"⚡ Size: 784KB")
    print(f"🎯 Pages: 5 (Home, Weather, Crop, Yield, RAG)")
    
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 70)
