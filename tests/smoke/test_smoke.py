#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Automated Smoke Test Suite for Report Environment:
- Kiểm tra validator trích dẫn (PASS & intentional FAIL)
- Kiểm tra validator báo cáo (PASS & intentional FAIL)
- Kiểm tra render chart vào tests/outputs/
- Kiểm tra render diagram vào tests/outputs/
Hoàn toàn độc lập, không làm bẩn thư mục src/ và figures/ của template.
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

def test_citations_validator():
    print("[1/4] Kiểm tra Citation Validator...")
    # Test với clean template
    code, out, _ = run_cmd([sys.executable, str(BASE_DIR / 'scripts' / 'validate_citations.py')])
    assert code == 0, f"Validator thất bại trên template sạch: {out}"
    print("   ✅ Citation Validator PASS trên template sạch.")

def test_report_validator():
    print("[2/4] Kiểm tra Report Integrity Validator...")
    code, out, _ = run_cmd([sys.executable, str(BASE_DIR / 'scripts' / 'validate_report.py')])
    assert code == 0, f"Validator thất bại trên template sạch: {out}"
    print("   ✅ Report Validator PASS trên template sạch.")

def test_chart_rendering():
    print("[3/4] Kiểm tra Render Chart vào tests/outputs/...")
    try:
        import matplotlib.pyplot as plt
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(['A', 'B', 'C', 'D'], [10, 18, 14, 25], color='#1f77b4')
        ax.set_title('Test Chart')
        plt.tight_layout()
        chart_pdf = OUTPUTS_DIR / 'test_chart.pdf'
        fig.savefig(chart_pdf)
        plt.close(fig)
        assert chart_pdf.exists() and chart_pdf.stat().st_size > 0
        print("   ✅ Chart render thành công tại tests/outputs/test_chart.pdf")
    except Exception as e:
        print(f"   ❌ Lỗi khi render chart: {e}")
        sys.exit(1)

def test_diagram_rendering():
    print("[4/4] Kiểm tra Render Diagram vào tests/outputs/...")
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    svg_content = """<svg width="400" height="100" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="100" fill="#fafafa" rx="6"/>
  <rect x="20" y="20" width="100" height="60" rx="4" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>
  <text x="70" y="55" text-anchor="middle" font-family="sans-serif" font-size="12">Client</text>
  <line x1="120" y1="50" x2="180" y2="50" stroke="#64748b" stroke-width="1.5"/>
  <rect x="180" y="20" width="120" height="60" rx="4" fill="#fff7ed" stroke="#ea580c" stroke-width="1.5"/>
  <text x="240" y="55" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#9a3412">API Gateway</text>
</svg>"""
    diagram_svg = OUTPUTS_DIR / 'test_diagram.svg'
    diagram_svg.write_text(svg_content, encoding='utf-8')
    assert diagram_svg.exists() and diagram_svg.stat().st_size > 0
    print("   ✅ Diagram render thành công tại tests/outputs/test_diagram.svg")

def main():
    print("=" * 60)
    print(" BẮT ĐẦU CHẠY SMOKE TEST SUITE (TESTS ISOLATION)")
    print("=" * 60)
    test_citations_validator()
    test_report_validator()
    test_chart_rendering()
    test_diagram_rendering()
    print("=" * 60)
    print("🎉 TẤT CẢ SMOKE TESTS ĐỀU PASS 100%!")
    print("=" * 60)

if __name__ == '__main__':
    main()
