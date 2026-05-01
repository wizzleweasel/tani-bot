# MEMORY.md - Long-Term Memory

*Last updated: 2026-05-01 04:48 UTC*

---

## 🚨 SECURITY INCIDENT - Bot Compromised & RECOVERED

**Date:** 2026-04-30 21:16 UTC
**Status:** ✅ RESOLVED - New bot token active

### What Happened

1. **Discovery:** Received message from @tani_pintar_bot in Russian
2. **Investigation:** Bot was repurposed as "Sherlock" doxxing service
3. **Finding:** Active webhook set by unauthorized party
4. **Action:** Token revoked immediately
5. **Recovery:** New bot token generated 2026-05-01 04:48 UTC

### Old Bot Details (COMPROMISED)

| Field | Value |
|-------|-------|
| Username | @tani_pintar_bot |
| Bot ID | 8693067374 |
| Old Token | `8693067374:AAEGnQrRfIXMvWf7wwhn8ELo_IiaOcBNKS0` |
| Status | ❌ REVOKED |

### New Bot Details (SECURE)

| Field | Value |
|-------|-------|
| Username | @tani_pintar_bot |
| Bot ID | 8693067374 (same) |
| New Token | `8693067374:AAFKH9RdXDHmT6yhYA4LWzBRhdDdOfWwQT8` |
| Status | ✅ ACTIVE |
| Chat ID | 8689301832 |
| Auto-notify | ✅ ENABLED |

### Attacker Activity

- **Service:** "Sherlock" search bot (doxxing)
- **Features:** Phone lookup, VK search, Telegram username search
- **Language:** Russian
- **Webhook:** Active (URL unknown) - NOW REMOVED

### Lessons Learned

1. **Never expose bot tokens** - Even in "private" files
2. **Use GitHub Secrets** - For all deployment tokens
3. **Monitor bot activity** - Check for unexpected messages
4. **Revoke immediately** - If compromise is suspected
5. **Rotate tokens regularly** - Don't use same token forever

---

## 📍 Kecamatan Coordinates Project - DEPLOYED! 🎉

**Milestone 2026-04-29:** ALL 7,215 kecamatan across 34 provinces - 100% complete & DEPLOYED!

**Timeline:**
- 16:06 UTC - Session started
- 16:27 UTC - Sumatera 100% complete (1,935)
- 16:30 UTC - Java 100% complete (2,143)
- 16:38 UTC - ALL INDONESIA COMPLETE (7,215)
- 17:54 UTC - DEPLOYED to HF Space + GitHub Actions auto-deploy
- 19:49 UTC - tani-bot-cuaca space updated with 7,215 kecamatan
- 21:21 UTC - Bot token COMPROMISED → REVOKED
- 2026-05-01 04:48 UTC - NEW BOT TOKEN ACTIVE

**Data Quality:**
- Real coordinates (`actual: true`): 31 entries (0.4%)
- Approximated (`actual: false`): 7,184 entries (99.6%)

**Deployment:**
- ✅ HF Space: https://huggingface.co/spaces/baguswicak/tani-bot
- ✅ GitHub CDN: raw.githubusercontent.com/wizzleweasel/tani-bot/main/datasets/kecamatan_coords.json
- ✅ Auto-deploy: GitHub Actions on push to main

**Key Learning:** Initial automation had 284 errors (114 invalid IDs + 170 wrong assignments). Root cause: scripts didn't validate against official CSV. Fixed by using CSV as single source of truth for IDs. Honesty about data quality matters more than appearing fast.

**Security:** All hardcoded tokens removed from git history. Secrets stored in GitHub Secrets. Auto-deploy via GitHub Actions.

---

## 🗺️ Kabupaten Coordinates

**Complete:** 514/514 kabupaten/kota (100%) - Finished 2026-04-29 11:30 UTC

**File:** `datasets/kecamatan_with_coords.json`

---

## 🚀 Tani-Bot Project

- V3.0 Unified App deployed to Hugging Face Spaces
- Weather Page v2.0 with Bahasa Indonesia UI
- RAG search optimization in progress (tsvector full-text search)
- Groq API rate limit handling needed (429 errors)
- ✅ Bot token rotated 2026-05-01 - New active token

---

## 📁 Key Files

| Path | Purpose |
|------|---------|
| `datasets/kecamatan_raw.csv` | Official 7,215 kecamatan list (source of truth) |
| `datasets/kecamatan_coords.json` | Active coordinate collection |
| `datasets/kecamatan_with_coords.json` | 514 kabupaten coordinates |
| `scripts/` | Automation scripts |
| `hf_spaces/` | Hugging Face Spaces deployment |
| `TOOLS.md` | Bot credentials (SECURE - gitignored) |

---

## ⚠️ Important Patterns

**For batch processing:**
1. Load CSV first (authoritative)
2. Check if ID exists before adding
3. Validate after each batch
4. Use ID-based matching, not name-based (names can collide across provinces)

**For data quality:**
- `actual: true` = high precision (4+ decimals, web-search verified)
- `actual: false` = estimated (kabupaten centroid + offset)

**For security:**
- NEVER commit tokens to Git
- Use GitHub Secrets for deployment
- Store sensitive data in gitignored files only
- Revoke immediately if compromised

---

## 🤖 Auto-Notify Configuration

**Bot:** @tani_pintar_bot
**Chat ID:** 8689301832
**Token:** `8693067374:AAFKH9RdXDHmT6yhYA4LWzBRhdDdOfWwQT8`
**Status:** ✅ ACTIVE
**Script:** `scripts/notify-bot.sh "Message"`

**What to notify:**
- ✅ Task completions (with stats)
- 🐛 Issues found & fixed
- 📊 Data updates/deployments
- 🚀 New features deployed

---
