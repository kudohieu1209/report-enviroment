---
name: academic-writing
description: >-
  Soạn thảo, phát triển nội dung, mở rộng ý và hoàn thiện các chương của báo cáo/bài báo
  theo cấu trúc linh hoạt theo từng loại tài liệu (Research Paper, Internship Report, Technical Report)
  hoặc theo quy định bắt buộc của Guideline.
---

# Academic Writing Skill

Skill này hướng dẫn quy trình lập dàn ý và soạn thảo nội dung các chương trong `src/chapters/`, đảm bảo tính mạch lạc, khoa học và phù hợp với từng loại tài liệu cụ thể.

---

## 1. Nguyên tắc Chọn Cấu trúc Tài liệu (Structure Selection Hierarchy)

> [!IMPORTANT]
> **Quy tắc Phân cấp Cấu trúc**:
> 1. **Nếu Guideline/Đề tài có quy định cấu trúc bắt buộc $\rightarrow$ GUIDELINE THẮNG (Normative).** Tuân thủ 100% mục lục và cấu trúc được chỉ định trong `docs/notes/requirement_matrix.md`.
> 2. **Nếu không có cấu trúc bắt buộc $\rightarrow$ Lựa chọn cấu trúc chuẩn theo Loại Tài liệu** dưới đây:

### A. Bài báo Khoa học / Nghiên cứu (Research Paper - Mô hình IMRaD)
- **Introduction**: Bối cảnh, bài toán, câu hỏi nghiên cứu và đóng góp.
- **Related Work / Background**: Tổng quan lý thuyết và các nghiên cứu liên quan.
- **Methodology (Methods)**: Kiến trúc mô hình, công thức toán học, thuật toán đề xuất.
- **Experiments & Results**: Thiết lập thử nghiệm, bộ dữ liệu, số liệu định lượng và thảo luận (Discussion).
- **Conclusion**: Tóm tắt đóng góp, hạn chế và hướng phát triển.
- **Abstract / Tóm tắt**: Viết sau cùng, 150-300 từ hoặc theo guideline, nêu bối cảnh, mục tiêu, phương pháp, kết quả chính và đóng góp; không trích dẫn, không mở rộng luận điểm mới.
- **Acknowledgments / Lời cảm ơn**: Viết ngắn gọn, trang trọng, cảm ơn đơn vị/cá nhân hỗ trợ theo đúng quy định; không đưa nội dung kỹ thuật hoặc kết quả nghiên cứu vào phần này.

### B. Báo cáo Thực tập Doanh nghiệp (Internship Report)
- **Chương 1 (Mở đầu - Introduction)**: Bối cảnh, lý do chọn đề tài, mục tiêu và phạm vi thực tập.
- **Chương 2 (Tổng quan Đơn vị - Organization/Company Overview)**: Lịch sử, cơ cấu tổ chức, lĩnh vực hoạt động, vị trí và nhiệm vụ được phân công.
- **Chương 3 (Nội dung Công việc & Giải pháp Kỹ thuật - Work Performed)**: Khảo sát hiện trạng, phân tích yêu cầu, thiết kế kiến trúc và quy trình hiện thực hóa.
- **Chương 4 (Kết quả Đạt được & Đánh giá - Results & Evaluation)**: Các sản phẩm/tính năng hoàn thành, số liệu thử nghiệm, kỹ năng tích lũy và bài học kinh nghiệm.
- **Chương 5 (Kết luận & Kiến nghị - Conclusion & Recommendations)**: Đánh giá quá trình thực tập, kiến nghị với nhà trường và doanh nghiệp.

### C. Báo cáo Kỹ thuật / Đồ án Môn học / Khóa luận Tốt nghiệp (Technical Report)
- **Chương 1 (Tổng quan Bài toán - Problem Statement)**: Mục tiêu đề tài, khảo sát các giải pháp tương tự.
- **Chương 2 (Phân tích Yêu cầu - Requirements & Specifications)**: Yêu cầu chức năng (Functional), phi chức năng (Non-functional), use case.
- **Chương 3 (Thiết kế Hệ thống - System Design & Architecture)**: Sơ đồ kiến trúc tổng thể, thiết kế cơ sở dữ liệu (ERD), API endpoints.
- **Chương 4 (Hiện thực hóa & Đánh giá - Implementation & Evaluation)**: Môi trường triển khai, thử nghiệm hiệu năng (Benchmark), kiểm thử bảo mật.
- **Chương 5 (Kết luận & Hướng phát triển - Conclusion & Future Work)**: Tổng kết sản phẩm, hạn chế và kế hoạch nâng cấp.

---

## 2. Quy trình Soạn thảo Từng bước

1. **Đối chiếu Requirement Matrix**: Đọc `docs/notes/requirement_matrix.md` để nắm rõ các mục bắt buộc.
2. **Lập Dàn ý Chi tiết (Outline)**: Tạo khung các mục con (`\section`, `\subsection`) trong `docs/drafts/outline.md`.
3. **Xác định phần đầu tài liệu (Frontmatter)**:
   - Nếu Requirement Matrix hoặc guideline yêu cầu Abstract/Tóm tắt, viết trong `src/frontmatter/abstract.tex` và đặt trước mục lục.
   - Nếu guideline yêu cầu Lời cảm ơn, viết trong `src/frontmatter/acknowledgments.tex`.
   - Không thêm trích dẫn trong Abstract/Tóm tắt; không dùng Abstract để giới thiệu kết quả chưa được trình bày ở thân bài.
4. **Soạn thảo Từng Đoạn (Paragraph Drafting)**: Áp dụng mô hình **PEEL** (Point - Evidence - Explanation - Link):
   - *Point*: Câu chủ đề nêu rõ luận điểm kỹ thuật.
   - *Evidence*: Dẫn chứng bằng số liệu bảng biểu, hình ảnh hoặc trích dẫn nguồn.
   - *Explanation*: Giải thích cơ chế, lý do hoặc ý nghĩa kỹ thuật.
   - *Link*: Mối liên hệ với mục tiêu chung của chương.
5. **Tích hợp Tham chiếu & Đồ họa**:
   - Bắt buộc dùng `diagram-design` khi guideline yêu cầu sơ đồ hoặc khi văn bản mô tả kiến trúc hệ thống, luồng xử lý, ERD/schema, sequence, state machine, phân quyền/trust boundary hay pipeline có từ 3 thành phần/bước trở lên.
   - Bắt buộc dùng `academic-charting` khi văn bản so sánh số liệu, trình bày xu hướng, phân phối, confusion matrix, benchmark hoặc kết quả thực nghiệm định lượng.
   - Tùy chọn dùng sơ đồ/biểu đồ khi chỉ minh họa khái niệm đơn giản; không tạo hình nếu nó không làm lập luận rõ hơn.
   - Trích dẫn nguồn qua `citation-bibtex` (`\cite{...}`).
