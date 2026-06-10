# Thiết kế dự án: Dịch "Designing Data-Intensive Applications" sang tiếng Việt

- **Ngày:** 2026-06-07
- **Nguồn:** `Designing Data Intensive Applications by Martin Kleppmann.pdf` — 613 trang, PDF có text trích xuất được (không phải scan ảnh).
- **Bản:** 1st edition (2017, Martin Kleppmann). *Lưu ý:* không phải 2nd edition (2nd vẫn đang ở dạng Early Release).
- **Mục đích:** Dịch phục vụ học tập cá nhân.

## 1. Quyết định đã chốt

| Hạng mục | Lựa chọn |
|----------|----------|
| Phạm vi khởi đầu | **Pilot Chương 1** trước, duyệt xong mới dịch tiếp |
| Thuật ngữ kỹ thuật | **Song ngữ** — lần đầu ghi `tiếng Việt (english term)`, sau đó dùng tiếng Việt nhất quán theo glossary |
| Định dạng đầu ra | **Markdown thuần tiếng Việt**, mỗi chương một file |
| Cách làm | **Glossary-first** (Cách A): vừa dịch vừa dựng bảng thuật ngữ |

## 2. Cấu trúc thư mục

```
translate_book/
├── Designing Data Intensive Applications by Martin Kleppmann.pdf   ← nguồn
├── README.md          ← tổng quan dự án + bảng theo dõi tiến độ 12 chương
├── glossary.md        ← bảng thuật ngữ Anh→Việt (xương sống giữ nhất quán toàn sách)
├── raw/               ← text tiếng Anh trích từ PDF (trung gian, để đối chiếu khi rà soát)
│   └── ch01.txt
└── vi/                ← bản dịch tiếng Việt (đầu ra)
    └── ch01-ung-dung-tin-cay-kha-mo-rong-de-bao-tri.md
```

## 3. Quy ước định dạng

- **Tiêu đề:** giữ đúng cấp heading (`#` cho tên chương, `##`/`###` cho mục/tiểu mục).
- **Thuật ngữ:** lần đầu xuất hiện trong mỗi chương ghi `tiếng Việt (english term)`; các lần sau dùng tiếng Việt nhất quán theo `glossary.md`. Thuật ngữ quá phổ biến có thể giữ nguyên tiếng Anh (ghi rõ trong glossary).
- **Hình vẽ (figures):** dịch chú thích, render dạng `> **Hình 1-1.** <nội dung chú thích>` kèm ghi chú `(xem hình gốc trong PDF, trang in N)`. *Tùy chọn (quyết định sau):* render trang PDF ra ảnh PNG và nhúng để file tự chứa hình.
- **Code / listing:** giữ nguyên trong khối ` ``` `; chỉ dịch comment khi có ích cho người đọc.
- **Chú thích / tham chiếu (footnotes):** giữ **nguyên gốc tiếng Anh** tên paper/sách/tác giả/URL; chỉ dịch phần diễn giải (nếu có).
- **Bảng:** dịch nội dung, giữ cấu trúc bảng Markdown.
- **Box "Note/Warning" hoặc sidebar:** render thành blockquote (`>`).
- **Thuật ngữ cần phân biệt cẩn thận:** ví dụ *fault* (lỗi/trục trặc của một thành phần) vs *failure* (sự cố khiến cả hệ thống ngừng phục vụ) — phải dịch nhất quán và ghi rõ trong glossary.

## 4. Glossary khởi đầu (sẽ mở rộng dần)

Cột trong `glossary.md`: `English | Tiếng Việt | Ghi chú`. Một số quyết định ban đầu (có thể chỉnh khi bạn duyệt pilot):

| English | Tiếng Việt (đề xuất) |
|---------|----------------------|
| data-intensive | thiên về dữ liệu (data-intensive) |
| reliability | độ tin cậy |
| scalability | khả năng mở rộng (scalability) |
| maintainability | khả năng bảo trì |
| fault | lỗi/trục trặc (fault) |
| failure | sự cố hệ thống (failure) |
| throughput | thông lượng (throughput) |
| latency | độ trễ (latency) |
| response time | thời gian phản hồi |
| percentile | phân vị (percentile) |
| load | tải |
| redundancy | dự phòng/dư thừa (redundancy) |

## 5. Quy trình mỗi chương (lặp lại được)

1. **Xác định dải trang PDF** cho chương (chênh lệch số trang in vs trang PDF ≈ **+22**; kiểm tra lại ranh giới đầu/cuối từng chương vì offset có thể đổi ở các phần).
2. **Trích text** chương ra `raw/chNN.txt` bằng `pdftotext`.
3. **Dịch theo từng mục**, đồng thời cập nhật `glossary.md` khi gặp thuật ngữ mới.
4. **Ráp file** `vi/chNN-*.md` và cập nhật bảng tiến độ trong `README.md`.
5. **Tự rà soát:** thuật ngữ nhất quán với glossary, không sót đoạn, đúng quy ước định dạng.
6. **Bàn giao** để bạn duyệt → chỉnh văn phong/thuật ngữ → chốt làm chuẩn cho các chương sau.

## 6. Kế hoạch thực thi pilot (Chương 1)

Chương 1 — *Reliable, Scalable, and Maintainable Applications* (trang in 3–26 → PDF ~25–48, kiểm tra ranh giới). Các mục dự kiến:

- Thinking About Data Systems → *Suy nghĩ về các hệ thống dữ liệu*
- Reliability → *Độ tin cậy* (Hardware Faults / Software Errors / Human Errors / How Important Is Reliability?)
- Scalability → *Khả năng mở rộng* (Describing Load / Describing Performance / Coping with Load)
- Maintainability → *Khả năng bảo trì* (Operability / Simplicity / Evolvability)
- Summary → *Tóm tắt*

Các bước:
1. Xác minh dải trang PDF chính xác của Chương 1.
2. Trích `raw/ch01.txt`.
3. Dịch lần lượt từng mục, dựng `glossary.md`.
4. Ráp `vi/ch01-ung-dung-tin-cay-kha-mo-rong-de-bao-tri.md` + tạo `README.md`.
5. Tự rà soát rồi bàn giao.

## 7. Tiêu chí hoàn thành (pilot)

- File `vi/ch01-*.md` đầy đủ các mục của Chương 1, đúng toàn bộ quy ước định dạng.
- `glossary.md` chứa các thuật ngữ chính của Chương 1.
- Bạn duyệt và xác nhận văn phong/thuật ngữ đạt yêu cầu.

## 8. Ngoài phạm vi (pilot này)

- Dịch các Chương 2–12 và phần phụ lục (thực hiện sau khi pilot được duyệt).
- Nhúng ảnh hình vẽ (tùy chọn, quyết định sau khi xem pilot).
- Dịch Index (chỉ mục) — thường không cần.
- Xuất bản/chia sẻ rộng rãi — cần xem xét vấn đề bản quyền với O'Reilly nếu phát hành.
