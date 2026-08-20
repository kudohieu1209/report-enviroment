---
name: citation-bibtex
description: >-
  Quản lý cơ sở dữ liệu trích dẫn BibTeX (src/bibliography.bib),
  chuẩn hóa các mục trích dẫn, kiểm tra tính toàn vẹn và định dạng theo các chuẩn học thuật (IEEE, APA, Harvard).
---

# Citation & BibTeX Management Skill

Skill này hướng dẫn quy trình tạo, cập nhật, chuẩn hóa và kiểm tra chéo file `src/bibliography.bib`.

## 1. Cấu trúc Mẫu các Mục BibTeX Chuẩn

### Bài báo Tạp chí (Journal Article)
```bibtex
@article{vaswani2017attention,
  author    = {Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N and Kaiser, {\L}ukasz and Polosukhin, Illia},
  title     = {Attention is All You Need},
  journal   = {Advances in Neural Information Processing Systems},
  volume    = {30},
  pages     = {5998--6008},
  year      = {2017},
  doi       = {10.48550/arXiv.1706.03762}
}
```

### Kỷ yếu Hội nghị (Conference Proceedings)
```bibtex
@inproceedings{he2016deep,
  author    = {He, Kaiming and Zhang, Xiangyu and Ren, Shaoqing and Sun, Jian},
  title     = {Deep Residual Learning for Image Recognition},
  booktitle = {Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages     = {770--778},
  year      = {2016},
  doi       = {10.1109/CVPR.2016.90}
}
```

### Sách (Book)
```bibtex
@book{goodfellow2016deep,
  author    = {Goodfellow, Ian and Bengio, Yoshua and Courville, Aaron},
  title     = {Deep Learning},
  publisher = {MIT Press},
  year      = {2016},
  isbn      = {978-0262035613}
}
```

### Báo cáo Kỹ thuật / Tài liệu Online / Website (Tech Report / Misc)
```bibtex
@techreport{iso25010,
  author      = {{ISO/IEC}},
  title       = {Systems and software engineering -- Systems and software Quality Requirements and Evaluation (SQuaRE) -- System and software quality models},
  institution = {International Organization for Standardization},
  number      = {ISO/IEC 25010:2011},
  year        = {2011}
}
```

## 2. Quy trình Kiểm tra Toàn vẹn Trích dẫn (Citation Validation)
1. **Kiểm tra thiếu mục**: Mọi `\cite{key}` trong thư mục `src/chapters/` phải có `@type{key, ...}` trong `src/bibliography.bib`.
2. **Kiểm tra mục thừa (Unused entries)**: Phát hiện các mục có trong `.bib` nhưng không bao giờ được trích dẫn trong văn bản.
3. **Chạy script kiểm tra tự động**:
   ```console
   python scripts/validate_citations.py
   ```
