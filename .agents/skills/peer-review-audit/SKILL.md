---
name: peer-review-audit
description: >-
  Đóng vai trò phản biện học thuật độc lập (Academic Peer Reviewer),
  thực hiện kiểm tra toàn diện về tính logic, lỗ hổng lập luận, mâu thuẫn số liệu,
  đối chiếu với Ma trận Yêu cầu (Requirement Matrix) và tính toàn vẹn của báo cáo trong chu trình Audit-Fix-Rebuild.
---

# Academic Peer Review & Audit Skill

Skill này hướng dẫn quy trình kiểm tra, rà soát và phản biện chất lượng toàn diện của báo cáo, đóng vai trò then chốt trong chu trình hoàn thiện tài liệu:

```text
Draft (Soạn thảo)
     ↓
Validation (validate_citations.py & validate_report.py)
     ↓
Build preview (python scripts/build.py)
     ↓
[★] peer-review-audit (Rà soát phản biện độc lập)
     ↓
Sửa & Khắc phục (Refine & Fix)
     ↓
Validation lần cuối (Final Validation)
     ↓
Final build (Biên dịch bản nộp chính thức)
```

---

## 1. Danh mục Rà soát Phản biện (Peer Review Checklist)

### A. Đối chiếu Ma trận Yêu cầu (Requirement Matrix Audit)
- [ ] Mọi yêu cầu bắt buộc (Mandatory) trong `docs/notes/requirement_matrix.md` đều đã được giải quyết ở các chương mục tương ứng (`[x]`).
- [ ] Cấu trúc số trang, font chữ, lề theo đúng quy định của trường/cơ quan (`docs/references/guidelines/`).

### B. Tính Logic & Lập luận (Logic & Structure)
- [ ] Phần Mở đầu (Chương 1) đã nêu bật được tính cấp thiết và bài toán cụ thể chưa?
- [ ] Mục tiêu đặt ra ở Chương 1 có được giải quyết và đánh giá đầy đủ ở các chương sau không?
- [ ] Phần Kết luận có trả lời trực tiếp cho các câu hỏi nghiên cứu / mục tiêu ban đầu không?

### C. Tính Chính xác của Số liệu & Thực nghiệm (Data & Technical Rigor)
- [ ] Số liệu trong bảng (`Table`) có khớp với phân tích trong văn bản và biểu đồ (`Figure`) không?
- [ ] Các kết quả so sánh có đi kèm điều kiện thực nghiệm rõ ràng không?
- [ ] Đã chỉ ra được nguyên nhân khi kết quả không đạt như kỳ vọng (Failure cases) chưa?
- [ ] Biểu đồ từ `academic-charting` có dùng đúng dữ liệu, đơn vị, nhãn trục, chú giải và phạm vi giá trị đã mô tả trong văn bản không?

### D. Tính Nhất quán & Toàn vẹn Kỹ thuật (Consistency & Integrity)
- [ ] Thuật ngữ chuyên ngành có được dùng thống nhất từ đầu đến cuối không?
- [ ] Sơ đồ từ `diagram-design` có khớp với mô tả kỹ thuật trong văn bản về actor/service, hướng mũi tên, luồng dữ liệu, trust boundary, trạng thái và quan hệ phụ thuộc không?
- [ ] Không có sơ đồ nào thêm thành phần, bước xử lý, database, API hoặc kết nối không được giải thích trong nội dung báo cáo.
- [ ] Mọi hình kiến trúc/quy trình/ERD/sequence đều có chú thích và đoạn văn giải thích trực tiếp ngay gần vị trí nhúng.
- [ ] **Chạy kiểm tra tự động**:
  ```console
  # Trong quá trình soạn thảo:
  python scripts/validate_citations.py
  python scripts/validate_report.py

  # Khi chuẩn bị nộp bản cuối (Bắt buộc kiểm tra nghiêm ngặt):
  python scripts/validate_citations.py --strict
  python scripts/validate_report.py --strict
  ```
- [ ] Không còn thẻ `\todo{...}`, `\note{...}` hoặc thông tin metadata mẫu trong tài liệu.
- [ ] Không có nhãn tham chiếu bị lỗi `??` (broken reference) hoặc hình ảnh bị thiếu.
- [ ] 100% trích dẫn trong văn bản đều có trong `src/bibliography.bib`.

---

## 2. Báo cáo Đánh giá Phản biện (Audit Report Template)
Khi hoàn tất rà soát, xuất báo cáo phản biện vào `docs/notes/peer_review_report.md` theo mẫu:

```markdown
# Báo cáo Phản biện Độc lập (Peer Review Report)

## 1. Đánh giá Tổng quan
- **Mức độ hoàn thành yêu cầu (Requirement Coverage)**: ...%
- **Điểm mạnh cốt lõi**:
- **Điểm cần cải thiện chính**:

## 2. Góp ý Chi tiết theo từng Chương
- **Chương 1 (Mở đầu)**: ...
- **Chương 2 (Tổng quan)**: ...
- **Chương 3 (Phương pháp / Nội dung)**: ...
- **Chương 4 (Kết quả / Thực nghiệm)**: ...
- **Chương 5 (Kết luận)**: ...

## 3. Danh sách Hành động Cần Khắc phục (Action Items)
1. [ ] Sửa đổi đoạn ... ở Chương 3 vì mâu thuẫn số liệu với Bảng 2.
2. [ ] Bổ sung trích dẫn cho khẳng định tại Chương 1.
```

Sau khi hoàn tất sửa đổi theo danh sách Action Items, bắt buộc chạy lại chu trình **Validation lần cuối** và **Final build**.
