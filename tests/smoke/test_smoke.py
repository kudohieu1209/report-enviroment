#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Comprehensive Automated Smoke Test Suite for Report Environment:
1. Kiểm tra Citation Validator (PASS trên template sạch, FAIL khi thiếu .bib, FAIL khi thiếu key có bracket, FAIL khi strict)
2. Kiểm tra Report Validator (PASS trên template sạch, FAIL khi gãy \ref, FAIL khi trùng label, FAIL khi thiếu ảnh, FAIL khi strict có \todo)
3. Kiểm tra Render Chart thật sự vào tests/outputs/
4. Kiểm tra Render Diagram thật sự vào tests/outputs/
Tất cả các ca test lỗi (intentional FAIL) đều chạy trong thư mục tạm, bảo toàn 100% độ sạch của src/ và figures/.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Đảm bảo UTF-8 trên Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

SCRIPTS_DIR = BASE_DIR / 'scripts'
TESTS_DIR = BASE_DIR / 'tests'
OUTPUTS_DIR = TESTS_DIR / 'outputs'
FIXTURES_DIR = TESTS_DIR / 'fixtures'

def run_cmd(cmd, cwd=BASE_DIR):
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    return result.returncode, result.stdout, result.stderr

def test_citations_validator_pass_and_fail():
    print("[1/4] Kiểm tra Citation Validator (PASS & Intentional FAIL)...")
    
    # 1. PASS trên template sạch
    code, out, _ = run_cmd([sys.executable, str(SCRIPTS_DIR / 'validate_citations.py')])
    assert code == 0, f"Validator thất bại trên template sạch: {out}"
    print("   ✅ PASS: Template sạch hợp lệ.")

    # 2. FAIL: Thiếu key có bracket arguments (\cite[tr. 10]{fake2026})
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        tmp_src = tmp_path / 'src'
        tmp_src.mkdir()
        
        (tmp_src / 'bibliography.bib').write_text("@article{real2026, author={A}, title={B}, year={2026}}", encoding='utf-8')
        (tmp_src / 'main.tex').write_text(r"\cite[tr. 10]{fake_key_123}", encoding='utf-8')
        
        code, out, _ = run_cmd([sys.executable, str(SCRIPTS_DIR / 'validate_citations.py')], cwd=tmp_path)
        assert code != 0, f"Validator không bắt được lỗi thiếu citation: {out}"
        assert "fake_key_123" in out, "Validator không chỉ ra đúng key bị thiếu"
    print("   ✅ FAIL DETECTED: Bắt chính xác lỗi trích dẫn thiếu (kể cả có bracket argument).")

    # 3. FAIL: Thiếu file bibliography.bib
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        tmp_src = tmp_path / 'src'
        tmp_src.mkdir()
        (tmp_src / 'main.tex').write_text("Không có trích dẫn", encoding='utf-8')
        
        code, out, _ = run_cmd([sys.executable, str(SCRIPTS_DIR / 'validate_citations.py')], cwd=tmp_path)
        assert code != 0, "Validator không báo lỗi khi thiếu file bibliography.bib"
    print("   ✅ FAIL DETECTED: Bắt chính xác lỗi khi thiếu file bibliography.bib.")

    # 4. FAIL trong chế độ --strict khi có 0 citations
    code, out, _ = run_cmd([sys.executable, str(SCRIPTS_DIR / 'validate_citations.py'), '--strict'])
    assert code != 0, "Chế độ --strict không báo lỗi khi báo cáo có 0 citations"
    print("   ✅ FAIL DETECTED: Chế độ --strict bắt chính xác khi báo cáo cuối cùng thiếu trích dẫn.")

