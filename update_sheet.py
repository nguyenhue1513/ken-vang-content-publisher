"""
Cập nhật link Google Doc vào cột I của dòng tương ứng trong sheet Plancontent.
Tìm dòng theo STT (cột A).
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")
from googleapiclient.discovery import build
from get_credentials import get_user_credentials
from config import SHEET_ID, SHEET_NAME


def update_doc_link(stt: str, link: str) -> None:
    creds = get_user_credentials()
    sheets = build("sheets", "v4", credentials=creds)

    result = sheets.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range=f"{SHEET_NAME}!A:A"
    ).execute()

    rows = result.get("values", [])
    row_index = None
    for i, row in enumerate(rows):
        if row and str(row[0]).strip() == str(stt).strip():
            row_index = i + 1
            break

    if row_index is None:
        print(f"Không tìm thấy STT {stt} trong sheet.")
        return

    sheets.spreadsheets().values().update(
        spreadsheetId=SHEET_ID,
        range=f"{SHEET_NAME}!I{row_index}",
        valueInputOption="RAW",
        body={"values": [[link]]},
    ).execute()

    print(f"Đã ghi link vào dòng STT {stt}, cột I.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python update_sheet.py <stt> <link>")
        sys.exit(1)

    stt = sys.argv[1]
    link = sys.argv[2]
    update_doc_link(stt, link)
