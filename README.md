# ScholarAI Studio

ScholarAI Studio is an advanced academic research assistant and oral defense intelligence copilot. It streamlines the lifecycle of academic literature ingestion, structured paper synthesis, vector-grounded Q&A, automated widescreen presentation generation, and adaptive mock viva defense examinations.

**Author:** [Prajwal-6364](https://github.com/Prajwal-6364)  
**License:** MIT

---

## 🚀 Key Capabilities

- **Page-Aware PDF Ingestion**: Extracts digital research paper contents with PyMuPDF (`fitz`), preserving 1-based page coordinates for strict citation provenance.
- **6-Dimension Academic Synthesis**: Synthesizes comprehensive research summaries across 6 core academic dimensions:
  1. *Research Problem*
  2. *Objective & Hypotheses*
  3. *Methodology & Data / Participants*
  4. *Key Empirical Findings*
  5. *Conclusion & Practical Takeaways*
  6. *Limitations & Validity Threats*
- **Key Conceptual Frameworks**: Extracts foundational theoretical ideas and study-specific novel concepts with plain-language explanations, paper significance, and verifiable page citations.
- **Grounded Vector RAG Q&A**: Interactive question-answering powered by ChromaDB vector store and Gemini embeddings, scoped strictly to the active document with excerpt evidence inspection.
- **Widescreen Slide Deck Studio**: Automatically generates widescreen (16:9) academic PowerPoint presentations (`.pptx`) with customizable styling, speaker notes, and in-browser interactive presentation mode.
- **Interactive Defense (Viva) Simulator**: Adaptive 6-turn oral examination agent with real-time rubric-based scoring (1–5 scale), strengths identification, improvement feedback, and page-cited justification.
- **Revision Flashcards & Learning Analytics**: Generates paper-grounded study flashcards with flip mechanics and records viva performance metrics in a local SQLite database with visual Plotly topic mastery charts.

---

## 🛠️ Architecture & Tech Stack

| Layer | Component | Description |
| :--- | :--- | :--- |
| **Frontend UI** | Streamlit | Responsive dark glassmorphic dashboard with custom CSS |
| **PDF Extraction** | PyMuPDF (`fitz`) | High-fidelity page-by-page text parsing with coordinate tracking |
| **Vector Database** | ChromaDB | Local persistent vector storage for embedded document chunks |
| **Embeddings & LLM** | Google Gemini API | Text embedding models and generative reasoning |
| **Orchestration** | LangChain & LCEL | Grounded prompt templates and structured generation pipelines |
| **Slide Generation** | python-pptx | Dynamic widescreen (16:9) PowerPoint presentation builder |
| **Analytics & Metrics** | Pandas & Plotly | Performance telemetry, topic mastery charts, and SQLite history |

---

## 📁 Repository Structure

```text
ScholarAI/
├── app.py                     # Main application entry point and UI controller
├── scholarai/
│   ├── analysis.py            # Academic synthesis and concept extraction logic
│   ├── config.py              # Environment configuration and API settings
│   ├── flashcards.py          # Study flashcard generation logic
│   ├── pdf.py                 # Page-aware PDF parsing and text extraction
│   ├── presentation.py        # Presentation slide generator and HTML renderer
│   ├── progress.py            # Local viva history and performance analytics
│   ├── prompts.py             # LangChain prompts and LLM chain pipelines
│   ├── rag.py                 # ChromaDB vector store and grounded RAG query engine
│   ├── router.py              # Query classification and intent routing
│   ├── styles.py              # UI theme, custom styles, and layouts
│   └── viva.py                # Mock defense evaluation and questioning agent
├── requirements.txt           # Project dependencies
├── .env.example               # Environment variables template
└── README.md                  # Project documentation
```

---

## ⚡ Installation & Setup

### 1. Prerequisites
- Python 3.10 or newer (tested on Python 3.12)
- A Google Gemini API key ([Google AI Studio](https://aistudio.google.com/))

### 2. Environment Setup

```bash
# Clone the repository
git clone https://github.com/Prajwal-6364/ai_assign.git
cd ai_assign

# Create and activate a virtual environment
python -m venv venv

# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Windows (CMD):
venv\Scripts\activate.bat
# Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure API Key

Copy `.env.example` to `.env` and insert your Gemini API key:

```bash
copy .env.example .env
```

Edit `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.8-flash
GEMINI_EMBEDDING_MODEL=models/gemini-embedding-001
CHROMA_DIR=./chroma_db
```

### 4. Run Application

```bash
streamlit run app.py
```

The application will be accessible at `http://localhost:8501`.

---

## 🔒 Grounding & Provenance Guarantees

ScholarAI enforces strict grounding principles:
1. **Zero Extrapolation**: Answers, summaries, and slides are restricted to retrieved page context from the active document.
2. **Page-Coordinate Citations**: Every factual claim cites original 1-based page numbers (e.g. `[Page 4]`).
3. **Transparent Evidence**: Users can inspect exact source text chunks and passages directly in the UI.
4. **Isolated Memory**: Switching papers resets session indices to prevent cross-contamination.
