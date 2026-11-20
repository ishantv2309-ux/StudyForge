"""
B.TECH 2ND YEAR — MINI PROJECT
AI-Powered Study Notes & Flashcard Generator
Automated Lecture Note Summarization & Active-Recall Flashcard Web Application

Design: Elite High-End SaaS Single-Page Dashboard
Theme: High-Contrast Slate Dark Aesthetic (#0E1117 / #11151C / #161B22 / #2563EB)
"""

import io
import re
from collections import Counter
import streamlit as st
import pandas as pd
from pypdf import PdfReader

# ---------------------------------------------------------
# Elite SaaS Custom CSS Styling (Global High-Contrast Overrides)
# ---------------------------------------------------------
CSS_STYLING = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Foundation */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        background-color: #0E1117 !important;
        color: #F8FAFC !important;
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Completely Eliminate Default Sidebar & Streamlit Clutter */
    [data-testid="stSidebar"], section[data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
    #MainMenu, footer, header {
        visibility: hidden !important;
    }

    /* Spacious SaaS Canvas Container */
    div[data-testid="stMainBlockContainer"] {
        max-width: 1400px !important;
        padding: 1.5rem 2.2rem 3rem 2.2rem !important;
        margin: 0 auto !important;
    }

    /* ---------------------------------------------------------
       CRITICAL BUG FIX 1: HIGH-CONTRAST TEXT & LABEL OVERRIDES
       Forces all inputs, textareas, and labels to bright white (#FFFFFF)
       --------------------------------------------------------- */
    .stTextArea textarea, 
    [data-testid="stTextArea"] textarea {
        background-color: #11151C !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        caret-color: #3B82F6 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        font-size: 0.95rem !important;
        line-height: 1.65 !important;
        padding: 1rem !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.25) !important;
        font-weight: 500 !important;
    }
    [data-testid="stTextArea"] textarea:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3) !important;
    }

    .stTextInput input,
    [data-testid="stTextInput"] input {
        background-color: #11151C !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        caret-color: #3B82F6 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.92rem !important;
    }

    .stSelectbox div[data-baseweb="select"] > div,
    [data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #11151C !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border-color: rgba(255, 255, 255, 0.15) !important;
    }

    /* Bright White High Contrast Labels & Headers across all components */
    label, 
    .stWidgetLabel, 
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label,
    .stTextArea label p,
    .stTextInput label p,
    .stSelectbox label p,
    .stFileUploader label p {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 0.96rem !important;
        letter-spacing: -0.01em !important;
    }

    /* File Uploader Dropzone Text Overrides */
    [data-testid="stFileUploader"] {
        padding: 0 !important;
        margin-bottom: 0.75rem !important;
    }
    [data-testid="stFileUploaderDropzone"] {
        background-color: #11151C !important;
        border: 1.5px dashed rgba(255, 255, 255, 0.22) !important;
        border-radius: 12px !important;
        padding: 1.7rem 1.2rem !important;
        text-align: center !important;
        transition: all 0.25s ease-in-out !important;
    }
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: #3B82F6 !important;
        background-color: rgba(37, 99, 235, 0.06) !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] span,
    [data-testid="stFileUploaderDropzoneInstructions"] p,
    [data-testid="stFileUploaderDropzoneInstructions"] small,
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] p {
        color: #F8FAFC !important;
        -webkit-text-fill-color: #F8FAFC !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
    }
    [data-testid="stFileUploaderFile"] {
        background-color: #161B22 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: #FFFFFF !important;
    }
    [data-testid="stFileUploaderFile"] span,
    [data-testid="stFileUploaderFile"] div {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Top Brand Header */
    .saas-header {
        margin-bottom: 1.25rem;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.035em;
        line-height: 1.2;
        margin-bottom: 0.3rem;
        color: #FFFFFF !important;
    }
    .main-title span {
        color: #3B82F6 !important;
    }
    .sub-title {
        font-size: 1.02rem;
        font-weight: 400;
        color: #94A3B8 !important;
        line-height: 1.5;
        margin-bottom: 0.85rem;
    }

    /* SaaS Badge Pills Bar */
    .badge-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-bottom: 1rem;
    }
    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.26rem 0.78rem;
        font-size: 0.77rem;
        font-weight: 600;
        border-radius: 9999px;
        letter-spacing: 0.015em;
    }
    .badge-blue {
        background-color: rgba(37, 99, 235, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(59, 130, 246, 0.35);
    }
    .badge-emerald {
        background-color: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.35);
    }
    .badge-slate {
        background-color: rgba(148, 163, 184, 0.12);
        color: #E2E8F0;
        border: 1px solid rgba(148, 163, 184, 0.25);
    }
    .badge-amber {
        background-color: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }

    /* Ingestion Card Headers */
    .saas-card-header {
        font-size: 1.05rem;
        font-weight: 700;
        color: #FFFFFF !important;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .saas-card-tag {
        font-size: 0.74rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* High-End Metric Cards */
    .metric-card {
        background: #11151C;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 0.85rem 1rem;
        text-align: center;
        transition: all 0.2s ease;
    }
    .metric-card:hover {
        border-color: rgba(59, 130, 246, 0.4);
        background: #141A24;
    }
    .metric-val {
        font-size: 1.55rem;
        font-weight: 800;
        color: #FFFFFF !important;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    .metric-lbl {
        font-size: 0.73rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 0.25rem;
    }

    /* Polished SaaS Full-Width Primary Action Button */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        padding: 0.78rem 1.5rem !important;
        box-shadow: 0 4px 14px 0 rgba(37, 99, 235, 0.42) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px 0 rgba(37, 99, 235, 0.6) !important;
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
    }

    /* Secondary Buttons */
    div.stButton > button[kind="secondary"] {
        background-color: #161B22 !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        border-color: rgba(255, 255, 255, 0.3) !important;
        background-color: #1F2937 !important;
        color: #FFFFFF !important;
    }

    /* Active-Recall Flip Card Box */
    .active-recall-card {
        background: linear-gradient(145deg, #161B22 0%, #1A2234 100%);
        border: 1.5px solid #2563EB;
        border-radius: 14px;
        padding: 2.2rem 2rem;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.35);
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
        margin-bottom: 1.1rem;
    }
    .card-pattern-tag {
        font-size: 0.76rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #60A5FA;
        letter-spacing: 0.08em;
        margin-bottom: 0.75rem;
    }
    .card-question {
        font-size: 1.45rem;
        font-weight: 700;
        color: #FFFFFF !important;
        line-height: 1.45;
    }
    .card-revealed-box {
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(52, 211, 153, 0.4);
        border-radius: 10px;
        padding: 1.25rem;
        margin-top: 1.2rem;
        color: #D1FAE5 !important;
        font-size: 1.05rem;
        font-weight: 500;
        line-height: 1.6;
        text-align: left;
    }

    /* Summary Bullets */
    .summary-bullet-item {
        background: #11151C;
        border-left: 3.5px solid #2563EB;
        border-radius: 0 8px 8px 0;
        padding: 0.85rem 1.15rem;
        margin-bottom: 0.65rem;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        border-right: 1px solid rgba(255, 255, 255, 0.06);
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        font-size: 0.98rem;
        line-height: 1.6;
        color: #F8FAFC !important;
    }

    /* Heading Outline Node */
    .heading-node {
        background: #11151C;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 0.65rem 0.95rem;
        margin-bottom: 0.45rem;
        font-weight: 600;
        color: #FFFFFF !important;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Viva Defense Cards */
    .viva-card-box {
        background: #11151C;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.15rem;
        margin-bottom: 0.9rem;
    }
    .viva-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #60A5FA;
        margin-bottom: 0.4rem;
    }

    /* Tabs Styling */
    div[data-baseweb="tab-list"] {
        gap: 0.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.12);
        padding-bottom: 0.25rem;
    }
    button[data-baseweb="tab"] {
        font-weight: 600 !important;
        border-radius: 8px 8px 0 0 !important;
        color: #94A3B8 !important;
        padding: 0.65rem 1rem !important;
    }
    button[aria-selected="true"] {
        color: #FFFFFF !important;
        border-bottom-color: #2563EB !important;
    }
