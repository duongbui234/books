#!/usr/bin/env python3
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GLOSSARY_PATH = ROOT / "books" / "ddia" / "glossary.md"

def load_glossary(glossary_path):
    pairs = []
    if not glossary_path.exists():
        return pairs
    for line in glossary_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        en_col = cells[0].strip()
        vi_col = cells[1].strip()
        if en_col.lower() in ("english", "term", "") or set(en_col) <= set("-: "):
            continue
        
        # Clean EN
        en_clean = re.sub(r"\([^)]*\)", "", en_col).strip()
        en_terms = [e.strip().lower() for e in re.split(r"[/]", en_clean) if e.strip()]
        
        # Clean VI
        vi_no_parens = re.sub(r"\([^)]*\)", "", vi_col).strip()
        vi_with_parens_cleaned = re.sub(r"[()]", "", vi_col).strip()
        
        vi_options = []
        for text in [vi_no_parens, vi_with_parens_cleaned, vi_col]:
            for option in re.split(r"[/;,]", text):
                opt = option.strip().lower()
                if opt and opt not in vi_options:
                    vi_options.append(opt)
                opt_no_prefix = re.sub(r"^(tính|sự|việc|hệ thống)\s+", "", opt).strip()
                if opt_no_prefix and opt_no_prefix not in vi_options:
                    vi_options.append(opt_no_prefix)

        for en in en_terms:
            if len(en) >= 3:
                pairs.append((en, vi_options, en_col, vi_col))
    return pairs

def split_blocks(text):
    blocks = re.split(r"\n[ \t]*\n", text.strip("\n"))
    return [b.strip("\n") for b in blocks if b.strip()]

def kind(block):
    first = block.lstrip().splitlines()[0] if block.strip() else ""
    if first.startswith("```"):
        return "code"
    if re.match(r"^#{1,6}\s", first):
        return "heading"
    lines = [l for l in block.splitlines() if l.strip()]
    if lines and all(l.lstrip().startswith("|") for l in lines):
        return "table"
    if lines and all(re.match(r"^\s*([-*+]|\d+\.)\s", l) for l in lines):
        return "list"
    return "para"

def is_tail(block):
    if kind(block) != "heading":
        return False
    first = block.lstrip().splitlines()[0] if block.strip() else ""
    m = re.match(r"^(#{1,6})\s+(.*)$", first.strip())
    t = m.group(2).strip() if m else first.strip()
    return t.lower().lstrip("#").strip() in ("references", "footnotes", "bibliography")

def split_body_tail(blocks):
    for i, b in enumerate(blocks):
        if is_tail(b):
            return blocks[:i], blocks[i:]
    return blocks, []

