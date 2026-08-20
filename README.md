# 📚 Môi trường Soạn thảo Báo cáo & Tài liệu Học thuật (Master Template v1.0)

Môi trường làm việc chuẩn mực (**Master Template**) chuyên dụng cho việc nghiên cứu, soạn thảo, quản lý trích dẫn và xuất bản các báo cáo kỹ thuật, báo cáo thực tập, luận văn và bài báo khoa học.

Tích hợp sẵn hệ thống **Antigravity Custom Skills & Rules** giúp tối ưu hóa khả năng hỗ trợ của AI Agent ở mức độ cao nhất.

---

## 💡 Nguyên tắc Sử dụng Master Template

> [!IMPORTANT]
> Thư mục `report-environment/` là **Master Template gốc**. Tuyệt đối **không viết báo cáo thật trực tiếp** trong thư mục này.
> 
> Khi bắt đầu một đề tài / bài báo cáo mới:
> 1. **Copy / Clone** toàn bộ thư mục `report-environment/` sang một thư mục dự án mới (ví dụ: `internship-techpal/` hoặc `thesis-deeplearning/`).
> 2. Đặt các tài liệu đề bài, quy định trình bày vào `docs/references/guidelines/`, báo cáo mẫu vào `docs/references/sample-reports/`, và các bài báo tham khảo vào `docs/references/papers/`.
> 3. **Câu lệnh đầu tiên cho AI Agent**:
>    > *"Phân tích toàn bộ tài liệu đầu vào và lập Requirement Matrix. Chưa viết báo cáo."*

---

## 📂 Cấu trúc Thư mục

```text
report-environment/
│
├── .agents/                      # Cấu hình trí tuệ nhân tạo (Antigravity Agent)
│   ├── rules/                    # Các quy tắc bắt buộc Agent phải tuân thủ
│   │   ├── academic-style.md     # Văn phong học thuật, quy chuẩn ngôn ngữ
│   │   ├── citation-integrity.md # Nguyên tắc chống bịa trích dẫn (Zero-Hallucination)
│   │   └── document-conventions.md # Quy chuẩn đặt nhãn, bảng biểu, công thức
│   └── skills/                   # Bộ kỹ năng tự động hóa theo từng giai đoạn
│       ├── document-analysis/    # Đọc hiểu guideline, lập Requirement Matrix
│       ├── academic-writing/     # Soạn thảo linh hoạt (Paper, Internship, Technical)
│       ├── literature-synthesis/ # Tổng hợp đa nguồn, ma trận tài liệu
│       ├── citation-bibtex/      # Quản lý & kiểm tra file .bib
│       ├── academic-charting/    # Vẽ biểu đồ khoa học số liệu (Loss, Bar, Plot)
│       ├── diagram-design/       # Vẽ 38 loại sơ đồ kiến trúc/quy trình Editorial SVG
│       ├── document-compiler/    # Quy trình biên dịch PDF/DOCX
│       └── peer-review-audit/    # Phản biện, soát lỗi toàn diện
│
├── docs/                         # Tài liệu phục vụ nghiên cứu & phác thảo
│   ├── references/               # Tài liệu tham khảo gốc
│   │   ├── guidelines/           # Quy định trình bày của trường / cơ quan (Ưu tiên số 1)
│   │   ├── papers/               # Các bài báo khoa học (PDF)
│   │   └── sample-reports/       # Các bài báo cáo mẫu để học hỏi (Chỉ tham khảo)
│   ├── notes/                    # Ghi chú, ma trận tổng hợp tài liệu, Requirement Matrix
│   └── drafts/                   # Bản nháp thô trước khi đưa vào mã nguồn
│
├── src/                          # Mã nguồn chính của tài liệu (LaTeX / Typst)
│   ├── main.tex                  # File điều phối chính
│   ├── bibliography.bib          # Cơ sở dữ liệu trích dẫn BibTeX sạch
│   ├── config/                   # Cấu hình gói lệnh, macro, metadata
│   │   ├── packages.tex
│   │   ├── macros.tex
│   │   └── metadata.tex
│   └── chapters/                 # Các chương nội dung dạng template sạch
│       ├── 01-introduction.tex
│       ├── 02-company-overview.tex
│       ├── 03-work-performed.tex
│       ├── 04-results.tex
│       └── 05-conclusion.tex
│
├── figures/                      # Hình ảnh & Đồ thị
│   ├── diagrams/                 # Sơ đồ kiến trúc, luồng hoạt động
│   ├── charts/                   # Biểu đồ số liệu thực nghiệm
│   ├── screenshots/              # Ảnh chụp màn hình hệ thống
│   └── images/                   # Hình ảnh minh họa khác
│
├── templates/                    # Các mẫu thiết kế có thể tái sử dụng
│   ├── cover/                    # Mẫu trang bìa đẹp
│   ├── tables/                   # Mẫu bảng so sánh số liệu
│   └── report/                   # Mẫu khung báo cáo dự phòng
│
├── tests/                        # Bộ kiểm thử độc lập (Không làm bẩn src/ & figures/)
│   ├── fixtures/                 # File dữ liệu mẫu cho test (test.bib)
│   ├── smoke/                    # Script chạy test tự động (test_smoke.py)
│   └── outputs/                  # Đầu ra của quá trình chạy test
│
├── scripts/                      # Bộ công cụ tự động hóa (Python)
│   ├── build.py                  # Tự động biên dịch PDF
│   ├── validate_citations.py     # Quét & đối chiếu trích dẫn 100%
│   ├── validate_report.py        # Kiểm tra nhãn trùng, tham chiếu gãy
│   └── render_chart.py           # Script mẫu vẽ biểu đồ chuẩn khoa học
│
├── output/                       # Thư mục chứa file PDF/DOCX thành phẩm
├── README.md                     # Hướng dẫn sử dụng môi trường
└── .gitignore                    # Bỏ qua file rác của LaTeX & Python
```

