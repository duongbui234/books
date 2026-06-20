#!/usr/bin/env python3
"""Translate extracted English Markdown into block-aligned Vietnamese Markdown.

The Markdown structure is preserved for headings and lists. Code, tables, and
images are represented by one placeholder block because merge_bilingual.py emits
the English source block once.

Usage:
  .venv-translate/bin/python scripts/translate_book.py building-microservices
  .venv-translate/bin/python scripts/translate_book.py building-microservices ch01
"""
import argparse
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MODEL = "vinai/vinai-translate-en2vi-v2"
os.environ.setdefault("HF_HOME", str(ROOT / ".hf-cache"))
os.environ.setdefault("DISABLE_SAFETENSORS_CONVERSION", "true")


def model_settings(model_name):
    if model_name.startswith("vinai/vinai-translate-en2vi"):
        return {
            "tokenizer_kwargs": {"src_lang": "en_XX"},
            "target_language": "vi_VN",
            "source_prefix": "",
            "max_input_tokens": 900,
            "num_beams": 5,
        }
    if model_name == "Helsinki-NLP/opus-mt-en-vi":
        return {
            "tokenizer_kwargs": {},
            "target_language": None,
            "source_prefix": ">>vie<< ",
            "max_input_tokens": 400,
            "num_beams": 4,
        }
    return {
        "tokenizer_kwargs": {},
        "target_language": None,
        "source_prefix": "",
        "max_input_tokens": 400,
        "num_beams": 4,
    }


def split_blocks(text):
    return [
        block.strip("\n")
        for block in re.split(r"\n[ \t]*\n", text.strip("\n"))
        if block.strip()
    ]


def block_kind(block):
    first = block.lstrip().splitlines()[0]
    if first.startswith("```"):
        return "code"
    if first.startswith("!["):
        return "image"
    if re.match(r"^#{1,6}\s", first):
        return "heading"
    lines = [line for line in block.splitlines() if line.strip()]
    if lines and all(line.lstrip().startswith("|") for line in lines):
        return "table"
    if lines and all(re.match(r"^\s*([-*+]|\d+\.)\s", line) for line in lines):
        return "list"
    return "para"


def protect_literals(text, protected_terms=()):
    patterns = [
        r"`[^`\n]+`",
        r"https?://[^\s)>]+",
        r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b",
    ]
    patterns.extend(
        rf"(?<!\w){re.escape(term)}(?!\w)"
        for term in sorted(set(protected_terms), key=len, reverse=True)
        if term
    )
    combined = re.compile("|".join(f"(?:{pattern})" for pattern in patterns), re.I)
    values = []

    def replace(match):
        marker = f"ZXQKEEP{len(values):04d}QXZ"
        values.append((marker, match.group(0)))
        return marker

    protected = combined.sub(replace, text)

    def restore(translated):
        for marker, value in values:
            translated = re.sub(re.escape(marker), value, translated, flags=re.I)
            translated = translated.replace(marker.replace("Q", " Q"), value)
        return translated

    return protected, restore


def load_protected_terms(glossary_path):
    terms = []
    if not glossary_path.exists():
        return terms
    for line in glossary_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 3 or cells[0].lower() in {"english", "term"}:
            continue
        if "giữ nguyên" not in cells[2].lower():
            continue
        terms.extend(part.strip() for part in cells[0].split("/") if part.strip())
    return terms


