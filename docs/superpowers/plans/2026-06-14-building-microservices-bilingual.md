# Building Microservices Bilingual Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a complete English-Vietnamese bilingual version of `Building Microservices, Second Edition` matching the existing Node.js Design Patterns motif.

**Architecture:** Use the existing multi-book pipeline: `books/building-microservices/en/` holds clean English extracted from the owned PDF, `vi/` holds aligned Vietnamese blocks, `chapters/` holds merged bilingual Markdown, and `output/` holds built artifacts. Because the source is PDF-only, extract images and English with `scripts/extract_pdf.py` and build PDF-first like the other PDF-only books.

**Tech Stack:** Poppler (`pdftotext`, `pdftohtml`), existing Python scripts (`extract_pdf.py`, `check_align.py`, `merge_bilingual.py`), Pandoc, XeLaTeX.

---

### Task 1: Skeleton and Metadata

**Files:**
- Create: `books/building-microservices/meta.yaml`
- Create: `books/building-microservices/glossary.md`
- Create/link: `books/building-microservices/source.pdf`
- Create directories: `books/building-microservices/{en,vi,chapters,images,output}`

- [x] **Step 1: Create the standard book folder**

Run:

```bash
mkdir -p books/building-microservices/{en,vi,chapters,images,output}
```

- [x] **Step 2: Link the source PDF**

Run:

```bash
ln 'books/Sam Newman - Building Microservices_ Designing Fine-Grained Systems - O′Reilly (2021)/source.pdf' books/building-microservices/source.pdf
```

Expected: `books/building-microservices/source.pdf` exists and has the same inode/link count as the original when hard-linking succeeds.

- [x] **Step 3: Add metadata and glossary**

Add `meta.yaml` and `glossary.md` following the existing `books/nodejs-design-patterns` style.

### Task 2: Extract English Chapters

**Files:**
- Create: `books/building-microservices/en/ch00.md` through `books/building-microservices/en/ch17.md`
- Create: `books/building-microservices/images/*`

- [ ] **Step 1: Use verified PDF page ranges**

Use these ranges:

```text
ch00 Preface: PDF 19-26
ch01 What Are Microservices?: PDF 29-60
ch02 How to Model Microservices: PDF 61-95
ch03 Splitting the Monolith: PDF 97-112
ch04 Microservice Communication Styles: PDF 115-143
ch05 Implementing Microservice Communication: PDF 147-196
ch06 Workflow: PDF 197-222
ch07 Build: PDF 223-243
ch08 Deployment: PDF 245-299
ch09 Testing: PDF 301-329
ch10 From Monitoring to Observability: PDF 331-368
ch11 Security: PDF 371-412
ch12 Resiliency: PDF 413-443
ch13 Scaling: PDF 445-477
ch14 User Interfaces: PDF 481-516
ch15 Organizational Structures: PDF 517-550
ch16 The Evolutionary Architect: PDF 551-574
ch17 Afterword: PDF 577-588
```

- [ ] **Step 2: Run the PDF extractor**

Run one command per chapter:

```bash
python3 scripts/extract_pdf.py building-microservices ch01 29 60 --head-size 18 --head-no-bold
```

Use the matching chapter id and page range from Step 1.

- [ ] **Step 3: Inspect samples**

Run:

```bash
sed -n '1,80p' books/building-microservices/en/ch01.md
python3 scripts/merge_bilingual.py building-microservices ch01 --plan
```

Expected: headings, paragraphs, lists, code, figures, and note/caution blocks are recognizable and no running headers dominate the output.

### Task 3: Translate Aligned Vietnamese Chapters

**Files:**
- Create: `books/building-microservices/vi/ch00.md` through `books/building-microservices/vi/ch17.md`

- [ ] **Step 1: Translate each English body block**

For each `en/chNN.md`, write `vi/chNN.md` with the same block count and order. Preserve placeholders for code/image/table blocks only when needed for alignment; `merge_bilingual.py` will render code/image/table from English once.

- [ ] **Step 2: Validate alignment per chapter**

Run after each translated chapter:

```bash
python3 scripts/check_align.py building-microservices chNN
```

Expected: `✅ KHỚP`.

### Task 4: Merge and Build

**Files:**
- Create: `books/building-microservices/chapters/ch00.md` through `books/building-microservices/chapters/ch17.md`
- Create: `books/building-microservices/output/building-microservices-song-ngu.pdf`
- Optionally create: `books/building-microservices/output/building-microservices-song-ngu.epub`

- [ ] **Step 1: Merge each chapter**

Run:

```bash
for ch in ch00 ch01 ch02 ch03 ch04 ch05 ch06 ch07 ch08 ch09 ch10 ch11 ch12 ch13 ch14 ch15 ch16 ch17; do
  python3 scripts/merge_bilingual.py building-microservices "$ch"
done
```

- [ ] **Step 2: Build outputs**

Run:

```bash
bash scripts/build.sh building-microservices --pdf-only
```

Expected: PDF exists under `books/building-microservices/output/`. EPUB may be added only after confirming image references and layout are suitable.

### Task 5: Final Verification

**Files:**
- Inspect: `books/building-microservices/output/`
- Inspect: generated `chapters/*.md`

- [ ] **Step 1: Verify all expected files exist**

Run:

```bash
find books/building-microservices/{en,vi,chapters} -maxdepth 1 -type f | sort
ls -lh books/building-microservices/output
```

- [ ] **Step 2: Re-run alignment checks**

Run:

```bash
for ch in ch00 ch01 ch02 ch03 ch04 ch05 ch06 ch07 ch08 ch09 ch10 ch11 ch12 ch13 ch14 ch15 ch16 ch17; do
  python3 scripts/check_align.py building-microservices "$ch"
done
```

Expected: every chapter reports `✅ KHỚP`.

- [ ] **Step 3: Smoke-check generated PDF**

Run:

```bash
pdfinfo books/building-microservices/output/building-microservices-song-ngu.pdf
```

Expected: `Title: Building Microservices` and a nonzero page count.
