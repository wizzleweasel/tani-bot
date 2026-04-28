#!/usr/bin/env python3
"""Create Assistant Bot GitHub Repo"""

import requests
import json

# Load GitHub token from file
try:
    with open('/mnt/data/openclaw/workspace/.openclaw/workspace/.github_token.txt', 'r') as f:
        GITHUB_TOKEN = f.read().strip()
except:
    print("❌ GitHub token not found")
    print("\nManual creation needed:")
    print("1. Go to: https://github.com/new")
    print("2. Repository name: assistant-bot")
    print("3. Create repository")
    print("4. I'll push the code")
    exit(1)

BOT_REPO_PATH = "/mnt/data/openclaw/workspace/assistant-bot-github"
USERNAME = "wizzleweasel"
REPO_NAME = "assistant-bot"

print("=" * 60)
print("📦 CREATING GITHUB REPO FOR ASSISTANT BOT")
print("=" * 60)

# Create repo via GitHub API
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

repo_data = {
    "name": REPO_NAME,
    "description": "🤖 Assistant Bot - General Purpose Telegram Bot (Deployed on Railway)",
    "private": False,
    "auto_init": False
}

print(f"\n1. Creating repo: {USERNAME}/{REPO_NAME}...")
response = requests.post(
    "https://api.github.com/user/repos",
    headers=headers,
    json=repo_data
)

if response.status_code == 201:
    print("✅ Repo created!")
    repo_url = response.json().get('html_url')
    print(f"   URL: {repo_url}")
    
    # Save repo URL
    with open('/mnt/data/openclaw/workspace/.openclaw/workspace/assistant_bot_github_url.txt', 'w') as f:
        f.write(repo_url)
    
    print("\n2. Now push the code:")
    print(f"   cd {BOT_REPO_PATH}")
    print(f"   git remote add origin https://github.com/{USERNAME}/{REPO_NAME}.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    
elif response.status_code == 422:
    print("ℹ️ Repo already exists!")
    repo_url = f"https://github.com/{USERNAME}/{REPO_NAME}"
    print(f"   URL: {repo_url}")
else:
    print(f"❌ Create failed: {response.status_code}")
    print(response.json())
