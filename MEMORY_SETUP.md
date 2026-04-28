# 🧠 Mempalace Memory Setup - TaniBot Project

## Overview
Mempalace is now configured to save conversations and project context locally, reducing computational load and improving recall.

---

## ✅ What's Set Up

### 1. Mempalace Installation
- **Location:** `/mnt/data/openclaw/workspace/.openclaw/workspace/composio-venv/`
- **Config:** `mempalace.yaml` (in workspace root)
- **Palace:** `~/.mempalace/palace/` (vector database)
- **Files Mined:** 46+ files

### 2. Conversation Saving
- **Directory:** `/mnt/data/openclaw/workspace/.openclaw/workspace/conversations/`
- **Format:** JSON with timestamp, topic, tags, content
- **Auto-mined:** Yes (run `mempalace mine conversations/` after adding)

### 3. Search Commands
```bash
# Search for anything
./composio-venv/bin/mempalace search "your query"

# Search with wing filter
./composio-venv/bin/mempalace search "TaniBot" --wing workspace

# Search with room filter
./composio-venv/bin/mempalace search "Notion setup" --room general
```

---

## 📝 How to Save Conversations

### Manual Save (After Important Sessions)
```bash
cd /mnt/data/openclaw/workspace/.openclaw/workspace
python3 save_conversation.py "Topic Name" "Summary content" tag1 tag2
```

### Auto-Save Template
Create a script that runs at the end of each session to save key decisions and context.

---

## 🔍 Example Searches

```bash
# Find TaniBot architecture decisions
./composio-venv/bin/mempalace search "TaniBot architecture ML LLM"

# Find Notion setup details
./composio-venv/bin/mempalace search "Notion tracker database"

# Find Composio configuration
./composio-venv/bin/mempalace search "Composio API key connections"

# Find Phase 1 tasks
./composio-venv/bin/mempalace search "Phase 1 tasks weather pipeline"
```

---

## 📊 Memory Structure

```
.mempalace/
├── palace/              # Vector database (ChromaDB)
├── config.json          # Global config
└── known_entities.json  # Entity registry

workspace/
├── mempalace.yaml       # Project config
├── conversations/       # Saved session records
└── .mempalace/          # Local palace data
```

---

## 🎯 Best Practices

1. **Save after key decisions** - Don't save every message, just important context
2. **Use descriptive tags** - Makes search more effective
3. **Include timestamps** - Helps with temporal context
4. **Re-mine periodically** - Run `mempalace mine .` after adding files
5. **Search before asking** - Check memory first for existing context

---

## 🔄 Integration with Future Sessions

At the start of each session:
```bash
# Search for recent context
./composio-venv/bin/mempalace search "TaniBot current status"

# Review last session
./composio-venv/bin/mempalace search "last session decisions"
```

---

## 📁 Session Summary Location
All session summaries are saved in:
`/mnt/data/openclaw/workspace/.openclaw/workspace/conversations/`

Latest: `20260428_010400_tanibot_session_setup.json`

---

## 🚀 Next Steps
1. ✅ Mempalace initialized
2. ✅ Session saved
3. ⏳ Continue Phase 1 development
4. ⏳ Save key milestones as you build

---

**Setup Date:** 2026-04-28  
**Setup By:** AI Assistant + Wicak  
**Project:** TaniBot