---

## 🔄 Chu trình Hoàn thiện Tài liệu (Canonical Workflow)

Khi thực hiện một báo cáo, Agent và người dùng phối hợp theo pipeline chuẩn:

```text
1. Thu thập & Phân tích tài liệu đầu vào (document-analysis)
   ↓ Tạo docs/notes/requirement_matrix.md
2. Tổng hợp tài liệu & Nghiên cứu liên quan (literature-synthesis & citation-bibtex)
   ↓ Lập docs/notes/synthesis_matrix.md & nạp src/bibliography.bib
3. Soạn thảo bản nháp (academic-writing, academic-charting, diagram-design)
   ↓ Soạn thảo src/chapters/*.tex & sinh figures/
4. Kiểm tra toàn vẹn kỹ thuật (Validation)
   ↓ Chạy scripts/validate_citations.py & scripts/validate_report.py
5. Biên dịch bản xem trước (Build preview)
   ↓ Chạy scripts/build.py ra output/report.pdf
6. Rà soát & Phản biện độc lập (peer-review-audit)
   ↓ Xuất docs/notes/peer_review_report.md & danh sách Action Items
7. Sửa đổi & Khắc phục (Refine & Fix)
   ↓ Sửa đổi các mục cần hoàn thiện trong src/
8. Kiểm tra lại lần cuối & Xuất bản chính thức (Final Validation & Final Build)
   ↓ Xuất bản bản nộp chính thức tại output/report.pdf
```

---

## 🛠️ Bộ Lệnh Command Line

```powershell
# 1. Chạy toàn bộ Smoke Test Suite tự động (9/9 test cases độc lập)
python tests/smoke/test_smoke.py

# 2. Kiểm tra tính toàn vẹn của trích dẫn BibTeX
python scripts/validate_citations.py
python scripts/validate_citations.py --strict  # Cho bản nộp cuối

# 3. Kiểm tra nhãn, tham chiếu gãy, ảnh thiếu và TODOs trong báo cáo
python scripts/validate_report.py
python scripts/validate_report.py --strict     # Cho bản nộp cuối

# 4. Biên dịch báo cáo ra PDF (Lưu tại output/report.pdf)
python scripts/build.py
```

---

## ⚙️ Yêu cầu Hệ thống & Định dạng Đầu ra
- **Định dạng Đầu ra**:
  - **PDF (Canonical / Chuẩn mực)**: Đầu ra chính thức được biên dịch từ `src/main.tex` qua MiKTeX/TeX Live.
  - **DOCX (Tùy chọn / Thử nghiệm)**: Hỗ trợ chuyển đổi qua Pandoc (`pandoc src/main.tex -o output/report.docx --citeproc`) nếu có cài đặt Pandoc.
- **Python 3.8+**: Các thư viện phục vụ vẽ đồ thị và trích xuất tài liệu (`pip install matplotlib seaborn pandas numpy pypdf`).
- **LaTeX Distribution** *(để build PDF từ .tex)*: [MiKTeX](https://miktex.org/) hoặc [TeX Live](https://www.tug.org/texlive/) (hỗ trợ Biber và gói tiếng Việt vntex/T5).