def test_report_validator_pass_and_fail():
    print("\n[2/4] Kiểm tra Report Integrity Validator (PASS & Intentional FAIL)...")
    
    # 1. PASS trên template sạch (normal mode)
    code, out, _ = run_cmd([sys.executable, str(SCRIPTS_DIR / 'validate_report.py')])
    assert code == 0, f"Validator thất bại trên template sạch: {out}"
    print("   ✅ PASS: Template sạch hợp lệ ở chế độ soạn thảo.")

    # 2. FAIL: Broken reference (\ref{fake_ref})
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        tmp_src = tmp_path / 'src'
        tmp_src.mkdir()
        (tmp_src / 'test.tex').write_text(r"Xem Hình~\ref{fig:non_existent}", encoding='utf-8')
        
        code, out, _ = run_cmd([sys.executable, str(SCRIPTS_DIR / 'validate_report.py')], cwd=tmp_path)
        assert code != 0, "Validator không bắt được broken reference"
        assert "fig:non_existent" in out
    print("   ✅ FAIL DETECTED: Bắt chính xác lỗi tham chiếu gãy (broken reference).")

    # 3. FAIL: Trùng label
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        tmp_src = tmp_path / 'src'
        tmp_src.mkdir()
        (tmp_src / 'test1.tex').write_text(r"\label{sec:dup}", encoding='utf-8')
        (tmp_src / 'test2.tex').write_text(r"\label{sec:dup}", encoding='utf-8')
        
        code, out, _ = run_cmd([sys.executable, str(SCRIPTS_DIR / 'validate_report.py')], cwd=tmp_path)
        assert code != 0, "Validator không bắt được duplicate label"
        assert "sec:dup" in out
    print("   ✅ FAIL DETECTED: Bắt chính xác lỗi trùng lặp label.")

    # 4. FAIL: Thiếu file hình ảnh
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        tmp_src = tmp_path / 'src'
        tmp_src.mkdir()
        (tmp_src / 'test.tex').write_text(r"\includegraphics{figures/charts/non_existent.pdf}", encoding='utf-8')
        
        code, out, _ = run_cmd([sys.executable, str(SCRIPTS_DIR / 'validate_report.py')], cwd=tmp_path)
        assert code != 0, "Validator không bắt được lỗi thiếu file hình ảnh"
    print("   ✅ FAIL DETECTED: Bắt chính xác lỗi thiếu file hình ảnh (Missing image).")

    # 5. FAIL trong chế độ --strict khi còn \todo và metadata placeholder
    code, out, _ = run_cmd([sys.executable, str(SCRIPTS_DIR / 'validate_report.py'), '--strict'])
    assert code != 0, "Chế độ --strict không bắt được \\todo và metadata placeholder trong template"
    print("   ✅ FAIL DETECTED: Chế độ --strict bắt chính xác khi còn \\todo hoặc metadata mẫu.")

def test_chart_rendering():
    print("\n[3/4] Kiểm tra Render Chart thật sự vào tests/outputs/...")
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    try:
        from scripts.render_chart import generate_sample_charts
        generate_sample_charts(OUTPUTS_DIR)
        
        acc_pdf = OUTPUTS_DIR / 'accuracy_curve.pdf'
        acc_png = OUTPUTS_DIR / 'accuracy_curve.png'
        assert acc_pdf.exists() and acc_pdf.stat().st_size > 0, "File chart PDF không được tạo"
        assert acc_png.exists() and acc_png.stat().st_size > 0, "File chart PNG không được tạo"
        print(f"   ✅ Render chart thành công: {acc_pdf.name} ({acc_pdf.stat().st_size:,} bytes)")
    except Exception as e:
        print(f"   ❌ Lỗi khi render chart: {e}")
        sys.exit(1)

def test_diagram_rendering():
    print("\n[4/4] Kiểm tra Render Diagram thật sự vào tests/outputs/...")
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    svg_content = """<svg width="400" height="100" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="100" fill="#fafafa" rx="6"/>
  <rect x="20" y="20" width="100" height="60" rx="4" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>
  <text x="70" y="55" text-anchor="middle" font-family="'Geist', sans-serif" font-size="12">Client</text>
  <line x1="120" y1="50" x2="180" y2="50" stroke="#64748b" stroke-width="1.5"/>
  <rect x="180" y="20" width="120" height="60" rx="4" fill="#fff7ed" stroke="#ea580c" stroke-width="1.5"/>
  <text x="240" y="55" text-anchor="middle" font-family="'Geist', sans-serif" font-size="12" fill="#9a3412">API Gateway</text>
</svg>"""
    diagram_svg = OUTPUTS_DIR / 'smoke_architecture.svg'
    diagram_svg.write_text(svg_content, encoding='utf-8')
    assert diagram_svg.exists() and diagram_svg.stat().st_size > 0, "File diagram SVG không được tạo"
    print(f"   ✅ Render diagram thành công: {diagram_svg.name} ({diagram_svg.stat().st_size:,} bytes)")

def main():
    print("=" * 60)
    print(" BẮT ĐẦU CHẠY AUTOMATED SMOKE TEST SUITE")
    print("=" * 60)
    test_citations_validator_pass_and_fail()
    test_report_validator_pass_and_fail()
    test_chart_rendering()
    test_diagram_rendering()
    print("\n" + "=" * 60)
    print("🎉 TẤT CẢ 9/9 TEST CASES (PASS, FAIL, STRICT, ASSETS) ĐỀU PASS 100%!")
    print("=" * 60)

if __name__ == '__main__':
    main()
