#!/usr/bin/env python3
"""Trích một chương tiếng Anh sạch từ EPUB nguồn của bạn -> books/<slug>/en/<chNN>.md

Chỉ đọc file EPUB sẵn có trên máy bạn và xuất ra Markdown theo từng khối
(heading / đoạn / list / code) để ghép song ngữ. Không tải nội dung từ nguồn khác.

Dùng: extract_epub.py <slug> <đường-dẫn-html-trong-epub> <chNN>
  vd:  extract_epub.py ddia OEBPS/ch01.html ch01
"""
import re
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOCK = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "pre", "figcaption"}


class Extractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks = []      # (type, value)
        self.cur = None       # tag khối hiện tại
        self.buf = []
        self.in_pre = False
        self.skip = 0         # bỏ nội dung trong <sup> (số chú thích)
        self.li_items = []
        self.in_li = False
        self.list_depth = 0
        self.in_table = False  # bảng <table>
        self.rows = []         # các hàng đã thu của bảng hiện tại
        self.cur_row = []      # các ô của hàng hiện tại
        self.in_cell = False

    def handle_starttag(self, tag, attrs):
        if tag == "sup":
            self.skip += 1
        elif tag == "table":
            self.in_table = True
            self.rows = []
        elif tag == "tr" and self.in_table:
            self.cur_row = []
        elif tag in ("td", "th") and self.in_table:
            self.in_cell = True
            self.buf = []
        elif self.in_table:
            if tag == "br" and self.in_cell:
                self.buf.append(" ")
        elif tag in ("ul", "ol"):
            self.list_depth += 1
            if self.list_depth == 1:
                self.li_items = []
        elif tag == "li":
            self.in_li = True
            self.buf = []
        elif tag in BLOCK and self.cur is None and not self.in_li:
            self.cur = tag
            self.buf = []
            self.in_pre = tag == "pre"
        elif tag == "br":
            self.buf.append("\n" if self.in_pre else " ")

    def handle_endtag(self, tag):
        if tag == "sup":
            self.skip = max(0, self.skip - 1)
        elif self.in_table:
            if tag in ("td", "th") and self.in_cell:
                self.cur_row.append(self._flush())
                self.in_cell = False
            elif tag == "tr":
                if self.cur_row:
                    self.rows.append(self.cur_row)
                self.cur_row = []
            elif tag == "table":
                self.in_table = False
                if self.rows:
                    self.blocks.append(("table", self.rows))
                self.rows = []
        elif tag == "li" and self.in_li:
            self.li_items.append(self._flush())
            self.in_li = False
        elif tag in ("ul", "ol"):
            self.list_depth = max(0, self.list_depth - 1)
            if self.list_depth == 0 and self.li_items:
                self.blocks.append(("list", [x for x in self.li_items if x]))
                self.li_items = []
        elif tag == self.cur:
            txt = self._flush(pre=self.in_pre)
            if txt.strip():
                if tag == "pre":
                    self.blocks.append(("code", txt))
                elif len(tag) == 2 and tag[0] == "h" and tag[1].isdigit():
                    self.blocks.append(("heading", (int(tag[1]), txt.strip())))
                else:
                    self.blocks.append(("para", txt.strip()))
            self.cur = None
            self.in_pre = False

    def handle_data(self, data):
        if self.skip:
            return
        if self.cur or self.in_li or self.in_cell:
            self.buf.append(data)

    def _flush(self, pre=False):
        s = "".join(self.buf)
        self.buf = []
        if not pre:
            s = re.sub(r"\s+", " ", s).strip()
        return s


def render(blocks):
    out = []
    for t, v in blocks:
        if t == "heading":
            lvl, txt = v
            out.append("#" * min(lvl, 6) + " " + txt)
        elif t == "list":
            out.append("\n".join("- " + it for it in v))
        elif t == "code":
            out.append("```\n" + v.rstrip("\n") + "\n```")
        elif t == "table":
            rows = [r for r in v if any(c.strip() for c in r)]
            if not rows:
                continue
            ncol = max(len(r) for r in rows)
            rows = [r + [""] * (ncol - len(r)) for r in rows]
            esc = lambda c: c.replace("|", "\\|").replace("\n", " ").strip()
            lines = ["| " + " | ".join(esc(c) for c in rows[0]) + " |",
                     "| " + " | ".join("---" for _ in range(ncol)) + " |"]
            for r in rows[1:]:
                lines.append("| " + " | ".join(esc(c) for c in r) + " |")
            out.append("\n".join(lines))
        else:
            out.append(v)
    return "\n\n".join(out) + "\n"


def main():
    if len(sys.argv) != 4:
        sys.exit("Dùng: extract_epub.py <slug> <html-trong-epub> <chNN>")
    slug, html_path, ch = sys.argv[1], sys.argv[2], sys.argv[3]
    book = ROOT / "books" / slug
    epub = book / "source.epub"
    if not epub.exists():
        sys.exit(f"❌ Không thấy {epub}")
    with zipfile.ZipFile(epub) as z:
        try:
            raw = z.read(html_path).decode("utf-8", "replace")
        except KeyError:
            sys.exit(f"❌ Không thấy {html_path} trong EPUB")
    ex = Extractor()
    ex.feed(raw)
    dest = book / "en" / f"{ch}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(render(ex.blocks), encoding="utf-8")

    # Chẩn đoán (không in toàn văn): số khối theo loại + danh sách heading
    from collections import Counter
    kinds = Counter(t for t, _ in ex.blocks)
    print(f"✅ {dest}  ({len(ex.blocks)} khối: {dict(kinds)})")
    print("Headings:")
    for t, v in ex.blocks:
        if t == "heading":
            print(f"  {'#'*v[0]} {v[1]}")


if __name__ == "__main__":
    main()
