# 🧪 Gensee Integration for TestClaw - May 4, 2026

**Date:** 2026-05-03 17:54 UTC  
**Status:** ✅ Complete & Deployed

---

## 📋 Summary

Successfully configured TestClaw (nested Hermes agent) to use Gensee API directly, bypassing OpenRouter authentication issues.

---

## 🎯 What Was Done

### 1. Installed MemPalace
- Cloned from `github.com/mempalace/mempalace`
- Installed via pip (v3.3.4)
- Initialized in workspace with entity detection

### 2. Restored Tani-Bot Backup
- Cloned from `wizzleweasel/tani-bot`
- Injected memory files into current workspace:
  - `MEMORY.md` - Long-term memory with bot security incident, kecamatan project
  - `memory/*.md` - Daily session logs (6 files)
  - Documentation files (12 files)
  - Datasets (kecamatan coordinates, RAG data)

### 3. Created Nested Agent (TestClaw)
- Cloned Hermes Agent v0.12.0 as `testclaw/`
- Installed with isolated Python 3.11 venv
- Configured as nested agent under OpenClaw workspace

### 4. Gensee API Integration
**Problem:** TestClaw defaulted to OpenRouter, causing HTTP 401 errors

**Solution:** Configured direct Gensee endpoint matching OpenClaw's setup

**Final Configuration:**
```yaml
Provider: gensee-397b
Model: Gensee/Qwen3.5-397B
Endpoint: http://forwarder.staging.svc.cluster.local:9105/forward/gensee-397b/v1
```

### 5. Telegram Bot Connection
- Bot Token: Configured (stored securely in .env)
- Allowed User: 8689301832 (Wicak)
- Gateway Status: Running (PID 786)

---

## 📁 Files Created/Modified

| File | Purpose |
|------|---------|
| `testclaw/` | Hermes Agent v0.12.0 installation |
| `mempalace-fork/` | MemPalace source (forked) |
| `tani-bot-backup/` | Tani-Bot backup repository |
| `.hermes/config.yaml` | TestClaw model/provider config |
| `.hermes/.env` | TestClaw environment secrets |
| `.hermes/auth.json` | TestClaw authentication |
| `memory/*.md` | Restored daily memory logs |
| `MEMORY.md` | Restored long-term memory |

---

## 🔑 API Configuration (SECURE)

**Gensee Endpoint:**
```
http://forwarder.staging.svc.cluster.local:9105/forward/gensee-397b/v1
```

**API Key:** Stored in `.hermes/.env` (gitignored)
- Variable: `GENSEE_397B_API_KEY`
- Source: Inherited from OpenClaw environment

**⚠️ Security Notes:**
- API keys stored ONLY in `.env` files (gitignored)
- Never commit credentials to `.md` files
- Use GitHub Secrets for deployment

---

## ✅ Verification

| Component | Status |
|-----------|--------|
| MemPalace | ✅ 2,497 drawers indexed |
| TestClaw Gateway | ✅ Running (PID 786) |
| Telegram Bot | ✅ Connected & Responding |
| Gensee API | ✅ Working (no 401 errors) |
| OpenRouter | ❌ Removed (not needed) |

---

## 🚀 TestClaw Capabilities

**Now Available:**
- Independent Telegram bot (`@macantutul_bot`)
- Parallel task execution
- Separate model/personality from OpenClaw
- Can be spawned as subagent

**Commands:**
```bash
# Check status
testclaw gateway status

# View config
testclaw config show

# Restart gateway
testclaw gateway run
```

---

## 📊 MemPalace Status

```
WING: workspace
  ROOM: datasets    2,214 drawers
  ROOM: skills        124 drawers
  ROOM: general        82 drawers
  ROOM: memory         77 drawers
─────────────────────────────
  TOTAL:          2,497 drawers
```

**Search Example:**
```bash
mempalace search "bot token"
```

---

## 📝 Lessons Learned

1. **Provider naming matters** - Must match exactly (`gensee-397b` not `gensee`)
2. **Clear old sessions** - Delete `~/.hermes/sessions/*.jsonl` when changing providers
3. **Auth.json is critical** - Hermes reads credentials from auth.json, not just .env
4. **Nested agents work** - Can run multiple Hermes instances in same workspace

---

## 🔗 Related Files

- `TOOLS.md` - Bot credentials (gitignored)
- `.hermes/config.yaml` - TestClaw configuration
- `mempalace.yaml` - MemPalace wing config
- `entities.json` - Detected entities (workspace, TaniBot)

---

## 🎯 Next Steps

1. Monitor TestClaw gateway stability
2. Consider Discord integration for multi-channel support
3. Build crop database for Page 3 enhancement
4. Set up GitHub Actions for auto-deploy

---

**Logged by:** OpenClaw Assistant  
**Session:** agent:main:main  
**Timestamp:** 2026-05-03 17:54 UTC
