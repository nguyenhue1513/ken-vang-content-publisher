# Kén Vàng — Content Publisher Skill

Claude Code skill tự động viết bài đăng Facebook/Instagram cho thương hiệu khăn đũi tơ tằm **Kén Vàng**, tạo Google Doc và cập nhật link vào Google Sheet kế hoạch nội dung.

## Cách dùng

Trong Claude Code, gõ:

```
Viết 2 bài cho Kén Vàng
```

Claude sẽ tự động:
1. Đọc Google Sheet để lấy N bài chưa có doc, sắp xếp theo mức ưu tiên (★★★ → ★★ → ★)
2. Viết nội dung hoàn chỉnh theo đúng format từng loại bài (Ảnh đơn / Carousel / Reels)
3. Tạo Google Doc cho từng bài trong Google Drive
4. Ghi link Doc vào cột I của sheet
5. Báo cáo bảng tổng kết kèm gợi ý hình ảnh

## Cấu trúc thư mục

```
content-publisher/
├── SKILL.md              ← Định nghĩa skill cho Claude Code
├── get_pending.py        ← Đọc sheet, trả danh sách bài chưa có doc
├── publish.py            ← Tạo Doc + ghi link vào cột I
├── create_doc.py         ← Tạo Google Doc qua Drive API
├── update_sheet.py       ← Cập nhật link vào cột I theo STT
├── get_credentials.py    ← Load OAuth token
├── setup_auth.py         ← Chạy một lần để xác thực Google account
├── config.py             ← SHEET_ID, FOLDER_ID, SHEET_NAME
├── requirements.txt      ← Python dependencies
└── credentials/          ← Không commit (xem .gitignore)
    ├── oauth_client.json
    └── token.json
```

## Setup

### 1. Cài dependencies

```bash
pip install -r requirements.txt
```

### 2. Tạo OAuth credentials

1. Vào [Google Cloud Console](https://console.cloud.google.com/) → tạo project
2. Bật APIs: **Google Docs API**, **Google Drive API**, **Google Sheets API**
3. Tạo OAuth 2.0 Client ID (loại Desktop App)
4. Download file JSON → đổi tên thành `oauth_client.json` → đặt vào thư mục `credentials/`

### 3. Xác thực lần đầu

```bash
python setup_auth.py
```

Trình duyệt sẽ mở → đăng nhập Google → token được lưu tự động vào `credentials/token.json`.

### 4. Cấu hình sheet

Trong `config.py`, cập nhật:

```python
SHEET_ID = "your-google-sheet-id"
FOLDER_ID = "your-google-drive-folder-id"
SHEET_NAME = "Plancontent"
```

## Yêu cầu Google Sheet

Sheet cần có các cột theo thứ tự:

| A | B | C | D | E | F | ... | H | I |
|---|---|---|---|---|---|---|---|---|
| STT | Tên bài | Nhóm | Loại bài | Tóm tắt | Gợi ý hình | ... | Ưu tiên | Link Doc |

Cột H chứa mức ưu tiên: `★★★` / `★★` / `★`  
Cột I sẽ được script tự động điền link Google Doc.

## Thông tin thương hiệu

**Kén Vàng** — Khăn đũi tơ tằm thủ công Việt Nam
- 100% tơ tằm tự nhiên, không nhuộm, không hóa chất
- Kéo tay hoàn toàn (70–100g/người/ngày)
- Nốt sần trên vải = dấu vân tay thợ, không phải lỗi

## Lưu ý bảo mật

- Thư mục `credentials/` đã được thêm vào `.gitignore` — không commit token và client secret
- Không hardcode credentials vào source code