def is_false_positive(en_term, en_block, vi_block):
    en_b_low = en_block.lower()
    vi_b_low = vi_block.lower()
    
    # 1. Heuristics for 'mean'
    if en_term == "mean":
        # Check if it's the verb "mean that", "mean to", "does not mean", "means", "meaning"
        # and not part of mathematical mean or "mean time to failure"
        if "mean time" in en_b_low:
            return False  # Real term
        # If it's a verb: "means", "meaning", "mean to", "mean that", "does not mean", "doesn't mean"
        if re.search(r"\b(means|meaning|mean\s+(that|to|a\s+lot|nothing|anything|something|the\s+limits|keeping|reducing|making))\b", en_b_low):
            return True
        if "does not mean" in en_b_low or "doesn't mean" in en_b_low or "not mean" in en_b_low:
            return True
        # If "average" is not in paragraph and "mean" is used generally
        if "average" not in en_b_low and "arithmetic" not in en_b_low:
            return True

    # 2. Heuristics for 'subject'
    if en_term == "subject":
        # "subject" is RDF triple subject. If not in RDF context, it's "chủ đề" or "phụ thuộc vào"
        rdf_context = any(w in en_b_low for w in ["triple", "predicate", "object", "rdf", "sparql", "datalog", "graph"])
        if not rdf_context:
            return True

    # 3. Heuristics for 'edge'
    if en_term == "edge":
        # Check if it's "edge case" (which is mapped to "trường hợp biên")
        # If "edge case" is in English, and "trường hợp biên" or "biên" is in Vietnamese, it's correct.
        if "edge case" in en_b_low:
            if "biên" in vi_b_low or "trường hợp biên" in vi_b_low:
                return True
        # If not in graph context, ignore edge
        graph_context = any(w in en_b_low for w in ["vertex", "vertices", "graph", "node", "relationship", "network"])
        if not graph_context:
            return True

    # 4. Contextual synonyms for 'failure'
    if en_term == "failure":
        # If Vietnamese has "hỏng", "sự cố", "lỗi", or "thất bại", it's fine.
        if any(w in vi_b_low for w in ["hỏng", "sự cố", "lỗi", "thất bại"]):
            return True

    # 5. Contextual synonyms for 'join'
    if en_term == "join":
        # "join" is often kept as "join" in Vietnamese (e.g. "phép join", "thao tác join", "không-cần-join")
        if "join" in vi_b_low:
            return True

    # 6. Contextual synonyms for 'load'
    if en_term == "load":
        # "load" can be a verb "nạp" or "tải lên". Accept "nạp" or "tải"
        if any(w in vi_b_low for w in ["nạp", "tải"]):
            return True

    # 7. Contextual synonyms for 'cache'
    if en_term == "cache":
        if any(w in vi_b_low for w in ["bộ đệm", "bộ nhớ đệm", "cache", "lưu đệm"]):
            return True

    # 8. Contextual synonyms for 'table'
    if en_term == "table":
        # "table" is often part of SSTable or hash table. Accept "bảng" or "sstable"
        if any(w in vi_b_low for w in ["bảng", "sstable"]):
            return True

    # 9. Contextual synonyms for 'instance'
    if en_term == "instance":
        # Accept "phiên bản", "trường hợp", "instance"
        if any(w in vi_b_low for w in ["phiên bản", "trường hợp", "instance"]):
            return True

    # 10. Contextual synonyms for 'client'
    if en_term == "client":
        if any(w in vi_b_low for w in ["client", "máy khách"]):
            return True

    # 11. Contextual synonyms for 'database'
    if en_term == "database":
        if any(w in vi_b_low for w in ["cơ sở dữ liệu", "database"]):
            return True

    # 12. Contextual synonyms for 'document'
    if en_term == "document":
        if any(w in vi_b_low for w in ["tài liệu", "document"]):
            return True

    # 13. Contextual synonyms for 'relation'
    if en_term == "relation":
        # "relation" in relational model can be translated as "quan hệ" or "bảng"
        if any(w in vi_b_low for w in ["quan hệ", "bảng"]):
            return True

    # 14. Contextual synonyms for 'abstraction'
    if en_term == "abstraction":
        if any(w in vi_b_low for w in ["trừu tượng", "trừu tượng hóa"]):
            return True

    return False

