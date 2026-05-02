# 🎯 TaniBot Subagent Workflow

**Discord + GitHub Issues Integration**

---

## 📋 Overview

This workflow combines:
- **Discord** for real-time subagent communication
- **GitHub Issues** for task tracking & documentation
- **OpenClaw** for subagent orchestration

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    YOU (Human)                          │
│  - Create GitHub Issues for tasks                       │
│  - Monitor Discord channels                             │
│  - Review subagent output                               │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  Discord Server                         │
│  #announcements  → Task assignments                     │
│  #crop-advisor   → Subagent 1 workspace                 │
│  #pest-disease   → Subagent 2 workspace                 │
│  #weather        → Subagent 3 workspace                 │
│  #status-updates → Automated progress logs              │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│               OpenClaw Subagents                        │
│  - Receive tasks via Discord                            │
│  - Report progress to Discord                           │
│  - Create/update GitHub Issues                          │
│  - Commit files to GitHub                               │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  GitHub Repository                      │
│  - Issues = Task tracking                               │
│  - PRs = Quality control                                │
│  - Files = Deliverables                                 │
│  - Actions = Auto-deploy                                │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Workflow Steps

### Step 1: Create Task (GitHub Issue)

**You create an issue:**
1. Go to: https://github.com/wizzleweasel/tani-bot/issues
2. Click "New Issue"
3. Select "🌾 Subagent Task" template
4. Fill in:
   - Task description
   - Expected output
   - Priority
   - Resources/links
5. Submit

**Example:**
```
Title: [TASK] Build crop database for 10 Indonesian crops

Description:
Create datasets/crop_database.json with:
- Rice, corn, cassava, soybeans, peanuts
- Chili, coffee, coconut, banana, mango
- Include: growing seasons, fertilizer, pests

Priority: 🔴 Urgent

Resources:
- datasets/youtube_keyword_research_agriculture_indonesia.md
- MEMORY.md (RAG dataset info)
```

---

### Step 2: Spawn Subagent (OpenClaw)

**In your OpenClaw session:**

```python
sessions_spawn(
    task="Build datasets/crop_database.json with 10 major Indonesian crops. See GitHub issue #101 for details.",
    runtime="subagent",
    mode="session",
    label="crop-db-builder",
    cleanup="keep"
)
```

---

### Step 3: Announce in Discord

**Post to Discord:**

```python
message(
    action="send",
    channel="discord",
    target="#announcements",
    message="🚀 New Task Started!\n\n**Task:** Build crop database\n**Subagent:** crop-db-builder\n**Issue:** #101\n**ETA:** 1 hour"
)
```

---

### Step 4: Subagent Reports Progress

**Subagent posts updates to its channel:**

```python
# In subagent code:
message(
    action="send",
    channel="discord",
    target="#crop-advisor",
    message="📊 Progress Update\n\n✅ Rice - Complete\n✅ Cassava - Complete\n🔄 Corn - In progress\n⏳ 7 crops remaining\n\n**ETA:** 45 minutes"
)
```

---

### Step 5: Monitor & Intervene

**You monitor from Discord:**
- Watch `#crop-advisor` for updates
- Reply directly if needed
- Check GitHub issue for detailed logs

**If subagent is stuck:**

```python
# Option A: Discord reply
# Just reply to their message in #crop-advisor

# Option B: OpenClaw steer
subagents(
    action="steer",
    target="crop-db-builder",
    message="Use youtube_keyword_research.md file instead of web search"
)
```

---

### Step 6: Task Complete

**Subagent marks complete:**

```python
# 1. Update GitHub Issue
exec(command="gh issue close 101")

# 2. Post to Discord
message(
    action="send",
    channel="discord",
    target="#status-updates",
    message="✅ Task Complete!\n\n**Task:** Crop database built\n**Files:** datasets/crop_database.json (10 crops)\n**Issue:** #101 closed\n**Time:** 58 minutes"
)

# 3. Commit to GitHub
exec(command="git add datasets/crop_database.json && git commit -m 'feat: Add crop database (10 crops)' && git push")
```

