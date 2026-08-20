#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Script kiểm tra tính toàn vẹn của trích dẫn (Citations & BibTeX):
1. Tìm tất cả các \cite{...} trong thư mục src/
2. Tìm tất cả các key trong src/bibliography.bib
3. Báo cáo:
   - Các trích dẫn trong văn bản bị thiếu trong .bib (Missing citations) -> Báo lỗi
   - Các mục trong .bib không được sử dụng (Unused entries) -> Cảnh báo
"""

import os
import re
import sys
from pathlib import Path

# Đảm bảo in UTF-8 mượt mà trên Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def get_bib_keys(bib_file_path):
    keys = set()
    if not os.path.exists(bib_file_path):
        print(f"[ERROR] Không tìm thấy file: {bib_file_path}")
        return keys
    
    with open(bib_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Bỏ qua dòng comment (%)
    clean_lines = [re.sub(r'%.*', '', l) for l in lines]
    clean_content = "\n".join(clean_lines)
    
    # Regex tìm @type{key, ...}
    pattern = re.compile(r'@\w+\s*\{\s*([^,\s]+)\s*,')
    for match in pattern.finditer(clean_content):
        keys.add(match.group(1).strip())
    return keys

def get_cited_keys(src_dir):
    cited_keys = {}
    cite_pattern = re.compile(r'\\(?:cite|parencite|textcite|citep|citet)\s*\{([^}]+)\}')
    
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.tex'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        # Bỏ qua dòng comment LaTeX (%)
                        clean_line = re.sub(r'(?<!\\)%.*', '', line)
                        for match in cite_pattern.finditer(clean_line):
                            raw_keys = match.group(1)
                            for k in raw_keys.split(','):
                                key = k.strip()
                                if key:
                                    if key not in cited_keys:
                                        cited_keys[key] = []
                                    cited_keys[key].append((file, line_num))
    return cited_keys

def main():
    base_dir = Path(__file__).resolve().parent.parent
    src_dir = base_dir / 'src'
    bib_file = src_dir / 'bibliography.bib'

    print("=" * 60)
    print(" BẮT ĐẦU KIỂM TRA TRÍCH DẪN (CITATION VALIDATION)")
    print("=" * 60)

    bib_keys = get_bib_keys(bib_file)
    cited_dict = get_cited_keys(src_dir)
    cited_keys = set(cited_dict.keys())

    print(f"[*] Tổng số entries trong {bib_file.name}: {len(bib_keys)}")
    print(f"[*] Tổng số unique citations trong src/: {len(cited_keys)}")
    print("-" * 60)

    # 1. Kiểm tra trích dẫn thiếu (Missing citations)
    missing = cited_keys - bib_keys
    if missing:
        print(f"[FAIL] PHÁT HIỆN {len(missing)} TRÍCH DẪN THIẾU TRONG BIBLIOGRAPHY:")
        for m in sorted(missing):
            locations = ", ".join([f"{f}:{l}" for f, l in cited_dict[m]])
            print(f"   ❌ '{m}' -> được gọi tại: {locations}")
    else:
        print("[PASS] Tất cả các trích dẫn trong văn bản đều có trong .bib!")

    # 2. Kiểm tra entries không dùng (Unused entries)
    unused = bib_keys - cited_keys
    if unused:
        print(f"\n[WARN] Phát hiện {len(unused)} mục trong .bib chưa được trích dẫn:")
        for u in sorted(unused):
            print(f"   ⚠️  '{u}'")
    else:
        print("\n[PASS] Tất cả các mục trong .bib đều được sử dụng.")

    print("=" * 60)
    if missing:
        sys.exit(1)
    else:
        print(">> KẾT LUẬN: Hợp lệ 100%!")
        sys.exit(0)

if __name__ == '__main__':
    main()
