#!/usr/bin/env python3
"""Trích một chương tiếng Anh sạch từ PDF nguồn (không có EPUB) -> books/<slug>/en/<chNN>.md

Dùng `pdftohtml -xml` (poppler) để lấy chữ + font (đậm/cỡ -> heading) + vị trí ảnh.
Ảnh của chương được xuất vào books/<slug>/images/ và chèn placeholder Markdown
`![](images/<chNN>-<trang>_<n>.<ext>)` đúng vị trí giữa các đoạn.

Quy ước khối giống extract_epub.py: heading / đoạn / list / ảnh, ngăn bởi dòng trống.

Dùng: extract_pdf.py <slug> <chNN> <trang-đầu> <trang-cuối>
  vd:  extract_pdf.py system-design ch01 5 33
"""
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GAP_PARA = 25      # khoảng cách dọc (px) lớn hơn mức này -> sang đoạn mới
GAP_LINE = 30      # gap tối đa để coi là dòng kế tiếp trong cùng khối
HEAD_SIZE = 20     # font size >= mức này + đậm -> heading
MIN_IMG = 40       # bỏ ảnh nhỏ hơn (icon/nhiễu)


def text_of(el):
    return "".join(el.itertext())


def main():
    if len(sys.argv) != 5:
        sys.exit("Dùng: extract_pdf.py <slug> <chNN> <trang-đầu> <trang-cuối>")
    slug, ch, first, last = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    book = ROOT / "books" / slug
    pdf = book / "source.pdf"
    if not pdf.exists():
        sys.exit(f"❌ Không thấy {pdf}")
    img_dir = book / "images"
    img_dir.mkdir(parents=True, exist_ok=True)
    base = img_dir / ch  # ảnh sẽ thành images/<chNN>-<trang>_<n>.jpg
    xml_path = base.with_suffix(".xml")
    subprocess.run(
        ["pdftohtml", "-xml", "-f", first, "-l", last, "-q", str(pdf), str(base)],
        check=True,
    )
    tree = ET.parse(xml_path)
    xml_path.unlink()

    # fontspec: id -> size
    fsize = {}
    for fs in tree.iter("fontspec"):
        fsize[fs.get("id")] = float(fs.get("size", "0"))

    # Thu item theo trang, theo thứ tự dọc
    items = []  # (page, top, kind, payload)
    for page in tree.iter("page"):
        pno = int(page.get("number"))
        for el in page:
            if el.tag == "image":
                w, h = float(el.get("width", 0)), float(el.get("height", 0))
                if w < MIN_IMG or h < MIN_IMG:
                    continue
                src = Path(el.get("src"))
                items.append((pno, float(el.get("top")), "image", src.name))
            elif el.tag == "text":
                txt = text_of(el).strip()
                if not txt:
                    continue
                bold = el.find("b") is not None
                size = fsize.get(el.get("font"), 0)
                left = float(el.get("left"))
                items.append((pno, float(el.get("top")), "text",
                              (txt, bold, size, left)))
        # đánh dấu hết trang để không nối đoạn xuyên trang bằng gap
        items.append((pno, 10**9, "pagebreak", None))
    items.sort(key=lambda x: (x[0], x[1]))

    blocks = []   # (kind, value): heading/para/list/image
    cur = None    # ('para'|'list'|'heading', [lines], last_top)

    def flush():
        nonlocal cur
        if not cur:
            return
        k, lines, _ = cur
        joined = []
        for ln in lines:
            if joined and joined[-1].endswith("-") and ln[:1].islower():
                joined[-1] = joined[-1] + ln  # nối từ bị ngắt gạch nối
            elif k == "list" and re.match(r"^([•◦▪‣·]|\d+\.)\s", ln):
                joined.append(ln)
            elif k == "list" and joined:
                joined[-1] = joined[-1] + " " + ln
            elif joined and k != "list":
                joined[-1] = joined[-1] + " " + ln
            else:
                joined.append(ln)
        if k == "list":
            out = []
            for it in joined:
                it = re.sub(r"^[•◦▪‣·]\s*", "", it)
                m = re.match(r"^(\d+)\.\s*(.*)$", it)
                out.append(f"{m.group(1)}. {m.group(2)}" if m else f"- {it}")
            blocks.append(("list", out))
        elif k == "heading":
            blocks.append(("heading", " ".join(joined)))
        else:
            blocks.append(("para", " ".join(joined)))
        cur = None

    for pno, top, kind, payload in items:
        if kind == "pagebreak":
            # Đoạn có thể chảy sang trang sau. Heading thì chốt luôn; văn xuôi
            # chốt nếu dòng cuối đã kết câu (. ! ? :) — tránh dính 2 đoạn khác nhau.
            if cur and (cur[0] == "heading" or cur[1][-1].rstrip()[-1:] in ".!?:"):
                flush()
            if cur:
                cur = (cur[0], cur[1], None)  # quên top để không tính gap xuyên trang
            continue
        if kind == "image":
            flush()
            blocks.append(("image", payload))
            continue
        txt, bold, size, left = payload
        is_head = bold and size >= HEAD_SIZE
        is_item = bool(re.match(r"^([•◦▪‣·]|\d+\.)\s", txt))
        # mục tham khảo "[n] ..." luôn mở khối mới (URL dài xuống dòng dễ dính mục sau)
        if re.match(r"^\[\d+\]\s", txt):
            flush()
        if cur:
            ck, lines, ltop = cur
            gap = (top - ltop) if ltop is not None else 0
            if ck == "heading":
                if is_head and (ltop is None or gap < GAP_LINE * 1.6):
                    lines.append(txt); cur = (ck, lines, top); continue
                flush()
            elif is_head:
                flush()
            elif ck == "list":
                if is_item or (ltop is None or gap <= GAP_PARA) :
                    lines.append(txt); cur = (ck, lines, top); continue
                flush()
            else:  # para
                if not is_item and (ltop is None or gap <= GAP_PARA):
                    lines.append(txt); cur = (ck, lines, top); continue
                flush()
        if is_head:
            cur = ("heading", [txt], top)
        elif is_item:
            cur = ("list", [txt], top)
        else:
            cur = ("para", [txt], top)
    flush()

    # Render
    out = []
    for k, v in blocks:
        if k == "heading":
            lvl = "#" if re.match(r"^(CHAPTER\s+\d+|FORWARD|AFTERWORD)", v, re.I) else "##"
            out.append(f"{lvl} {v}")
        elif k == "list":
            out.append("\n".join(v))
        elif k == "image":
            out.append(f"![](images/{v})")
        else:
            out.append(v)
    dest = book / "en" / f"{ch}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n\n".join(out) + "\n", encoding="utf-8")

    from collections import Counter
    kinds = Counter(k for k, _ in blocks)
    print(f"✅ {dest}  ({len(blocks)} khối: {dict(kinds)})")
    for k, v in blocks:
        if k == "heading":
            print(f"  ## {v}")


if __name__ == "__main__":
    main()
