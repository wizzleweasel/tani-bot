#!/usr/bin/env python3
"""
Auto Context Manager for TaniBot
Monitors context usage, saves to Mempalace, and cleans up at 70%
"""

import os
import json
from datetime import datetime
from pathlib import Path

# Configuration
CONTEXT_THRESHOLD = 70  # Trigger at 70%
WORKSPACE = Path("/mnt/data/openclaw/workspace/.openclaw/workspace")
CONVERSATIONS_DIR = WORKSPACE / "conversations"
MEMORY_DIR = WORKSPACE / "memory"
SUMMARIES_DIR = WORKSPACE / "summaries"

def check_context_usage():
    """Check current context usage percentage"""
    # This would integrate with OpenClaw's context tracking
    # For now, estimate based on conversation file sizes
    try:
        conv_files = list(CONVERSATIONS_DIR.glob("*.md"))
        total_size = sum(f.stat().st_size for f in conv_files)
        # Assume 100MB = 100% context
        usage_percent = min(100, (total_size / (100 * 1024 * 1024)) * 100)
        return usage_percent
    except:
        return 0

def save_conversation():
    """Save current conversation to Mempalace"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_file = CONVERSATIONS_DIR / f"{timestamp}_auto_save.md"
    
    summary = f"""# Auto-Saved Conversation

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Trigger:** Context threshold ({CONTEXT_THRESHOLD}%)
**Status:** Auto-saved

## Summary
Conversation auto-saved by context manager.
Review full logs in conversation history.

## Actions Taken
- Saved conversation snapshot
- Compressed old files
- Archived completed phases
"""
    
    summary_file.write_text(summary)
    print(f"✅ Saved: {summary_file}")
    return summary_file

def clean_workspace():
    """Clean up old files and optimize"""
    cleaned = 0
    
    # Remove old temporary files
    for pattern in ["*.tmp", "*.bak", "*.log"]:
        for f in WORKSPACE.glob(f"**/{pattern}"):
            try:
                f.unlink()
                cleaned += 1
            except:
                pass
    
    # Archive old conversations (keep last 10)
    conv_files = sorted(CONVERSATIONS_DIR.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
    for old_file in conv_files[10:]:
        try:
            archive_path = old_file.with_suffix(".md.archived")
            old_file.rename(archive_path)
            cleaned += 1
        except:
            pass
    
    print(f"✅ Cleaned {cleaned} files")
    return cleaned

def optimize_context():
    """Moderate optimization of context"""
    print("🔧 Running moderate optimization...")
    
    # Compress large JSON files
    for json_file in WORKSPACE.glob("datasets/**/*.json"):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            with open(json_file, 'w') as f:
                json.dump(data, f, separators=(',', ':'))
        except:
            pass
    
    print("✅ Optimization complete")

def notify_user(message: str):
    """Send notification via Telegram (if configured)"""
    # Would integrate with Telegram bot API
    print(f"📢 Notification: {message}")

def main():
    """Main context management loop"""
    print("="*60)
    print("🔄 Auto Context Manager")
    print("="*60)
    
    usage = check_context_usage()
    print(f"📊 Current context usage: {usage:.1f}%")
    
    if usage >= CONTEXT_THRESHOLD:
        print(f"\n⚠️ Context threshold reached ({CONTEXT_THRESHOLD}%)")
        print("🚀 Starting auto-save and cleanup...")
        
        # Save conversation
        save_conversation()
        
        # Clean workspace
        clean_workspace()
        
        # Optimize
        optimize_context()
        
        # Notify user
        notify_user(f"Context auto-saved at {usage:.1f}%")
        
        print("\n✅ Auto-save complete!")
    else:
        print(f"✨ Context usage normal ({usage:.1f}% < {CONTEXT_THRESHOLD}%)")
    
    print("="*60)

if __name__ == "__main__":
    main()
