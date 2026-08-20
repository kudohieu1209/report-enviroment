---
name: diagram-design
description: >-
  Thiết kế và kết xuất các sơ đồ kiến trúc hệ thống, quy trình, luồng dữ liệu, sequence, ERD,
  state machine (38 loại sơ đồ) theo chuẩn Editorial Design (HTML + inline SVG độc lập, lưới 4px,
  font fallback an toàn, viền 1px siêu nét, không đổ bóng, xuất SVG/PDF vào figures/diagrams/).
  Phân biệt rõ với biểu đồ số liệu thực nghiệm (academic-charting).
---

# Diagram Design Skill (Editorial Diagrams)

Skill này chuyên trách về **sơ đồ kiến trúc hệ thống, lưu đồ quy trình, mô hình dữ liệu và các sơ đồ khái niệm kỹ thuật** (Conceptual, System & Process Diagrams).

> [!NOTE]
> **Phân định Trách nhiệm**:
> - Sử dụng `diagram-design` khi cần vẽ: Kiến trúc Microservices, Sơ đồ triển khai Cloud, Sequence Diagram, State Machine, ERD/Database Schema, Data Flow, Swimlane, Hierarchy, Roadmap. Đầu ra lưu vào `figures/diagrams/`.
> - **KHÔNG** dùng skill này để vẽ biểu đồ thống kê, đồ thị hàm số hay biểu đồ cột/đường từ số liệu thực nghiệm $\rightarrow$ Dùng `academic-charting`.

---

## 1. Triết lý Thiết kế Cốt lõi (The Editorial Design System)

1. **Hệ thống Lưới 4px (4px Grid Rule - Bắt buộc)**:
   - Mọi tọa độ ($x, y$), chiều rộng (`width`), chiều cao (`height`), khoảng cách lề (`padding`, `gap`) đều phải chia hết cho 4.
2. **Đường nét Tinh tế (1px Hairline Borders)**:
   - Sử dụng viền mảnh 1px (`stroke-width="1"` hoặc `border: 1px solid`).
   - Tuyệt đối **không dùng hiệu ứng đổ bóng mờ (No Box Shadows / Drop Shadows)** gây cảm giác nặng nề.
   - Bo góc tối đa 8-10px (`rx="6"` hoặc `rx="8"` cho các node thông thường).
3. **Typography 3 Tầng & Font Fallback An toàn**:
   - **Tiêu đề & Chú thích nổi bật (Editorial Callouts)**:
     - Font: `'Instrument Serif', Georgia, 'Times New Roman', serif` (italic).
   - **Tên Node & Luồng chính (Node Names)**:
     - Font: `'Geist', Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif` (Sans-serif, clean).
   - **Nội dung kỹ thuật (Ports, Endpoints, Data Types, SQL)**:
     - Font: `'Geist Mono', 'JetBrains Mono', 'Fira Code', Consolas, 'Courier New', monospace`.
4. **Bảng màu Tối giản & Điểm nhấn Rõ ràng (Color & Focal Points)**:
   - Tối đa **1 màu điểm nhấn chính (Accent Color)** và **1-2 node trọng tâm (Focal Nodes)** trong toàn bộ sơ đồ.
   - Nền sáng (`paper`: `#FFFFFF` hoặc `#FAFAFA`), nét vẽ (`ink`: `#0F172A`), đường nối mờ (`muted`: `#64748B` hoặc `#E2E8F0`).

---

## 2. 38 Loại Sơ đồ Hỗ trợ (Diagram Types Selection)

Đọc `references/types-guide.md` khi cần chọn loại sơ đồ cụ thể hoặc kiểm tra tên `type-*`. Không tự đặt thêm loại ngoài catalog nếu người dùng không yêu cầu biến thể mới.

| Phân nhóm | Các loại sơ đồ tiêu biểu | Khi nào sử dụng? |
| :--- | :--- | :--- |
| **Kiến trúc & Hệ thống** | `type-architecture`, `type-deployment`, `type-dependency`, `type-layers`, `type-nested` | Mô tả Microservices, Cloud AWS/GCP, Kiến trúc phân tầng, Quan hệ phụ thuộc package. |
| **Quy trình & Luồng** | `type-flowchart`, `type-sequence`, `type-swimlane`, `type-state`, `type-journey` | Luồng xử lý nghiệp vụ, Sequence OAuth2/API call, Máy trạng thái (State Machine), Phân quyền. |
| **Dữ liệu & Cấu trúc** | `type-er`, `type-db-schema`, `type-uml-class`, `type-tree`, `type-sankey` | Sơ đồ quan hệ thực thể cơ sở dữ liệu, Cấu trúc cây thư mục, Sơ đồ lớp UML, Luồng phân phối dữ liệu. |
| **Phân tích & Chiến lược** | `type-quadrant`, `type-timeline`, `type-venn`, `type-pyramid`, `type-fishbone`, `type-wardley`, `type-mind-map` | Ma trận 4 góc (Impact vs. Effort), Lộ trình phát triển (Roadmap), Phân tích nguyên nhân gốc rễ. |
| **Phụ thuộc & Mạng lưới** | `type-network-topology`, `type-api-map`, `type-event-flow`, `type-call-graph`, `type-pipeline` | Mạng, API, pub/sub, call graph, CI/CD hoặc ETL pipeline. |
| **Vận hành & Bảo mật** | `type-threat-model`, `type-access-control`, `type-observability`, `type-incident-response` | Trust boundary, quyền truy cập, telemetry, incident response. |
| **Sản phẩm & Tương tác** | `type-wireflow`, `type-user-flow`, `type-information-architecture`, `type-decision-tree` | Luồng màn hình, luồng người dùng, cấu trúc thông tin, cây quyết định. |

---

## 3. Quy trình Xuất bản & Tích hợp vào Báo cáo

1. **Sinh Mã Sơ đồ**: Tạo file SVG độc lập (hoặc file HTML preview) và lưu vào `figures/diagrams/<name>.svg`.
2. **Đảm bảo Tương thích LaTeX**:
   - Nếu biên dịch bằng `pdflatex`: Chuyển SVG sang PDF (`figures/diagrams/<name>.pdf`) hoặc PNG chất lượng cao.
   - Nếu biên dịch bằng `xelatex` hoặc `typst`: Có thể nhúng trực tiếp SVG.
3. **Nhúng vào Chương Báo cáo**:
   ```latex
   \begin{figure}[htbp]
       \centering
       \includegraphics[width=0.9\textwidth]{figures/diagrams/system_architecture.pdf}
       \caption{Kiến trúc tổng thể của hệ thống phân tích dữ liệu}
       \label{fig:system-architecture}
   \end{figure}
   ```
4. **Kiểm tra**: Chạy `python scripts/validate_report.py` để xác minh tham chiếu `\ref{fig:system-architecture}` hợp lệ.