def translate_markdown(text, translate_many, protected_terms=()):
    blocks = split_blocks(text)
    units = []
    recipes = []

    for block in blocks:
        kind = block_kind(block)
        if kind in {"code", "image", "table"}:
            recipes.append((kind, None))
            continue
        if kind == "heading":
            match = re.match(r"^(#{1,6})\s+(.*)$", block.strip(), re.S)
            hashes, body = match.groups()
            protected, restore = protect_literals(body, protected_terms)
            recipes.append((kind, (hashes, len(units), restore)))
            units.append(protected)
            continue
        if kind == "list":
            items = []
            for line in block.splitlines():
                match = re.match(r"^(\s*(?:[-*+]|\d+\.)\s+)(.*)$", line)
                prefix, body = match.groups()
                protected, restore = protect_literals(body, protected_terms)
                items.append((prefix, len(units), restore))
                units.append(protected)
            recipes.append((kind, items))
            continue
        protected, restore = protect_literals(block, protected_terms)
        recipes.append((kind, (len(units), restore)))
        units.append(protected)

    translated = translate_many(units)
    if len(translated) != len(units):
        raise ValueError(
            f"Translator returned {len(translated)} results for {len(units)} inputs"
        )

    output = []
    for kind, recipe in recipes:
        if kind in {"code", "image", "table"}:
            output.append(f"<!-- {kind} -->")
        elif kind == "heading":
            hashes, index, restore = recipe
            output.append(f"{hashes} {restore(translated[index]).strip()}")
        elif kind == "list":
            output.append(
                "\n".join(
                    f"{prefix}{restore(translated[index]).strip()}"
                    for prefix, index, restore in recipe
                )
            )
        else:
            index, restore = recipe
            output.append(restore(translated[index]).strip())
    return "\n\n".join(output) + "\n"


def split_long_text(text, tokenizer, max_tokens=400):
    if len(tokenizer.encode(text, add_special_tokens=True)) <= max_tokens:
        return [text]
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks = []
    current = ""
    for sentence in sentences:
        candidate = f"{current} {sentence}".strip()
        if current and len(tokenizer.encode(candidate, add_special_tokens=True)) > max_tokens:
            chunks.append(current)
            current = sentence
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


class MarianTranslator:
    def __init__(self, model_name=DEFAULT_MODEL, batch_size=12):
        import torch
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        self.torch = torch
        self.batch_size = batch_size
        self.settings = model_settings(model_name)
        torch.set_num_threads(min(12, os.cpu_count() or 1))
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            **self.settings["tokenizer_kwargs"],
        )
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name,
            use_safetensors=False,
        )
        self.model.eval()

    def __call__(self, texts):
        chunks = []
        owners = []
        for owner, text in enumerate(texts):
            for chunk in split_long_text(
                text,
                self.tokenizer,
                self.settings["max_input_tokens"],
            ):
                chunks.append(f"{self.settings['source_prefix']}{chunk}")
                owners.append(owner)

        translated_chunks = []
        generation_kwargs = {
            "max_new_tokens": 1024,
            "num_beams": self.settings["num_beams"],
            "early_stopping": True,
        }
        target_language = self.settings["target_language"]
        if target_language:
            generation_kwargs["decoder_start_token_id"] = (
                self.tokenizer.lang_code_to_id[target_language]
            )
        with self.torch.inference_mode():
            for start in range(0, len(chunks), self.batch_size):
                batch = chunks[start : start + self.batch_size]
                encoded = self.tokenizer(
                    batch,
                    return_tensors="pt",
                    padding=True,
                    truncation=True,
                    max_length=self.settings["max_input_tokens"] + 100,
                )
                generated = self.model.generate(**encoded, **generation_kwargs)
                translated_chunks.extend(
                    self.tokenizer.batch_decode(generated, skip_special_tokens=True)
                )
                done = min(start + self.batch_size, len(chunks))
                print(f"  translated {done}/{len(chunks)} chunks", flush=True)

        results = [""] * len(texts)
        for owner, translated in zip(owners, translated_chunks):
            results[owner] = f"{results[owner]} {translated}".strip()
        return results


def chapter_ids(book, requested):
    if requested:
        return requested
    return [path.stem for path in sorted((book / "en").glob("ch*.md"))]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("chapters", nargs="*")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    book = ROOT / "books" / args.slug
    translator = MarianTranslator(args.model, args.batch_size)
    protected_terms = load_protected_terms(book / "glossary.md")
    (book / "vi").mkdir(parents=True, exist_ok=True)

    for chapter in chapter_ids(book, args.chapters):
        source = book / "en" / f"{chapter}.md"
        target = book / "vi" / f"{chapter}.md"
        if target.exists() and not args.overwrite:
            print(f"SKIP {target}")
            continue
        translated = translate_markdown(
            source.read_text(encoding="utf-8"),
            translator,
            protected_terms,
        )
        target.write_text(translated, encoding="utf-8")
        print(f"OK {target}")


if __name__ == "__main__":
    main()
