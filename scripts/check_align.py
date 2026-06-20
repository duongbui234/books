#!/usr/bin/env python3
"""Kiểm tra căn khối giữa en/chNN.md (phần thân) và vi/chNN.md.

In rõ: số khối hai bên; nếu lệch, chỉ ra CHỈ SỐ KHỐI ĐẦU TIÊN bị lệch loại
(heading/para/list/code/table) kèm ngữ cảnh, để dễ sửa vi/ cho khớp.

Dùng: check_align.py <slug> <chNN>
  vd:  check_align.py ddia ch03
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAIL = ("references", "footnotes", "bibliography", "reference materials",
        "further reading", "additional resources")


def split_blocks(t):
    return [b.strip("\n") for b in re.split(r"\n[ \t]*\n", t.strip("\n")) if b.strip()]


def kind(b):
    f = b.lstrip().splitlines()[0] if b.strip() else ""
    if f.startswith("```"):
        return "code"
    if f.startswith("!["):
        return "image"
    if re.match(r"^#{1,6}\s", f):
        return "heading"
    lines = [l for l in b.splitlines() if l.strip()]
    if lines and all(l.lstrip().startswith("|") for l in lines):
        return "table"
    if lines and all(re.match(r"^\s*([-*+]|\d+\.)\s", l) for l in lines):
        return "list"
    return "para"


def is_tail(b):
    if kind(b) != "heading":
        return False
    m = re.match(r"^#{1,6}\s+(.*)$", b.strip())
    return bool(m) and m.group(1).strip().lower() in TAIL


def main():
    if len(sys.argv) != 3:
        sys.exit("Dùng: check_align.py <slug> <chNN>")
    slug, ch = sys.argv[1], sys.argv[2]
    book = ROOT / "books" / slug
    en_file, vi_file = book / "en" / f"{ch}.md", book / "vi" / f"{ch}.md"
    if not en_file.exists():
        sys.exit(f"❌ Thiếu {en_file}")
    if not vi_file.exists():
        sys.exit(f"❌ Thiếu {vi_file}")
    en = split_blocks(en_file.read_text(encoding="utf-8"))
    body = []
    for b in en:
        if is_tail(b):
            break
        body.append(b)
    vi = split_blocks(vi_file.read_text(encoding="utf-8"))

    if len(body) == len(vi):
        # cảnh báo nhẹ nếu loại khối lệch (ví dụ list dịch thành para)
        warns = [(i, kind(body[i]), kind(vi[i])) for i in range(len(body))
                 if kind(body[i]) != kind(vi[i])
                 and not (kind(body[i]) in ("code", "table", "image"))]
        print(f"✅ KHỚP: {len(body)} khối thân (en) == {len(vi)} khối (vi)")
        if warns:
            print(f"⚠️  {len(warns)} khối khác LOẠI (có thể ổn nếu cố ý):")
            for i, ke, kv in warns[:12]:
                print(f"   khối {i}: en={ke} vi={kv} | en: {body[i][:50]!r}")
        return

    print(f"❌ LỆCH: en(thân)={len(body)}  vi={len(vi)}  (chênh {len(vi)-len(body):+d})")
    n = min(len(body), len(vi))
    # code/table/image trong vi là placeholder (para) -> không tính lệch loại
    first = next((i for i in range(n)
                  if kind(body[i]) != kind(vi[i])
                  and kind(body[i]) not in ("code", "table", "image")), n)
    print(f"   Khối đầu tiên lệch LOẠI: index {first}")
    lo, hi = max(0, first - 2), min(n, first + 3)
    for i in range(lo, hi):
        be = f"{kind(body[i])}: {body[i].splitlines()[0][:54]}" if i < len(body) else "—"
        bv = f"{kind(vi[i])}: {vi[i].splitlines()[0][:54]}" if i < len(vi) else "—"
        mark = "  <<<" if i == first else ""
        print(f"   [{i}] EN {be}")
        print(f"       VI {bv}{mark}")
    sys.exit(1)


if __name__ == "__main__":
    main()
