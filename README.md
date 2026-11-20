# 📚 StudyForge — AI-Powered Study Notes & Flashcard Generator

> **Automated Lecture Note Summarization & Active-Recall Revision Workspace**  
> *B.Tech Computer Science & Engineering — 2nd Year Mini Project*

---

## 📌 Project Overview & Submission Details

| Field | Details |
| :--- | :--- |
| **Project Name** | **StudyForge AI** |
| **Architectures** | 1. **Standalone High-Contrast Web App** ([index.html](file:///Users/ishantverma/Desktop/mini%20project/index.html))<br>2. **Streamlit Python Dashboard** ([app.py](file:///Users/ishantverma/Desktop/mini%20project/app.py)) |
| **Visual Aesthetic** | Deep obsidian canvas (`#090A0D`), elevated surfaces (`#111318`), crisp editorial borders (`#222630`), warm amber (`#F59E0B`) accents. |
| **Target Level** | B.Tech Computer Science & Engineering — 2nd Year (3rd / 4th Semester) |
| **Core Technologies** | HTML5, CSS3, JavaScript (ES6+), PDF.js (CDN), Python 3, Streamlit, `pypdf`, Pandas |
| **Key Advantage** | **100% Offline & Client-Side Capable** — Zero external API costs, zero live viva evaluation failure risk |

---

## 🚀 How to Run the Applications

### Option A: Standalone Modern Web App (`index.html`) — Recommended

The standalone `index.html` requires zero external Python dependencies and extracts multi-page PDFs client-side directly in the browser via PDF.js.

```bash
# Serve locally on port 8000
python3 -m http.server 8000
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser (or double-click [index.html](file:///Users/ishantverma/Desktop/mini%20project/index.html)).

---

### Option B: Streamlit Python Dashboard (`app.py`)

```bash
cd "/Users/ishantverma/Desktop/mini project"
source venv/bin/activate
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

### Run Test Suite
```bash
python -m unittest test_engine.py
```
*7 unit tests covering tokenization, frequency tables, line unwrapping, and flashcard generation pass in 0.007s.*

---

## ✨ Features & Architecture

1. **Clean High-Contrast UI & Editorial Aesthetic:**
   - Deep obsidian canvas (`#090A0D`), `#111318` card surfaces, and `#222630` subtle borders.
   - Warm amber (`#F59E0B`) interactive elements and active tab underlines.
   - High-contrast text: `#F3F4F6` main text, `#E5E7EB` inactive tabs (no washed-out text), `#FFFFFF` on active controls.
2. **Side-by-Side Ingestion Workspace:**
   - Left: Multi-page PDF (`pdf.js`) and `.txt` drag-and-drop zone with status banner and clear button.
   - Right: Live notes editor textarea.
   - Live character, word, reading time counters, and engine readiness indicator.
3. **Multi-Page PDF Line Unwrapping (`normalizeParagraphs`):**
   - Automatically rejoins wrapped lines and hyphenated breaks (`comput-\ner` $\to$ `computer`).
   - Normalizes colon headers (`Deadlock:\n<definition>` $\to$ `Deadlock: <definition>`).
4. **Extractive Summarizer:**
   - $O(N)$ Hash Map token frequency counting with $O(1)$ stopword filtering.
   - Scores sentences based on keyword density weights, position bonuses, and definition tags.
   - $O(S \log S)$ sorting for top-$K$ selection, preserving chronological narrative sequence.
5. **Interactive Active-Recall Flashcards:**
   - Interactive flip card with reveal toggle, Previous/Next navigation, mastery tracking (`Mastered` / `Needs Review`), and progress bar.
   - Full deck accordion view.
   - One-click UTF-8 **CSV download** formatted for Anki/Quizlet/Excel import.
6. **B.Tech Viva Defense & Syllabus Mapping:**
   - Automata Theory (lookbehind regex sentence segmentation).
   - Data Structures (Hash Maps and Sets).
   - Design and Analysis of Algorithms (Sentence Ranking & Sorting).
   - Examiner Viva Q&A cheat sheet.

---

## 🧪 Built-in Syllabus Presets

- **Operating Systems:** Process Management, Concurrency & Deadlocks
- **Data Structures & Algorithms:** Trees, Graphs & Asymptotic Complexity
- **Database Management Systems:** Relational Models & ACID Properties
- **Computer Networks:** OSI 7-Layer Architecture & Protocol Suite

---

## 📂 File Directory

```text
mini project/
├── index.html                 # Standalone StudyForge Web App (Client-side PDF.js & NLP)
├── app.py                     # Streamlit Python Web Dashboard
├── requirements.txt           # Python dependencies (streamlit, pandas, pypdf)
├── test_engine.py             # Automated unit test suite (7 passing tests)
├── README.md                  # Complete documentation and viva guide
└── ai-study-notes-generator/  # Synced mirror package
    ├── index.html
    ├── app.py
    ├── requirements.txt
    └── README.md
```
