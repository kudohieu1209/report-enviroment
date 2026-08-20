# Citation Integrity & Anti-Hallucination Guidelines

Mục đích: Đảm bảo 100% tính chính xác, trung thực, có thể truy xuất nguồn gốc của mọi trích dẫn khoa học và tài liệu tham khảo trong toàn bộ báo cáo.

## 1. Nguyên tắc Chống Bịa đặt Tuyệt đối (Zero-Hallucination Policy)
- **Tuyệt đối không fabricate citation**:
  - Không tự tạo tên tác giả giả mạo hoặc gán ghép sai tác giả.
  - Không tự bịa mã định danh DOI, ISBN, ISSN, URL.
  - Không tự bịa năm xuất bản, tên tạp chí (`journal`), tên hội nghị (`booktitle`), hay số trang (`pages`).
- **Nguồn gốc có thể xác minh (Verifiable Provenance)**: Mọi trích dẫn (`\cite{...}`) bắt buộc phải truy ngược được về tài liệu đã thực sự đọc trong `docs/references/` hoặc nguồn online đã được xác thực chính xác.
- **Nguồn chưa kiểm chứng**: Nếu một tài liệu chưa được xác minh đầy đủ metadata, phải ghi chú rõ ràng `[Chưa xác minh]`, không được trích dẫn như một công trình khoa học đã được peer-reviewed.
- **Không suy diễn nội dung**: Khi trích dẫn một khẳng định từ bài báo X, phải đảm bảo bài báo X thực sự đưa ra kết luận hoặc số liệu đó.

## 2. Quản lý Cơ sở Dữ liệu Trích dẫn (`src/bibliography.bib`)
- **Single Source of Truth**: File `src/bibliography.bib` là nơi duy nhất quản lý các mục trích dẫn của dự án.
- **Bất biến Key Trích dẫn (Key Immutability)**: Citation key một khi đã được sử dụng trong văn bản (`\cite{key}`) thì **không được tùy tiện đổi tên**, tránh làm gãy các liên kết trong các chương khác.
- **Quy chuẩn Đặt tên Key**: Đặt theo định dạng `[Author][Year][Keyword]` (ví dụ: `vaswani2017attention`, `he2016deep`, `goodfellow2016deep`).

## 3. Quy chuẩn Metadata cho từng Loại Tài liệu
- `@article`: `author`, `title`, `journal`, `volume`, `number`, `pages`, `year`, `doi`.
- `@inproceedings`: `author`, `title`, `booktitle`, `pages`, `year`, `doi`.
- `@book`: `author` / `editor`, `title`, `publisher`, `year`, `isbn`.
- `@techreport` / `@misc`: `author` / `institution`, `title`, `year`, `url`, `urldate`.

## 4. Quy chuẩn Sử dụng Trích dẫn trong Văn bản
- Đặt dấu trích dẫn ngay sau nhận định hoặc cuối câu trước dấu chấm:
  - Đúng: `...đạt hiệu năng vượt trội \cite{vaswani2017attention}.`
  - Đúng (nhiều nguồn): `...được chứng minh trong nhiều nghiên cứu \cite{he2016deep, vaswani2017attention}.`
- Không sử dụng trích dẫn như một danh từ làm chủ ngữ trừ khi phong cách văn bản cho phép:
  - Tránh: `\cite{he2016deep} đã đề xuất mạng ResNet.`
  - Khuyến khích: `He và cộng sự \cite{he2016deep} đã đề xuất kiến trúc mạng ResNet...`
- **Validation bắt buộc**: Chạy `python scripts/validate_citations.py` trước mọi lần build hoặc bàn giao.
