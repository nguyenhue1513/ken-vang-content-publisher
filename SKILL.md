# Skill: Content Publisher — Kén Vàng

Đọc kế hoạch nội dung từ Google Sheet, viết bài đăng Facebook/Instagram cho thương hiệu khăn đũi tơ tằm **Kén Vàng**, tạo Google Doc và ghi link vào cột I của sheet.

---

## Khi nào dùng skill này

Khi người dùng nói:
- "Viết 1 bài cho Kén Vàng"
- "Viết 3 bài cho Kén Vàng"
- "Viết N bài cho Kén Vàng"

---

## Bước 1 — Lấy danh sách bài cần viết

Chạy lệnh sau để lấy N bài tiếp theo chưa có doc, sắp xếp theo ưu tiên:

```bash
cd "D:\Hoc Claude\B3\skills\content-publisher"
python get_pending.py <N>
```

Script trả về danh sách JSON gồm các trường:
- `stt`: số thứ tự trong sheet
- `title`: tên bài / chủ đề
- `group`: nhóm nội dung
- `type`: loại bài (Ảnh đơn / Carousel / Reels)
- `summary`: nội dung tóm tắt từ cột E
- `image_hint`: gợi ý hình ảnh từ cột F
- `priority`: mức ưu tiên (★★★ / ★★ / ★)

**Thứ tự ưu tiên**: ★★★ trước → ★★ → ★; cùng mức thì lấy STT nhỏ hơn trước.

---

## Bước 2 — Viết nội dung từng bài

Với mỗi bài trong danh sách, viết nội dung hoàn chỉnh dựa trên `summary` và `type`.

### Thông tin thương hiệu

- **Tên**: Kén Vàng
- **Sản phẩm**: Khăn đũi tơ tằm thủ công — 100% tơ tằm tự nhiên, không nhuộm, không hóa chất
- **Điểm khác biệt**: Kéo tay hoàn toàn (70–100g/người/ngày), không máy thay thế được; nốt sần trên vải là dấu vân tay thợ, không phải lỗi

### Điều bắt buộc phải nhớ

- **Đũi ≠ Lụa mịn**: Sản phẩm Kén Vàng là ĐŨI tơ tằm thủ công, không phải lụa mịn ươm máy — không được nhầm lẫn hoặc dùng chung
- **Không dùng**: số liệu COF 0.23 vs 0.72 (nghiên cứu lụa mịn, không áp dụng cho đũi)
- **Không dùng**: "sợi liên tục 1.500m từ một kén" (đặc điểm lụa ươm máy)
- **Không bịa**: Mọi công dụng, số liệu phải có cơ sở thực tế

### Cấu trúc bài

```
[TIÊU ĐỀ — dưới 10 từ, có từ khóa, gây tò mò]

[Mở đầu: 1–2 câu gây chú ý — đặt câu hỏi hoặc nêu vấn đề gần gũi]

[Nội dung chính: 3–5 điểm hoặc đoạn văn, có ví dụ cụ thể]

[Kết luận: tóm tắt + call-to-action rõ ràng]

[Hashtag: 5–10 hashtag tiếng Việt phù hợp]
```

### Quy tắc giọng văn

- **Thân thiện, gần gũi** — như người bạn chia sẻ kiến thức, không phải quảng cáo cứng
- **Yếu tố dân gian** — khuyến khích dùng: tục ngữ, thành ngữ, hình ảnh làng nghề, câu chuyện người thợ nếu phù hợp
- **Độ dài**: 250–450 từ cho bài thường; carousel thì mỗi slide 1–2 câu ngắn
- **Không dùng**: teencode, viết tắt kiểu "k" "đc" "vs", ngôn ngữ sáo rỗng
- **Nền tảng**: phù hợp cả Facebook lẫn Instagram — tránh format chỉ đọc được trên một nền tảng

### Yêu cầu theo loại bài (field `type`)

| Loại bài | Yêu cầu |
|---|---|
| Ảnh đơn | 1 caption hoàn chỉnh, hook đầu mạnh |
| Carousel N slide | Viết từng slide: slide 1 = hook, slide 2–(N-1) = nội dung, slide cuối = CTA |
| Reels / Video | Script ngắn: lời dẫn + điểm chính + kết |

---

## Bước 3 — Tạo Google Doc và cập nhật sheet

Với mỗi bài đã viết xong, chạy:

```bash
cd "D:\Hoc Claude\B3\skills\content-publisher"
python publish.py "<stt>" "<tiêu đề>" "<toàn bộ nội dung>"
```

Script sẽ:
1. Tạo Google Doc trong folder **Content Publisher** trên Drive
2. Ghi link vào **cột I**, dòng STT tương ứng trong sheet Plancontent

Lặp lại Bước 2–3 cho đến hết danh sách.

---

## Bước 4 — Báo cáo kết quả

Sau khi viết xong tất cả N bài, tổng kết cho người dùng dưới dạng bảng:

| STT | Tên bài | Ưu tiên | Link Doc | Gợi ý hình ảnh |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

---

## Cấu trúc thư mục

```
content-publisher/
├── SKILL.md              ← file này
├── get_pending.py        ← đọc sheet, trả danh sách bài chưa có doc
├── publish.py            ← tạo Doc + ghi link vào cột I
├── create_doc.py         ← tạo Google Doc qua Drive API
├── update_sheet.py       ← cập nhật link vào cột I theo STT
├── get_credentials.py    ← load OAuth token
├── setup_auth.py         ← chạy một lần để xác thực
├── config.py             ← SHEET_ID, FOLDER_ID, SHEET_NAME
├── requirements.txt      ← dependencies
└── credentials/
    ├── oauth_client.json ← OAuth client (không commit)
    └── token.json        ← token người dùng (không commit)
```

---

## Ví dụ

**Người dùng**: "Viết 2 bài cho Kén Vàng"

**Claude sẽ**:
1. Chạy `python get_pending.py 2` → lấy 2 bài ưu tiên cao nhất chưa có doc
2. Viết bài STT 2 (★★★): Carousel 5 slide về đũi tơ tằm
3. Chạy `python publish.py "2" "..." "..."` → tạo Doc + ghi cột I
4. Viết bài STT 3 (★★★): Carousel 7 slide về hành trình từ kén đến khăn
5. Chạy `python publish.py "3" "..." "..."` → tạo Doc + ghi cột I
6. Báo cáo bảng tổng kết + gợi ý hình ảnh cho từng bài
