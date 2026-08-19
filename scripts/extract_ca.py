#!/usr/bin/env python3
"""Trích tiếng Anh cho cuốn Clean Architecture (books/clean-architecture/).

Sách do InDesign dàn trang, có bốn đặc điểm mà extract_pdf.py không xử lý được:

  1. CHROME PHÂN BIỆT BẰNG MÀU, không bằng vị trí. Running header ("Chapter 2  A
     Tale of Two Values") và số trang đều là màu xám #a7a9ab; watermark
     "www.EBooksWorld.ir" màu #d4d4d4. Số trang nằm ở top≈1024/1188 = 86% chiều
     cao nên bộ lọc footer theo vị trí của extract_pdf.py (>92%) không bắt được.

  2. HEADING BỊ GIÃN CHỮ (letter-spacing của InDesign). Tiêu đề xuất ra thành
     "Th e  G oa l?" hay "Wh at  I s  D e s ig n". Khoảng cách giữa hai CHỮ CÁI
     là một dấu cách, giữa hai TỪ là hai dấu cách trở lên — despace() dựa vào
     đúng chỗ đó để dựng lại "The Goal?" / "What Is Design".

  3. HÌNH VẼ LÀ VECTOR, không phải ảnh nhúng. `pdftohtml -xml` trả về 0 <image>
     cho cả cuốn, nên cách làm của extract_pdf.py sẽ mất sạch 88 hình. Ở đây ta
     xác định dải dọc của hình (từ đáy đoạn văn cuối tới dòng "Figure N.M") rồi
     render đúng dải đó bằng pdftoppm.

  4. XML CỦA POPPLER CÓ BYTE HỎNG (một href ở trang 429 chứa byte 0x84 không
     hợp lệ UTF-8) làm ET.parse ném lỗi -> đọc bằng bytes rồi decode errors=replace.

Phân cấp heading theo (cỡ chữ, font):
  54 GillSansMTPro          -> '#'    tên chương / tên phần
  17 GillSansMTPro-Medium   -> '#'    tiêu đề phần đầu sách (Foreword, Preface…)
  21 GillSansMTPro          -> '##'   mục
  18 GillSansMTPro          -> '###'  tiểu mục
  14 GillSansMTPro-Medium   -> '####' tiểu mục nhỏ
Thân bài là SabonMTPro 17/15; code là CourierPSPro; chú thích chân trang là
SabonMTPro 12.

Dùng: extract_ca.py <chNN> <trang-đầu> <trang-cuối> [--no-figures]
      extract_ca.py all
"""
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "clean-architecture"
PDF = BOOK / "source.pdf"

# Lệch `top` trong CÙNG một dòng đo được tối đa 6px; hai dòng liền nhau cách tối
# thiểu 13px (đỉnh phân bố 21px). Chọn 9: rộng hơn hẳn nhiễu baseline, hẹp hơn
# hẳn bước dòng. Trần chống trôi 2*9 = 18 < 21 nên không bao giờ nuốt dòng sau.
LINE_TOL = 9
GAP_PARA = 25      # bước dòng thân bài 21px; > mức này -> đoạn mới
LEFT_TOL = 8       # lề trái đổi quá mức này -> khối mới (trích dẫn thụt, list)
CHROME = {"#a7a9ab", "#d4d4d4"}   # running header + số trang, watermark
FIG_PAD = 5        # chừa mép khi cắt hình (đơn vị toạ độ XML)
DPI = 150
XML_DPI = 108     # pdftohtml -xml luôn dựng trang ở 108 DPI (1188 đv = 792pt)

# --- cấu trúc sách: chNN -> (trang đầu, trang cuối) ---
UNITS = [
    ("ch00",  16,  27), ("ch01",  28,  29), ("ch02",  30,  39), ("ch03",  40,  45),
    ("ch04",  46,  47), ("ch05",  48,  51), ("ch06",  52,  59), ("ch07",  60,  75),
    ("ch08",  76,  83), ("ch09",  84,  87), ("ch10",  88,  95), ("ch11",  96, 103),
    ("ch12", 104, 109), ("ch13", 110, 113), ("ch14", 114, 119), ("ch15", 120, 121),
    ("ch16", 122, 129), ("ch17", 130, 137), ("ch18", 138, 159), ("ch19", 160, 161),
    ("ch20", 162, 173), ("ch21", 174, 185), ("ch22", 186, 201), ("ch23", 202, 209),
    ("ch24", 210, 215), ("ch25", 216, 221), ("ch26", 222, 227), ("ch27", 228, 237),
    ("ch28", 238, 243), ("ch29", 244, 247), ("ch30", 248, 257), ("ch31", 258, 265),
    ("ch32", 266, 275), ("ch33", 276, 281), ("ch34", 282, 301), ("ch35", 302, 303),
    ("ch36", 304, 311), ("ch37", 312, 317), ("ch38", 318, 323), ("ch39", 324, 329),
    ("ch40", 330, 349), ("ch41", 350, 351), ("ch42", 352, 401),
]

LIGATURES = str.maketrans({"ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl",
                           "ﬃ": "ffi", "ﬄ": "ffl", " ": " "})
