#!/usr/bin/env python3
"""Chia phần THÂN của en/chNN.md thành lát để dịch song song, rồi ghép lại.

Bản dịch phải khớp TỪNG KHỐI với bản gốc (xem merge_bilingual.py). Khi nhiều
người/agent cùng dịch một chương, cách an toàn là đánh số khối: mỗi khối được
bọc bởi một dấu mốc `⟦n⟧`, bản dịch giữ nguyên dấu mốc đó. Lúc ghép, script
kiểm tra đủ và đúng thứ tự các số rồi mới gỡ mốc — lệch khối bị bắt ngay tại
đúng vị trí thay vì chỉ báo "lệch tổng số".

Dùng:
  slice_blocks.py plan  <slug> [--max N]     # in kế hoạch lát (JSON) cho cả sách
  slice_blocks.py show  <slug> <chNN> <i> <j>  # in khối [i, j) kèm dấu mốc
  slice_blocks.py showidx <slug> <chNN> 3,7,9  # in đúng các khối rời rạc
  slice_blocks.py build <slug> <chNN>         # ghép vi/parts/<chNN>.*.md -> vi/<chNN>.md
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from merge_bilingual import split_blocks, split_body_tail, kind  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MARK = re.compile(r"^⟦(\d+)⟧\s*$")
PLACEHOLDER = {"code": "<!-- code -->", "image": "<!-- image -->",
               "table": "<!-- table -->"}


def body_blocks(slug, ch):
    f = ROOT / "books" / slug / "en" / f"{ch}.md"
    if not f.exists():
        sys.exit(f"❌ Thiếu {f}")
    return split_body_tail(split_blocks(f.read_text(encoding="utf-8")))[0]


def cmd_plan(slug, max_blocks):
    """Chia mỗi chương thành lát <= max_blocks, cắt ưu tiên ngay trước heading."""
    out = []
    for f in sorted((ROOT / "books" / slug / "en").glob("*.md")):
        ch = f.stem
        body = body_blocks(slug, ch)
        if not body:
            continue  # vd Bibliography: toàn phần đuôi, giữ nguyên tiếng Anh
        heads = {i for i, b in enumerate(body) if kind(b) == "heading"}
        cuts, start = [], 0
        while len(body) - start > max_blocks:
            hard = start + max_blocks
            # lùi về heading gần nhất để lát không cắt ngang một mục
            soft = max((h for h in heads if start + max_blocks // 2 < h <= hard),
                       default=hard)
            cuts.append((start, soft))
            start = soft
        cuts.append((start, len(body)))
        for n, (i, j) in enumerate(cuts, 1):
            out.append({"ch": ch, "part": f"{n:02d}", "start": i, "end": j,
                        "blocks": j - i,
                        "words": sum(len(body[k].split()) for k in range(i, j))})
    print(json.dumps(out, ensure_ascii=False))


def cmd_show(slug, ch, i, j):
    body = body_blocks(slug, ch)
    i, j = max(0, i), min(len(body), j)
    print(f"# CHƯƠNG {ch} — khối {i}..{j - 1} (tổng thân {len(body)} khối)\n")
    for n in range(i, j):
        b = body[n]
        k = kind(b)
        print(f"⟦{n}⟧")
        if k in PLACEHOLDER:
            print(f"[{k.upper()} — bản dịch chỉ cần ghi: {PLACEHOLDER[k]}]")
        else:
            print(b)
        print()


def cmd_showidx(slug, ch, idxs):
    """In các khối RỜI RẠC theo chỉ số — dùng khi chỉ cần dịch bù vài khối."""
    body = body_blocks(slug, ch)
    print(f"# CHƯƠNG {ch} — {len(idxs)} khối cần dịch (tổng thân {len(body)} khối)\n")
    for n in idxs:
        if not 0 <= n < len(body):
            sys.exit(f"❌ chỉ số ngoài phạm vi: {n}")
        b, k = body[n], kind(body[n])
        print(f"⟦{n}⟧")
        print(f"[{k.upper()} — bản dịch chỉ cần ghi: {PLACEHOLDER[k]}]" if k in PLACEHOLDER else b)
        print()


def cmd_build(slug, ch):
    book = ROOT / "books" / slug
    body = body_blocks(slug, ch)
    parts = sorted((book / "vi" / "parts").glob(f"{ch}.*.md"))
    if not parts:
        sys.exit(f"❌ Không thấy lát nào: {book}/vi/parts/{ch}.*.md")

    got = {}
    for p in parts:
        cur, buf = None, []
        for line in p.read_text(encoding="utf-8").splitlines():
            m = MARK.match(line)
            if m:
                if cur is not None:
                    got[cur] = "\n".join(buf).strip("\n")
                cur, buf = int(m.group(1)), []
            elif cur is not None:
                buf.append(line)
        if cur is not None:
            got[cur] = "\n".join(buf).strip("\n")

    missing = [n for n in range(len(body)) if n not in got or not got[n].strip()]
    extra = sorted(n for n in got if n >= len(body))
    if missing or extra:
        print(f"❌ {ch}: thân EN {len(body)} khối, bản dịch có {len(got)}", file=sys.stderr)
        if missing:
            print(f"   thiếu/rỗng: {missing[:20]}{' …' if len(missing) > 20 else ''}",
                  file=sys.stderr)
        if extra:
            print(f"   thừa: {extra[:20]}", file=sys.stderr)
        sys.exit(1)

    # khối code/ảnh/bảng phải là placeholder đúng quy ước, không phải bản dịch
    fixed = 0
    for n, b in enumerate(body):
        k = kind(b)
        if k in PLACEHOLDER and got[n].strip() != PLACEHOLDER[k]:
            got[n] = PLACEHOLDER[k]
            fixed += 1

    dest = book / "vi" / f"{ch}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n\n".join(got[n] for n in range(len(body))) + "\n",
                    encoding="utf-8")
    note = f", chuẩn hoá {fixed} placeholder" if fixed else ""
    print(f"✅ {dest}  ({len(body)} khối từ {len(parts)} lát{note})")


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "plan":
        mx = int(a[a.index("--max") + 1]) if "--max" in a else 120
        cmd_plan(a[1], mx)
    elif a[0] == "show":
        cmd_show(a[1], a[2], int(a[3]), int(a[4]))
    elif a[0] == "showidx":
        cmd_showidx(a[1], a[2], [int(x) for x in a[3].split(",") if x != ""])
    elif a[0] == "build":
        cmd_build(a[1], a[2])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
