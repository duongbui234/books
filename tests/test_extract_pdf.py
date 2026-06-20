import importlib.util
import unittest
from pathlib import Path


def load_extract_pdf():
    script = Path(__file__).resolve().parents[1] / "scripts" / "extract_pdf.py"
    spec = importlib.util.spec_from_file_location("extract_pdf", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExtractPdfTests(unittest.TestCase):
    def test_detects_footer_page_numbers_without_dropping_footnotes(self):
        extract_pdf = load_extract_pdf()

        self.assertTrue(extract_pdf.is_footer_page_number("3", 915, 918))
        self.assertTrue(extract_pdf.is_footer_page_number("xvii", 915, 918))
        self.assertFalse(extract_pdf.is_footer_page_number("1", 840, 918))
        self.assertFalse(extract_pdf.is_footer_page_number("Figure 1-1", 616, 918))

    def test_detects_running_headers_with_roman_or_arabic_page_numbers(self):
        extract_pdf = load_extract_pdf()

        self.assertTrue(extract_pdf.is_running_header_footer("Preface  |  xvii"))
        self.assertTrue(extract_pdf.is_running_header_footer("xviii  |  Preface"))
        self.assertTrue(extract_pdf.is_running_header_footer("4  |  Chapter 1: What Are Microservices?"))
        self.assertFalse(extract_pdf.is_running_header_footer("Request | Response"))


if __name__ == "__main__":
    unittest.main()
