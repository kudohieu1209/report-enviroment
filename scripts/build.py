#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Script tự động biên dịch báo cáo LaTeX sang PDF:
1. Tạo thư mục output/ nếu chưa có
2. Kiểm tra công cụ biên dịch khả dụng (latexmk, pdflatex, biber, xelatex)
3. Chạy quy trình build đầy đủ giải quyết trích dẫn và liên kết chéo
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# Đảm bảo in UTF-8 mượt mà trên Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def run_command(cmd, cwd):
    print(f"[*] Thực thi: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        if result.returncode != 0:
            print(f"[ERROR] Lệnh trả về mã lỗi: {result.returncode}")
            if result.stdout:
                print(result.stdout[-1500:] if len(result.stdout) > 1500 else result.stdout)
            if result.stderr:
                print(result.stderr[-1500:] if len(result.stderr) > 1500 else result.stderr)
            return False
        return True
    except Exception as e:
        print(f"[ERROR] Ngoại lệ khi thực thi lệnh: {e}")
        return False

def build_pdf():
    base_dir = Path(__file__).resolve().parent.parent
    src_dir = base_dir / 'src'
    output_dir = base_dir / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)

    main_tex = src_dir / 'main.tex'
    if not main_tex.exists():
        print(f"[ERROR] Không tìm thấy file nguồn chính: {main_tex}")
        sys.exit(1)

    print("=" * 60)
    print(" BẮT ĐẦU BIÊN DỊCH BÁO CÁO (LATEX COMPILATION)")
    print("=" * 60)

    # 1. Kiểm tra latexmk
    if shutil.which("latexmk"):
        print("[+] Sử dụng latexmk để tự động hóa toàn bộ chu trình build...")
        cmd = [
            "latexmk",
            "-pdf",
            "-interaction=nonstopmode",
            "-synctex=1",
            f"-outdir={output_dir}",
            str(main_tex)
        ]
        if run_command(cmd, base_dir):
            target_pdf = output_dir / 'main.pdf'
            final_pdf = output_dir / 'report.pdf'
            if target_pdf.exists():
                shutil.copy2(target_pdf, final_pdf)
                print(f"\n🎉 [SUCCESS] Đã tạo thành công file: {final_pdf}")
                return
        else:
            print("[!] latexmk trả về mã lỗi, chuyển sang quy trình thủ công (pdflatex + biber/bibtex)...")

    # 2. Quy trình dự phòng: pdflatex + biber/bibtex
    if shutil.which("pdflatex"):
        print("[+] Chạy quy trình thủ công: pdflatex -> biber/bibtex -> pdflatex -> pdflatex...")
        
        # Bước 1: pdflatex
        print("\n--- Bước 1/4: Khởi tạo aux ---")
        run_command(["pdflatex", "-interaction=nonstopmode", f"-output-directory={output_dir}", str(main_tex)], base_dir)

        # Bước 2: biber / bibtex
        print("\n--- Bước 2/4: Xử lý tài liệu tham khảo ---")
        if shutil.which("biber"):
            run_command(["biber", f"--input-directory={output_dir}", f"--output-directory={output_dir}", "main"], base_dir)
        elif shutil.which("bibtex"):
            run_command(["bibtex", str(output_dir / "main")], base_dir)

        # Bước 3: pdflatex lần 2
        print("\n--- Bước 3/4: Cập nhật nhãn và trích dẫn ---")
        run_command(["pdflatex", "-interaction=nonstopmode", f"-output-directory={output_dir}", str(main_tex)], base_dir)

        # Bước 4: pdflatex lần 3
        print("\n--- Bước 4/4: Hoàn thiện liên kết tham chiếu chéo ---")
        run_command(["pdflatex", "-interaction=nonstopmode", f"-output-directory={output_dir}", str(main_tex)], base_dir)
        
        target_pdf = output_dir / 'main.pdf'
        final_pdf = output_dir / 'report.pdf'
        if target_pdf.exists():
            shutil.copy2(target_pdf, final_pdf)
            print(f"\n🎉 [SUCCESS] Đã tạo thành công file: {final_pdf}")
            return
        else:
            print("[FAIL] Biên dịch thất bại, không tìm thấy file PDF đầu ra.")
            sys.exit(1)

    else:
        print("[!] Không tìm thấy trình biên dịch LaTeX (pdflatex hoặc latexmk) trên hệ thống.")
        print("[!] Hướng dẫn cài đặt:")
        print("    - Windows: Cài đặt MiKTeX (https://miktex.org) hoặc TeX Live.")
        print("    - Hoặc nếu bạn muốn dùng Typst: Chạy 'typst compile src/main.typ output/report.pdf'")
        sys.exit(1)

if __name__ == '__main__':
    build_pdf()
