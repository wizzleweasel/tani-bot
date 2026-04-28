#!/usr/bin/env python3
"""Trigger HF Spaces rebuild"""

from huggingface_hub import HfApi, login

HF_TOKEN = "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"
REPO_ID = "baguswicak/tani-bot"

print("Triggering HF Spaces rebuild...")

login(token=HF_TOKEN)
api = HfApi()

# Upload a dummy file to trigger rebuild
import tempfile
import os

with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
    f.write("Trigger rebuild - API key fix")
    temp_file = f.name

try:
    api.upload_file(
        path_or_fileobj=temp_file,
        path_in_repo=".rebuild-trigger",
        repo_id=REPO_ID,
        repo_type="space",
        commit_message="trigger: Rebuild to apply API key fix"
    )
    print("✅ Rebuild triggered!")
    print(f"\n🔗 Space: https://huggingface.co/spaces/{REPO_ID}")
    print("\n⏳ Wait 2-3 minutes for rebuild")
finally:
    os.unlink(temp_file)
