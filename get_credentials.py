"""
Load user credentials từ token.json (tạo bởi setup_auth.py).
"""
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from config import CREDENTIALS_PATH

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]

TOKEN_PATH = os.path.join(os.path.dirname(CREDENTIALS_PATH), "token.json")


def get_user_credentials() -> Credentials:
    if not os.path.exists(TOKEN_PATH):
        raise FileNotFoundError(
            "Chưa có token.json. Chạy: python setup_auth.py"
        )
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return creds