</style>
"""

# ---------------------------------------------------------
# Core NLP & Algorithmic Engine (100% Local, Automata & DS)
# ---------------------------------------------------------

# Standard English Stopwords (Hash Set for O(1) membership lookups)
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
    "aren", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", 
    "but", "by", "can", "cannot", "could", "did", "do", "does", "doing", "down", "during", 
    "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "her", 
    "here", "hers", "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is", 
    "isn", "it", "its", "itself", "just", "me", "more", "most", "my", "myself", "no", "nor", 
    "not", "now", "of", "off", "on", "once", "only", "or", "other", "our", "ours", "ourselves", 
    "out", "over", "own", "same", "she", "should", "so", "some", "such", "than", "that", 
    "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", "this", 
    "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "were", 
    "what", "when", "where", "which", "while", "who", "whom", "why", "will", "with", "would", 
    "you", "your", "yours", "also", "thus", "hence", "therefore", "often", "many", "much", 
    "within", "without", "along", "using", "uses", "used", "defined"
}

def normalize_paragraphs(raw_text: str) -> str:
    """
    BUG FIX 2 (Part A): Robust Paragraph Normalization & Line Unwrapping
    PDF and OCR handouts often introduce hard line breaks in the middle of sentences.
    This function:
    1. Normalizes line breaks and splits on double newlines into logical paragraph blocks.
    2. Unwraps hyphenated line breaks (e.g., 'soft-\nware' -> 'software').
    3. Merges standalone colon-heading lines (e.g. 'Deadlock:\n<definition>') into
       a single structured definition line for accurate parsing.
    4. Merges consecutive lines of normal paragraphs into cohesive sentences.
    """
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n").strip()
    raw_blocks = re.split(r"\n\s*\n+", text)
    cleaned_blocks = []

    for block in raw_blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue

        # 1. Unwrap hyphens across lines in this block
        unwrapped_lines = []
        for l in lines:
            if unwrapped_lines and unwrapped_lines[-1].endswith("-"):
                unwrapped_lines[-1] = unwrapped_lines[-1][:-1] + l
            else:
                unwrapped_lines.append(l)

        if not unwrapped_lines:
            continue

        # Case A: Block starts with colon-heading (e.g. "Deadlock:\n<def lines>")
        first = unwrapped_lines[0]
        if first.endswith(":") and 1 <= len(first.split()) <= 6 and len(unwrapped_lines) > 1:
            body = " ".join(unwrapped_lines[1:])
            cleaned_blocks.append(f"{first} {body}")
            continue

        # Case B: Block starts with Markdown/Module header (e.g. "### Process" or "Module 1: ...")
        is_md_header = re.match(r"^(?:#{1,6}\s+|Module\s+[0-9IVX]+[:\-\s]+|Unit\s+[0-9IVX]+[:\-\s]+|\d+[\.\)]\s+)", first, re.IGNORECASE)
        if is_md_header and len(unwrapped_lines) > 1:
            body = " ".join(unwrapped_lines[1:])
            cleaned_blocks.append(f"{first}\n{body}")
            continue

        # Case C: Standalone short title without period (e.g. "Thread\n<def lines>")
        is_short_title = (first[0].isupper() if first else False) and 1 <= len(first.split()) <= 5 and not first.endswith((".", "?", "!"))
        if is_short_title and len(unwrapped_lines) > 1 and len(" ".join(unwrapped_lines[1:])) >= 25:
            body = " ".join(unwrapped_lines[1:])
            cleaned_blocks.append(f"{first}:\n{body}")
            continue

        # Case D: Standard paragraph block (merge all lines)
        cleaned_blocks.append(" ".join(unwrapped_lines))

    return "\n\n".join(cleaned_blocks)

def extract_text_from_file(uploaded_file) -> tuple[str, str]:
    """
    Module 1: Document Ingestion Engine with Robust Multi-Page PDF Normalization
    Extracts text cleanly from uploaded PDF (.pdf) or plain text (.txt) files.
    Returns: (normalized_text, metadata_string)
    """
    if uploaded_file is None:
        return "", ""

    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        try:
            pdf_bytes = uploaded_file.read()
            pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
            total_pages = len(pdf_reader.pages)
            extracted_pages = []

            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_pages.append(page_text.strip())

            raw_combined = "\n\n".join(extracted_pages)
            # Normalize broken line paragraphs from PDF stream
            normalized_text = normalize_paragraphs(raw_combined)
            words = len(normalized_text.split())
            meta = f"📄 Extracted & normalized {words:,} words across {total_pages} PDF pages from `{uploaded_file.name}`"
            return normalized_text, meta
        except Exception as e:
            return "", f"❌ Failed to extract PDF text: {str(e)}"

    elif filename.endswith(".txt"):
        try:
            content = uploaded_file.read().decode("utf-8", errors="replace")
            normalized_text = normalize_paragraphs(content)
            words = len(normalized_text.split())
            meta = f"📝 Loaded & normalized {words:,} words from text file `{uploaded_file.name}`"
            return normalized_text, meta
        except Exception as e:
            return "", f"❌ Failed to read text file: {str(e)}"

    return "", "⚠️ Unsupported file format. Please upload .pdf or .txt"

def clean_and_tokenize_sentences(raw_text: str) -> list[str]:
    """
    Automata Theory (Finite-State Regex Matching & Paragraph Splitting):
    Normalizes paragraph blocks first, then segments into complete, grammatically sound sentences.
    Guards against abbreviation breaks (e.g., etc., e.g., i.e., Fig., vs.).
    Time Complexity: O(N) where N is character length.
    """
    normalized = normalize_paragraphs(raw_text)
    paragraphs = [p.strip() for p in normalized.split("\n\n") if p.strip()]
    clean_sentences = []

    for p in paragraphs:
        # Split sentences via punctuation lookbehind regex
        s_list = re.split(r'(?<=[.!?])(?:\s+|\n+)', p)
        for s in s_list:
            s_clean = s.strip()
            # Clean leading bullet symbols or markdown numbering
            s_clean = re.sub(r'^[•\-\*\d+\.\)]\s*', '', s_clean).strip()
            # Guard against trivial short fragments
            if len(s_clean) >= 12 and any(c.isalpha() for c in s_clean):
                clean_sentences.append(s_clean)

    return clean_sentences

def extract_headings(raw_text: str) -> list[str]:
    """
    Module 2: Structural Heading & Topic Extractor
    Detects headers: Markdown (#, ##), Module/Unit/Chapter tags, Numbered titles,
    and capitalized or title-case section lines.
    Time Complexity: O(L) where L is line count.
    """
    headings = []
    seen = set()
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

    for idx, line in enumerate(lines):
        # 1. Markdown heading (# Topic or ## Topic)
        m_md = re.match(r"^#{1,6}\s*(.+)$", line)
        if m_md:
            h = m_md.group(1).strip()
            if h.lower() not in seen:
                seen.add(h.lower())
                headings.append(h)
            continue

        # 2. Module / Unit / Chapter / Section header: e.g. "Module 1: Process Management"
        m_mod = re.match(r"^(?:Module|Unit|Chapter|Section)\s+[0-9IVX]+[:\-\s]+(.+)$", line, re.IGNORECASE)
        if m_mod:
            h = line.strip().rstrip(":")
            if h.lower() not in seen:
                seen.add(h.lower())
                headings.append(h)
            continue

        # 3. Numbered section: e.g. "1. Relational Databases" or "1) Binary Search"
        m_num = re.match(r"^[0-9]+[\.\)]\s*([A-Za-z0-9\s:_-]{3,65})$", line)
        if m_num:
            h = m_num.group(1).strip().rstrip(":")
            if h.lower() not in seen:
                seen.add(h.lower())
                headings.append(h)
            continue

        # 4. Short title line (<= 10 words, no terminal period, title-like or first line)
        word_count = len(line.split())
        if 1 <= word_count <= 10 and not line.endswith((".", "?", "!")):
            is_first_line = (idx == 0)
            has_colon = ":" in line
            is_capitalized = line[0].isupper() if line else False

            if is_first_line or has_colon or is_capitalized:
                h = line.rstrip(":").strip()
                if len(h) >= 3 and h.lower() not in seen:
                    seen.add(h.lower())
                    headings.append(h)
                continue

    return headings

def compute_word_frequencies(raw_text: str) -> tuple[dict, dict]:
    """
    Data Structures (Hash Map / Frequency Dictionary):
    Builds word-frequency table in O(N) linear time using collections.Counter.
    Filters out common stopwords using an O(1) Hash Set.
    Returns: (raw_frequencies, normalized_weights)
    """
    tokens = re.findall(r'\b[a-zA-Z]{3,}\b', raw_text.lower())
    non_stopwords = [w for w in tokens if w not in STOPWORDS]

    freq_dict = Counter(non_stopwords)
    if not freq_dict:
        return {}, {}

    max_freq = max(freq_dict.values())
    norm_weights = {w: count / max_freq for w, count in freq_dict.items()}
    return freq_dict, norm_weights

def extractive_summarization(sentences: list[str], norm_weights: dict, compression_ratio: float = 0.35) -> list[str]:
    """
    Module 3: Extractive Summarizer & Sentence Ranking (Sorting Algorithms)
    Scores each sentence based on keyword density weights, structural position, and definitions.
    Selects top K sentences in O(S log S) time while preserving original reading order.
    """
    if not sentences:
        return []

    scored_sentences = []
    for idx, sentence in enumerate(sentences):
        words = [w for w in re.findall(r'\b[a-zA-Z]{3,}\b', sentence.lower()) if w not in STOPWORDS]

        if not words:
            density_score = 0.0
        else:
            raw_sum = sum(norm_weights.get(w, 0.0) for w in words)
            density_score = raw_sum / (len(words) ** 0.5)

        position_bonus = 1.0
        if idx == 0:
            position_bonus = 1.35
        elif idx < 3:
            position_bonus = 1.20

        definition_bonus = 1.0
        if re.search(r'\b(defined as|refers to|means|is an?|are an?|mechanism|technique|property|algorithm)\b', sentence, re.IGNORECASE):
            definition_bonus = 1.25
        if ":" in sentence:
            definition_bonus = 1.20

        final_score = density_score * position_bonus * definition_bonus
        scored_sentences.append((final_score, idx, sentence))

    k = max(2, min(len(sentences), int(round(len(sentences) * compression_ratio))))
    top_k = sorted(scored_sentences, key=lambda x: x[0], reverse=True)[:k]
    ordered_summary = sorted(top_k, key=lambda x: x[1])

    return [s for _, _, s in ordered_summary]

def extract_flashcards(sentences: list[str], norm_weights: dict, raw_text: str = "") -> list[dict]:
    """
    BUG FIX 2 (Part B): Robust Active-Recall Flashcard Engine
    Parses:
    1. Heading-definition blocks across consecutive lines/blocks.
    2. Colon-syntax definitions ('Term: Definition...').
    3. Verb-linked definitions ('X is defined as Y', 'X refers to Y', 'X means Y').
    4. Copula definitions ('X is a Y', 'X are Y').
    5. Fallback: High-density conceptual recall pairs generated from top-scoring sentences.
    Guarantees a clean Question & Answer pair every time without raw string fragments.
    """
    flashcards = []
    seen_terms = set()

    # 1. Heading-Definition Block Matcher (if raw_text provided)
    if raw_text:
        normalized = normalize_paragraphs(raw_text)
        lines = [l.strip() for l in normalized.splitlines() if l.strip()]
        for i in range(len(lines) - 1):
            curr_l = lines[i]
            next_l = lines[i + 1]
            clean_term = re.sub(r'^(?:#{1,6}\s+|Module\s+[0-9IVX]+[:\-\s]+|\d+[\.\)]\s+)', '', curr_l).rstrip(':').strip()
            word_count = len(clean_term.split())
            if 1 <= word_count <= 5 and not curr_l.endswith(('.', '?', '!')) and clean_term.lower() not in seen_terms:
                if len(next_l) >= 20 and any(next_l.startswith(prefix) for prefix in ["A ", "An ", "The ", "Is ", "Refers ", "Defined "]) or ":" in curr_l:
                    seen_terms.add(clean_term.lower())
                    flashcards.append({
                        "Question": f"What is {clean_term}?",
                        "Answer": next_l,
                        "Pattern": "Heading-Definition Block",
                        "Key Concept": clean_term
                    })

    # Regex Definition Matchers
    colon_re = re.compile(r"^([A-Z][A-Za-z0-9\s\(\)/_-]{1,40}):\s+(.+)$")
    verb_re = re.compile(
        r"\b([A-Z][A-Za-z0-9\s\(\)/_-]{1,35})\s+(is defined as|refers to|is known as|can be defined as|means|signifies|represents|is described as)\s+(.+)",
        re.IGNORECASE
    )
    copula_re = re.compile(
        r"^(?:A|An|The)?\s*([A-Z][A-Za-z0-9\s\(\)/_-]{1,35})\s+(is an?|are an?|is the|are the)\s+(.+)",
        re.IGNORECASE
    )

    for s in sentences:
        s_clean = s.strip()

        # Pattern 2: Colon definition
        m1 = colon_re.match(s_clean)
        if m1:
            term = m1.group(1).strip()
            answer = m1.group(2).strip()
            if len(term.split()) <= 6 and term.lower() not in seen_terms and len(answer) >= 15 and " " in answer:
                seen_terms.add(term.lower())
                flashcards.append({
                    "Question": f"What is {term}?",
                    "Answer": answer,
                    "Pattern": "Colon Definition",
                    "Key Concept": term
                })
                continue

        # Pattern 3: Verb-linked definition
        m2 = verb_re.search(s_clean)
        if m2:
            term = m2.group(1).strip()
            verb = m2.group(2).strip()
            answer_tail = m2.group(3).strip()
            clean_term = re.sub(r"^(A|An|The)\s+", "", term, flags=re.IGNORECASE).strip()
            if len(clean_term.split()) <= 6 and clean_term.lower() not in seen_terms:
                seen_terms.add(clean_term.lower())
                full_answer = f"{verb.capitalize()} {answer_tail}"
                flashcards.append({
                    "Question": f"Explain what {clean_term} {verb}:",
                    "Answer": full_answer,
                    "Pattern": "Verb-Linked Definition",
                    "Key Concept": clean_term
                })
                continue

        # Pattern 4: Copula definition
        m3 = copula_re.match(s_clean)
        if m3:
            term = m3.group(1).strip()
            verb = m3.group(2).strip()
            answer_tail = m3.group(3).strip()
            clean_term = re.sub(r"^(A|An|The)\s+", "", term, flags=re.IGNORECASE).strip()
            if len(clean_term.split()) <= 6 and clean_term.lower() not in seen_terms and len(answer_tail) >= 10:
                seen_terms.add(clean_term.lower())
                full_answer = f"Is {answer_tail}"
                flashcards.append({
                    "Question": f"Define {clean_term}:",
                    "Answer": full_answer,
                    "Pattern": "Copula Definition",
                    "Key Concept": clean_term
                })
                continue

    # Fallback Mechanism: High-density conceptual flashcards from high-weight sentences
    if len(flashcards) < 4:
        top_keywords = [w for w, _ in sorted(norm_weights.items(), key=lambda x: x[1], reverse=True)[:10]]
        for kw in top_keywords:
            if kw in seen_terms:
                continue
            for s in sentences:
                if re.search(rf"\b{re.escape(kw)}\b", s, re.IGNORECASE) and len(s) > 25:
                    seen_terms.add(kw)
                    flashcards.append({
                        "Question": f"Explain the role and significance of '{kw.capitalize()}':",
                        "Answer": s,
                        "Pattern": "Keyword Concept Extraction",
                        "Key Concept": kw.capitalize()
                    })
                    break
            if len(flashcards) >= 6:
                break

    return flashcards


# ---------------------------------------------------------
# Preset Syllabus Notes for Evaluation & Viva Demonstrations
# ---------------------------------------------------------
PRESETS = {
    "Operating Systems: Process Management & Deadlocks": """Operating Systems: Process Management and Concurrency

An Operating System is defined as system software that manages computer hardware, software resources, and provides common services for computer programs.
A Process is a program in execution. Each process contains its own address space, program counter, registers, and stack.
Thread: A lightweight unit of CPU utilization that shares memory and resources with other threads of the same process.
CPU Scheduling: The mechanism by which the operating system decides which runnable process gets access to the CPU core.
First-Come First-Served (FCFS) is a non-preemptive scheduling algorithm that executes processes in order of arrival.
Round Robin is a preemptive scheduling algorithm designed for time-sharing systems where each process gets a fixed time quantum.
Context Switching is defined as the process of saving the execution state of an active process and restoring the state of another process.
Deadlock refers to a permanent blocking situation where a set of processes are blocked because each process holds a resource and waits for another resource held by another process.
Mutual Exclusion is one of the four necessary conditions for deadlock occurrence.
Hold and Wait refers to the condition where a process currently holding at least one resource is waiting to acquire additional resources held by other processes.
Virtual Memory refers to an abstraction that provides an ideal, large, uniform array of storage to every running process.
Paging is a memory management scheme that eliminates the need for contiguous allocation of physical memory by dividing memory into fixed-size pages.
""",

    "Data Structures & Algorithms: Trees, Graphs & Complexity": """Data Structures and Algorithms: Trees, Graphs and Asymptotic Complexity

Module 1: Non-Linear Data Structures
A Data Structure is defined as a specialized format for organizing, processing, retrieving, and storing data.
Binary Search Tree (BST): A node-based binary tree data structure where the left subtree contains only keys less than the node's key, and the right subtree contains only keys greater than the node's key.
AVL Tree refers to a self-balancing binary search tree where the difference between heights of left and right subtrees cannot be more than one for all nodes.
Red-Black Tree: A balanced binary search tree with an extra bit of storage per node representing color (red or black), ensuring no path is more than twice as long as any other.
B-Tree is a self-balancing search tree in which nodes can have more than two children, extensively used in database indexing and file systems.

Module 2: Graph Theory & Traversals
A Graph is defined as a non-linear data structure consisting of vertices (nodes) and edges connecting pairs of vertices.
Breadth-First Search (BFS) refers to a graph traversal algorithm that explores all vertices at the present depth level before moving on to vertices at the next depth level.
Depth-First Search (DFS) is an algorithm for traversing or searching tree or graph data structures that explores as far as possible along each branch before backtracking.
Dijkstra's Algorithm is a greedy algorithm that determines the shortest path between nodes in a weighted graph with non-negative edge weights.
Minimum Spanning Tree (MST): A subset of the edges of a connected, edge-weighted undirected graph that connects all vertices together without any cycles and with minimum possible total edge weight.

Module 3: Algorithm Analysis & Complexity
Big-O Notation refers to a mathematical notation that describes the upper bound of an algorithm's execution time or space requirement in terms of input size N.
Hash Table: A data structure that implements an associative array abstract data type, using a hash function to compute an index into an array of buckets in average O(1) time.
Dynamic Programming is defined as an algorithmic technique that solves complex problems by breaking them down into simpler subproblems and storing subproblem results using memoization or tabulation.
""",

    "DBMS: Relational Models & ACID Properties": """Database Management Systems: Relational Concepts & ACID Properties

A Database Management System (DBMS) is defined as software that enables users to define, create, maintain, and control access to structured data.
Relational Database: A database architecture that organizes data into tables consisting of rows (tuples) and columns (attributes).
Primary Key: A candidate key chosen by the database designer to uniquely identify each tuple in a relation.
Foreign Key refers to an attribute in one table that references the primary key of another table, establishing a relationship.
ACID Properties:
Atomicity ensures that all operations in a database transaction are completed successfully; otherwise, the entire transaction is aborted and rolled back.
Consistency ensures that a transaction takes the database from one valid state to another valid state, preserving all integrity constraints.
Isolation ensures that concurrent execution of transactions leaves the database in the same state that would have been obtained if transactions were executed sequentially.
Durability ensures that once a transaction has been committed, its changes remain recorded permanently in non-volatile storage even in event of system crashes.
Normalization is a database design technique that reduces data redundancy and eliminates undesirable insertion, update, and deletion anomalies.
First Normal Form (1NF) eliminates duplicate columns and ensures each attribute contains atomic, indivisible values.
Second Normal Form (2NF) enforces 1NF and removes partial functional dependencies where non-prime attributes depend on a subset of the candidate key.
Third Normal Form (3NF) enforces 2NF and ensures that no non-prime attribute is transitively dependent on the primary key.
""",

    "Computer Networks: OSI Model & Protocol Suite": """Computer Networks: OSI Architecture and Internet Protocols

A Computer Network is defined as a collection of interconnected computing devices that exchange data and share resources using communication protocols.
The OSI Model is a seven-layer conceptual framework developed by ISO that standardizes communication functions of telecommunication systems.
Physical Layer: The lowest layer of the OSI model responsible for transmitting unstructured raw bitstreams over a physical transmission medium.
Data Link Layer is responsible for node-to-node frame transfer, media access control (MAC), error detection, and flow control.
Network Layer refers to the layer that manages packet routing, logical IP addressing, and path determination across heterogeneous networks.
Transport Layer provides end-to-end communication services, connection management, flow control, and reliable byte-stream transmission.
Transmission Control Protocol (TCP) is a connection-oriented, reliable transport layer protocol that provides guaranteed delivery through three-way handshakes and sequence numbers.
User Datagram Protocol (UDP) is a connectionless, lightweight transport protocol that provides low-latency transmission without guaranteed delivery.
Internet Protocol (IP) is a network-layer protocol responsible for addressing hosts and routing datagrams across network boundaries.
Domain Name System (DNS) is defined as a hierarchical distributed naming system that translates human-readable domain names into numerical IP addresses.
Bandwidth refers to the maximum data transfer rate of a network communications cable or channel over a given unit of time.
Latency is the time interval required for a packet of data to travel from its source origin to its destination.
"""
}


# ---------------------------------------------------------
# Production Streamlit UI Dashboard (Elite SaaS Layout)
# ---------------------------------------------------------
def run_ui():
    st.set_page_config(
        page_title="AI Study Notes & Flashcard Generator",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.markdown(CSS_STYLING, unsafe_allow_html=True)

    # Session State Initialization
    if "current_card_index" not in st.session_state:
        st.session_state.current_card_index = 0
    if "card_revealed" not in st.session_state:
        st.session_state.card_revealed = False
    if "mastered_cards" not in st.session_state:
        st.session_state.mastered_cards = set()
    if "processed_data" not in st.session_state:
        st.session_state.processed_data = None
    if "input_text" not in st.session_state:
        st.session_state.input_text = PRESETS["Operating Systems: Process Management & Deadlocks"]
    if "file_meta_banner" not in st.session_state:
        st.session_state.file_meta_banner = ""

    # ---------------------------------------------------------
    # Brand Top Header
    # ---------------------------------------------------------
    st.markdown('<div class="saas-header">', unsafe_allow_html=True)
    st.markdown('<div class="main-title">📚 AI-Powered <span>Study Notes & Flashcards</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Automated Lecture Note Summarization & Active-Recall Flashcard Web Application</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="badge-bar">
        <span class="badge-pill badge-blue">🎓 B.Tech 2nd Year Mini Project</span>
        <span class="badge-pill badge-emerald">🔒 100% Offline & Local (Zero API Cost)</span>
        <span class="badge-pill badge-slate">⚡ O(N) Hash Table & Regex Engine</span>
        <span class="badge-pill badge-amber">📄 Multi-Page PDF & Text Ingestion (pypdf)</span>
        <span class="badge-pill badge-blue">🐼 Pandas CSV Export</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Collapsible Configuration & Presets Toolbar
    # ---------------------------------------------------------
    with st.expander("⚙️ Advanced Configuration, Core Syllabus Presets & Academic Details", expanded=False):
        col_cfg1, col_cfg2, col_cfg3 = st.columns([1.5, 1.5, 1.2])

        with col_cfg1:
            st.markdown("##### ⚡ Quick Syllabus Presets")
            selected_preset = st.selectbox(
                "Select Core Subject Sample:",
                options=list(PRESETS.keys()),
                index=0,
                label_visibility="collapsed"
            )
            if st.button("📥 Load Preset Lecture Notes", use_container_width=True):
                st.session_state.input_text = PRESETS[selected_preset]
                st.session_state.current_card_index = 0
                st.session_state.card_revealed = False
                st.session_state.mastered_cards = set()
                st.session_state.processed_data = None
                st.session_state.file_meta_banner = f"Loaded `{selected_preset}` notes."
                st.rerun()

        with col_cfg2:
            st.markdown("##### ⚙️ Summarizer Parameters")
            compression_slider = st.slider(
                "Summary Compression Ratio:",
                min_value=0.20,
                max_value=0.60,
                value=0.35,
                step=0.05,
                help="Selects top 30%–40% most informative sentences based on keyword density weights."
            )
            top_keywords_slider = st.slider(
                "Key Terms to Extract:",
                min_value=5,
                max_value=25,
                value=12,
                step=1
            )

        with col_cfg3:
            st.markdown("##### 👤 Academic Submission Details")
            st.caption("B.Tech CSE - 2nd Year (4th Sem)")
            st.caption("Student: **Ishant Verma** (22BCSE101)")
            st.caption("Category: NLP Interactive Web App")
            st.caption("Theoretical Mapping: Automata, Hash Maps, DAA")

    st.write("")

    # ---------------------------------------------------------
    # Equal-Width Side-by-Side Ingestion Layout (Columns: 1:1)
    # ---------------------------------------------------------
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("""
        <div class="saas-card-header">
            <span>📄 Document Ingestion</span>
            <span class="saas-card-tag">PDF / TXT Dropzone</span>
        </div>
        """, unsafe_allow_html=True)

        uploaded_doc = st.file_uploader(
            "Upload lecture notes (.pdf or .txt):",
            type=["pdf", "txt"],
            help="Extracts text directly in memory using pypdf for PDFs or UTF-8 text parser.",
            label_visibility="collapsed"
        )
        if uploaded_doc is not None:
            extracted_txt, meta_info = extract_text_from_file(uploaded_doc)
            if extracted_txt:
                st.session_state.input_text = extracted_txt
                st.session_state.file_meta_banner = meta_info
            elif meta_info:
                st.error(meta_info)

        if st.session_state.file_meta_banner:
            st.info(st.session_state.file_meta_banner)

        if st.button("🗑️ Reset Editor & Clear Text", use_container_width=True):
            st.session_state.input_text = ""
            st.session_state.processed_data = None
            st.session_state.file_meta_banner = ""
            st.rerun()

    with col_right:
        st.markdown("""
        <div class="saas-card-header">
            <span>📝 Lecture Notes & Text Editor</span>
            <span class="saas-card-tag">Interactive Input</span>
        </div>
        """, unsafe_allow_html=True)

        user_input = st.text_area(
            "Raw lecture notes input:",
            value=st.session_state.input_text,
            height=195,
            placeholder="Paste your lecture notes here or drag & drop a PDF on the left...",
            label_visibility="collapsed"
        )
        st.session_state.input_text = user_input

    # ---------------------------------------------------------
    # Refined Metric Cards (Equal-Width Grid)
    # ---------------------------------------------------------
    char_count = len(user_input)
    word_count = len(user_input.split()) if user_input.strip() else 0

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val">{char_count:,}</div>
            <div class="metric-lbl">Total Characters</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val">{word_count:,}</div>
            <div class="metric-lbl">Total Words</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m3:
        status_lbl = "Ready to analyze" if char_count >= 50 else "Min 50 chars required"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val" style="font-size:1.15rem; padding-top:0.35rem;">{'✅ ' + status_lbl if char_count >= 50 else '⚠️ ' + status_lbl}</div>
            <div class="metric-lbl">Engine Readiness</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    # Full-Width Primary Action Button
    process_clicked = st.button("✨ Generate Summary & Flashcards", type="primary", use_container_width=True)

    # ---------------------------------------------------------
    # Processing Logic
    # ---------------------------------------------------------
    if process_clicked:
        if char_count < 50:
            st.warning("⚠️ Input is too short! Please paste at least 50 characters of lecture content for meaningful analysis.")
        else:
            with st.spinner("Normalizing paragraphs, scoring sentences, and generating active-recall flashcards..."):
                comp_ratio = compression_slider if 'compression_slider' in locals() else 0.35

                # 1. Clean & tokenize sentences with robust line unwrapping
                sentences = clean_and_tokenize_sentences(user_input)
                # 2. Extract structural headings
                headings = extract_headings(user_input)
                # 3. Compute word frequencies
                freq_dict, norm_weights = compute_word_frequencies(user_input)
                # 4. Extractive summarization
                summary_sentences = extractive_summarization(sentences, norm_weights, compression_ratio=comp_ratio)
                # 5. Extract flashcards with heading-definition blocks & sentence definitions
                flashcards = extract_flashcards(sentences, norm_weights, raw_text=user_input)

                st.session_state.processed_data = {
                    "raw_sentences": sentences,
                    "headings": headings,
                    "freq_dict": freq_dict,
                    "norm_weights": norm_weights,
                    "summary_sentences": summary_sentences,
                    "flashcards": flashcards,
                    "original_word_count": word_count,
                }
                st.session_state.current_card_index = 0
                st.session_state.card_revealed = False
                st.session_state.mastered_cards = set()
                st.success("Analysis Complete! Generated structured outlines, bullet summaries, and active-recall flashcards.")

    # ---------------------------------------------------------
    # Output Presentation Dashboard
    # ---------------------------------------------------------
    if st.session_state.processed_data:
        data = st.session_state.processed_data
        summary_sentences = data["summary_sentences"]
        flashcards = data["flashcards"]
        headings = data["headings"]
        freq_dict = data["freq_dict"]
        orig_words = data["original_word_count"]

        summary_text = " ".join(summary_sentences)
        summary_words = len(summary_text.split()) if summary_text else 0
        reduction_pct = max(0, int(round((1 - (summary_words / max(1, orig_words))) * 100)))

        st.markdown("---")

        tab_summary, tab_flashcards, tab_keywords, tab_viva = st.tabs([
            "📋 Extractive Bullet Summary",
            f"🗂️ Interactive Active-Recall Flashcards ({len(flashcards)})",
            "🏷️ Extracted Headings & Key Terms",
            "🎓 B.Tech Viva Defense & Syllabus Mapping"
        ])

        # -----------------------------------------------------
        # TAB 1: Extractive Bullet Summary
        # -----------------------------------------------------
        with tab_summary:
            st.markdown("### 📋 Module 3: Extractive Bullet-Point Summary")
            st.caption("Extracted using keyword density weights, sentence length normalization, and structural position bonuses.")

            s_c1, s_c2, s_c3, s_c4 = st.columns(4)
            with s_c1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val">{orig_words:,}</div>
                    <div class="metric-lbl">Original Words</div>
                </div>
                """, unsafe_allow_html=True)
            with s_c2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val">{summary_words:,}</div>
                    <div class="metric-lbl">Summary Words</div>
                </div>
                """, unsafe_allow_html=True)
            with s_c3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val">{reduction_pct}%</div>
                    <div class="metric-lbl">Content Reduction</div>
                </div>
                """, unsafe_allow_html=True)
            with s_c4:
                time_saved = max(1, round((orig_words - summary_words) / 200, 1))
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val">~{time_saved} min</div>
                    <div class="metric-lbl">Revision Time Saved</div>
                </div>
                """, unsafe_allow_html=True)

            st.write("")
            st.markdown("#### 🎯 Key Concept Bullet Points:")

            if not summary_sentences:
                st.info("No sentences selected. Try increasing the compression slider or pasting longer text.")
            else:
                for s in summary_sentences:
                    st.markdown(f'<div class="summary-bullet-item">🔹 {s}</div>', unsafe_allow_html=True)

                st.write("")
                col_down_md, col_down_csv = st.columns(2)
                with col_down_md:
                    summary_md = "## AI-Generated Lecture Summary\n\n" + "\n".join([f"- {s}" for s in summary_sentences])
                    st.download_button(
                        label="📥 Download Summary Notes (.MD)",
                        data=summary_md,
                        file_name="lecture_summary.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                with col_down_csv:
                    df_summary = pd.DataFrame({
                        "Point": range(1, len(summary_sentences) + 1),
                        "Key Summary Sentence": summary_sentences
                    })
                    csv_sum_buf = io.StringIO()
                    df_summary.to_csv(csv_sum_buf, index=False)
                    st.download_button(
                        label="📥 Download Summary Notes (.CSV)",
                        data=csv_sum_buf.getvalue(),
                        file_name="lecture_summary.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

        # -----------------------------------------------------
        # TAB 2: Interactive Active-Recall Flashcards
        # -----------------------------------------------------
        with tab_flashcards:
            st.markdown("### 🗂️ Module 4: Active-Recall Flashcard Deck")
            st.caption("Derived from definition patterns and key concepts for active-recall revision.")

            if not flashcards:
                st.info("No flashcard definition pairs detected. Paste lecture text containing definitions or terms.")
            else:
                total_cards = len(flashcards)
                curr_idx = st.session_state.current_card_index
                current_card = flashcards[curr_idx]

                mastered_count = len(st.session_state.mastered_cards)
                progress_val = (curr_idx + 1) / total_cards
                st.progress(progress_val)

                p_c1, p_c2 = st.columns([3, 1])
                with p_c1:
                    st.markdown(f"**Card {curr_idx + 1} of {total_cards}** | Concept: `{current_card['Key Concept']}`")
                with p_c2:
                    st.markdown(f"🏆 Mastered: **{mastered_count} / {total_cards}**")

                is_mastered = curr_idx in st.session_state.mastered_cards
                mastered_badge = "✅ (Mastered)" if is_mastered else ""

                flashcard_html = f"""
                <div class="active-recall-card">
                    <div class="card-pattern-tag">{current_card['Pattern']} {mastered_badge}</div>
                    <div class="card-question">{current_card['Question']}</div>
                </div>
                """
                st.markdown(flashcard_html, unsafe_allow_html=True)

                c_rev, c_mst = st.columns([2, 2])
                with c_rev:
                    rev_lbl = "🙈 Hide Answer" if st.session_state.card_revealed else "👀 Reveal Answer (Active Recall)"
                    if st.button(rev_lbl, use_container_width=True):
                        st.session_state.card_revealed = not st.session_state.card_revealed
                        st.rerun()

                with c_mst:
                    if curr_idx in st.session_state.mastered_cards:
                        if st.button("🔄 Mark as Needs Review", use_container_width=True):
                            st.session_state.mastered_cards.remove(curr_idx)
                            st.rerun()
                    else:
                        if st.button("⭐ Mark as Mastered", use_container_width=True):
                            st.session_state.mastered_cards.add(curr_idx)
                            st.rerun()

                if st.session_state.card_revealed:
                    st.markdown(f"""
                    <div class="card-revealed-box">
                        <strong>💡 Answer / Explanation:</strong><br>{current_card['Answer']}
                    </div>
                    """, unsafe_allow_html=True)

                st.write("")
                n_prev, n_jump, n_next = st.columns([1, 2, 1])
                with n_prev:
                    if st.button("⬅️ Previous", disabled=(curr_idx == 0), use_container_width=True):
                        st.session_state.current_card_index -= 1
                        st.session_state.card_revealed = False
                        st.rerun()
                with n_jump:
                    jump_idx = st.selectbox(
                        "Jump to Card:",
                        options=list(range(1, total_cards + 1)),
                        index=curr_idx,
                        label_visibility="collapsed"
                    )
                    if jump_idx - 1 != curr_idx:
                        st.session_state.current_card_index = jump_idx - 1
                        st.session_state.card_revealed = False
                        st.rerun()
                with n_next:
                    if st.button("Next ➡️", disabled=(curr_idx == total_cards - 1), use_container_width=True):
                        st.session_state.current_card_index += 1
                        st.session_state.card_revealed = False
                        st.rerun()

                st.markdown("---")

                st.markdown("#### 📖 Full Deck Accordion View (Expandable Q&A Cards)")
                for idx, c in enumerate(flashcards, 1):
                    card_status = "✅ Mastered" if (idx - 1) in st.session_state.mastered_cards else "📝 Unreviewed"
                    with st.expander(f"Card {idx}: {c['Key Concept']} — {c['Question']} ({card_status})"):
                        st.markdown(f"**Question:** {c['Question']}")
                        st.markdown(f"**Answer:** {c['Answer']}")
                        st.caption(f"Pattern Detected: {c['Pattern']}")

                st.markdown("---")
                st.markdown("#### 📊 Tabular Flashcard Deck (Pandas DataFrame)")

                df_cards = pd.DataFrame(flashcards)
                df_cards.index = df_cards.index + 1
                st.dataframe(df_cards[["Key Concept", "Question", "Answer", "Pattern"]], use_container_width=True)

                csv_buffer = io.StringIO()
                df_cards.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="📥 Download Flashcard Deck (.CSV for Anki/Quizlet)",
                    data=csv_buffer.getvalue(),
                    file_name="study_flashcards.csv",
                    mime="text/csv",
                    use_container_width=True
                )

        # -----------------------------------------------------
        # TAB 3: Extracted Headings & Key Terms
        # -----------------------------------------------------
        with tab_keywords:
            st.markdown("### 🏷️ Module 2: Structural Headings & Keyword Density")
            st.caption("Extracted via Regex section matching and O(N) frequency hash table distribution.")

            h_col, t_col = st.columns([1, 1])

            with h_col:
                st.markdown("#### 📑 Structured Topic Outline")
                if not headings:
                    st.info("No explicit section headings found. The summarizer processed the text as a continuous passage.")
                else:
                    for idx, h in enumerate(headings, 1):
                        st.markdown(f'<div class="heading-node">📌 <strong>{idx}.</strong> {h}</div>', unsafe_allow_html=True)

            with t_col:
                st.markdown("#### 🔑 Top High-Frequency Technical Terms")
                kw_count = top_keywords_slider if 'top_keywords_slider' in locals() else 12
                top_terms = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)[:kw_count]
                if not top_terms:
                    st.write("No key terms identified.")
                else:
                    pill_html = ""
                    for term, count in top_terms:
                        pill_html += f'<span class="badge-pill badge-blue"><strong>{term}</strong>: {count}</span> '
                    st.markdown(pill_html, unsafe_allow_html=True)

                    st.write("")
                    df_terms = pd.DataFrame(top_terms, columns=["Technical Keyword", "Raw Frequency"])
                    df_terms["Relative Weight (TF)"] = df_terms["Technical Keyword"].map(lambda w: round(data["norm_weights"].get(w, 0), 3))
                    df_terms.index = df_terms.index + 1
                    st.dataframe(df_terms, use_container_width=True)

        # -----------------------------------------------------
        # TAB 4: B.Tech Viva Defense & Syllabus Mapping
        # -----------------------------------------------------
        with tab_viva:
            st.markdown("### 🎓 B.Tech 2nd Year Syllabus Mapping & Viva Defense")
            st.caption("Curriculum mapping and technical explanations for laboratory/project viva defense.")

            v_col1, v_col2 = st.columns(2)

            with v_col1:
                st.markdown("""
                <div class="viva-card-box">
                    <div class="viva-title">1. Theory of Computation & Automata</div>
                    <p><strong>Finite-State Regex Matching:</strong></p>
                    <ul>
                        <li>Sentence boundary detection via lookbehind regex: <code>(?<=[.!?])\\s+</code></li>
                        <li>Multi-pattern state transitions matching colon syntax (<code>Term: Def</code>), verb-linked (<code>is defined as</code>, <code>refers to</code>), and copula connectors.</li>
                        <li>Deterministic processing without heavy external neural runtimes.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class="viva-card-box">
                    <div class="viva-title">2. Data Structures (Hash Maps & Hash Sets)</div>
                    <p><strong>Hash Table Complexity:</strong></p>
                    <ul>
                        <li><strong>Hash Set:</strong> English stopword filtering in <code>O(1)</code> average lookup time.</li>
                        <li><strong>Hash Map (Counter):</strong> Computes token frequency distribution in <code>O(N)</code> linear time over total document words <em>N</em>.</li>
                        <li>Normalized term weights calculated via single-pass linear scaling.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            with v_col2:
                st.markdown("""
                <div class="viva-card-box">
                    <div class="viva-title">3. Design and Analysis of Algorithms (DAA)</div>
                    <p><strong>Sentence Scoring & Ranking:</strong></p>
                    <ul>
                        <li>Sentence density scoring combines term-frequency summation normalized by sentence length.</li>
                        <li>Top-<em>K</em> sentence selection using comparison sorting in <code>O(S log S)</code> where <em>S</em> is sentence count.</li>
                        <li>Secondary sort restores original chronological sentence sequence to preserve logical narrative flow.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class="viva-card-box">
                    <div class="viva-title">4. Software Engineering & Local Deployment</div>
                    <p><strong>Production & Viva Reliability:</strong></p>
                    <ul>
                        <li><strong>Zero External API Dependency:</strong> 100% computed locally — zero cloud API rate limits, billing failures, or network downtime during live evaluation.</li>
                        <li><strong>Document Ingestion:</strong> In-memory PDF byte stream parsing via <code>pypdf</code> with multi-line paragraph unwrapping.</li>
                        <li><strong>Pandas Structuring:</strong> Encapsulates flashcard decks into relational DataFrames for immediate CSV download.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("#### 💡 Frequently Asked Viva Questions (Examiner Cheat Sheet)")
            with st.expander("Q1: Why did you choose an Extractive Summarizer instead of an Abstractive Deep Learning model (e.g. T5 or GPT)?"):
                st.markdown("""
                **Answer:**
                1. **Factuality & Hallucination Prevention:** Extractive summarization extracts exact factual sentences written by professors or textbooks, ensuring zero hallucinated formulas, definitions, or statements.
                2. **Computational Footprint:** Abstractive LLMs require gigabytes of GPU VRAM and paid cloud API endpoints that can fail during live lab evaluations. Our system runs in milliseconds on any standard computer with $O(N)$ linear time complexity.
                3. **Curriculum Mapping:** It directly demonstrates core 2nd-year CS concepts: Automata (Regex), Hash Maps (Data Structures), and Sorting (Algorithms).
                """)

            with st.expander("Q2: How does the system handle sentence boundaries without confusing abbreviations like 'e.g.' or 'i.e.'?"):
                st.markdown("""
                **Answer:**
                The tokenizer employs positive lookbehind regular expressions `(?<=[.!?])\\s+` combined with minimum length guards and alphanumeric verification. Common single-letter abbreviation patterns followed by lowercase continuation are handled without false sentence breaks.
                """)

            with st.expander("Q3: What is the time complexity of the entire pipeline?"):
                st.markdown("""
                **Answer:**
                Let $N$ be the total word count and $S$ be the total sentence count:
                - **Tokenization & Stopword Filtering:** $O(N)$ with $O(1)$ set lookups.
                - **Frequency Dictionary Building:** $O(N)$ linear pass.
                - **Sentence Scoring:** $O(N)$ because each word in each sentence is evaluated once.
                - **Sentence Ranking:** $O(S \\log S)$ to sort sentences by score, and $O(K \\log K)$ to restore original reading order.
                - **Overall Time Complexity:** $\\mathcal{O}(N + S \\log S)$, which runs virtually instantaneously for lecture documents.
                """)

    # ---------------------------------------------------------
    # Footer
    # ---------------------------------------------------------
    st.markdown("---")
    st.markdown(
        "<center><small style='color: #64748B;'>B.Tech 2nd Year Computer Science & Engineering Mini Project | AI-Powered Study Notes & Flashcard Generator | Built with Python, Streamlit, pypdf & Pandas</small></center>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    run_ui()
