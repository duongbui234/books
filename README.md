# Dự án dịch sách song ngữ Anh–Việt

Dịch sách kỹ thuật sang **song ngữ Anh–Việt** (để vừa đọc vừa học tiếng Anh), xuất ra **PDF + EPUB**. Hỗ trợ **nhiều sách**.

- Bản dịch tiếng Việt do mình (Claude) thực hiện.
- Phần tiếng Anh được **script trích trực tiếp từ file EPUB gốc của bạn** rồi ghép với bản dịch — không sao chép thủ công.

## Cấu trúc

```
books/<slug>/
├── meta.yaml         # metadata cho pandoc (tên sách, tác giả…)
├── source.pdf        # bản gốc PDF
├── source.epub       # bản gốc EPUB (nguồn tiếng Anh để trích)
├── glossary.md       # bảng thuật ngữ Anh→Việt (nhất quán cả sách)
├── en/chNN.md        # tiếng Anh sạch (script trích từ EPUB)
├── vi/chNN.md        # bản dịch tiếng Việt (căn khối với en/)
├── chapters/chNN.md  # SONG NGỮ đã trộn (đầu vào build)
└── output/           # chNN…-song-ngu.pdf / .epub
scripts/   extract_epub.py · merge_bilingual.py · build.sh
templates/ epub.css · pdf-header.tex
docs/superpowers/specs/  # tài liệu thiết kế
```

## Quy trình dịch một chương

```bash
# 1. Trích tiếng Anh từ EPUB (xem tên file html trong EPUB: unzip -l source.epub)
python3 scripts/extract_epub.py ddia OEBPS/ch01.html ch01
# 2. (Claude viết) vi/ch01.md khớp từng khối với en/ch01.md
# 3. Trộn song ngữ
python3 scripts/merge_bilingual.py ddia ch01      # thêm --plan để xem cấu trúc khối
# 4. Build PDF + EPUB
bash scripts/build.sh ddia
```

## Thêm sách mới

Tạo `books/<slug>/` với `source.epub`, `source.pdf`, `meta.yaml`, `glossary.md` rồi lặp quy trình trên. Không ảnh hưởng các sách cũ.

## Định dạng song ngữ

Đoạn tiếng Anh (tô đậm thuật ngữ khóa) → bản dịch tiếng Việt ngay dưới (blockquote). References/Footnotes giữ nguyên tiếng Anh. Xem thiết kế đầy đủ: [docs/superpowers/specs/2026-06-07-multibook-bilingual-publishing-design.md](docs/superpowers/specs/2026-06-07-multibook-bilingual-publishing-design.md).

## Tiến độ

### 📕 Designing Data-Intensive Applications (`books/ddia/`)

| # | Chương | Song ngữ | Ghi chú |
|---|--------|:--------:|---------|
| 1 | Reliable, Scalable & Maintainable Applications | ✅ | đã build PDF+EPUB |
| 2 | Data Models & Query Languages | ✅ | đã build PDF+EPUB |
| 3 | Storage & Retrieval | ✅ | đã build PDF+EPUB |
| 4 | Encoding & Evolution | ✅ | đã build PDF+EPUB |
| 5 | Replication | ✅ | đã build PDF+EPUB |
| 6 | Partitioning | ✅ | đã build PDF+EPUB |
| 7 | Transactions | ✅ | đã build PDF+EPUB |
| 8 | The Trouble with Distributed Systems | ✅ | đã build PDF+EPUB |
| 9 | Consistency & Consensus | ✅ | đã build PDF+EPUB |
| 10 | Batch Processing | ✅ | đã build PDF+EPUB |
| 11 | Stream Processing | ✅ | đã build PDF+EPUB |
| 12 | The Future of Data Systems | ✅ | đã build PDF+EPUB |

**Hoàn thành: 12/12 chương** 🎉 · Đầu ra: `books/ddia/output/ddia-song-ngu.{pdf,epub}`

### 📘 System Design Interview – An Insider's Guide (`books/system-design/`)

Nguồn chỉ có PDF (không EPUB) → trích bằng `scripts/extract_pdf.py` (giữ cả **hình vẽ**, 225 ảnh). Chỉ xuất **PDF** (không EPUB).

**Hoàn thành: 18/18 phần** 🎉 (Forward + 16 chương + Afterword) · 378 trang · Đầu ra: `books/system-design/output/system-design-song-ngu.pdf`
