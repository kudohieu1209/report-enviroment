---
name: document-compiler
description: >-
  Biên dịch (compile) tài liệu nguồn trong src/ sang file PDF chuẩn mực trong output/,
  xử lý lỗi biên dịch LaTeX/Typst và hỗ trợ xuất bản DOCX thử nghiệm qua Pandoc.
---

# Document Compiler Skill

Skill này hướng dẫn quy trình biên dịch toàn bộ tài liệu nguồn sang định dạng xuất bản: **PDF (Định dạng chuẩn Canonical)** và **DOCX (Tùy chọn thử nghiệm qua Pandoc)**.

---

## 1. Biên dịch PDF Chuẩn (Canonical Pipeline)

### Sử dụng Script Tự động:
Chạy script tự động trong thư mục `scripts/`:
```powershell
python scripts/build.py
```

### Quy trình Biên dịch Từng bước (4 bước giải quyết Cross-reference & BibTeX):
1. **Lần 1 (Tạo file aux & lof/lot/toc)**:
   ```powershell
   pdflatex -interaction=nonstopmode -output-directory=output src/main.tex
   ```
2. **Lần 2 (Biên dịch BibTeX / Biber)**:
   ```powershell
   biber --input-directory=output --output-directory=output main
   # hoặc: bibtex output/main
   ```
3. **Lần 3 (Cập nhật số trang & nhãn trích dẫn)**:
   ```powershell
   pdflatex -interaction=nonstopmode -output-directory=output src/main.tex
   ```
4. **Lần 4 (Hoàn tất liên kết tham chiếu chéo)**:
   ```powershell
   pdflatex -interaction=nonstopmode -output-directory=output src/main.tex
   ```

---

## 2. Hỗ trợ Xuất bản DOCX (Optional / Experimental)

> [!NOTE]
> File **PDF** là sản phẩm đầu ra chính thức (*Canonical Output*) để nộp và bảo vệ báo cáo. Tính năng xuất ra file **DOCX** là tùy chọn bổ trợ phục vụ nhu cầu chỉnh sửa văn bản thô hoặc gửi phản hồi qua Word Track Changes.

### Xuất DOCX bằng Pandoc (nếu hệ thống đã cài đặt Pandoc):
```powershell
pandoc src/main.tex -o output/report.docx --bibliography=src/bibliography.bib --citeproc
```

---

## 3. Xử lý Lỗi Biên dịch Thường gặp
- **Undefined control sequence**: Thiếu gói lệnh (`\usepackage{...}`) trong `src/config/packages.tex`.
- **Reference `...` on page X undefined**: Quên chạy lại `pdflatex` lần 2/3 hoặc tên nhãn `\ref{...}` bị gõ sai $\rightarrow$ Chạy `python scripts/validate_report.py` để kiểm tra.
- **Citation `...` undefined**: Kiểm tra xem key trích dẫn có tồn tại trong `src/bibliography.bib` chưa $\rightarrow$ Chạy `python scripts/validate_citations.py` để kiểm tra.
- **Missing file / image error**: Đường dẫn hình ảnh không chính xác hoặc file chưa tồn tại trong `figures/`.
