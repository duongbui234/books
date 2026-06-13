#!/usr/bin/env python3
"""Trích tiếng Anh cho cuốn The Pragmatic Programmer (books/pragmatic-programmer/).

Sách này có layout ĐA CỘT + trích dẫn lề (epigraph) nên extract_pdf.py (sắp theo top)
sẽ trộn lẫn. Ở đây dùng pdftohtml -xml và:
  - BỎ header/footer cỡ nhỏ (size < MINSIZE) và số trang.
  - TÁCH epigraph theo MÀU teal (#447777) -> khối blockquote đặt đầu mục.
  - Nhận HEADING theo FONT FAMILY: LiberationSans cỡ lớn = tên chương (#);
    TrebuchetMS = tên Topic / tiểu mục; nhãn "Topic N"/"Tip N" (TrebuchetMS nhỏ)
    là dấu hiệu phân biệt. Khối còn lại (Georgia) là thân bài, sắp theo top.
  - TÁCH FILE theo từng Topic (khớp danh sách tên topic đã biết). Tên chương + đoạn
    mở đầu chương gắn vào file của Topic ĐẦU TIÊN trong chương.

Dùng: extract_pp.py <key>     (key in STRUCTURE: vd "ch1".."ch9", "front", "postface",
                                "bibliography", "answers")
       extract_pp.py all
"""
import re
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "pragmatic-programmer"
PDF = BOOK / "source.pdf"

MINSIZE = 12       # bỏ chữ nhỏ hơn (header/footer/page number)
GAP_PARA = 14      # gap dọc (px) > mức này trong cùng cột -> đoạn mới (font ~23, line ~29)
TEAL = ("#447777", "#557777", "#336666")  # màu epigraph/trích dẫn

# --- cấu trúc sách: (out_no, chapter_title, first, last, [(topic_no, title), ...]) ---
CH = {
    "ch1": (1, "A Pragmatic Philosophy", 34, 72, [
        (1, "It’s Your Life"), (2, "The Cat Ate My Source Code"), (3, "Software Entropy"),
        (4, "Stone Soup and Boiled Frogs"), (5, "Good-Enough Software"),
        (6, "Your Knowledge Portfolio"), (7, "Communicate!")]),
    "ch2": (2, "A Pragmatic Approach", 73, 142, [
        (8, "The Essence of Good Design"), (9, "DRY—The Evils of Duplication"),
        (10, "Orthogonality"), (11, "Reversibility"), (12, "Tracer Bullets"),
        (13, "Prototypes and Post-it Notes"), (14, "Domain Languages"), (15, "Estimating")]),
    "ch3": (3, "The Basic Tools", 143, 187, [
        (16, "The Power of Plain Text"), (17, "Shell Games"), (18, "Power Editing"),
        (19, "Version Control"), (20, "Debugging"), (21, "Text Manipulation"),
        (22, "Engineering Daybooks")]),
    "ch4": (4, "Pragmatic Paranoia", 188, 225, [
        (23, "Design by Contract"), (24, "Dead Programs Tell No Lies"),
        (25, "Assertive Programming"), (26, "How to Balance Resources"),
        (27, "Don’t Outrun Your Headlights")]),
    "ch5": (5, "Bend, or Break", 226, 288, [
        (28, "Decoupling"), (29, "Juggling the Real World"), (30, "Transforming Programming"),
        (31, "Inheritance Tax"), (32, "Configuration")]),
    "ch6": (6, "Concurrency", 289, 323, [
        (33, "Breaking Temporal Coupling"), (34, "Shared State Is Incorrect State"),
        (35, "Actors and Processes"), (36, "Blackboards")]),
    "ch7": (7, "While You Are Coding", 324, 402, [
        (37, "Listen to Your Lizard Brain"), (38, "Programming by Coincidence"),
        (39, "Algorithm Speed"), (40, "Refactoring"), (41, "Test to Code"),
        (42, "Property-Based Testing"), (43, "Stay Safe Out There"), (44, "Naming Things")]),
    "ch8": (8, "Before the Project", 403, 434, [
        (45, "The Requirements Pit"), (46, "Solving Impossible Puzzles"),
        (47, "Working Together"), (48, "The Essence of Agility")]),
    "ch9": (9, "Pragmatic Projects", 435, 468, [
        (49, "Pragmatic Teams"), (50, "Coconuts Don’t Cut It"),
        (51, "Pragmatic Starter Kit"), (52, "Delight Your Users"), (53, "Pride and Prejudice")]),
}
# các đơn vị một-file (không tách topic). out_no -> chNN
SINGLE = {
    "front":        ("ch00", None, 13, 33),
    "postface":     ("ch54", "Postface", 469, 473),
    "bibliography": ("ch55", "Bibliography", 474, 477),
    "answers":      ("ch56", "Possible Answers to the Exercises", 478, 497),
}


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = s.replace("’", "'").replace("—", "-").replace("–", "-")
    return re.sub(r"[^a-z0-9]", "", s.lower())


