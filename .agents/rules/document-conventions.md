# Document Conventions & Formatting Standards

Mục đích: Chuẩn hóa toàn diện hệ thống nhãn (labels), tham chiếu chéo (cross-referencing), bảng biểu, hình ảnh, công thức toán học và đường dẫn tương đối.

## 1. Quy chuẩn Tiền tố Nhãn (Label Prefix Conventions)
Mọi đối tượng tham chiếu trong tài liệu bắt buộc phải có tiền tố thống nhất:
- **Chương**: `\label{chap:intro}`, `\label{chap:methodology}`
- **Mục / Tiểu mục**: `\label{sec:system-architecture}`, `\label{subsec:data-preprocessing}`
- **Hình ảnh / Sơ đồ**: `\label{fig:network-diagram}`, `\label{fig:loss-curve}`
- **Bảng số liệu**: `\label{tab:hyperparameters}`, `\label{tab:benchmark-results}`
- **Công thức toán**: `\label{eq:cross-entropy}`, `\label{eq:attention-score}`
- **Thuật toán / Code**: `\label{alg:training-loop}`, `\label{lst:api-handler}`

## 2. Quy chuẩn Tham chiếu Chéo (Cross-Referencing)
- Luôn gọi tên loại đối tượng kèm lệnh tham chiếu và dùng dấu ngã `~` (non-breaking space) để tránh ngắt dòng:
  - *Hình*: `Hình~\ref{fig:loss-curve}` hoặc `Figure~\ref{fig:loss-curve}`
  - *Bảng*: `Bảng~\ref{tab:benchmark-results}` hoặc `Table~\ref{tab:benchmark-results}`
  - *Công thức*: `Phương trình~(\ref{eq:cross-entropy})` hoặc `Equation~\eqref{eq:cross-entropy}`
  - *Mục*: `Mục~\ref{sec:system-architecture}` hoặc `Section~\ref{sec:system-architecture}`
  - *Chương*: `Chương~\ref{chap:methodology}` hoặc `Chapter~\ref{chap:methodology}`

## 3. Quy chuẩn Bảng biểu (Tables)
- Bắt buộc sử dụng gói `booktabs` (`\toprule`, `\midrule`, `\bottomrule`).
- **Không** sử dụng đường kẻ dọc (`|`) trong bảng khoa học tiêu chuẩn.
- **Vị trí Caption**: `\caption{...}` bắt buộc đặt ở **TRÊN** bảng, ngay trước hoặc trong môi trường bảng, kèm `\label{tab:...}`.
- Căn lề: Căn phải cho số liệu, căn trái cho văn bản mô tả, căn giữa cho ký hiệu/trạng thái ngắn.

## 4. Quy chuẩn Hình ảnh & Sơ đồ (Figures & Diagrams)
- **Vị trí Caption**: `\caption{...}` bắt buộc đặt ở **DƯỚI** hình, kèm `\label{fig:...}`.
- **Đường dẫn**: Sử dụng đường dẫn tương đối từ gốc workspace (ví dụ: `figures/diagrams/architecture.pdf`, `figures/charts/accuracy_curve.pdf`).
- **Chất lượng**: Độ phân giải tối thiểu 300 DPI đối với ảnh raster (PNG/JPG), ưu tiên định dạng vector (PDF, SVG).
- Font chữ trong hình phải có kích thước tương đương font chữ văn bản chính (~10-12pt) khi hiển thị trên khổ A4.

## 5. Quy chuẩn Công thức Toán học (Math & Equations)
- Biến số đơn lẻ in nghiêng: `$x$`, `$y$`, `$w \in \mathbb{R}^d$`.
- Ma trận và vector in đậm: `\mathbf{W}`, `\mathbf{x}`, `\boldsymbol{\theta}`.
- Các hàm chuẩn viết dạng chữ đứng: `\sin`, `\log`, `\max`, `\exp` (không viết `$sin$`, `$log$`).
- Công thức quan trọng đứng riêng một dòng dùng môi trường `equation` để đánh số tự động và gắn `\label{eq:...}`.

## 6. Quy chuẩn Quản lý File & Nạp Module
- Sử dụng đường dẫn tương đối từ thư mục gốc dự án: `src/config/packages.tex`, `src/chapters/01-introduction.tex`.
- Không hardcode đường dẫn tuyệt đối của máy tính cá nhân vào bất kỳ file nào.
- **Validation bắt buộc**: Chạy `python scripts/validate_report.py` để phát hiện nhãn trùng lặp, tham chiếu gãy hoặc file hình ảnh bị thiếu.