---

## 📊 Discord Channel Structure

| Channel | Purpose | Who Posts |
|---------|---------|-----------|
| **#announcements** | Task assignments, major milestones | You + Bot |
| **#crop-advisor** | Crop database subagent workspace | Subagent 1 |
| **#pest-disease** | Pest research subagent workspace | Subagent 2 |
| **#weather** | Weather integration subagent | Subagent 3 |
| **#status-updates** | Automated progress summaries | Bot |
| **#general** | Casual chat, questions | Everyone |

---

## 🏷️ GitHub Labels

| Label | Color | Purpose |
|-------|-------|---------|
| `subagent` | 🔵 Blue | Task assigned to subagent |
| `triage` | 🟡 Yellow | Needs review |
| `in-progress` | 🟢 Green | Currently being worked on |
| `blocked` | 🔴 Red | Waiting on something |
| `progress` | 🟣 Purple | Progress report |
| `documentation` | 📖 Gray | Documentation task |

---

## 📝 File Structure

```
.github/
├── ISSUE_TEMPLATE/
│   ├── subagent-task.md      ← Task creation template
│   └── progress-report.md    ← Progress logging template
└── workflows/
    └── discord-notify.yml    ← Discord notifications on issue events

datasets/
├── crop_database.json        ← Subagent output
└── ...

scripts/
└── discord-notify.sh         ← Helper for Discord messages
```

---

## 🔧 Setup Checklist

### Discord Setup
- [ ] Create Discord server "TaniBot HQ"
- [ ] Create 6 channels (see structure above)
- [ ] Create Discord bot application
- [ ] Get bot token
- [ ] Invite bot to server
- [ ] Enable Message Content Intent
- [ ] Get channel IDs

### OpenClaw Config
- [ ] Add Discord channel config
- [ ] Add bot token (securely)
- [ ] Test message sending
- [ ] Test channel routing

### GitHub Setup
- [ ] Enable Issues
- [ ] Add issue templates (done ✅)
- [ ] Create labels (see above)
- [ ] Set up Discord webhook (optional)

### Documentation
- [ ] This workflow doc (done ✅)
- [ ] README update
- [ ] Team onboarding guide

---

## 🎯 Example: Crop Database Task

### Full Workflow in Action:

**1. You create GitHub Issue #101:**
```
Title: [TASK] Build crop database for 10 Indonesian crops
Labels: subagent, triage, 🔴 Urgent
```

**2. You spawn subagent:**
```python
sessions_spawn(
    task="See GitHub issue #101",
    label="crop-db-builder"
)
```

**3. Bot posts to Discord:**
```
#announcements: 🚀 New task: Crop database (#101)
#crop-advisor: Starting work on issue #101...
```

**4. Subagent works, posts updates:**
```
#crop-advisor: 📊 3/10 crops complete (rice, cassava, corn)
#crop-advisor: 📊 7/10 crops complete (added soybeans, peanuts, chili)
```

**5. You check in via Discord:**
```
@crop-db-builder How's the fertilizer data looking?
```

**6. Subagent responds:**
```
Found NPK ratios for 5 crops. Missing data for coffee and coconut.
Searching Ministry of Agriculture docs...
```

**7. Task complete:**
```
#status-updates: ✅ Issue #101 closed
#status-updates: 📁 datasets/crop_database.json created (10 crops)
#status-updates: 🔄 GitHub push complete
```

---

## 💡 Tips

### For You (Human)
- Monitor Discord on desktop (easier to watch multiple channels)
- Use GitHub issue templates for consistency
- Review subagent output before merging
- Close issues when tasks are truly done

### For Subagents
- Post progress every 15-20 minutes
- Tag blockers early (don't wait)
- Link to GitHub issues in Discord messages
- Commit frequently, not just at end

### For Both
- Keep Discord channels organized (stay in your lane!)
- Use GitHub for permanent records
- Use Discord for real-time coordination
- Archive completed tasks (close issues)

---

**Last Updated:** 2026-05-02 17:55 UTC  
**Status:** Draft (awaiting Discord setup)
