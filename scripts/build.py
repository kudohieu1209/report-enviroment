#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Script tự động biên dịch báo cáo LaTeX sang PDF:
1. Làm sạch file PDF cũ trước khi build để tránh false-success
2. Kiểm tra công cụ biên dịch khả dụng (latexmk, pdflatex, biber)
3. Chạy quy trình build đầy đủ giải quyết trích dẫn và liên kết chéo
4. Kiểm tra tính toàn vẹn của PDF mới sinh trước khi kết luận thành công
"""

import os
import shutil
import subprocess
import sys
import time
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
            print(f"[WARN] Lệnh trả về mã: {result.returncode}")
            if result.stdout:
                print(result.stdout[-1500:] if len(result.stdout) > 1500 else result.stdout)
            if result.stderr:
                print(result.stderr[-1500:] if len(result.stderr) > 1500 else result.stderr)
            return False, result.stdout
        return True, result.stdout
    except Exception as e:
        print(f"[ERROR] Ngoại lệ khi thực thi lệnh: {e}")
        return False, str(e)

def check_log_for_fatal_errors(log_file):
    if not log_file.exists():
        return False, "Không tìm thấy file log"
    with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    fatal_indicators = [
        "! Emergency stop",
        "Fatal error occurred",
        "! LaTeX Error: File `"
    ]
    for indicator in fatal_indicators:
        if indicator in content:
            return True, f"Phát hiện lỗi nghiêm trọng trong log: {indicator}"
    return False, ""

def build_pdf():
    base_dir = Path(__file__).resolve().parent.parent
    src_dir = base_dir / 'src'
    output_dir = base_dir / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)

    main_tex = src_dir / 'main.tex'
    if not main_tex.exists():
        print(f"[ERROR] Không tìm thấy file nguồn chính: {main_tex}")
        sys.exit(1)

    # 1. Xóa PDF cũ để tránh false-success từ lần build trước
    target_pdf = output_dir / 'main.pdf'
    final_pdf = output_dir / 'report.pdf'
    log_file = output_dir / 'main.log'

    for old_file in [target_pdf, final_pdf]:
        if old_file.exists():
            try:
                old_file.unlink()
            except Exception as e:
                print(f"[WARN] Không thể xóa file cũ {old_file.name}: {e}")

    build_start_time = time.time()

    print("=" * 60)
    print(" BẮT ĐẦU BIÊN DỊCH BÁO CÁO (LATEX COMPILATION)")
    print("=" * 60)

    success = False

    # 2. Thử biên dịch với latexmk nếu có
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
        ok, _ = run_command(cmd, base_dir)
        has_fatal, msg = check_log_for_fatal_errors(log_file)
        if ok and not has_fatal and target_pdf.exists() and target_pdf.stat().st_mtime >= build_start_time - 1:
            success = True
        else:
            print("[!] latexmk không hoàn tất hoặc có cảnh báo, chuyển sang quy trình thủ công chuẩn...")

    # 3. Quy trình thủ công chuẩn: pdflatex -> biber -> pdflatex -> pdflatex
    if not success and shutil.which("pdflatex"):
        print("[+] Chạy quy trình thủ công: pdflatex -> biber -> pdflatex -> pdflatex...")
        
        # Bước 1: pdflatex lần 1
        print("\n--- Bước 1/4: Khởi tạo aux và bcf ---")
        run_command(["pdflatex", "-interaction=nonstopmode", f"-output-directory={output_dir}", str(main_tex)], base_dir)

        # Bước 2: biber (bắt buộc cho biblatex backend=biber)
        print("\n--- Bước 2/4: Xử lý tài liệu tham khảo (Biber) ---")
        bcf_file = output_dir / "main.bcf"
        if bcf_file.exists():
            if shutil.which("biber"):
                run_command(["biber", f"--input-directory={output_dir}", f"--output-directory={output_dir}", "main"], base_dir)
            else:
                print("[WARN] File cấu hình biblatex (main.bcf) tồn tại nhưng không tìm thấy công cụ 'biber' trên PATH.")
        
        # Bước 3: pdflatex lần 2
        print("\n--- Bước 3/4: Cập nhật nhãn và trích dẫn ---")
        run_command(["pdflatex", "-interaction=nonstopmode", f"-output-directory={output_dir}", str(main_tex)], base_dir)

        # Bước 4: pdflatex lần 3
        print("\n--- Bước 4/4: Hoàn thiện liên kết tham chiếu chéo ---")
        run_command(["pdflatex", "-interaction=nonstopmode", f"-output-directory={output_dir}", str(main_tex)], base_dir)

        # Kiểm tra tính toàn vẹn của PDF mới tạo
        has_fatal, fatal_msg = check_log_for_fatal_errors(log_file)
        if has_fatal:
            print(f"\n[FAIL] Biên dịch thất bại: {fatal_msg}")
            sys.exit(1)

        if target_pdf.exists() and target_pdf.stat().st_size > 0 and target_pdf.stat().st_mtime >= build_start_time - 1:
            success = True

    if not shutil.which("pdflatex") and not shutil.which("latexmk"):
        print("[!] Không tìm thấy trình biên dịch LaTeX (pdflatex hoặc latexmk) trên hệ thống.")
        sys.exit(1)

    if success:
        shutil.copy2(target_pdf, final_pdf)
        print(f"\n🎉 [SUCCESS] Đã tạo thành công file PDF mới: {final_pdf} ({final_pdf.stat().st_size:,} bytes)")
        sys.exit(0)
    else:
        print("\n[FAIL] Biên dịch thất bại. Không tạo được file PDF mới hợp lệ.")
        sys.exit(1)

if __name__ == '__main__':
    build_pdf()
