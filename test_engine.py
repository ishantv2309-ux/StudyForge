"""
Automated Unit Tests for AI Study Notes & Flashcard Generator Engine
"""
import unittest
import io
import pandas as pd
from pypdf import PdfWriter
from app import (
    clean_and_tokenize_sentences,
    extract_headings,
    compute_word_frequencies,
    extractive_summarization,
    extract_flashcards,
    extract_text_from_file,
    normalize_paragraphs,
    PRESETS,
    STOPWORDS
)

class MockUploadedFile:
    def __init__(self, name, data):
        self.name = name
        self._data = data

    def read(self):
        return self._data

class TestEngine(unittest.TestCase):
    def setUp(self):
        self.os_text = PRESETS["Operating Systems: Process Management & Deadlocks"]
        self.dsa_text = PRESETS["Data Structures & Algorithms: Trees, Graphs & Complexity"]
        self.dbms_text = PRESETS["DBMS: Relational Models & ACID Properties"]

    def test_sentence_tokenization(self):
        sentences = clean_and_tokenize_sentences(self.os_text)
        self.assertGreater(len(sentences), 8)
        for s in sentences:
            self.assertTrue(len(s) >= 10)

    def test_heading_extraction(self):
        headings_os = extract_headings(self.os_text)
        self.assertIn("Operating Systems: Process Management and Concurrency", headings_os)

        headings_dsa = extract_headings(self.dsa_text)
        self.assertTrue(any("Module 1" in h for h in headings_dsa))
        self.assertTrue(any("Module 2" in h for h in headings_dsa))

        headings_dbms = extract_headings(self.dbms_text)
        self.assertTrue(any("ACID Properties" in h for h in headings_dbms))

    def test_stopword_and_frequency(self):
        freq_dict, norm_weights = compute_word_frequencies(self.dsa_text)
        self.assertNotIn("the", freq_dict)
        self.assertNotIn("and", freq_dict)
        self.assertNotIn("is", freq_dict)
        self.assertTrue(any(term in freq_dict for term in ["tree", "graph", "algorithm"]))
        for w, weight in norm_weights.items():
            self.assertGreaterEqual(weight, 0.0)
            self.assertLessEqual(weight, 1.0)

    def test_extractive_summarization(self):
        sentences = clean_and_tokenize_sentences(self.dsa_text)
        _, norm_weights = compute_word_frequencies(self.dsa_text)
        summary = extractive_summarization(sentences, norm_weights, compression_ratio=0.35)
        self.assertGreater(len(summary), 0)
        self.assertLessEqual(len(summary), len(sentences))
        summary_indices = [sentences.index(s) for s in summary]
        self.assertEqual(summary_indices, sorted(summary_indices))

    def test_flashcard_generation(self):
        sentences = clean_and_tokenize_sentences(self.dsa_text)
        _, norm_weights = compute_word_frequencies(self.dsa_text)
        flashcards = extract_flashcards(sentences, norm_weights, raw_text=self.dsa_text)
        self.assertGreaterEqual(len(flashcards), 5)
        
        for card in flashcards:
            self.assertIn("Question", card)
            self.assertIn("Answer", card)
            self.assertIn("Pattern", card)
            self.assertIn("Key Concept", card)

        df = pd.DataFrame(flashcards)
        self.assertFalse(df.empty)
        csv_str = df.to_csv(index=False)
        self.assertIn("Question", csv_str)
        self.assertIn("Answer", csv_str)

    def test_text_and_pdf_ingestion(self):
        txt_file = MockUploadedFile("test_notes.txt", b"An Operating System is defined as system software that manages hardware.")
        text, meta = extract_text_from_file(txt_file)
        self.assertIn("Operating System", text)
        self.assertIn("test_notes.txt", meta)

        writer = PdfWriter()
        writer.add_blank_page(width=100, height=100)
        buf = io.BytesIO()
        writer.write(buf)
        pdf_file = MockUploadedFile("lecture.pdf", buf.getvalue())
        text_pdf, meta_pdf = extract_text_from_file(pdf_file)
        self.assertIn("lecture.pdf", meta_pdf)

    def test_paragraph_unwrapping_and_heading_blocks(self):
        broken_pdf_text = """
        Operating Systems: Concurrency

        An Operating System is soft-
        ware that manages computer hardware and software
        resources for all applications.

        Deadlock:
        A permanent blocking situation where processes wait
        indefinitely for resources held by each other.
        """
        normalized = normalize_paragraphs(broken_pdf_text)
        self.assertIn("software", normalized)
        self.assertNotIn("soft-\n", normalized)

        sentences = clean_and_tokenize_sentences(broken_pdf_text)
        _, norm_weights = compute_word_frequencies(broken_pdf_text)
        flashcards = extract_flashcards(sentences, norm_weights, raw_text=broken_pdf_text)
        
        # Verify Deadlock was captured as a flashcard
        concepts = [c["Key Concept"].lower() for c in flashcards]
        self.assertTrue(any("deadlock" in c for c in concepts))

if __name__ == "__main__":
    unittest.main()
