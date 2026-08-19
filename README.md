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

**Hoàn thành: 57/57 Topic** 🎉 (9 chương + Front matter + Postface + Bibliography + Possible Answers) · 3.658 khối song ngữ · Đầu ra: `books/pragmatic-programmer/output/pragmatic-programmer-song-ngu.pdf`

> 🔧 **Đã vá lỗi xếp sai thứ tự chữ.** `extract_pp.py` vốn không gom dòng, chỉ `sorted(body, key=top)`, nên mọi run lệch baseline vài px bị xếp theo chiều dọc thay vì trái→phải: từ khoá trong code nhảy chỗ (`def calculate_account_fees(account)` → `calculate_account_fees(account) def`), chỉ số chú thích `[n]` dời sang câu khác, chữ Hy Lạp bị đẩy xuống cuối đoạn. Nặng nhất: nhãn `Tip N` nằm cùng dòng với tiêu đề (lệch 2px) nên ra SAU tiêu đề, khiến **49/100 Tip mất định dạng**, biến thành `###` thường. Sau khi vá: 221 → 5 chỗ nghi vấn (đều là dương tính giả), **100/100 Tip đúng**. Giữ lại 3.222/3.658 khối bản dịch cũ, chỉ dịch bù 436 khối.

> ⚠️ Còn tồn: `extract_pp.py` xuất code thành đoạn văn thường (không bọc ```), nên bản song ngữ lặp lại đoạn code hai lần (bản thường + blockquote). Lỗi có sẵn từ trước, chưa sửa.

### 📕 Building Microservices (`books/building-microservices/`)

Nguồn chỉ có PDF — **Designing Fine-Grained Systems, Second Edition** (Sam Newman, O'Reilly 2021). Trích bằng `scripts/extract_pdf.py` (giữ hình vẽ). Chỉ xuất **PDF**.

**Hoàn thành: 18/18 chương** 🎉 · 882 trang · Đầu ra: `books/building-microservices/output/building-microservices-song-ngu.pdf`

### 📗 Database Internals (`books/database-internals/`)

Nguồn chỉ có PDF — **A Deep Dive into How Distributed Data Systems Work** (Alex Petrov). Trích bằng `scripts/extract_pdf.py` (giữ hình vẽ). Chỉ xuất **PDF**.

**Hoàn thành: 19/19 phần** 🎉 · 2.540 khối song ngữ · Đầu ra: `books/database-internals/output/database-internals-song-ngu.pdf`

> 🔧 **Đã vá lỗi mất chỉ số dưới (subscript).** `LINE_TOL = 6` quá chặt với cách dàn trang của sách này: dòng chữ ở top 193–196 còn subscript ở top 203 (lệch 7–10px), nên subscript rơi khỏi nhóm dòng, thành "khối code một từ" rồi bị bộ lọc nhiễu xoá. Hậu quả: `T₁ and T₂ read the value of V` bị trích thành `T and T read the value of V` — mất nghĩa hoàn toàn ở sách dùng ký hiệu toán dày đặc. Trích lại với `--line-tol 8` (dòng kế tiếp cách 19px nên 8 an toàn cả hai phía): **+103 token subscript khôi phục**, −38 token là số trang/running header mà bộ lọc header-footer (thêm vào pipeline SAU khi cuốn này được trích lần đầu) nay dọn sạch. Giữ 2.448/2.540 khối bản dịch cũ, dịch bù 92 khối.

> ℹ️ Lỗi này KHÔNG phát hiện được khi audit ở tolerance 6 — vì chính tolerance 6 là nguyên nhân. Phải quét ở tolerance rộng hơn mới lộ ra.

### 📘 Designing Distributed Systems (`books/designing-distributed-system/`)

Nguồn chỉ có PDF — **Patterns and Paradigms for Scalable, Reliable Services** (Brendan Burns). Trích bằng `scripts/extract_pdf.py` (giữ hình vẽ). Chỉ xuất **PDF**.

**Hoàn thành: 14/14 chương** 🎉 · 219 trang · Đầu ra: `books/designing-distributed-system/output/designing-distributed-system-song-ngu.pdf`

### 📙 Fundamentals of Data Engineering (`books/fundamentals-of-data-engineer/`)

Nguồn chỉ có PDF — **Plan and Build Robust Data Systems** (Joe Reis & Matt Housley). Trích bằng `scripts/extract_pdf.py` (giữ hình vẽ). Chỉ xuất **PDF**.

**Hoàn thành: 14/14 chương** 🎉 · 571 trang · Đầu ra: `books/fundamentals-of-data-engineer/output/fundamentals-of-data-engineer-song-ngu.pdf`

### 📒 Node.js Design Patterns (`books/nodejs-design-patterns/`)

Nguồn chỉ có PDF — **Third Edition** (Mario Casciaro & Luciano Mammino). Trích bằng `scripts/extract_pdf.py` (giữ hình vẽ). Chỉ xuất **PDF**.

**Hoàn thành: 14/14 chương** 🎉 · 700 trang · Đầu ra: `books/nodejs-design-patterns/output/nodejs-design-patterns-song-ngu.pdf`

### 📓 Clean Code, Second Edition (`books/clean-code/`)

Nguồn chỉ có PDF — **A Handbook of Agile Software Craftsmanship, 2nd Edition** (Robert C. Martin, Addison-Wesley 2025, bản *Early Release*). PDF do calibre xuất nên **toàn sách chỉ dùng một font family** (DejaVuSans) → không phân biệt heading bằng font được như `extract_pp.py`, phải dựa vào **cỡ chữ + in đậm**: `--head-size 26 --code-family Mono --gap-para 30 --gap-line 40`. Giữ cả hình vẽ (122 ảnh). Chỉ xuất **PDF**.

Năm cải tiến cho `scripts/extract_pdf.py` từ sách này: trải phẳng **ligature** (`ﬁ ﬀ ﬂ` → `fi ff fl`), nối **tiêu đề chương bị xuống dòng**, nhận đúng cấp heading cho `Part / Appendix / Bibliography / Introduction` (sửa luôn typo `FORWARD` → `FOREWORD`), gom các đoạn chữ cùng dòng theo **chuỗi** thay vì so với run đầu tiên (cờ mới `--line-tol`), và nhận **dấu đầu dòng đứng riêng một run** là đầu mục danh sách.

> ⚠️ Hai sửa đổi cuối là lỗi **mất nội dung**, không phải lỗi thẩm mỹ: khi một dòng có chữ mono lệch baseline (vd `▪ Shape.java does not need to change.`), run mono rớt khỏi nhóm dòng, bị coi là "khối code một từ" rồi bị bộ lọc nhiễu xoá hẳn — tên file/class biến mất khỏi bản tiếng Anh. Ảnh hưởng 25/42 chương.

Thêm `scripts/slice_blocks.py`: chia thân chương thành lát ≤120 khối có **dấu mốc `⟦n⟧`**, cho phép nhiều agent dịch song song một chương mà vẫn bắt được lệch khối **đúng tại vị trí** (thay vì chỉ báo lệch tổng số như `merge_bilingual.py`).

**Hoàn thành: 42/42 phần** 🎉 (Foreword + Introduction + 37 chương + 4 trang Part + Afterword + Appendix + Bibliography) · 5.257 khối song ngữ · Đầu ra: `books/clean-code/output/clean-code-song-ngu.pdf`

### 📔 Clean Architecture (`books/clean-architecture/`)

Nguồn chỉ có PDF — **A Craftsman's Guide to Software Structure and Design** (Robert C. Martin, Pearson 2018), 429 trang, dàn trang InDesign. Cuốn này cần **extractor riêng** `scripts/extract_ca.py` vì bốn đặc điểm mà `extract_pdf.py` không xử lý được:

1. **Chrome phân biệt bằng MÀU, không bằng vị trí** — running header và số trang đều `#a7a9ab`, watermark `www.EBooksWorld.ir` màu `#d4d4d4`. Số trang nằm ở 86% chiều cao nên bộ lọc footer theo vị trí (>92%) không bắt được.
2. **Heading bị InDesign giãn chữ** — xuất ra thành `Wh at  I s  D e s ig n`. `despace()` dựa vào quy luật *1 dấu cách = trong từ, ≥2 = giữa hai từ* để dựng lại `What Is Design`.
3. **97 hình đều là VECTOR** — `pdftohtml -xml` trả về **0** `<image>` cho cả cuốn. Phải xác định dải dọc chứa hình (từ đáy đoạn văn tới dòng `Figure N.M`) rồi render bằng `pdftoppm` + xén lề bằng Pillow. Lưu ý: `pdftohtml -xml` **luôn** dựng trang ở 108 DPI cố định (1188 đơn vị = 792pt), nên tỉ lệ là `DPI/108` — KHÔNG suy từ `pdfinfo` vì sách có nhiều khổ trang.
4. **XML của poppler có byte hỏng** (byte `0x84` trong một href ở trang 429) làm `ET.parse` ném lỗi → đọc bytes rồi `decode(errors="replace")`.

Tham số chọn theo **đo đạc thực tế** chứ không đoán: phân bố lệch baseline lưỡng cực rõ — trong cùng dòng 1–6px, giữa hai dòng ≥13px (đỉnh 21px) — nên `LINE_TOL = 9` an toàn cả hai phía.

**Hoàn thành: 43/43 phần** 🎉 (Front matter + 34 chương + 7 trang Part + Appendix A) · 2.467 khối song ngữ · 97 hình · 397 trang · Đầu ra: `books/clean-architecture/output/clean-architecture-song-ngu.pdf`

> ✅ **Đã qua vòng soát đối kháng.** 8 cụm chương × 4 lăng kính độc lập (đúng nghĩa · thuật ngữ · thiếu nội dung · văn phong) sinh 278 phát hiện; mỗi phát hiện bị một agent khác cố bác bỏ → 145 sống sót, gộp trùng còn 84 khối. Bắt được các lỗi một lượt soát đơn hay bỏ qua: `straightforward` → "thẳng thắn", `idealistic` → "duy tâm", `resistance` → "trở kháng", `sump pump` → "máy bơm hố ga", thành ngữ `I've been known to` và `heartburn` bị dịch nghĩa đen, mất lượng từ trong `not all substitutable`, và hai tiêu đề chương bỏ quên chưa dịch.
