"""
Script chính: nhận STT + nội dung, tạo Doc, ghi link vào cột I của sheet.
Usage: python publish.py <stt> <title> <content>
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")
from create_doc import create_doc
from update_sheet import update_doc_link


def publish(stt: str, title: str, content: str) -> None:
    print(f"Đang tạo Google Doc: {title}")
    result = create_doc(title, content)

    print(f"Doc tạo xong: {result['link']}")
    print(f"Đang ghi link vào sheet, dòng STT {stt}...")
    update_doc_link(stt, result["link"])

    print("\n=== HOÀN THÀNH ===")
    print(f"Tiêu đề : {result['title']}")
    print(f"Link Doc : {result['link']}")
    print(f"Đã cập nhật cột I, dòng STT {stt}.")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python publish.py <stt> <title> <content>")
        sys.exit(1)

    stt = sys.argv[1]
    title = sys.argv[2]
    content = sys.argv[3]
    publish(stt, title, content)
