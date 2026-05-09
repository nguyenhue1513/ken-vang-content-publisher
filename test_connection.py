import sys
sys.stdout.reconfigure(encoding="utf-8")

from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import CREDENTIALS_PATH, SHEET_ID

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]

print("=== Test kết nối Google APIs ===\n")

# Test 1: Load credentials
try:
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH, scopes=SCOPES
    )
    print(f"[OK] Credentials loaded: {creds.service_account_email}")
except Exception as e:
    print(f"[FAIL] Credentials: {e}")
    sys.exit(1)

# Test 2: Sheets API
try:
    sheets = build("sheets", "v4", credentials=creds)
    result = sheets.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    print(f"[OK] Sheets API: Sheet '{result['properties']['title']}' truy cập được")
except Exception as e:
    print(f"[FAIL] Sheets API: {e}")

# Test 3: Docs API
try:
    docs = build("docs", "v1", credentials=creds)
    doc = docs.documents().create(body={"title": "TEST - có thể xóa"}).execute()
    doc_id = doc["documentId"]
    link = f"https://docs.google.com/document/d/{doc_id}/edit"
    print(f"[OK] Docs API: Doc tạo được - {link}")
except Exception as e:
    print(f"[FAIL] Docs API: {e}")
