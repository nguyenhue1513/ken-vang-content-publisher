"""
Tạo Google Doc mới với tiêu đề và nội dung cho trước.
Trả về: tiêu đề, link doc, doc_id
"""

import sys
import json
sys.stdout.reconfigure(encoding="utf-8")
from googleapiclient.discovery import build
from get_credentials import get_user_credentials
from config import FOLDER_ID


def create_doc(title: str, content: str) -> dict:
    creds = get_user_credentials()
    docs = build("docs", "v1", credentials=creds)
    drive = build("drive", "v3", credentials=creds)

    file = drive.files().create(
        body={"name": title, "mimeType": "application/vnd.google-apps.document", "parents": [FOLDER_ID]}
    ).execute()
    doc_id = file["id"]

    requests = [
        {
            "insertText": {
                "location": {"index": 1},
                "text": content,
            }
        }
    ]
    docs.documents().batchUpdate(
        documentId=doc_id, body={"requests": requests}
    ).execute()

    link = f"https://docs.google.com/document/d/{doc_id}/edit"
    return {"title": title, "doc_id": doc_id, "link": link}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python create_doc.py <title> <content>")
        sys.exit(1)

    title = sys.argv[1]
    content = sys.argv[2]
    result = create_doc(title, content)
    print(json.dumps(result, ensure_ascii=False))
