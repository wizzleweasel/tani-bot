# 🚀 Push TaniBot to GitHub

## Quick Push (2 minutes)

Since the repo is created, you need to push the code from your local workspace.

### Option A: Using GitHub CLI (Easiest)

1. **Install GitHub CLI** (if not installed):
   ```bash
   # On Linux
   sudo apt install gh
   
   # Or follow: https://cli.github.com/
   ```

2. **Authenticate:**
   ```bash
   gh auth login
   ```
   - Choose: GitHub.com
   - Choose: HTTPS
   - Login with browser

3. **Push the code:**
   ```bash
   cd /mnt/data/openclaw/workspace/tani-bot
   git remote add origin https://github.com/wizzleweasel/tani-bot.git
   git branch -M main
   git push -u origin main
   ```

### Option B: Using Personal Access Token

1. **Create Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Check: `repo` (Full control of private repositories)
   - Click "Generate token"
   - **Copy the token** (starts with `ghp_...`)

2. **Push with token:**
   ```bash
   cd /mnt/data/openclaw/workspace/tani-bot
   git remote add origin https://YOUR_USERNAME:YOUR_TOKEN@github.com/wizzleweasel/tani-bot.git
   git branch -M main
   git push -u origin main
   ```
   
   Replace:
   - `YOUR_USERNAME` = wizzleweasel
   - `YOUR_TOKEN` = the token you copied

### Option C: GitHub Desktop (GUI)

1. Download: https://desktop.github.com/
2. Clone `wizzleweasel/tani-bot`
3. Copy all files from `/mnt/data/openclaw/workspace/tani-bot/` into the cloned folder
4. Commit and push via GUI

---

## Verify Push

After pushing, check: https://github.com/wizzleweasel/tani-bot

You should see:
- ✅ All files (15+ files)
- ✅ Commit history (10 commits)
- ✅ Latest commit: "feat: Add deployment documentation and configs"

---

## Need Help?

Tell me which option you chose and I'll guide you through!
