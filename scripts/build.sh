#!/usr/bin/env bash
# Build PDF + EPUB song ngữ từ books/<slug>/chapters/*.md
# Dùng: scripts/build.sh <slug> [--pdf-only]   (vd: scripts/build.sh ddia)
set -euo pipefail

SLUG="${1:-}"
[ -z "$SLUG" ] && { echo "Dùng: build.sh <slug> [--pdf-only]"; exit 1; }
PDF_ONLY=0
[ "${2:-}" = "--pdf-only" ] && PDF_ONLY=1

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BOOK="$ROOT/books/$SLUG"
[ -d "$BOOK" ] || { echo "❌ Không thấy sách: $BOOK"; exit 1; }
command -v pandoc >/dev/null || { echo "❌ Thiếu pandoc"; exit 1; }

shopt -s nullglob
CHAPTERS=("$BOOK"/chapters/*.md)
[ ${#CHAPTERS[@]} -gt 0 ] || { echo "❌ Chưa có chương nào trong $BOOK/chapters/"; exit 1; }

OUT="$BOOK/output"; mkdir -p "$OUT"
META="$BOOK/meta.yaml"
echo "📚 $SLUG — ${#CHAPTERS[@]} chương"

# Sách kỹ thuật: '$' (shell/awk/giá tiền) và '\' trong văn xuôi KHÔNG phải LaTeX.
# Tắt diễn giải toán '$...$', '\(...\)' và raw TeX để xelatex không vỡ.
FMT="markdown-tex_math_dollars-tex_math_single_backslash-tex_math_double_backslash-raw_tex"

if [ "$PDF_ONLY" = "0" ]; then
  echo "📘 EPUB…"
  pandoc -f "$FMT" "$META" "${CHAPTERS[@]}" \
    -o "$OUT/$SLUG-song-ngu.epub" \
    --toc --toc-depth=2 \
    --css "$ROOT/templates/epub.css" \
    --resource-path ".:$BOOK" \
    --metadata lang=vi
fi

if command -v xelatex >/dev/null; then
  echo "📕 PDF…"
  pandoc -f "$FMT" "$META" "${CHAPTERS[@]}" \
    -o "$OUT/$SLUG-song-ngu.pdf" \
    --pdf-engine=xelatex \
    --resource-path ".:$BOOK" \
    --toc --toc-depth=2 \
    -V documentclass=report \
    -V mainfont="Noto Serif" \
    -V monofont="Noto Sans Mono" \
    -V lang=vi \
    -V geometry:margin=2.5cm \
    -H "$ROOT/templates/pdf-header.tex"
else
  echo "⚠️  Không có xelatex — bỏ qua PDF."
fi

echo "✅ Xong:"
ls -lh "$OUT"
