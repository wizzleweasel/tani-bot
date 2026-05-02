#!/usr/bin/env python3
"""Upload kecamatan_coords.json to GitHub via API"""

from github import Github
import os

# Get GitHub token from environment or use default
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "ghp_xxxxx")

# Initialize GitHub client
g = Github(GITHUB_TOKEN)

# Get repository
repo = g.get_repo("wizzleweasel/tani-bot")

# Upload kecamatan_coords.json
print("🚀 Uploading kecamatan_coords.json to GitHub...")

with open("datasets/kecamatan_coords.json", "r") as f:
    content = f.read()

try:
    # Upload file
    repo.create_file(
        path="datasets/kecamatan_coords.json",
        message="feat: Add 7,215 kecamatan coordinates database",
        content=content,
        branch="main"
    )
    print("✅ File uploaded successfully!")
except Exception as e:
    print(f"Error: {e}")
    print("Note: This might fail if file already exists. Try updating instead.")
