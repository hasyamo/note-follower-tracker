#!/usr/bin/env python3
"""
noteのフォロワー数を取得してJSONファイルに追記するスクリプト
"""

import json
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path
import urllib.request
import urllib.error

# .env ファイルがあれば読み込み
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    pass  # dotenv がなくても動作する（GitHub Actions 環境など）

# 設定
NOTE_CREATOR_ID = os.environ.get("NOTE_CREATOR_ID", "your_creator_id")
DATA_FILE = Path(__file__).parent.parent / "data" / "followers.json"

# 日本時間
JST = timezone(timedelta(hours=9))


def fetch_follower_count(creator_id: str) -> int:
    """noteのAPIからフォロワー数を取得"""
    api_url = f"https://note.com/api/v2/creators/{creator_id}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    }
    
    request = urllib.request.Request(api_url, headers=headers)
    
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise Exception(f"API request failed: HTTP {e.code}")
    except urllib.error.URLError as e:
        raise Exception(f"API request failed: {e.reason}")
    
    # フォロワー数を探す（複数パターン対応）
    follower_count = None
    if "data" in data:
        if "followerCount" in data["data"]:
            follower_count = data["data"]["followerCount"]
        elif "user" in data["data"] and "followerCount" in data["data"]["user"]:
            follower_count = data["data"]["user"]["followerCount"]
    
    if follower_count is None:
        raise Exception(f"Could not find followerCount in API response")
    
    return int(follower_count)


def load_data() -> dict:
    """既存のデータを読み込む"""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"records": []}


def save_data(data: dict) -> None:
    """データを保存"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    print(f"Fetching follower count for: {NOTE_CREATOR_ID}")
    
    # フォロワー数を取得
    follower_count = fetch_follower_count(NOTE_CREATOR_ID)
    print(f"Current followers: {follower_count}")
    
    # 既存データを読み込み
    data = load_data()
    
    # 今日の日付（JST）
    now = datetime.now(JST)
    today = now.strftime("%Y-%m-%d")
    
    # 前日比を計算
    change = 0
    if data["records"]:
        last_record = data["records"][-1]
        change = follower_count - last_record["followers"]
    
    # 同日のデータがあれば更新、なければ追加
    existing_today = next(
        (r for r in data["records"] if r["date"] == today), None
    )
    
    if existing_today:
        print(f"Updating existing record for {today}")
        existing_today["followers"] = follower_count
        existing_today["change"] = change
        existing_today["updated_at"] = now.isoformat()
    else:
        new_record = {
            "date": today,
            "followers": follower_count,
            "change": change,
            "updated_at": now.isoformat(),
        }
        data["records"].append(new_record)
        print(f"Added new record: {new_record}")
    
    # メタデータを更新
    data["last_updated"] = now.isoformat()
    data["creator_id"] = NOTE_CREATOR_ID
    
    # 保存
    save_data(data)
    print(f"Data saved to {DATA_FILE}")
    
    # GitHub Actions の出力
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"followers={follower_count}\n")
            f.write(f"change={change}\n")


if __name__ == "__main__":
    main()