def get_lines(first, last):
    """Trả về danh sách dòng: dict(page, top, left, size, fam, color, bold, text)."""
    base = BOOK / "images" / "_pp_tmp"
    base.parent.mkdir(parents=True, exist_ok=True)
    xmlp = base.with_suffix(".xml")
    subprocess.run(["pdftohtml", "-xml", "-f", str(first), "-l", str(last), "-q",
                    str(PDF), str(base)], check=True)
    tree = ET.parse(xmlp)
    xmlp.unlink()
    fs = {}
    for f in tree.iter("fontspec"):
        fs[f.get("id")] = (float(f.get("size", "0")), f.get("family", ""), f.get("color", ""))
    out = []
    for page in tree.iter("page"):
        pno = int(page.get("number"))
        for el in page.iter("text"):
            txt = "".join(el.itertext()).strip()
            if not txt:
                continue
            size, fam, color = fs.get(el.get("font"), (0, "", ""))
            out.append(dict(page=pno, top=float(el.get("top")), left=float(el.get("left")),
                            size=size, fam=fam, color=color,
                            bold=el.find("b") is not None, text=txt))
    return out


def classify(ln):
    """heading kind: 'chapter' | 'topiclabel' | 'tiplabel' | 'treb' | 'caps' | None"""
    t, fam, sz, col, b = ln["text"], ln["fam"], ln["size"], ln["color"], ln["bold"]
    if "LiberationSans" in fam and sz >= 30:
        return "chapter"
    if "TrebuchetMS" in fam and sz < 18 and re.match(r"^Topic\s+\d+$", t):
        return "topiclabel"
    if "TrebuchetMS" in fam and sz < 18 and re.match(r"^Tip\s+\d+$", t):
        return "tiplabel"
    if "TrebuchetMS" in fam and sz >= 18:
        return "treb"
    if "LiberationSans" in fam and b and sz >= 16 and t == t.upper() and len(t) > 3:
        return "caps"
    return None


def build_blocks(lines):
    """Trả về danh sách block: (kind, payload). kind: heading/topic/tip/para/quote/caps.
    payload cho 'topic' = (no_or_None, title)."""
    # bỏ số trang & dòng quá nhỏ
    lines = [l for l in lines if l["size"] >= MINSIZE and not re.fullmatch(r"\d{1,4}", l["text"])]
    # gom theo trang, tách epigraph (teal) ra trước thân
    by_page = {}
    for l in lines:
        by_page.setdefault(l["page"], []).append(l)

    blocks = []
    cur = None          # ('para'|'quote', [texts], last_top)
    pending_label = None  # ('topic'|'tip', number)

    def flush():
        nonlocal cur
        if cur:
            kind, parts, _ = cur
            text = " ".join(parts)
            text = re.sub(r"(\w)-\s+(\w)", lambda m: m.group(1)+m.group(2)
                          if m.group(2).islower() else m.group(0), text)
            blocks.append((kind, text))
            cur = None

    for pno in sorted(by_page):
        items = by_page[pno]
        quote = [i for i in items if any(c in i["color"] for c in TEAL)]
        body = [i for i in items if i not in quote]
        # epigraph -> 1 khối quote đặt đầu trang (nếu có)
        if quote:
            flush()
            qs = sorted(quote, key=lambda x: x["top"])
            blocks.append(("quote", " ".join(q["text"] for q in qs)))
        for ln in sorted(body, key=lambda x: x["top"]):
            k = classify(ln)
            if k == "chapter":
                flush()
                if re.match(r"^Chapter\s+\d+$", ln["text"]):
                    continue  # bỏ nhãn "Chapter N", giữ tên chương
                blocks.append(("heading", ln["text"]))
                continue
            if k == "topiclabel":
                flush()
                pending_label = ("topic", int(re.search(r"\d+", ln["text"]).group()))
                continue
            if k == "tiplabel":
                flush()
                pending_label = ("tip", int(re.search(r"\d+", ln["text"]).group()))
                continue
            if k == "treb":
                flush()
                if pending_label and pending_label[0] == "topic":
                    blocks.append(("topic", (pending_label[1], ln["text"])))
                elif pending_label and pending_label[0] == "tip":
                    blocks.append(("tip", (pending_label[1], ln["text"])))
                else:
                    blocks.append(("sub", ln["text"]))
                pending_label = None
                continue
            if k == "caps":
                flush()
                blocks.append(("caps", ln["text"]))
                continue
            # thân bài thường: nối theo gap dọc
            kindp = "para"
            if cur and cur[0] == kindp and cur[2] is not None and \
               (ln["top"] - cur[2]) <= GAP_PARA + ln["size"]:
                cur[1].append(ln["text"]); cur = (kindp, cur[1], ln["top"])
            else:
                flush(); cur = (kindp, [ln["text"]], ln["top"])
        flush()
        # reset gap qua trang
        if cur:
            cur = (cur[0], cur[1], None)
    flush()
    return blocks


