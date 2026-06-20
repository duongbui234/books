import importlib.util
import unittest
from pathlib import Path


def load_translate_book():
    script = Path(__file__).resolve().parents[1] / "scripts" / "translate_book.py"
    spec = importlib.util.spec_from_file_location("translate_book", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TranslateBookTests(unittest.TestCase):
    def test_translates_markdown_blocks_without_changing_alignment(self):
        translate_book = load_translate_book()
        source = """# Chapter One

An API uses `HTTP` at https://example.com.

- First item
- Second item

![](images/example.png)

```js
console.log("hello")
```
"""

        def fake_translate(texts):
            return [f"VI:{text}" for text in texts]

        result = translate_book.translate_markdown(source, fake_translate)
        blocks = translate_book.split_blocks(result)

        self.assertEqual(len(blocks), 5)
        self.assertEqual(blocks[0], "# VI:Chapter One")
        self.assertEqual(
            blocks[1],
            "VI:An API uses `HTTP` at https://example.com.",
        )
        self.assertEqual(blocks[2], "- VI:First item\n- VI:Second item")
        self.assertEqual(blocks[3], "<!-- image -->")
        self.assertEqual(blocks[4], "<!-- code -->")

    def test_protects_glossary_terms_and_literals_from_translation(self):
        translate_book = load_translate_book()

        protected, restore = translate_book.protect_literals(
            "A microservice calls `kubectl` at https://example.com.",
            ["microservice"],
        )

        self.assertNotIn("microservice", protected)
        self.assertNotIn("`kubectl`", protected)
        self.assertNotIn("https://example.com", protected)
        self.assertEqual(restore(protected), "A microservice calls `kubectl` at https://example.com.")

    def test_uses_vinai_language_codes(self):
        translate_book = load_translate_book()

        settings = translate_book.model_settings("vinai/vinai-translate-en2vi-v2")

        self.assertEqual(settings["tokenizer_kwargs"], {"src_lang": "en_XX"})
        self.assertEqual(settings["target_language"], "vi_VN")
        self.assertEqual(settings["max_input_tokens"], 900)


if __name__ == "__main__":
    unittest.main()