FIG_RE = re.compile(r"^Figure\s+([A-Z]?\d*\.\d+)")   # 1.1, 34.2, A.1


def despace(s):
    """Dựng lại chữ bị InDesign giãn: 1 dấu cách = trong từ, >=2 = giữa hai từ.

    "Wh at  I s  D e s ig n" -> "What Is Design";  "Th e  G oa l?" -> "The Goal?"
    Chỉ áp cho heading GillSansMTPro cỡ lớn, tuyệt đối không áp cho thân bài.
    """
    s = re.sub(r"\s{2,}", "\x00", s.strip())
    return s.replace(" ", "").replace("\x00", " ")


def load_xml(first, last):
    with tempfile.TemporaryDirectory() as td:
        base = Path(td) / "x"
        subprocess.run(["pdftohtml", "-xml", "-i", "-q", "-f", str(first),
                        "-l", str(last), str(PDF), str(base)], check=True)
        raw = base.with_suffix(".xml").read_bytes()
    # poppler thỉnh thoảng nhả byte không hợp lệ trong href -> đừng để vỡ cả file
    return ET.fromstring(raw.decode("utf-8", errors="replace"))


def kind_of(size, fam, color):
    """-> ('heading', level) | 'code' | 'figcap' | 'note' | 'body' | None(bỏ)."""
    if color in CHROME:
        return None
    if "TimesNewRoman" in fam:
        return None            # "This page intentionally left blank" (26 trang)
    if "Helvetica" in fam:
        return None            # nhãn/tiêu đề BÊN TRONG hình vẽ -> đã nằm trong ảnh render
    if "CourierPSPro" in fam:
        return "code"
    if "GillSans" in fam:
        if size >= 45:
            return ("heading", 1)
        if size >= 20:
            return ("heading", 2)
        if size >= 17.5 and "Medium" not in fam:
            return ("heading", 3)
        if size >= 16:                      # 17 Medium: Foreword/Preface…
            return ("heading", 1)
        return "figcap"                     # 14: "Figure N.M" + tên hình
    if "Sabon" in fam and size <= 13:
        return "note"
    return "body"


def page_lines(page, fonts):
    """Gom <text> thành DÒNG hiển thị: nối theo chuỗi rồi sắp trái->phải."""
    runs = []
    for el in page.iter("text"):
        txt = "".join(el.itertext()).translate(LIGATURES)
        if not txt.strip():
            continue
        size, fam, color = fonts.get(el.get("font"), (0, "", ""))
        k = kind_of(size, fam, color)
        if k is None:
            continue
        runs.append({"top": float(el.get("top")), "left": float(el.get("left")),
                     "h": float(el.get("height", 0)), "text": txt,
                     "kind": k, "size": size, "fam": fam})
    runs.sort(key=lambda r: (r["top"], r["left"]))

    lines, i, n = [], 0, len(runs)
    while i < n:
        j, top0, prev = i + 1, runs[i]["top"], runs[i]["top"]
        while (j < n and runs[j]["top"] - prev < LINE_TOL
               and runs[j]["top"] - top0 < LINE_TOL * 2):
            prev = runs[j]["top"]
            j += 1
        grp = sorted(runs[i:j], key=lambda r: r["left"])
        base = max(grp, key=lambda r: len(r["text"].strip()))
        code_chars = sum(len(r["text"].strip()) for r in grp if r["kind"] == "code")
        total = sum(len(r["text"].strip()) for r in grp) or 1
        lines.append({
            "top": top0,
            "bottom": max(r["top"] + r["h"] for r in grp),
            "left": grp[0]["left"],
            "kind": "code" if code_chars / total > 0.6 else base["kind"],
            "raw": "".join(r["text"] for r in grp).rstrip(),
            "text": " ".join(r["text"].strip() for r in grp),
        })
        i = j
    return lines


def render_figure(pno, y0, y1, xml_w, dest):
    """Cắt dải dọc [y0, y1] của trang pno ra PNG.

    Hình trong sách này là VECTOR nên không có <image> để trích; phải render lại
    đúng dải chứa hình. pdftoppm tự cắt được (-x -y -W -H, đơn vị pixel) nên
    không cần render cả trang; Pillow chỉ làm nốt việc xén lề trắng thừa.
    """
    if y1 - y0 < 40:
        return False
    scale = DPI / XML_DPI
    y = max(0, int(y0 * scale))
    hgt = int((y1 - y0) * scale)
    wid = int(xml_w * scale)
    if hgt < 30:
        return False
    with tempfile.TemporaryDirectory() as td:
        base = Path(td) / "fig"
        subprocess.run(["pdftoppm", "-r", str(DPI), "-f", str(pno), "-l", str(pno),
                        "-x", "0", "-y", str(y), "-W", str(wid), "-H", str(hgt),
                        "-png", str(PDF), str(base)],
                       check=True, capture_output=True)
        pngs = sorted(Path(td).glob("fig*.png"))
        if not pngs:
            return False
        from PIL import Image, ImageChops, ImageOps
        im = Image.open(pngs[0]).convert("RGB")
        bbox = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255))).getbbox()
        if bbox:
            im = im.crop(bbox)
        if im.width < 30 or im.height < 30:
            return False
        ImageOps.expand(im, border=10, fill="white").save(dest)
    return dest.exists()


