#!/usr/bin/env python3
"""Trích một chương tiếng Anh sạch từ PDF nguồn (không có EPUB) -> books/<slug>/en/<chNN>.md

Dùng `pdftohtml -xml` (poppler) để lấy chữ + font (đậm/cỡ -> heading) + vị trí ảnh.
Ảnh của chương được xuất vào books/<slug>/images/ và chèn placeholder Markdown
`![](images/<chNN>-<trang>_<n>.<ext>)` đúng vị trí giữa các đoạn.

Quy ước khối giống extract_epub.py: heading / đoạn / list / ảnh, ngăn bởi dòng trống.

Dùng: extract_pdf.py <slug> <chNN> <trang-đầu> <trang-cuối> [tùy chọn]
  vd:  extract_pdf.py system-design ch01 5 33

Tùy chọn (cho sách có heading KHÔNG in đậm, phân biệt bằng cỡ/font):
  --head-size N        ngưỡng cỡ chữ coi là heading (mặc định 20)
  --head-no-bold       heading nhận theo CỠ CHỮ thôi, không bắt buộc in đậm
  --title-family STR   heading có font family chứa STR -> cấp '#' (vd: Calibri-Light)
  --code-family STR    text có font family chứa STR (vd: Mono) -> khối CODE: giữ
                       xuống dòng & thụt lề, bọc ```, KHÔNG nhập vào văn xuôi
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


def is_footer_page_number(txt, top, page_height):
    """True for standalone page numbers in the bottom margin."""
    if not page_height:
        return False
    return (
        top > page_height * 0.92
        and re.fullmatch(r"(\d+|[ivxlcdm]+)", txt.strip(), re.IGNORECASE)
    )


def is_running_header_footer(txt):
    """True for running headers/footers such as '12 | Chapter'."""
    page = r"(?:\d+|[ivxlcdm]+)"
    return bool(
        re.match(rf"^{page}\s*\|", txt, re.IGNORECASE)
        or re.search(rf"\|\s*{page}$", txt, re.IGNORECASE)
    )


def text_of(el):
    return "".join(el.itertext())


def main():
    argv = sys.argv[1:]
    # tách cờ tùy chọn
    global HEAD_SIZE, GAP_PARA, GAP_LINE
    require_bold = True
    title_family = None
    code_family = None
    rest = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--head-size":
            HEAD_SIZE = float(argv[i + 1]); i += 2; continue
        if a == "--head-no-bold":
            require_bold = False; i += 1; continue
        if a == "--title-family":
            title_family = argv[i + 1]; i += 2; continue
        if a == "--code-family":
            code_family = argv[i + 1]; i += 2; continue
        if a == "--gap-para":
            GAP_PARA = float(argv[i + 1]); i += 2; continue
        if a == "--gap-line":
            GAP_LINE = float(argv[i + 1]); i += 2; continue
        rest.append(a); i += 1
    if len(rest) != 4:
        sys.exit("Dùng: extract_pdf.py <slug> <chNN> <trang-đầu> <trang-cuối> "
                 "[--head-size N] [--head-no-bold] [--title-family STR] [--code-family STR] "
                 "[--gap-para N] [--gap-line N]")
    slug, ch, first, last = rest
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

    # fontspec: id -> size, family
    fsize = {}
    ffam = {}
    for fs in tree.iter("fontspec"):
        fsize[fs.get("id")] = float(fs.get("size", "0"))
        ffam[fs.get("id")] = fs.get("family", "")

    # Thu item theo trang, theo thứ tự dọc
    items = []  # (page, top, kind, payload)
    for page in tree.iter("page"):
        pno = int(page.get("number"))
        page_height = float(page.get("height", 0) or 0)
        for el in page:
            if el.tag == "image":
                w, h = float(el.get("width", 0)), float(el.get("height", 0))
                if w < MIN_IMG or h < MIN_IMG:
                    continue
                src = Path(el.get("src"))
                items.append((pno, float(el.get("top")), "image", src.name))
            elif el.tag == "text":
                raw = text_of(el).replace("\n", " ")
                txt = raw.strip()
                if not txt:
                    continue
                top = float(el.get("top"))
                if is_footer_page_number(txt, top, page_height):
                    continue
                # Bỏ running header/footer: "12 | Chapter 1: ..." (trang chẵn)
                # hoặc "Tên mục | 13" (trang lẻ). Không đụng footnote (không có " | ").
                if is_running_header_footer(txt):
                    continue
                bold = el.find("b") is not None
                size = fsize.get(el.get("font"), 0)
                fam = ffam.get(el.get("font"), "")
                left = float(el.get("left"))
                is_code = bool(code_family) and code_family in fam
                # code giữ thụt lề: dùng raw (chỉ bỏ khoảng trắng cuối)
                code_txt = raw.rstrip()
                items.append((pno, top, "text",
                              (txt, bold, size, left, fam, is_code, code_txt)))
        # đánh dấu hết trang để không nối đoạn xuyên trang bằng gap
        items.append((pno, 10**9, "pagebreak", None))
    items.sort(key=lambda x: (x[0], x[1]))
    # Gom item cùng một DÒNG (cùng trang, chênh top < LINE_TOL) rồi sắp trái->phải.
    # Chữ nghiêng (thuật ngữ) thường lệch baseline 1-2px so với chữ thường cùng dòng;
    # nếu chỉ sắp theo top thì các run này bị xáo lung tung giữa câu.
    LINE_TOL = 6
    leftof = lambda it: it[3][3] if it[2] == "text" else 0.0
    ordered, i, n = [], 0, len(items)
    while i < n:
        j, page0, top0 = i + 1, items[i][0], items[i][1]
        while j < n and items[j][0] == page0 and abs(items[j][1] - top0) < LINE_TOL:
            j += 1
        line = items[i:j]
        line.sort(key=leftof)
        # Một DÒNG là CODE nếu phần lớn ký tự thuộc code-family (tránh nhầm 1-2 từ
        # mã inline trong văn xuôi). Gộp các run thành 1 dòng, giữ nguyên thụt lề.
        runs = [it for it in line if it[2] == "text"]
        if code_family and runs:
            code_chars = sum(len(it[3][0]) for it in runs if it[3][5])
            total = sum(len(it[3][0]) for it in runs) or 1
            if code_chars / total > 0.6:
                merged = "".join(it[3][6] for it in runs)
                ordered.append((page0, top0, "codeline", merged))
                i = j
                continue
        ordered.extend(line)
        i = j
    items = ordered

    blocks = []   # (kind, value): heading/para/list/image
    cur = None    # ('para'|'list'|'heading', [lines], last_top, font_family)

    def flush():
        nonlocal cur
        if not cur:
            return
        k, lines, _, fam = cur
        if k == "code":
            blocks.append(("code", lines))
            cur = None
            return
        joined = []
        for ln in lines:
            if joined and ln[:1].islower() and joined[-1][-1:] in "-‐­":
                # nối từ bị ngắt cuối dòng: gạch Unicode (‐ U+2010, ­ U+00AD) bỏ hẳn;
                # '-' ascii giữ lại (thường là từ ghép thật, vd "index-organized")
                tail = joined[-1]
                joined[-1] = (tail[:-1] if tail[-1] in "‐­" else tail) + ln
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
            text = " ".join(joined)
            if re.match(r"^(CHAPTER\s+\d+|FORWARD|AFTERWORD)", text, re.I):
                lvl = "#"
            elif title_family and title_family in (fam or ""):
                lvl = "#"
            elif title_family:
                lvl = "##"   # sách phân cấp theo font: không phải title-family -> mục con
            else:
                lvl = "##"
            blocks.append(("heading", f"{lvl} {text}"))
        else:
            blocks.append(("para", " ".join(joined)))
        cur = None

    for pno, top, kind, payload in items:
        if kind == "pagebreak":
            # Đoạn có thể chảy sang trang sau. Heading & code thì chốt luôn; văn xuôi
            # chốt nếu dòng cuối đã kết câu (. ! ? :) — tránh dính 2 đoạn khác nhau.
            if cur and (cur[0] in ("heading", "code") or cur[1][-1].rstrip()[-1:] in ".!?:"):
                flush()
            if cur:
                cur = (cur[0], cur[1], None, cur[3])  # quên top để không tính gap xuyên trang
            continue
        if kind == "image":
            flush()
            blocks.append(("image", payload))
            continue
        if kind == "codeline":
            if cur and cur[0] == "code":
                cur[1].append(payload)
                cur = ("code", cur[1], top, cur[3])
            else:
                flush()
                cur = ("code", [payload], top, "")
            continue
        txt, bold, size, left, fam, is_code, code_txt = payload
        if cur and cur[0] == "code":
            flush()  # văn xuôi quay lại -> chốt khối code
        is_head = size >= HEAD_SIZE and (bold or not require_bold)
        is_item = bool(re.match(r"^([•◦▪‣·]|\d+\.)\s", txt))
        # mục tham khảo "[n] ..." luôn mở khối mới (URL dài xuống dòng dễ dính mục sau)
        if re.match(r"^\[\d+\]\s", txt):
            flush()
        if cur:
            ck, lines, ltop, cfam = cur
            gap = (top - ltop) if ltop is not None else 0
            if ck == "heading":
                if is_head and (ltop is None or gap < GAP_LINE * 1.6):
                    lines.append(txt); cur = (ck, lines, top, cfam); continue
                flush()
            elif is_head:
                flush()
            elif ck == "list":
                if not is_head and (is_item or (ltop is None or gap <= GAP_PARA)):
                    lines.append(txt); cur = (ck, lines, top, cfam); continue
                flush()
            else:  # para
                if not is_head and not is_item and (ltop is None or gap <= GAP_PARA):
                    lines.append(txt); cur = (ck, lines, top, cfam); continue
                flush()
        if is_head:
            cur = ("heading", [txt], top, fam)
        elif is_item:
            cur = ("list", [txt], top, fam)
        else:
            cur = ("para", [txt], top, fam)
    flush()

    # Bỏ "code" rởm: nhãn số/biến 1-2 ký tự trong HÌNH (vd "1212", "21221", "K")
    # bị bắt nhầm là code vì cùng font mono. Xét cả khối nên không cắt code thật.
    def _noise_code(lines):
        s = "\n".join(lines).strip()
        if re.fullmatch(r"[\d\s.;:,]+", s) or len(s.replace(" ", "")) <= 2:
            return True
        # khối 1 DÒNG không có cú pháp code (= ; { } ( ) [ ] < > |): nếu là 1 token
        # hoặc rất ngắn (<=12 ký tự) thì là nhãn rời trong hình -> bỏ.
        if len(lines) == 1 and not re.search(r"[=;{}()\[\]<>|]", s):
            if len(s.split()) == 1 or len(s.replace(" ", "")) <= 12:
                return True
        return False
    blocks = [b for b in blocks if not (b[0] == "code" and _noise_code(b[1]))]

    # Render
    out = []
    for k, v in blocks:
        if k == "heading":
            out.append(v)
        elif k == "list":
            out.append("\n".join(v))
        elif k == "image":
            out.append(f"![](images/{v})")
        elif k == "code":
            out.append("```\n" + "\n".join(v) + "\n```")
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
            print(f"  {v}")


if __name__ == "__main__":
    main()
