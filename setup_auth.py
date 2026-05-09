"""
Chạy một lần để xác thực tài khoản Google của bạn.
Sẽ mở trình duyệt → đăng nhập → lưu token vào credentials/token.json
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from config import CREDENTIALS_PATH

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]

OAUTH_CLIENT_PATH = os.path.join(os.path.dirname(CREDENTIALS_PATH), "oauth_client.json")
TOKEN_PATH = os.path.join(os.path.dirname(CREDENTIALS_PATH), "token.json")

flow = InstalledAppFlow.from_client_secrets_file(OAUTH_CLIENT_PATH, SCOPES)
creds = flow.run_local_server(port=0)

with open(TOKEN_PATH, "w") as f:
    f.write(creds.to_json())

print(f"[OK] Token đã lưu tại: {TOKEN_PATH}")
print("Bây giờ bạn có thể chạy publish.py")
