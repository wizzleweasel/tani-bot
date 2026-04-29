#!/usr/bin/env python3
"""
Auto-Push Coordinates After Each Batch
Monitors progress file and pushes to GitHub
"""

import subprocess
import time
import json
import os
from datetime import datetime

PROGRESS_FILE = "datasets/coords_progress.json"
OUTPUT_FILE = "datasets/kecamatan_with_coords.json"

def check_progress():
    """Check if progress file has been updated"""
    if not os.path.exists(PROGRESS_FILE):
        return None
    
    with open(PROGRESS_FILE, 'r') as f:
        return json.load(f)

def push_to_github():
    """Push changes to GitHub"""
    try:
        # Add all changes
        subprocess.run(['git', 'add', '-A'], check=True)
        
        # Commit with timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        subprocess.run([
            'git', 'commit', '-m', 
            f'Auto-update: Coordinates batch at {timestamp}'
        ], check=True)
        
        # Push
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Pushed to GitHub")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Push failed: {e}")
        return False

def main():
    print("👀 Monitoring progress file...")
    print("Press Ctrl+C to stop\n")
    
    last_count = 0
    
    try:
        while True:
            progress = check_progress()
            
            if progress:
                current_count = len(progress.get('processed', []))
                
                if current_count > last_count:
                    print(f"\n📊 Progress: {current_count} kabupaten processed")
                    print("🚀 Pushing to GitHub...")
                    push_to_github()
                    last_count = current_count
            else:
                print(f"⏳ Waiting for progress... ({datetime.now().strftime('%H:%M:%S')})")
            
            time.sleep(10)  # Check every 10 seconds
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped monitoring")

if __name__ == "__main__":
    main()