def build(ch, first, last, do_figures=True):
    root = load_xml(first, last)
    fonts = {f.get("id"): (float(f.get("size", "0")), f.get("family", ""),
                           f.get("color", ""))
             for f in root.iter("fontspec")}
    img_dir = BOOK / "images"
    img_dir.mkdir(parents=True, exist_ok=True)

    blocks = []          # (kind, payload)
    cur = None           # (kind, [lines], last_top, left)
    head_buf = None      # (level, [dòng tiêu đề])

    def flush_head():
        nonlocal head_buf
        if head_buf:
            lvl, parts = head_buf
            blocks.append(("heading", (lvl, " ".join(despace(p) for p in parts))))
            head_buf = None

    def flush():
        nonlocal cur
        if not cur:
            return
        k, lines, _, _ = cur
        if k == "code":
            blocks.append(("code", lines))
        else:
            joined = []
            for ln in lines:
                if joined and ln[:1].islower() and joined[-1][-1:] in "‐­":
                    joined[-1] = joined[-1][:-1] + ln
                elif joined:
                    joined[-1] = joined[-1] + " " + ln
                else:
                    joined.append(ln)
            blocks.append((k, " ".join(joined)))
        cur = None

    for page in root.iter("page"):
        pno = int(page.get("number"))
        xml_w = float(page.get("width", 918))
        lines = page_lines(page, fonts)

        for idx, ln in enumerate(lines):
            k = ln["kind"]

            # --- chú thích hình: chèn ảnh đã cắt NGAY TRƯỚC dòng chú thích ---
            if k == "figcap" and FIG_RE.match(ln["text"]):
                flush(); flush_head()
                if do_figures:
                    prev_bot = 190.0
                    for p in lines[:idx]:
                        if p["kind"] in ("body", "note", "code") and p["bottom"] < ln["top"]:
                            prev_bot = max(prev_bot, p["bottom"])
                    name = FIG_RE.match(ln["text"]).group(1).replace(".", "-")
                    dest = img_dir / f"{ch}-fig{name}.png"
                    if render_figure(pno, prev_bot + FIG_PAD, ln["top"] - FIG_PAD,
                                     xml_w, dest):
                        blocks.append(("image", dest.name))
                blocks.append(("figcap", ln["text"]))
                continue
            if k == "figcap":                 # dòng nguồn ảnh / chú thích phụ
                flush(); flush_head()
                blocks.append(("figcap", ln["text"]))
                continue

            if isinstance(k, tuple) and k[0] == "heading":
                flush()
                lvl = k[1]
                if head_buf and head_buf[0] == lvl:
                    head_buf[1].append(ln["text"])
                else:
                    flush_head()
                    head_buf = (lvl, [ln["text"]])
                continue
            flush_head()

            if k == "code":
                if cur and cur[0] == "code":
                    cur[1].append(ln["raw"]); cur = ("code", cur[1], ln["top"], cur[3])
                else:
                    flush(); cur = ("code", [ln["raw"]], ln["top"], ln["left"])
                continue

            item = bool(re.match(r"^([•◦▪‣·]|\d+\.)\s", ln["text"]))
            kk = "list" if item else k
            if cur and cur[0] == kk and cur[2] is not None and not item \
               and (ln["top"] - cur[2]) <= GAP_PARA \
               and abs(ln["left"] - cur[3]) <= LEFT_TOL:
                cur[1].append(ln["text"]); cur = (kk, cur[1], ln["top"], cur[3])
            else:
                flush(); cur = (kk, [ln["text"]], ln["top"], ln["left"])

        flush(); flush_head()
        if cur:
            cur = (cur[0], cur[1], None, cur[3])   # đừng tính gap xuyên trang
    flush(); flush_head()

    out = []
    for k, v in blocks:
        if k == "heading":
            lvl, t = v
            out.append("#" * lvl + " " + t)
        elif k == "code":
            out.append("```\n" + "\n".join(v) + "\n```")
        elif k == "image":
            out.append(f"![](images/{v})")
        elif k == "list":
            items = re.split(r"(?=(?:^|\s)[•◦▪‣·]\s)", v)
            out.append("\n".join("- " + re.sub(r"^[•◦▪‣·]\s*", "", s.strip())
                                 for s in items if s.strip()))
        else:
            out.append(v)

    dest = BOOK / "en" / f"{ch}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n\n".join(out) + "\n", encoding="utf-8")
    from collections import Counter
    c = Counter(k for k, _ in blocks)
    print(f"✅ {dest.name}  ({len(blocks)} khối: {dict(c)})")
    return blocks


def main():
    a = [x for x in sys.argv[1:] if x != "--no-figures"]
    figs = "--no-figures" not in sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "all":
        for ch, f, l in UNITS:
            build(ch, f, l, figs)
    else:
        build(a[0], int(a[1]), int(a[2]), figs)


if __name__ == "__main__":
    main()
