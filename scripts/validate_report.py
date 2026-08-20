#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Script kiểm tra tính toàn vẹn của báo cáo LaTeX:
1. Kiểm tra nhãn trùng lặp (\label{...})
2. Kiểm tra tham chiếu bị hỏng (\ref{...}, \eqref{...} không tìm thấy \label)
3. Kiểm tra các file hình ảnh (\includegraphics{...}) có tồn tại không
4. Hỗ trợ cờ --strict cho bản nộp cuối (kiểm tra \todo, \note, và metadata mẫu)
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

PLACEHOLDER_METADATA = [
    "Nguyễn Văn A",
    "20260001",
    "TS. Trần Văn B",
    "ThS. Lê Văn C",
    "Công ty Cổ phần Công nghệ XYZ",
    "Trường Đại học Bách Khoa",
    "Khoa Công nghệ Thông tin"
]

def validate_latex(base_dir, is_strict=False):
    src_dir = base_dir / 'src'
    if not src_dir.exists():
        print(f"[ERROR] Không tìm thấy thư mục src: {src_dir}")
        return False
    
    labels = {}
    references = []
    includes = []
    todos = []
    notes = []
    placeholder_matches = []
    
    label_pattern = re.compile(r'\\label\{([^}]+)\}')
    ref_pattern = re.compile(r'\\(?:ref|eqref|pageref|autoref|cref)\{([^}]+)\}')
    img_pattern = re.compile(r'\\includegraphics(?:\[.*?\])?\{([^}]+)\}')
    todo_pattern = re.compile(r'\\todo\{([^}]+)\}')
    note_pattern = re.compile(r'\\note\{([^}]+)\}')
    
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.tex'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, base_dir)
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    for line_num, line in enumerate(f, 1):
                        clean_line = re.sub(r'(?<!\\)%.*', '', line)
                        
                        # Labels
                        for match in label_pattern.finditer(clean_line):
                            lbl = match.group(1).strip()
                            if lbl not in labels:
                                labels[lbl] = []
                            labels[lbl].append((rel_path, line_num))
                        
                        # References
                        for match in ref_pattern.finditer(clean_line):
                            ref = match.group(1).strip()
                            references.append((ref, rel_path, line_num))
                            
                        # Images
                        for match in img_pattern.finditer(clean_line):
                            img_path = match.group(1).strip()
                            includes.append((img_path, rel_path, line_num))

                        # TODOs & Notes
                        for match in todo_pattern.finditer(clean_line):
                            todos.append((match.group(1).strip(), rel_path, line_num))
                        for match in note_pattern.finditer(clean_line):
                            notes.append((match.group(1).strip(), rel_path, line_num))

                        # Placeholder metadata (chỉ kiểm tra trong file metadata.tex)
                        if file == 'metadata.tex':
                            for ph in PLACEHOLDER_METADATA:
                                if ph in line:
                                    placeholder_matches.append((ph, rel_path, line_num))

    print("=" * 60)
    print(f" BẮT ĐẦU KIỂM TRA BÁO CÁO (REPORT INTEGRITY AUDIT{' - STRICT MODE' if is_strict else ''})")
    print("=" * 60)

    has_error = False

    # 1. Trùng lặp labels
    print("[1] KIỂM TRA TRÙNG LẶP LABELS:")
    duplicate_labels = {k: v for k, v in labels.items() if len(v) > 1}
    if duplicate_labels:
        has_error = True
        for lbl, locs in duplicate_labels.items():
            loc_str = ", ".join([f"{f}:{l}" for f, l in locs])
            print(f"   ❌ Duplicate label '{lbl}' tại: {loc_str}")
    else:
        print("   ✅ Không có label nào bị trùng lặp.")

    # 2. Tham chiếu bị gãy (Broken references)
    print("\n[2] KIỂM TRA THAM CHIẾU GÃY (BROKEN REFERENCES):")
    broken_refs = [(r, f, l) for r, f, l in references if r not in labels]
    if broken_refs:
        has_error = True
        for r, f, l in broken_refs:
            print(f"   ❌ Broken reference '\\ref{{{r}}}' tại {f}:{l}")
    else:
        print("   ✅ Tất cả các tham chiếu (\\ref) đều có \\label tương ứng.")

    # 3. Kiểm tra file hình ảnh
    print("\n[3] KIỂM TRA FILE HÌNH ẢNH (IMAGES / FIGURES):")
    missing_imgs = []
    for img, f, l in includes:
        full_img_path = base_dir / img
        found = False
        if full_img_path.exists():
            found = True
        else:
            for ext in ['.pdf', '.png', '.jpg', '.jpeg', '.eps', '.svg']:
                if (base_dir / (img + ext)).exists():
                    found = True
                    break
        if not found:
            missing_imgs.append((img, f, l))

    if missing_imgs:
        has_error = True
        for img, f, l in missing_imgs:
            print(f"   ❌ Missing image: '{img}' được gọi tại {f}:{l}")
    else:
        print("   ✅ Tất cả các file hình ảnh đều tồn tại.")

    # 4. Kiểm tra TODOs và Metadata mẫu (Strict Mode)
    if is_strict:
        print("\n[4] KIỂM TRA CHẾ ĐỘ NGHIÊM NGẶT (STRICT SUBMISSION CHECK):")
        if todos:
            has_error = True
            print(f"   ❌ Phát hiện {len(todos)} mục \\todo chưa hoàn thành:")
            for t, f, l in todos[:10]:
                print(f"      - [{f}:{l}] {t}")
            if len(todos) > 10:
                print(f"      ... và {len(todos) - 10} mục khác.")
        else:
            print("   ✅ Không còn thẻ \\todo nào trong tài liệu.")

        if notes:
            has_error = True
            print(f"   ❌ Phát hiện {len(notes)} mục \\note cần xử lý:")
            for n, f, l in notes:
                print(f"      - [{f}:{l}] {n}")

        if placeholder_matches:
            has_error = True
            print(f"   ❌ Phát hiện {len(placeholder_matches)} metadata mẫu chưa được cập nhật thông tin thật:")
            for ph, f, l in placeholder_matches:
                print(f"      - [{f}:{l}] Metadata placeholder: '{ph}'")
        else:
            print("   ✅ Thông tin metadata đã được cập nhật.")
    else:
        if todos:
            print(f"\n[INFO] Tài liệu hiện có {len(todos)} mục \\todo (bình thường trong quá trình soạn thảo).")

    print("=" * 60)
    if has_error:
        print(">> KẾT LUẬN: Phát hiện lỗi toàn vẹn cần khắc phục!")
        return False
    else:
        print(">> KẾT LUẬN: Cấu trúc báo cáo hoàn toàn hợp lệ!")
        return True

def main():
    parser = argparse.ArgumentParser(description="Kiểm tra tính toàn vẹn của báo cáo LaTeX")
    parser.add_argument("--base-dir", type=str, default=None, help="Đường dẫn thư mục gốc dự án (chứa src/)")
    parser.add_argument("--strict", action="store_true", help="Chế độ nghiêm ngặt cho bản nộp cuối (kiểm tra TODOs và metadata mẫu)")
    args = parser.parse_args()

    if args.base_dir:
        base_dir = Path(args.base_dir).resolve()
    elif (Path.cwd() / 'src').exists():
        base_dir = Path.cwd().resolve()
    else:
        base_dir = Path(__file__).resolve().parent.parent

    ok = validate_latex(base_dir, is_strict=args.strict)
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
