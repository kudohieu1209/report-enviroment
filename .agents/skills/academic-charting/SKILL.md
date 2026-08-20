---
name: academic-charting
description: >-
  Tạo, định dạng và xuất các biểu đồ số liệu khoa học (Quantitative Data Visualization) như
  Loss/Accuracy curves, Bar charts, Scatter plots, Boxplots, Confusion matrices từ dữ liệu thực nghiệm,
  lưu vào figures/charts/. Phân biệt rõ với sơ đồ hệ thống (diagram-design).
---

# Academic Charting & Data Visualization Skill

Skill này chuyên trách về **trực quan hóa số liệu thực nghiệm và dữ liệu định lượng** (Data Visualization).

> [!NOTE]
> **Phân định Trách nhiệm**:
> - Sử dụng `academic-charting` khi cần vẽ: Đồ thị hàm số, biểu đồ cột/đường/phân tán so sánh hiệu năng, ma trận nhầm lẫn (Confusion matrix), kết quả benchmark, phân phối dữ liệu thống kê. Đầu ra lưu vào `figures/charts/`.
> - **KHÔNG** dùng skill này để vẽ sơ đồ kiến trúc hệ thống, lưu đồ quy trình hay ERD $\rightarrow$ Dùng `diagram-design`.

---

## 1. Tiêu chuẩn Biểu đồ Khoa học
- **Đầu ra Mặc định**: Lưu vào `figures/charts/<chart_name>.pdf` (vector) và `figures/charts/<chart_name>.png` (raster $\ge 300\text{ DPI}$).
- **Bảng màu (Color Palette)**: Sử dụng các bảng màu chuyên dụng trong nghiên cứu khoa học:
  - Bảng màu phân biệt (Qualitative): `deep`, `muted`, `Set2`, `Dark2`.
  - Thân thiện với người mù màu (Colorblind-safe): `viridis`, `cividis`, `mako`.
- **Kích thước & Typography**:
  - Trục tọa độ (X-axis, Y-axis) phải có nhãn rõ ràng kèm đơn vị đo lường trong ngoặc vuông: ví dụ `Thời gian phản hồi [ms]`, `Độ chính xác [%]`.
  - Cỡ chữ nhãn trục và chú giải (Legend) phải tương đương cỡ chữ văn bản chính (~10-12pt) khi đưa vào trang A4.
  - Lưới phụ (Grid lines) mờ nét đứt (`alpha=0.5`, `linestyle='--'`).

---

## 2. Quy trình Thực hiện Chuẩn

1. **Chuẩn bị Dữ liệu**: Dữ liệu từ file CSV, JSON hoặc số liệu thực nghiệm do người dùng cung cấp.
2. **Viết Script Tạo Biểu đồ**: Viết code Python vào `scripts/render_chart.py` hoặc script chuyên biệt.
3. **Thực thi Script**: Chạy script để xuất file ảnh vào `figures/charts/`.
4. **Nhúng vào Tài liệu**: Chèn vào chương tương ứng trong `src/chapters/`:
   ```latex
   \begin{figure}[htbp]
       \centering
       \includegraphics[width=0.8\textwidth]{figures/charts/accuracy_curve.pdf}
       \caption{Đồ thị độ chính xác qua các epoch huấn luyện}
       \label{fig:accuracy-curve}
   \end{figure}
   ```
5. **Kiểm tra**: Chạy `python scripts/validate_report.py` để đảm bảo file ảnh tồn tại và nhãn `\label` hợp lệ.
