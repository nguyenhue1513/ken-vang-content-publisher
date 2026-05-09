"""
Đọc sheet Plancontent, trả về danh sách bài chưa có link doc,
sắp xếp theo mức ưu tiên (★★★ trước) rồi theo STT từ trên xuống.
Usage: python get_pending.py [số lượng]
"""

import sys
import json
sys.stdout.reconfigure(encoding="utf-8")
from googleapiclient.discovery import build
from get_credentials import get_user_credentials
from config import SHEET_ID, SHEET_NAME

PRIORITY_ORDER = {"★★★": 0, "★★": 1, "★": 2}


def get_pending(limit: int = None) -> list:
    creds = get_user_credentials()
    sheets = build("sheets", "v4", credentials=creds)

    result = sheets.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range=f"{SHEET_NAME}!A:K"
    ).execute()

    rows = result.get("values", [])
    pending = []

    for row in rows:
        if not row or not row[0].strip().isdigit():
            continue

        stt = row[0].strip()
        title = row[1].strip() if len(row) > 1 else ""
        group = row[2].strip() if len(row) > 2 else ""
        post_type = row[3].strip() if len(row) > 3 else ""
        summary = row[4].strip() if len(row) > 4 else ""
        image_hint = row[5].strip() if len(row) > 5 else ""
        priority = row[7].strip() if len(row) > 7 else ""
        doc_link = row[8].strip() if len(row) > 8 else ""

        if doc_link:
            continue

        pending.append({
            "stt": stt,
            "title": title,
            "group": group,
            "type": post_type,
            "summary": summary,
            "image_hint": image_hint,
            "priority": priority,
            "priority_order": PRIORITY_ORDER.get(priority, 9),
        })

    pending.sort(key=lambda x: (x["priority_order"], int(x["stt"])))

    if limit:
        pending = pending[:limit]

    return pending


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    result = get_pending(limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))
