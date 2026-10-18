"""queue/x-posts.json から今日(JST)の未投稿エントリを1件だけXに投稿する。
形式: [{"date": "2026-10-20", "text": "...", "posted": false}, ...]
"""
import json, os, sys, datetime
from requests_oauthlib import OAuth1Session

QUEUE = "queue/x-posts.json"
today = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).date().isoformat()

with open(QUEUE, encoding="utf-8") as f:
    queue = json.load(f)

entry = next((e for e in queue if e["date"] == today and not e.get("posted")), None)
if not entry:
    print(f"{today}: 投稿予定なし")
    sys.exit(0)

text = entry["text"].strip()
if not text or len(text) > 140:
    print(f"{today}: 本文が空か140字超のためスキップ ({len(text)}字)")
    sys.exit(1)

x = OAuth1Session(
    os.environ["X_API_KEY"], os.environ["X_API_SECRET"],
    os.environ["X_ACCESS_TOKEN"], os.environ["X_ACCESS_SECRET"],
)
r = x.post("https://api.x.com/2/tweets", json={"text": text})
if r.status_code >= 300:
    print(f"投稿失敗 {r.status_code}: {r.text}")
    sys.exit(1)

entry["posted"] = True
entry["tweet_id"] = r.json()["data"]["id"]
with open(QUEUE, "w", encoding="utf-8") as f:
    json.dump(queue, f, ensure_ascii=False, indent=2)
print(f"{today}: 投稿完了 {entry['tweet_id']}")
