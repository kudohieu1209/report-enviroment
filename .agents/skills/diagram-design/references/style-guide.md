# Diagram Design Style Guide & Tokens

Hệ thống token màu sắc, typography và kích thước dùng chung cho toàn bộ sơ đồ editorial:

## 1. Color Palette (Bảng màu Chuẩn)

| Token Name | Hex Code | Ý nghĩa & Vị trí áp dụng |
| :--- | :--- | :--- |
| `paper` | `#FFFFFF` / `#FAFAFA` | Nền canvas, nền các container |
| `paper-subtle` | `#F1F5F9` | Nền các cụm phân nhóm (subgraphs, boundaries) |
| `ink` | `#0F172A` | Tiêu đề, chữ chính của Node, viền khung quan trọng |
| `ink-muted` | `#64748B` | Sublabel kỹ thuật, chú thích, nhãn đường nối |
| `border-subtle` | `#E2E8F0` | Viền của các node thông thường, viền hộp bao |
| `border-strong` | `#94A3B8` | Viền node đang được trỏ hoặc nhóm cha |
| `accent` | `#EA580C` | Màu cam điểm nhấn (Focal node, cảnh báo, luồng chính) |
| `accent-subtle` | `#FFF7ED` | Nền của Focal node |
| `blue-accent` | `#0284C7` | Điểm nhấn thay thế cho hệ thống mạng/Cloud |
| `green-accent` | `#16A34A` | Điểm nhấn cho trạng thái Success, Output cuối |

## 2. Typography Rules

- **Instrument Serif** (Google Fonts): Dùng cho tiêu đề sơ đồ và các câu chú thích bên lề (*Callout annotations*).
- **Geist / Inter** (Sans-serif): Dùng cho tên Node, bước thực hiện trong quy trình. Trọng lượng `font-weight: 600` cho tên node, `font-weight: 400` cho mô tả.
- **Geist Mono / Fira Code** (Monospace): Dùng cho cổng kết nối (`:8080`), phương thức HTTP (`GET /api/v1`), kiểu dữ liệu (`UUID`, `VARCHAR`), mã lệnh.

## 3. Geometry & Grid Metrics (Lưới 4px)

- **Node Width**: `120px`, `140px`, `160px`, `180px`, `220px`
- **Node Height**: `60px`, `72px`, `80px`, `96px`
- **Border Radius**: `6px` hoặc `8px` (cho node), `12px` (cho container bao ngoài)
- **Padding**: `16px`, `24px`, `32px`
- **Line Width**: `1.0px` (đường nối phụ), `1.5px` (đường nối chính), `2.0px` (luồng dữ liệu trọng tâm)
- **Arrowhead Marker**: Chiều dài `6px`, chiều rộng `6px`, góc nhọn tinh tế.
