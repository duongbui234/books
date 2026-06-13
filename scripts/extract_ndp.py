#!/usr/bin/env python3
"""Trích một chương tiếng Anh sạch từ "Node.js Design Patterns" (Packt, InDesign)
-> books/nodejs-design-patterns/en/<chNN>.md

Khác extract_pdf.py: sách này NHIỀU CODE và CODE INLINE (font Consolas), bố cục
Packt có header/footer cố định. extract_pdf.py coi mỗi <text> là 1 item rồi sắp
theo `top` -> code inline (font khác, top lệch vài px) bị TRỘN sai thứ tự câu và
khối code bị làm phẳng thành văn xuôi. Vì vậy phải:

  1. DỰNG LẠI DÒNG: gom các <text> cùng `top` (±LINE_TOL) thành 1 dòng, sắp theo
     `left`, nối lại -> giữ đúng thứ tự đọc (vá lỗi code inline nhảy chỗ).
  2. NHẬN DIỆN CODE theo font family chứa "Consolas":
     - dòng >50% ký tự là Consolas  -> dòng CODE (gom thành khối ``` ```,
       thụt lề giữ nguyên nhờ các span khoảng trắng đầu dòng).
     - span Consolas lẫn trong văn xuôi -> bọc `inline code` bằng backtick.
  3. HEADING theo font Arial + CỠ: 45->#  30->##  27->###  24->####  21->#####
     (thân bài là BookAntiqua nên không nhầm). Trang mở chương có font
     Chapter_Number_PACKT (số lớn) + ArialMT 45 (tên chương) -> "# Chapter N: ...".
  4. BỎ header chạy (top<160) và footer/số trang "[ N ]" (top>955).

CODE phải là MỘT khối không có dòng trống bên trong (merge_bilingual tách khối theo
dòng trống) -> dòng trống trong code bị BỎ để giữ căn khối 1-1 với vi/.

Dùng: extract_ndp.py <chNN> <trang-đầu-pdf> <trang-cuối-pdf>
  vd:  extract_ndp.py ch01 30 45
"""
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent.parent
SLUG = "nodejs-design-patterns"

HEADER_MAX = 160     # top < mức này -> header chạy (bỏ)
FOOTER_MIN = 985     # top > mức này -> footer / số trang "[ N ]" ở ~998 (bỏ)
LINE_TOL = 11        # chênh `top` <= mức này -> cùng một dòng hiển thị
GAP_PARA = 26        # gap dọc > mức này -> sang đoạn mới (bước dòng ~19)
MIN_IMG = 45


def text_of(el):
    return "".join(el.itertext())


def heading_level(size):
    if size >= 40:
        return 1
    if size >= 28:
        return 2
    if size >= 25.5:
        return 3
    if size >= 22.5:
        return 4
    if size >= 18:
        return 5
    return 0


