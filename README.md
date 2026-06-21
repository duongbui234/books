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

### 📗 Grokking the System Design Interview (`books/grokking/`)

Nguồn chỉ có PDF (196 trang). Trích bằng `scripts/extract_pdf.py` với cờ mới cho sách có **heading không in đậm** (phân biệt bằng cỡ chữ + font): `--head-size 24 --head-no-bold --title-family Calibri-Light`. Giữ cả **hình vẽ** (114 ảnh). Chỉ xuất **PDF**.

**Hoàn thành: 18/18 chương** 🎉 (16 bài toán thiết kế: TinyURL, Pastebin, Instagram, Dropbox, Messenger, Twitter, YouTube, Typeahead, Rate Limiter, Twitter Search, Web Crawler, Newsfeed, Yelp, Uber, Ticketmaster + 2 chương System Design Basics) · 319 trang · Đầu ra: `books/grokking/output/grokking-song-ngu.pdf`

### 📙 The Pragmatic Programmer, 20th Anniversary Ed. (`books/pragmatic-programmer/`)

Nguồn chỉ có PDF (497 trang), **layout đa cột + trích dẫn lề** → extractor cũ không dùng được. Viết extractor riêng `scripts/extract_pp.py` (pdftohtml XML: tách epigraph theo màu teal, nhận heading theo **font family** LiberationSans/TrebuchetMS, nhận hộp **Tip N**, tách file theo từng Topic). Bỏ hình raster, giữ code+bảng. Chỉ xuất **PDF**.

**Hoàn thành: 57/57 Topic** 🎉 (9 chương + Front matter + Postface + Bibliography + Possible Answers) · 416 trang · Đầu ra: `books/pragmatic-programmer/output/pragmatic-programmer-song-ngu.pdf`

### 📕 Building Microservices (`books/building-microservices/`)

Nguồn chỉ có PDF — **Designing Fine-Grained Systems, Second Edition** (Sam Newman, O'Reilly 2021). Trích bằng `scripts/extract_pdf.py` (giữ hình vẽ). Chỉ xuất **PDF**.

**Hoàn thành: 18/18 chương** 🎉 · 882 trang · Đầu ra: `books/building-microservices/output/building-microservices-song-ngu.pdf`

### 📗 Database Internals (`books/database-internals/`)

Nguồn chỉ có PDF — **A Deep Dive into How Distributed Data Systems Work** (Alex Petrov). Trích bằng `scripts/extract_pdf.py` (giữ hình vẽ). Chỉ xuất **PDF**.

**Hoàn thành: 18/19 chương** ⏳ (thiếu ch18 ở bản dịch tiếng Việt) · 489 trang · Đầu ra: `books/database-internals/output/database-internals-song-ngu.pdf`

### 📘 Designing Distributed Systems (`books/designing-distributed-system/`)

Nguồn chỉ có PDF — **Patterns and Paradigms for Scalable, Reliable Services** (Brendan Burns). Trích bằng `scripts/extract_pdf.py` (giữ hình vẽ). Chỉ xuất **PDF**.

**Hoàn thành: 14/14 chương** 🎉 · 219 trang · Đầu ra: `books/designing-distributed-system/output/designing-distributed-system-song-ngu.pdf`

### 📙 Fundamentals of Data Engineering (`books/fundamentals-of-data-engineer/`)

Nguồn chỉ có PDF — **Plan and Build Robust Data Systems** (Joe Reis & Matt Housley). Trích bằng `scripts/extract_pdf.py` (giữ hình vẽ). Chỉ xuất **PDF**.

**Hoàn thành: 14/14 chương** 🎉 · 571 trang · Đầu ra: `books/fundamentals-of-data-engineer/output/fundamentals-of-data-engineer-song-ngu.pdf`

### 📒 Node.js Design Patterns (`books/nodejs-design-patterns/`)

Nguồn chỉ có PDF — **Third Edition** (Mario Casciaro & Luciano Mammino). Trích bằng `scripts/extract_pdf.py` (giữ hình vẽ). Chỉ xuất **PDF**.

**Hoàn thành: 14/14 chương** 🎉 · 700 trang · Đầu ra: `books/nodejs-design-patterns/output/nodejs-design-patterns-song-ngu.pdf`
