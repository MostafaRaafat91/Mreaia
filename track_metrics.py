#!/usr/bin/env python3
"""
Mreaia Live Telemetry & Download Tracker
========================================
Tracks real-world downloads, clones, and community traction
across Hugging Face Hub and GitHub for Mostafa Raafat.
"""

import sys
import json
import urllib.request
from datetime import datetime

HF_REPO = "mostafaraafat91/Mreaia"
GITHUB_REPO = "MostafaRaafat91/Mreaia"


def fetch_huggingface_metrics():
    url = f"https://huggingface.co/api/models/{HF_REPO}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mreaia-Tracker/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {
                "downloads": data.get("downloads", 0),
                "likes": data.get("likes", 0),
                "last_modified": data.get("lastModified", "N/A"),
                "pipeline_tag": data.get("pipeline_tag", "N/A"),
                "tags": len(data.get("tags", [])),
            }
    except Exception as e:
        return {"error": str(e)}


def fetch_github_metrics():
    url = f"https://api.github.com/repos/{GITHUB_REPO}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mreaia-Tracker/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "watchers": data.get("watchers_count", 0),
                "open_issues": data.get("open_issues_count", 0),
                "default_branch": data.get("default_branch", "main"),
            }
    except Exception as e:
        return {"error": str(e)}


def main():
    print("=" * 65)
    print("       🪞 MREAIA TRACTION & DOWNLOAD TELEMETRY TRACKER")
    print(f"       Checked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

    print("\n[1] Hugging Face Model Hub (https://huggingface.co/" + HF_REPO + ")")
    hf = fetch_huggingface_metrics()
    if "error" in hf:
        print(f"    ⚠️ Error contacting Hugging Face: {hf['error']}")
    else:
        print(f"    📥 Total Downloads : {hf.get('downloads', 0):,}")
        print(f"    ❤️ Likes / Upvotes  : {hf.get('likes', 0):,}")
        print(f"    🏷️ Pipeline Tag     : {hf.get('pipeline_tag')}")
        print(f"    🕒 Last Synchronized : {hf.get('last_modified')}")

    print("\n[2] GitHub Repository (https://github.com/" + GITHUB_REPO + ")")
    gh = fetch_github_metrics()
    if "error" in gh:
        print(f"    ⚠️ Error contacting GitHub: {gh['error']}")
    else:
        print(f"    ⭐ Stars           : {gh.get('stars', 0):,}")
        print(f"    🍴 Forks           : {gh.get('forks', 0):,}")
        print(f"    👀 Watchers        : {gh.get('watchers', 0):,}")

    print("\n" + "=" * 65)
    print("To view full traffic graphs & visitors:")
    print("👉 GitHub Traffic : https://github.com/MostafaRaafat91/Mreaia/graphs/traffic")
    print("👉 Hugging Face   : https://huggingface.co/mostafaraafat91/Mreaia")
    print("=" * 65)


if __name__ == "__main__":
    main()
