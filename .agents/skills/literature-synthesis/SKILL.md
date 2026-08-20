---
name: literature-synthesis
description: >-
  Tổng hợp nhiều tài liệu nghiên cứu, bài báo khoa học, lập ma trận tổng hợp (Synthesis Matrix)
  và viết phần Tổng quan lý thuyết / Nghiên cứu liên quan có tính phản biện cao.
---

# Literature Synthesis Skill

Skill này hướng dẫn phương pháp tổng hợp đa nguồn tài liệu thành một bức tranh toàn cảnh, tránh lỗi "liệt kê từng bài báo riêng lẻ" (annotated bibliography) mà hướng tới "tổng hợp theo chủ đề / phương pháp".

## 1. Phương pháp Lập Ma trận Tổng hợp (Synthesis Matrix)

Khi đọc nhiều bài báo trong `docs/references/papers/`, hãy lập bảng ma trận trong `docs/notes/synthesis_matrix.md`:

| Nguồn / Tác giả | Bài toán giải quyết | Phương pháp / Mô hình | Bộ dữ liệu thử nghiệm | Kết quả chính | Hạn chế / Điểm yếu |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Paper A (2022) | ... | ... | ... | ... | ... |
| Paper B (2023) | ... | ... | ... | ... | ... |
| Paper C (2024) | ... | ... | ... | ... | ... |

## 2. Kỹ thuật Viết Tổng hợp theo Cụm Chủ đề (Thematic Synthesis)

Thay vì viết:
> *"Tác giả A làm X. Sau đó tác giả B làm Y. Tiếp theo tác giả C làm Z."*

Hãy viết theo cụm chủ đề / hướng tiếp cận:
> *"Về hướng tiếp cận dựa trên mô hình học sâu, các nghiên cứu ban đầu tập trung vào mạng CNN \cite{paperA}. Tuy nhiên, để giải quyết vấn đề phụ thuộc xa trong chuỗi dữ liệu, các kiến trúc Transformer đã được áp dụng rộng rãi \cite{paperB, paperC}. Mặc dù đạt độ chính xác cao hơn 15%, các mô hình này vẫn gặp thách thức lớn về chi phí tính toán khi triển khai thực tế."*

## 3. Danh sách Kiểm tra Tổng quan Nghiên cứu
- [ ] Đã phân nhóm các nghiên cứu theo hướng tiếp cận logic (ví dụ: phương pháp truyền thống vs. học máy vs. học sâu).
- [ ] Đã chỉ ra rõ ràng khoảng trống nghiên cứu (Research Gap) mà đề tài/báo cáo này sẽ giải quyết.
- [ ] Đã có bảng so sánh tổng hợp (Summary Table) tóm tắt các công trình tiêu biểu.
- [ ] Toàn bộ trích dẫn đã được đăng ký trong `src/bibliography.bib`.
