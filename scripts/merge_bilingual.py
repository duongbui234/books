#!/usr/bin/env python3
"""Trộn song ngữ: ghép en/chNN.md (tiếng Anh, trích từ EPUB của bạn) với
vi/chNN.md (bản dịch tiếng Việt) thành chapters/chNN.md theo từng đoạn.

Quy ước: phần THÂN của hai file phải CÙNG SỐ KHỐI, CÙNG THỨ TỰ
(khối = ngăn bởi dòng trống).
- heading  -> "## <EN> — <VI>"
- đoạn văn -> đoạn EN (tô đậm thuật ngữ theo glossary) + đoạn VI (blockquote)
- list     -> list EN, rồi list VI (blockquote)
- code     -> in một lần (bản EN)
Phần "Footnotes"/"References" ở cuối -> giữ NGUYÊN tiếng Anh (không cần bản VI).

Dùng:
  merge_bilingual.py <slug> <chNN>           # trộn
  merge_bilingual.py <slug> <chNN> --plan    # in cấu trúc khối phần thân (để viết vi/)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAIL_TITLES = ("references", "footnotes", "bibliography", "reference materials",
               "further reading", "additional resources")


def load_glossary_terms(book_dir):
    gloss = book_dir / "glossary.md"
    terms = []
    if not gloss.exists():
        return terms
    for line in gloss.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        en = cells[0]
        if en.lower() in ("english", "term", "") or set(en) <= set("-: "):
            continue
        en = re.sub(r"\([^)]*\)", "", en)
        for cand in re.split(r"[/]", en):
            cand = cand.strip()
            if len(cand) >= 3:
                terms.append(cand)
    return sorted(set(terms), key=len, reverse=True)


def split_blocks(text):
    blocks = re.split(r"\n[ \t]*\n", text.strip("\n"))
    return [b.strip("\n") for b in blocks if b.strip()]


def kind(block):
    first = block.lstrip().splitlines()[0] if block.strip() else ""
    if first.startswith("```"):
        return "code"
    if first.startswith("!["):
        return "image"
    if re.match(r"^#{1,6}\s", first):
        return "heading"
    lines = [l for l in block.splitlines() if l.strip()]
    if lines and all(l.lstrip().startswith("|") for l in lines):
        return "table"
    if lines and all(re.match(r"^\s*([-*+]|\d+\.)\s", l) for l in lines):
        return "list"
    return "para"


def heading_text(block):
    m = re.match(r"^(#{1,6})\s+(.*)$", block.strip())
    return (m.group(1), m.group(2).strip()) if m else ("##", block.strip())


def is_tail(block):
    if kind(block) != "heading":
        return False
    _, t = heading_text(block)
    return t.strip().lower().lstrip("#").strip() in TAIL_TITLES


def bold_terms(text, terms, used):
    for term in terms:
        if term.lower() in used:
            continue
        pat = re.compile(r"(?<![\w*])(" + re.escape(term) + r")(?![\w*])", re.IGNORECASE)
        m = pat.search(text)
        if m:
            s, e = m.span(1)
            text = text[:s] + "**" + text[s:e] + "**" + text[e:]
            used.add(term.lower())
    return text


def as_blockquote(block):
    return "\n".join("> " + l if l.strip() else ">" for l in block.splitlines())


def split_body_tail(blocks):
    for i, b in enumerate(blocks):
        if is_tail(b):
            return blocks[:i], blocks[i:]
    return blocks, []


def print_plan(body):
    """In cấu trúc khối phần thân theo từng mục (để viết vi/ khớp)."""
    print(f"PHẦN THÂN: {len(body)} khối\n")
    sec = "(mở đầu)"
    counts = {}
    idx = 0

    def flush():
        if counts:
            desc = ", ".join(f"{k}×{v}" for k, v in counts.items())
            print(f"  [{sec}] {sum(counts.values())} khối: {desc}")

    for b in body:
        k = kind(b)
        if k == "heading":
            flush()
            lvl, t = heading_text(b)
            sec = f"{'#'*len(lvl)} {t}"
            counts = {}
        else:
            counts[k] = counts.get(k, 0) + 1
        idx += 1
    flush()


def main():
    args = sys.argv[1:]
    plan = "--plan" in args
    args = [a for a in args if a != "--plan"]
    if len(args) != 2:
        sys.exit("Dùng: merge_bilingual.py <slug> <chNN> [--plan]")
    slug, ch = args
    book = ROOT / "books" / slug
    en_file = book / "en" / f"{ch}.md"
    if not en_file.exists():
        sys.exit(f"❌ Thiếu {en_file}")
    en_all = split_blocks(en_file.read_text(encoding="utf-8"))
    body_en, tail_en = split_body_tail(en_all)

    if plan:
        print_plan(body_en)
        print(f"\nPhần đuôi (giữ nguyên EN): {len(tail_en)} khối.")
        return

    vi_file = book / "vi" / f"{ch}.md"
    if not vi_file.exists():
        sys.exit(f"❌ Thiếu {vi_file}")
    vi_blocks = split_blocks(vi_file.read_text(encoding="utf-8"))

    if len(vi_blocks) != len(body_en):
        print(f"❌ Lệch số khối: en(thân)={len(body_en)} vs vi={len(vi_blocks)}", file=sys.stderr)
        print("   Cấu trúc phần thân EN để đối chiếu:", file=sys.stderr)
        print_plan(body_en)
        sys.exit(1)

    terms = load_glossary_terms(book)
    used = set()
    out = []
    for en, vi in zip(body_en, vi_blocks):
        k = kind(en)
        if k == "heading":
            eh, et = heading_text(en)
            _, vt = heading_text(vi)
            out.append(f"{eh} {et} — {vt}")
        elif k in ("code", "table", "image"):
            out.append(en)
        else:  # para / list
            out.append(bold_terms(en, terms, used))
            out.append(as_blockquote(vi))

    # Đuôi: References/Footnotes giữ nguyên tiếng Anh
    for b in tail_en:
        out.append(b)

    dest = book / "chapters" / f"{ch}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n\n".join(out) + "\n", encoding="utf-8")
    print(f"✅ {dest}  (thân {len(body_en)} khối song ngữ + đuôi {len(tail_en)} khối EN, tô đậm {len(used)} thuật ngữ)")


if __name__ == "__main__":
    main()