def check_chapter(slug, ch_num, glossary_pairs):
    book_dir = ROOT / "books" / slug
    en_file = book_dir / "en" / f"ch{ch_num:02d}.md"
    vi_file = book_dir / "vi" / f"ch{ch_num:02d}.md"
    
    if not en_file.exists() or not vi_file.exists():
        return None, f"Thiếu file cho chương {ch_num}"
        
    en_blocks = split_blocks(en_file.read_text(encoding="utf-8"))
    vi_blocks = split_blocks(vi_file.read_text(encoding="utf-8"))
    
    body_en, _ = split_body_tail(en_blocks)
    
    if len(body_en) != len(vi_blocks):
        return None, f"Lệch số khối thân: en={len(body_en)} vs vi={len(vi_blocks)}"
        
    mismatches = []
    for idx, (en_b, vi_b) in enumerate(zip(body_en, vi_blocks)):
        k = kind(en_b)
        if k in ("code", "table"):
            continue
            
        # Scan glossary
        for en_term, vi_options, original_en, original_vi in glossary_pairs:
            # Word boundary search for English
            if "-" in en_term:
                has_en = en_term in en_b.lower()
            else:
                has_en = bool(re.search(r"\b" + re.escape(en_term) + r"\b", en_b, re.IGNORECASE))
                
            if has_en:
                # First check if the standard translation options are present
                has_vi = False
                for vi_opt in vi_options:
                    if vi_opt in vi_b.lower():
                        has_vi = True
                        break
                
                # If not present, check semantic/contextual heuristics to filter out false positives
                if not has_vi:
                    if is_false_positive(en_term, en_b, vi_b):
                        continue
                    
                    mismatches.append({
                        "block_idx": idx,
                        "kind": k,
                        "en_term": en_term,
                        "original_en": original_en,
                        "original_vi": original_vi,
                        "en_text_snippet": en_b.replace("\n", " ")[:100] + "...",
                        "vi_text_snippet": vi_b.replace("\n", " ")[:100] + "..."
                    })
                    
    return mismatches, None

def main():
    slug = "ddia"
    print("📖 Đang nạp bảng thuật ngữ...")
    glossary_pairs = load_glossary(GLOSSARY_PATH)
    print(f"Loaded {len(glossary_pairs)} thuật ngữ từ glossary.md.\n")
    
    report = []
    report.append("# Báo cáo rà soát thuật ngữ chuyên ngành (Bilingual Terminology Check - Lọc Thực Tế)\n")
    report.append("Báo cáo tự động đối chiếu từ [glossary.md](file:///home/ddevtk/code/translate_book/books/ddia/glossary.md) với toàn bộ 12 chương sách sau khi đã lọc bỏ các cảnh báo giả do đa nghĩa hoặc biến thể dịch từ loại.\n")
    
    total_warnings = 0
    
    for ch in range(1, 13):
        print(f"Checking Chương {ch:02d}...")
        mismatches, error = check_chapter(slug, ch, glossary_pairs)
        if error:
            print(f"  ❌ Lỗi: {error}")
            report.append(f"## Chương {ch:02d}\n")
            report.append(f"❌ **Lỗi cấu trúc:** {error}\n")
            continue
            
        if not mismatches:
            print(f"  ✅ Chương {ch:02d} khớp hoàn toàn thuật ngữ chuyên ngành.")
            report.append(f"## Chương {ch:02d}\n")
            report.append("✅ **Hoàn hảo:** Không phát hiện sai lệch thuật ngữ chuyên ngành thực tế nào.\n")
        else:
            print(f"  ⚠️  Chương {ch:02d} phát hiện {len(mismatches)} điểm cần kiểm tra.")
            total_warnings += len(mismatches)
            report.append(f"## Chương {ch:02d} (Cảnh báo thực tế: {len(mismatches)})\n")
            report.append("| Khối | Thuật ngữ gốc (EN) | Bản dịch yêu cầu (VI) | Ngữ cảnh Tiếng Anh | Bản dịch Tiếng Việt thực tế |\n")
            report.append("|---|---|---|---|---|\n")
            for m in mismatches:
                report.append(f"| Khối {m['block_idx']} | `{m['original_en']}` | `{m['original_vi']}` | *{m['en_text_snippet']}* | {m['vi_text_snippet']} |\n")
            report.append("\n")
            
    report_file = ROOT / "term_validation_report.md"
    report_file.write_text("\n".join(report), encoding="utf-8")
    print(f"\n📊 Đã hoàn thành! Tìm thấy tổng cộng {total_warnings} cảnh báo thuật ngữ thực tế sau khi lọc.")
    print(f"📝 Báo cáo chi tiết đã được cập nhật tại tệp: {report_file}")

if __name__ == "__main__":
    main()
