# Thiết kế v2: Dự án dịch sách đa cuốn, song ngữ, xuất PDF/EPUB

- **Ngày:** 2026-06-07
- **Bối cảnh:** Mở rộng dự án dịch (xem v1: `2026-06-07-ddia-translation-design.md`). Thay đổi lớn: (1) **nhiều sách**, (2) **song ngữ Anh-Việt** (để học tiếng Anh), (3) **xuất PDF + EPUB**.

## 1. Nguyên tắc nội dung

- **Bản dịch tiếng Việt** do mình tạo (tác phẩm phái sinh).
- **Phần tiếng Anh nguyên văn** được **script trích trực tiếp từ file nguồn của bạn** (EPUB sạch) — không sao chép thủ công cả cuốn sách. Bản song ngữ được lắp ráp **ngay trên máy bạn** từ cuốn sách bạn sở hữu.
- Glossary giữ nhất quán thuật ngữ.

## 2. Quyết định đã chốt

| Hạng mục | Lựa chọn |
|----------|----------|
| Đa sách | `books/<slug>/` mỗi sách một folder |
| Bố cục song ngữ | **Theo đoạn**: đoạn EN trên, đoạn VI (blockquote) ngay dưới |
| Nguồn tiếng Anh | **EPUB sạch của bạn** (`books/<slug>/source.epub`) → script tách đoạn |
| Thuật ngữ | Việt sạch; **tô đậm thuật ngữ khóa trong EN** (script tự tô theo glossary); bảng từ khóa cuối chương; `glossary.md` |
| Lắp ráp | `vi/` (mình dịch) + `en/` (script trích từ EPUB) → `merge` → `chapters/` (song ngữ) |
| Xuất bản | PDF (pandoc + xelatex + Noto) và EPUB (pandoc) |
| Công cụ | `pandoc 3.1.3`, `xelatex` (TeX Live 2023), `fonts-noto` — đã cài & xác minh |

## 3. Cấu trúc thư mục

```
translate_book/
├── README.md                  # trang chủ: danh mục sách + tiến độ
├── books/
│   └── ddia/
│       ├── meta.yaml          # metadata pandoc
│       ├── source.pdf         # PDF gốc
│       ├── source.epub        # EPUB gốc (bạn cung cấp) — nguồn tiếng Anh
│       ├── glossary.md        # glossary riêng sách
│       ├── en/chNN.md         # tiếng Anh sạch (script trích từ EPUB)
│       ├── vi/chNN.md         # bản dịch tiếng Việt (mình viết)
│       ├── chapters/chNN.md   # SONG NGỮ đã trộn (đầu vào build)
│       └── output/            # ddia-song-ngu.pdf / .epub
├── scripts/
│   ├── extract_epub.py        # extract_epub.py <slug> → tách chương EN từ EPUB
│   ├── merge_bilingual.py     # merge_bilingual.py <slug> <chNN> → trộn en+vi
│   └── build.sh               # build.sh <slug> → PDF + EPUB
├── templates/
│   ├── epub.css               # style EPUB (phân biệt EN/VI)
│   └── pdf-header.tex         # font Noto + style blockquote cho PDF
└── docs/superpowers/specs/
```

## 4. Quy ước file `en/` và `vi/` (để trộn được)

- Cả hai là Markdown, **cùng số khối, cùng thứ tự khối** (khối = phân tách bởi dòng trống).
- Khối heading: `en/` ghi tiêu đề EN, `vi/` ghi tiêu đề VI → merge tạo `## EN — VI`.
- Khối đoạn văn: nội dung tương ứng 1–1.
- Khối list / code / caption: tương ứng 1–1 (code xuất một lần).
- `merge_bilingual.py` **kiểm tra số khối khớp**; lệch thì báo lỗi để chỉnh `vi/` cho khớp `en/`.

## 5. Định dạng song ngữ (đầu ra `chapters/chNN.md`)

```markdown
## Reliability — Độ tin cậy

The things that can go wrong are called **faults**, and systems that
anticipate faults are called **fault-tolerant** or **resilient**.

> Những thứ có thể trục trặc được gọi là lỗi, và những hệ thống lường
> trước được lỗi được gọi là chịu lỗi hay kiên cường.

### 🔑 Từ khóa
| Term | Tiếng Việt | Ghi chú |
| fault | lỗi/trục trặc | một thành phần lệch chuẩn |
```
- Thuật ngữ khóa trong EN được **merge tự tô đậm** theo cột English của `glossary.md` (lần đầu/chương).
- References giữ nguyên gốc EN.

## 6. Xuất bản

`scripts/build.sh <slug>`:
- **EPUB:** `pandoc meta.yaml chapters/*.md -o output/<slug>-song-ngu.epub --toc --toc-depth=2 --css templates/epub.css --metadata lang=vi`
- **PDF:** `pandoc … --pdf-engine=xelatex --toc --toc-depth=2 -V documentclass=report -V mainfont="Noto Serif" -V monofont="Noto Sans Mono" -V lang=vi -V geometry:margin=2.5cm -H templates/pdf-header.tex`

## 7. Quy trình mỗi chương

1. `extract_epub.py ddia` → `en/chNN.md` (EN sạch từ EPUB).
2. Mình viết `vi/chNN.md` khớp khối với `en/chNN.md`.
3. `merge_bilingual.py ddia chNN` → `chapters/chNN.md`.
4. `build.sh ddia` → PDF + EPUB; kiểm tra mở được, tiếng Việt đúng.

## 8. Tiêu chí hoàn thành (pilot Ch.1)

- `chapters/ch01.md` song ngữ theo đoạn, thuật ngữ tô đậm, bảng từ khóa.
- `build.sh ddia` ra **PDF + EPUB** mở được, tiếng Việt hiển thị đúng.

## 9. Ngoài phạm vi hiện tại

- Dịch chương 2–12 và sách khác (làm dần).
- Nhúng ảnh hình vẽ (vẫn tham chiếu trang gốc); trang bìa nâng cao.
