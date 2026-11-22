# ScholarAI Studio — Architecture & Roadmap

ScholarAI Studio is engineered as an end-to-end academic copilot for paper analysis, presentation generation, and oral defense mastery.

---

## Technical Architecture

```text
[PDF Upload]
     │
     ▼
[PyMuPDF Page Parser] ───────────► [1-Based Page Indexer]
     │                                     │
     ▼                                     ▼
[Text Chunking & Metadata]        [ChromaDB Vector Store]
     │                                     │
     ▼                                     ▼
[Gemini Embeddings] ─────────────► [Similarity Retrieval]
                                           │
                                           ▼
                                 [Grounded LLM Reasoning]
                                           │
     ┌──────────────────┬──────────────────┼──────────────────┬──────────────────┐
     ▼                  ▼                  ▼                  ▼                  ▼
[6-Section         [Conceptual        [Grounded          [16:9 Slide         [6-Turn Viva
 Synthesis]        Frameworks]        Vector Q&A]         Studio]            Simulator]
```

---

## Architectural Stages

### 1. High-Fidelity PDF Intake & Provenance
- Ingests academic research papers and extracts text per page preserving exact 1-based page numbers.
- Validates file constraints (empty, corrupt, encrypted, or image-only scanned PDFs) with clear diagnostic recovery steps.

### 2. Isolated Vector Storage & Embeddings
- Splits document text into overlapping chunks with embedded metadata (`filename`, `page_number`, `chunk_index`).
- Uses Gemini document and query retrieval embeddings.
- Manages local ChromaDB collections with strict document isolation.

### 3. Intent Detection & Intelligent Routing
- Automatic classification of natural language queries into 7 distinct intents:
  - `paper_question`: Scoped vector retrieval and grounded synthesis.
  - `summary`: Full-paper 6-section academic synthesis.
  - `key_concepts`: Core theoretical frameworks with plain-language definitions.
  - `viva`: Oral defense simulation.
  - `presentation`: Widescreen slide deck generation.
  - `flashcards`: Active recall study deck.
  - `unclear`: Disambiguation guidance.

### 4. Automated Slide Deck Generation
- Synthesizes presentation outlines tailored to custom slide counts, audience technical levels, and talk durations.
- Builds widescreen (16:9) PowerPoint presentations (`.pptx`) with typography, bullet formatting, speaker notes, and citations.
- Provides interactive in-browser slide presentation mode with keyboard and button navigation.

### 5. Adaptive Oral Defense (Viva) Simulator
- Simulates faculty examiner questioning across 6 progressive turns.
- Evaluates student answers on a 5-point rubric with actionable strengths, improvement areas, and examiner commentary.
- Records session analytics to a private local SQLite database.

### 6. Revision Flashcards & Analytics
- Creates balanced question-and-answer revision decks with evidence citations.
- Visualizes topic comprehension and score distribution with interactive Plotly charts.
