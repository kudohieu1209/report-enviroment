---
name: document-analysis
description: >-
  Phân tích, giải mã và trích xuất thông tin có cấu trúc từ tài liệu gốc,
  hướng dẫn trình bày (guidelines), tiêu chuẩn báo cáo, hoặc báo cáo mẫu trong docs/references/.
  Lập ma trận yêu cầu (Requirement Matrix) trước khi viết.
---

# Document Analysis Skill

Skill này hướng dẫn quy trình phân tích tài liệu đầu vào, trích xuất yêu cầu và lập **Ma trận Yêu cầu (Requirement Matrix)** làm kim chỉ nam trước khi tiến hành lập dàn ý và soạn thảo.

---

## 1. Nguyên tắc Phân cấp Tài liệu (Source Hierarchy)
- **Tài liệu Hướng dẫn Chính thức (`docs/references/guidelines/`) [MỨC ƯU TIÊN CAO NHẤT]**:
  - Là nguồn quy định bắt buộc (Normative Requirements) về cấu trúc, độ dài, lề, font chữ, quy chuẩn trích dẫn và tiêu chí đánh giá của trường/công ty.
- **Báo cáo Mẫu (`docs/references/sample-reports/`) [CHỈ THAM KHẢO]**:
  - Chỉ dùng để tham khảo phong cách trình bày, cách phân chia đề mục, mức độ chi tiết kỹ thuật.
  - **Tuyệt đối không** coi quy định trong báo cáo mẫu là yêu cầu bắt buộc nếu mâu thuẫn với Guideline chính thức.
- **Tài liệu Nghiên cứu / Bài báo (`docs/references/papers/`)**:
  - Cung cấp cơ sở lý thuyết, số liệu benchmark và giải pháp kỹ thuật cho `literature-synthesis`.

---

## 2. Quy trình Trích xuất & Lập Requirement Matrix

Quy trình bắt buộc phải tuân theo luồng:
```text
Guideline / Tài liệu gốc
       ↓
Trích xuất yêu cầu
       ↓
Ma trận Yêu cầu (docs/notes/requirement_matrix.md)
       ↓
Dàn ý Báo cáo (docs/drafts/outline.md)
       ↓
Soạn thảo chi tiết (src/chapters/)
```

### Cấu trúc file `docs/notes/requirement_matrix.md`:

```markdown
# Ma trận Yêu cầu Báo cáo (Requirement Matrix)

| STT | Yêu cầu cụ thể (Requirement) | Nguồn tài liệu (Source) | Trang/Mục | Bắt buộc / Tùy chọn | Mục tương ứng trong Báo cáo | Trạng thái | Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Độ dài 40 - 60 trang (không tính phụ lục) | Guideline ĐHBK | Trang 4, Mục 2.1 | Bắt buộc | Toàn bộ báo cáo | [ ] Chưa hoàn thành | Giãn dòng 1.5, font 12pt |
| 2 | Bắt buộc có phần đánh giá rủi ro an toàn | Guideline ĐHBK | Trang 8, Mục 3.4 | Bắt buộc | Chương 3 (Mục 3.4) | [ ] Chưa hoàn thành | Cần lập bảng đánh giá |
| 3 | Trích dẫn tối thiểu 10 bài báo quốc tế | Guideline ĐHBK | Trang 12 | Bắt buộc | src/bibliography.bib | [ ] Đã có 4/10 | Cần bổ sung thêm |
```

---

## 3. Công cụ & Quy trình Kỹ thuật
1. **Đọc và Trích xuất Nội dung**:
   - File văn bản / Markdown: Sử dụng `view_file`.
   - File PDF / Word: Chạy script Python (ví dụ sử dụng `pypdf`, `pymupdf` hoặc `docx2txt`) để trích xuất văn bản, bảng biểu, danh mục kiểm tra.
2. **Cập nhật Trạng thái**:
   - Khi hoàn thành từng mục trong báo cáo (`src/chapters/`), cập nhật trạng thái trong `requirement_matrix.md` (`[x] Đã hoàn thành`).
3. **Chuyển tiếp Quy trình**:
   - Sau khi hoàn thành Requirement Matrix, kích hoạt `academic-writing` để tạo khung `docs/drafts/outline.md` và các file `src/chapters/*.tex`.
