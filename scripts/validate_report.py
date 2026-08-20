#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Script kiểm tra tính toàn vẹn của báo cáo LaTeX:
1. Kiểm tra nhãn trùng lặp (\label{...})
2. Kiểm tra tham chiếu bị hỏng (\ref{...}, \eqref{...} không tìm thấy \label)
3. Kiểm tra các file hình ảnh (\includegraphics{...}) có tồn tại không
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

def validate_latex(base_dir):
    src_dir = base_dir / 'src'
    
    labels = {}
    references = []
    includes = []
    
    label_pattern = re.compile(r'\\label\{([^}]+)\}')
    ref_pattern = re.compile(r'\\(?:ref|eqref|pageref|autoref|cref)\{([^}]+)\}')
    img_pattern = re.compile(r'\\includegraphics(?:\[.*?\])?\{([^}]+)\}')
    
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.tex'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, base_dir)
                with open(file_path, 'r', encoding='utf-8') as f:
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

    print("=" * 60)
    print(" BẮT ĐẦU KIỂM TRA BÁO CÁO (REPORT INTEGRITY AUDIT)")
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
            for ext in ['.pdf', '.png', '.jpg', '.jpeg', '.eps']:
                if (base_dir / (img + ext)).exists():
                    found = True
                    break
        if not found:
            missing_imgs.append((img, f, l))

    if missing_imgs:
        print("   ⚠️  Cảnh báo file hình ảnh chưa có sẵn:")
        for img, f, l in missing_imgs:
            print(f"   ⚠️  '{img}' được gọi tại {f}:{l}")
    else:
        print("   ✅ Tất cả các file hình ảnh đều tồn tại.")

    print("=" * 60)
    if has_error:
        print(">> KẾT LUẬN: Cần khắc phục các lỗi trên!")
        sys.exit(1)
    else:
        print(">> KẾT LUẬN: Cấu trúc báo cáo hoàn toàn hợp lệ!")
        sys.exit(0)

if __name__ == '__main__':
    base_dir = Path(__file__).resolve().parent.parent
    validate_latex(base_dir)