def main():
    if len(sys.argv) != 4:
        sys.exit("Dùng: extract_ndp.py <chNN> <trang-đầu> <trang-cuối>")
    ch, first, last = sys.argv[1], sys.argv[2], sys.argv[3]
    book = ROOT / "books" / SLUG
    pdf = book / "source.pdf"
    if not pdf.exists():
        sys.exit(f"❌ Không thấy {pdf}")
    img_dir = book / "images"
    img_dir.mkdir(parents=True, exist_ok=True)
    base = img_dir / ch
    xml_path = base.with_suffix(".xml")
    subprocess.run(
        ["pdftohtml", "-xml", "-f", first, "-l", last, "-q", str(pdf), str(base)],
        check=True,
    )
    tree = ET.parse(xml_path)
    xml_path.unlink()

    fsize, ffam, fcolor = {}, {}, {}
    for fs in tree.iter("fontspec"):
        fsize[fs.get("id")] = float(fs.get("size", "0"))
        ffam[fs.get("id")] = fs.get("family", "")
        fcolor[fs.get("id")] = fs.get("color", "#000000")

    def is_code(fid):
        return "Consolas" in ffam.get(fid, "")

    # Khối code dùng bảng màu tô cú pháp (#383a42, #a626a4, #50a14f, ...).
    # Code INLINE trong văn xuôi là Consolas MÀU ĐEN (#000000). Vì vậy span
    # Consolas KHÁC đen <=> đang ở trong một khối code.
    def is_block_code(fid):
        return "Consolas" in ffam.get(fid, "") and fcolor.get(fid, "#000000") != "#000000"

    def is_sans(fid):
        return "Arial" in ffam.get(fid, "")

    # ---- Thu thập span theo trang, dựng lại DÒNG ----
    # mỗi "line" = dict(page, top, spans=[(left,text,fid)], images=[...])
    lines = []          # các dòng văn bản (đã dựng)
    images = []         # (page, top, name)
    chap_num = None
    title_parts = []    # các đoạn tên chương (ArialMT >= 40)

    for page in tree.iter("page"):
        pno = int(page.get("number"))
        spans = []      # (top, left, text, fid)
        for el in page:
            if el.tag == "image":
                w, h = float(el.get("width", 0)), float(el.get("height", 0))
                if w < MIN_IMG or h < MIN_IMG:
                    continue
                images.append((pno, float(el.get("top")), Path(el.get("src")).name))
                continue
            if el.tag != "text":
                continue
            raw = text_of(el)
            if raw == "":
                continue  # giữ span chỉ-khoảng-trắng (là dấu cách/thụt lề trong code)
            top = float(el.get("top"))
            left = float(el.get("left"))
            fid = el.get("font")
            fam = ffam.get(fid, "")
            # số chương lớn ở trang mở chương
            if "Chapter_Number" in fam:
                m = re.search(r"\d+", raw)
                if m:
                    chap_num = m.group(0)
                continue
            if top < HEADER_MAX or top > FOOTER_MIN:
                continue  # header chạy / footer / số trang
            spans.append((top, left, raw, fid))

        # gom span thành dòng theo `top`
        spans.sort(key=lambda s: (s[0], s[1]))
        cur = []
        cur_top = None
        page_lines = []
        for top, left, raw, fid in spans:
            if cur and top - cur_top > LINE_TOL:
                page_lines.append((cur_top, cur))
                cur = []
            if not cur:
                cur_top = top
            cur.append((left, raw, fid))
        if cur:
            page_lines.append((cur_top, cur))

        for ltop, cur in page_lines:
            cur.sort(key=lambda s: s[0])  # theo left
            # tên chương (ArialMT cỡ >= 40)
            if all(is_sans(fid) and fsize.get(fid, 0) >= 40 for _, _, fid in cur):
                title_parts.append(" ".join(t.strip() for _, t, _ in cur).strip())
                continue
            lines.append({"page": pno, "top": ltop, "spans": cur})

    # gộp ảnh vào dòng theo (page, top) để giữ vị trí
    stream = []  # (page, top, kind, payload)
    for ln in lines:
        stream.append((ln["page"], ln["top"], "line", ln["spans"]))
    for pno, top, name in images:
        stream.append((pno, top, "image", name))
    stream.append((10**9, 0, "end", None))
    stream.sort(key=lambda x: (x[0], x[1]))

    # ---- Phân loại dòng + gom khối ----
    def classify(spans):
        total = sum(len(t) for _, t, _ in spans)
        block_code_chars = sum(len(t) for _, t, fid in spans if is_block_code(fid))
        nonspace = sum(len(t.strip()) for _, t, _ in spans)
        # heading: toàn span sans cỡ heading
        sans_sizes = [fsize.get(fid, 0) for _, _, fid in spans if is_sans(fid)]
        nonsans = [t for _, t, fid in spans if not is_sans(fid) and t.strip()]
        if sans_sizes and not nonsans:
            lvl = heading_level(max(sans_sizes))
            if lvl:
                return ("heading", lvl)
        # dòng CODE = có span Consolas tô màu cú pháp (khác đen) chiếm ưu thế.
        # văn xuôi chứa code-inline (Consolas ĐEN) -> KHÔNG bị nhầm là khối code.
        if nonspace and block_code_chars / max(total, 1) > 0.5:
            return ("code", None)
        first_txt = "".join(t for _, t, _ in spans).lstrip()
        if re.match(r"^[•◦▪‣·]\s*", first_txt) or re.match(r"^\d+\.\s", first_txt):
            return ("list", None)
        return ("para", None)

    def render_prose(spans):
        """Nối span theo left, bọc backtick cho code inline, giữ khoảng trắng span."""
        out = []
        i = 0
        n = len(spans)
        while i < n:
            _, t, fid = spans[i]
            if is_code(fid):
                j = i
                buf = ""
                while j < n and is_code(spans[j][2]):
                    buf += spans[j][1]
                    j += 1
                lead = buf[: len(buf) - len(buf.lstrip())]
                trail = buf[len(buf.rstrip()):]
                core = buf.strip()
                out.append(lead + (f"`{core}`" if core else "") + trail)
                i = j
            else:
                out.append(t)
                i += 1
        return re.sub(r"[ \t]{2,}", " ", "".join(out)).strip()

    def render_code(spans):
        return "".join(t for _, t, _ in spans).rstrip()

    blocks = []   # (kind, payload)
    cur = None    # dict(kind, lines=[str], lvl, last_top, page)

    def flush():
        nonlocal cur
        if not cur:
            return
        k = cur["kind"]
        if k == "code":
            body = [l for l in cur["lines"] if l.strip() != ""]
            blocks.append(("code", "```js\n" + "\n".join(body) + "\n```"))
        elif k == "heading":
            txt = " ".join(cur["lines"]).strip()
            blocks.append(("heading", "#" * cur["lvl"] + " " + txt))
        elif k == "list":
            blocks.append(("list", "\n".join(cur["lines"])))
        else:
            blocks.append(("para", " ".join(cur["lines"])))
        cur = None

    for pno, top, knd, payload in stream:
        if knd == "end":
            flush()
            break
        if knd == "image":
            flush()
            blocks.append(("image", f"![](images/{payload})"))
            continue
        spans = payload
        kind_, lvl = classify(spans)
        same_page = cur is not None and cur["page"] == pno
        gap = (top - cur["last_top"]) if (cur and same_page) else None

        if kind_ == "code":
            line = render_code(spans)
            if cur and cur["kind"] == "code":
                # dòng trống trong code: chèn nếu gap lớn (sẽ bị bỏ khi flush)
                cur["lines"].append(line)
                cur["last_top"] = top
                cur["page"] = pno
                continue
            flush()
            cur = {"kind": "code", "lines": [line], "last_top": top, "page": pno}
            continue

        if kind_ == "heading":
            text = render_prose(spans).strip()
            if cur and cur["kind"] == "heading" and cur["lvl"] == lvl \
                    and same_page and gap is not None and gap < 48:
                cur["lines"].append(text)
                cur["last_top"] = top
                continue
            flush()
            cur = {"kind": "heading", "lines": [text], "lvl": lvl,
                   "last_top": top, "page": pno}
            continue

        if kind_ == "list":
            text = render_prose(spans).rstrip()
            m = re.match(r"^\s*([•◦▪‣·]|\d+\.)\s*(.*)$", text)
            item = m.group(2) if m else text
            num = re.match(r"^\s*(\d+)\.\s", text)
            rendered = (f"{num.group(1)}. {item}" if num else f"- {item}")
            if cur and cur["kind"] == "list":
                if m:  # mục mới
                    cur["lines"].append(rendered)
                else:  # nối tiếp mục trước
                    cur["lines"][-1] += " " + text.strip()
                cur["last_top"] = top
                cur["page"] = pno
                continue
            flush()
            cur = {"kind": "list", "lines": [rendered], "last_top": top, "page": pno}
            continue

        # para
        text = render_prose(spans).rstrip()
        # dòng cuộn (không có bullet) nối tiếp một mục list -> nhập vào mục cuối
        if cur and cur["kind"] == "list" and same_page \
                and gap is not None and gap <= GAP_PARA:
            prev = cur["lines"][-1]
            if prev.endswith("-") and text[:1].islower():
                cur["lines"][-1] = prev[:-1] + text
            else:
                cur["lines"][-1] = prev + " " + text
            cur["last_top"] = top
            cur["page"] = pno
            continue
        if cur and cur["kind"] == "para":
            if not same_page or (gap is not None and gap <= GAP_PARA):
                prev = cur["lines"][-1]
                if prev.endswith("-") and text[:1].islower():
                    cur["lines"][-1] = prev[:-1] + text
                else:
                    cur["lines"].append(text)
                cur["last_top"] = top
                cur["page"] = pno
                continue
            flush()
        elif cur:
            flush()
        cur = {"kind": "para", "lines": [text], "last_top": top, "page": pno}
    flush()

    # ---- Tiêu đề chương ----
    out_blocks = []
    if title_parts:
        title = " ".join(title_parts).strip()
        title = re.sub(r"\s+", " ", title)
        if chap_num:
            out_blocks.append(("heading", f"# Chapter {chap_num}: {title}"))
        else:
            out_blocks.append(("heading", f"# {title}"))
    out_blocks.extend(blocks)

    out = []
    for k, v in out_blocks:
        out.append(v)
    dest = book / "en" / f"{ch}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n\n".join(out) + "\n", encoding="utf-8")

    from collections import Counter
    kinds = Counter(k for k, _ in out_blocks)
    print(f"✅ {dest}  ({len(out_blocks)} khối: {dict(kinds)})")
    for k, v in out_blocks:
        if k == "heading":
            print("  " + v)


if __name__ == "__main__":
    main()
