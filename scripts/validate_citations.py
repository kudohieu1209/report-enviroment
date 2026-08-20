#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Script kiểm tra tính toàn vẹn của trích dẫn (Citations & BibTeX):
1. Tìm tất cả các \cite, \autocite, \parencite, \textcite, \footcite... trong thư mục src/
2. Tìm tất cả các key trong src/bibliography.bib
3. Báo cáo:
   - File .bib bị thiếu -> Báo lỗi
   - Các trích dẫn trong văn bản bị thiếu trong .bib (Missing citations) -> Báo lỗi
   - Các mục trong .bib không được sử dụng (Unused entries) -> Cảnh báo
   - Hỗ trợ cờ --strict cho bản nộp cuối (yêu cầu bắt buộc có citation thật)
"""

import argparse
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
    if not os.path.exists(bib_file_path):
        print(f"[ERROR] Không tìm thấy file cơ sở dữ liệu trích dẫn: {bib_file_path}")
        return None
    
    keys = set()
    with open(bib_file_path, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    
    # Bỏ qua dòng comment (%)
    clean_lines = [re.sub(r'%.*', '', l) for l in lines]
    clean_content = "\n".join(clean_lines)
    
    # Regex tìm @type{key, ...}
    pattern = re.compile(r'@\w+\s*\{\s*([^,\s]+)\s*,')
    for match in pattern.finditer(clean_content):
        keys.add(match.group(1).strip())
    return keys

def add_key_location(key_map, key, file, line_num):
    if key not in key_map:
        key_map[key] = []
    key_map[key].append((file, line_num))

def get_tex_bib_references(src_dir):
    cited_keys = {}
    nocite_keys = {}
    has_nocite_all = False
    if not src_dir.exists():
        return cited_keys, nocite_keys, has_nocite_all
    
    # Hỗ trợ đầy đủ các lệnh cite chuẩn và biblatex kèm 0-2 cặp ngoặc vuông [arg1][arg2]
    cite_pattern = re.compile(
        r'\\(cite|autocite|textcite|parencite|footcite|nocite|citep|citet|citeauthor|citeyear|Cite|Autocite|Textcite|Parencite|Footcite)'
        r'(?:\[[^\]]*\]){0,2}\s*\{([^}]+)\}'
    )
    
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.tex'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    for line_num, line in enumerate(f, 1):
                        clean_line = re.sub(r'(?<!\\)%.*', '', line)
                        for match in cite_pattern.finditer(clean_line):
                            command = match.group(1).lower()
                            raw_keys = match.group(2)
                            for k in raw_keys.split(','):
                                key = k.strip()
                                if not key:
                                    continue
                                if command == "nocite":
                                    if key == "*":
                                        has_nocite_all = True
                                    else:
                                        add_key_location(nocite_keys, key, file, line_num)
                                else:
                                    add_key_location(cited_keys, key, file, line_num)
    return cited_keys, nocite_keys, has_nocite_all

def get_cited_keys(src_dir):
    cited_keys, _, _ = get_tex_bib_references(src_dir)
    return cited_keys

def main():
    parser = argparse.ArgumentParser(description="Kiểm tra tính toàn vẹn của trích dẫn BibTeX")
    parser.add_argument("--base-dir", type=str, default=None, help="Đường dẫn thư mục gốc dự án (chứa src/)")
    parser.add_argument("--strict", action="store_true", help="Chế độ nghiêm ngặt cho bản nộp cuối (yêu cầu bắt buộc có trích dẫn thật)")
    args = parser.parse_args()

    if args.base_dir:
        base_dir = Path(args.base_dir).resolve()
    elif (Path.cwd() / 'src').exists():
        base_dir = Path.cwd().resolve()
    else:
        base_dir = Path(__file__).resolve().parent.parent

    src_dir = base_dir / 'src'
    bib_file = src_dir / 'bibliography.bib'

    print("=" * 60)
    print(f" BẮT ĐẦU KIỂM TRA TRÍCH DẪN (CITATION VALIDATION{' - STRICT MODE' if args.strict else ''})")
    print("=" * 60)

    bib_keys = get_bib_keys(bib_file)
    if bib_keys is None:
        print(f"[FAIL] File bibliography.bib không tồn tại tại: {bib_file}")
        sys.exit(1)

    cited_dict, nocite_dict, has_nocite_all = get_tex_bib_references(src_dir)
    cited_keys = set(cited_dict.keys())
    nocite_keys = set(nocite_dict.keys())
    referenced_keys = cited_keys | nocite_keys

    print(f"[*] Tổng số entries trong {bib_file.name}: {len(bib_keys)}")
    print(f"[*] Tổng số unique citations trong src/: {len(cited_keys)}")
    print(f"[*] Tổng số nocite entries trong src/: {'*' if has_nocite_all else len(nocite_keys)}")
    print("-" * 60)

    has_error = False

    # Kiểm tra chế độ strict
    if args.strict:
        if len(cited_keys) == 0:
            print("[FAIL-STRICT] Báo cáo cuối cùng chưa có bất kỳ trích dẫn nào trong văn bản!")
            has_error = True
        if len(bib_keys) == 0:
            print("[FAIL-STRICT] File bibliography.bib đang trống, chưa có tài liệu tham khảo!")
            has_error = True

    # 1. Kiểm tra trích dẫn thiếu (Missing citations)
    missing = referenced_keys - bib_keys
    if missing:
        has_error = True
        print(f"[FAIL] PHÁT HIỆN {len(missing)} TRÍCH DẪN THIẾU TRONG BIBLIOGRAPHY:")
        for m in sorted(missing):
            locations = ", ".join([f"{f}:{l}" for f, l in (cited_dict.get(m) or nocite_dict.get(m) or [])])
            print(f"   ❌ '{m}' -> được gọi tại: {locations}")
    else:
        print("[PASS] Tất cả các trích dẫn trong văn bản đều có trong .bib!")

    # 2. Kiểm tra entries không dùng (Unused entries)
    unused = set() if has_nocite_all else bib_keys - referenced_keys
    if unused:
        print(f"\n[WARN] Phát hiện {len(unused)} mục trong .bib chưa được trích dẫn:")
        for u in sorted(unused):
            print(f"   ⚠️  '{u}'")
    else:
        print("\n[PASS] Tất cả các mục trong .bib đều được sử dụng.")

    print("=" * 60)
    if has_error:
        print(">> KẾT LUẬN: Phát hiện lỗi trích dẫn cần khắc phục!")
        sys.exit(1)
    else:
        print(">> KẾT LUẬN: Trích dẫn hợp lệ 100%!")
        sys.exit(0)

if __name__ == '__main__':
    main()