def render_block(kind, payload):
    if kind == "heading":
        return f"# {payload}"
    if kind == "topic":
        no, title = payload
        return f"## Topic {no}. {title}"
    if kind == "sub":
        return f"### {payload}"
    if kind == "caps":
        return f"### {payload.title()}"
    if kind == "tip":
        no, title = payload
        return f"**Tip {no}: {title}**"
    if kind == "quote":
        return "\n".join("> " + l for l in [payload])
    return payload  # para


def write_file(chno, blocks):
    out = [render_block(k, p) for k, p in blocks]
    dest = BOOK / "en" / f"{chno}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n\n".join(out) + "\n", encoding="utf-8")
    from collections import Counter
    c = Counter(k for k, _ in blocks)
    print(f"✅ {dest.name}  ({len(blocks)} khối: {dict(c)})")


def do_chapter(key):
    cno, ctitle, first, last, topics = CH[key]
    blocks = build_blocks(get_lines(first, last))
    # chèn tên chương làm heading '#' ở đầu (thay cho 'heading' tự nhận nếu có)
    # xác định điểm bắt đầu mỗi topic theo khối 'topic'
    known = {norm(t): no for no, t in topics}
    # gắn số topic đúng nếu lệch nhận dạng: dựa vào title khớp
    splits = []  # (index_in_blocks, topic_no)
    for i, (k, p) in enumerate(blocks):
        if k == "topic":
            no, title = p
            n2 = known.get(norm(title), no)
            blocks[i] = ("topic", (n2, title))
            splits.append((i, n2))
    if not splits:
        print(f"⚠️  {key}: không thấy topic nào — kiểm tra lại")
        write_file(f"ch{cno:02d}x", blocks)
        return
    # phần trước topic đầu = tên chương + đoạn mở đầu -> gắn vào file topic đầu
    first_topic_no = splits[0][1]
    intro = blocks[:splits[0][0]]
    # bỏ heading tự nhận trùng tên chương trong intro, thay bằng '# ctitle'
    intro = [(k, p) for k, p in intro if not (k == "heading")]
    header = [("heading", ctitle)]
    seg_bounds = [s[0] for s in splits] + [len(blocks)]
    for j, (idx, tno) in enumerate(splits):
        seg = blocks[idx:seg_bounds[j+1]]
        if j == 0:
            seg = header + intro + seg
        write_file(f"ch{tno:02d}", seg)


def do_single(key):
    chno, title, first, last = SINGLE[key]
    blocks = build_blocks(get_lines(first, last))
    blocks = [(k, p) for k, p in blocks if k != "heading"]
    if title:
        blocks = [("heading", title)] + blocks
    write_file(chno, blocks)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    key = sys.argv[1]
    if key == "all":
        for k in SINGLE:
            do_single(k)
        for k in CH:
            do_chapter(k)
    elif key in CH:
        do_chapter(key)
    elif key in SINGLE:
        do_single(key)
    else:
        sys.exit(f"key lạ: {key}")


if __name__ == "__main__":
    main()
