#!/usr/bin/env python3
"""
restore.py — STANDALONE restore script (no dependencies).

This script does NOT depend on shared.py, project.json, or any other file.
It can run by itself after a rollback, as long as you have:
1. This file (restore.py)
2. A backup ZIP file (local or downloaded from GitHub)

Usage:
  python3 restore.py list                          List local backups
  python3 restore.py list-github                   List GitHub backups (public, no PAT needed)
  python3 restore.py download <timestamp>          Download backup from GitHub
  python3 restore.py restore <zip_path>            Restore from local ZIP
  python3 restore.py restore-timestamp <timestamp> Download + restore in one step

GitHub repo: hungnguyenhoang0103/harry_potter-fanfic-z.ai-images-9ad58zx
Branch: staging
Backup folder: backups/

This file should be saved to: /home/z/my-project/restore.py (ROOT level, not in scripts/)
"""
import sys
import os
import zipfile
import json
import requests

PROJECT_ROOT = "/home/z/my-project"
BACKUP_DIR = f"{PROJECT_ROOT}/backups"
REPO = "hungnguyenhoang0103/harry_potter-fanfic-z.ai-images-9ad58zx"
BRANCH = "staging"
GH_BACKUP_FOLDER = "backups"
GH_RAW_BASE = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{GH_BACKUP_FOLDER}"
GH_API_BASE = f"https://api.github.com/repos/{REPO}/contents/{GH_BACKUP_FOLDER}?ref={BRANCH}"


def list_local():
    """List local backups."""
    if not os.path.exists(BACKUP_DIR):
        print("No local backups directory.")
        return
    backups = [f for f in sorted(os.listdir(BACKUP_DIR)) if f.endswith(".zip")]
    if not backups:
        print("No local backups found.")
        return
    print(f"Local backups ({len(backups)}):")
    for f in backups:
        size = os.path.getsize(os.path.join(BACKUP_DIR, f))
        ts = f.split("backup_")[-1].replace(".zip", "") if "backup_" in f else "?"
        print(f"  {ts} | {size:,} bytes | {f}")


def list_github():
    """List GitHub backups (public repo, no PAT needed)."""
    try:
        r = requests.get(GH_API_BASE, timeout=30)
        if r.status_code != 200:
            print(f"GitHub API error: HTTP {r.status_code}")
            return
        items = r.json()
        if isinstance(items, dict) and "message" in items:
            print(f"GitHub API: {items['message']}")
            return
        backups = [x for x in items if x.get("type") == "file" and x["name"].endswith(".zip")]
        if not backups:
            print("No GitHub backups found.")
            return
        print(f"GitHub backups ({len(backups)}):")
        for b in backups:
            ts = b["name"].split("backup_")[-1].replace(".zip", "") if "backup_" in b["name"] else "?"
            print(f"  {ts} | {b.get('size', 0):,} bytes | {b['name']}")
            print(f"    URL: {GH_RAW_BASE}/{b['name']}")
    except Exception as e:
        print(f"Error: {e}")


def download_backup(timestamp):
    """Download backup from GitHub by timestamp."""
    # First list to find matching file
    try:
        r = requests.get(GH_API_BASE, timeout=30)
        if r.status_code != 200:
            print(f"GitHub API error: HTTP {r.status_code}")
            return None
        items = r.json()
        if isinstance(items, dict) and "message" in items:
            print(f"GitHub API: {items['message']}")
            return None
    except Exception as e:
        print(f"Error listing GitHub: {e}")
        return None

    # Find matching backup
    match = None
    for item in items:
        if item.get("type") == "file" and item["name"].endswith(".zip") and timestamp in item["name"]:
            match = item
            break

    if not match:
        print(f"Backup with timestamp '{timestamp}' not found on GitHub.")
        return None

    # Download
    raw_url = f"{GH_RAW_BASE}/{match['name']}"
    print(f"Downloading: {raw_url}")
    try:
        r = requests.get(raw_url, timeout=120)
        if r.status_code != 200:
            print(f"Download failed: HTTP {r.status_code}")
            return None
    except Exception as e:
        print(f"Download error: {e}")
        return None

    # Save locally
    os.makedirs(BACKUP_DIR, exist_ok=True)
    local_path = os.path.join(BACKUP_DIR, match["name"])
    with open(local_path, "wb") as f:
        f.write(r.content)
    print(f"  ✓ Downloaded: {len(r.content):,} bytes → {local_path}")
    return local_path


def restore_backup(zip_path):
    """Restore from local ZIP file."""
    if not os.path.exists(zip_path):
        print(f"File not found: {zip_path}")
        return False

    print(f"⚠ WARNING: This will OVERWRITE existing files in {PROJECT_ROOT}")
    print(f"  Source: {zip_path}")
    confirm = input("Type 'yes' to continue: ")
    if confirm != "yes":
        print("Cancelled.")
        return False

    print(f"Extracting...")
    file_count = 0
    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.namelist():
            target_path = os.path.join(PROJECT_ROOT, member)
            # Skip if parent would be outside PROJECT_ROOT
            if not target_path.startswith(PROJECT_ROOT):
                continue
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with zf.open(member) as src, open(target_path, "wb") as dst:
                dst.write(src.read())
            file_count += 1

    print(f"  ✓ Restored {file_count} files to {PROJECT_ROOT}")
    print(f"\nNext steps:")
    print(f"  1. Verify HTML files in download/")
    print(f"  2. Verify agents in scripts/agents/")
    print(f"  3. Create new PAT if needed")
    print(f"  4. Run: python3 scripts/agents/backup_agent.py create  (new backup)")
    return True


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "list":
        list_local()
    elif cmd == "list-github":
        list_github()
    elif cmd == "download":
        if len(sys.argv) < 3:
            print("Usage: python3 restore.py download <timestamp>")
            return
        download_backup(sys.argv[2])
    elif cmd == "restore":
        if len(sys.argv) < 3:
            print("Usage: python3 restore.py restore <zip_path>")
            return
        restore_backup(sys.argv[2])
    elif cmd == "restore-timestamp":
        if len(sys.argv) < 3:
            print("Usage: python3 restore.py restore-timestamp <timestamp>")
            return
        zip_path = download_backup(sys.argv[2])
        if zip_path:
            restore_backup(zip_path)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
