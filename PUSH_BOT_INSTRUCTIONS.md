# 📦 Push Assistant Bot to GitHub

## Quick Push (2 minutes)

### Option 1: GitHub Desktop (Easiest)

1. **Download:** https://desktop.github.com/
2. **Clone:** `wizzleweasel/usual-bot`
3. **Copy files** from: `/mnt/data/openclaw/workspace/assistant-bot/`
4. **Commit & Push** via GUI

---

### Option 2: Command Line with Token

1. **Create token:** https://github.com/settings/tokens/new
   - Check: `repo` ✅
   - Generate token (copy it - starts with `ghp_...`)

2. **Push:**
```bash
cd /mnt/data/openclaw/workspace/assistant-bot-github
git remote set-url origin https://wizzleweasel:YOUR_TOKEN@github.com/wizzleweasel/usual-bot.git
git branch -M main
git push -u origin main
```

Replace `YOUR_TOKEN` with your actual token.

---

### Option 3: Railway Direct from Files

If GitHub is troublesome:

1. **Go to:** https://railway.app
2. **Click:** "New Project"
3. **Select:** "Deploy from GitHub repo"
4. **Choose:** "Deploy from CLI" or upload files manually
5. **Add env vars** and deploy

---

## Files to Upload

All files are in: `/mnt/data/openclaw/workspace/assistant-bot/`

- `app.py` - Bot code
- `requirements.txt` - Dependencies
- `Dockerfile` - Container config
- `railway.json` - Railway config
- `RAILWAY_DEPLOY.md` - Deployment guide
- `README.md` - Documentation

---

**Once pushed, deploy to Railway!** 🚀
