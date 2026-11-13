# ScholarAI Workbench

ScholarAI Workbench is an academic research assistant designed for paper analysis, presentation deck generation, and defense preparation. It streamlines the workflow of reading research papers, generating presentation slides, and practicing viva questions.

## Features & Capabilities

- **Page-Aware PDF Ingestion**: Extracts digital research paper contents while preserving 1-based page coordinates and structure using PyMuPDF.
- **Deep Academic Synthesis**: Generates structured 6-section research summaries (Problem, Objective, Methodology, Findings, Conclusions, Limitations) and extracts key conceptual frameworks with citations.
- **Grounded Vector RAG**: Interactive paper Q&A powered by ChromaDB vector store and Gemini embeddings with strict page-referenced citations.
- **Automated Presentation Deck Builder**: Automatically designs academic PowerPoint presentation slides with customizable styling and an interactive in-browser preview mode.
- **Interactive Defense (Viva) Simulator**: Adaptive mock examination sessions (up to 6 questions) with real-time rubric-based evaluation, scoring, and improvement feedback.
- **Study Flashcards & Analytics**: Generates paper-grounded flashcards for revision and tracks viva performance metrics and topic mastery over time.

---

## Architecture & Technology Stack

| Layer | Component | Description |
| :--- | :--- | :--- |
| **Frontend / UI** | Streamlit | Responsive dashboard with modern slate & indigo theme |
| **PDF Extraction** | PyMuPDF (`fitz`) | High-fidelity page-by-page text parsing |
| **Vector Database** | ChromaDB | Fast local vector storage for embedded chunks |
| **Language & Embeddings** | Google Gemini API | Text embedding models and generative reasoning |
| **Orchestration** | LangChain / LCEL | Grounded prompt templates and structured generation |
| **Slide Generation** | python-pptx | Dynamic PowerPoint deck generation |
| **Analytics & Metrics** | Pandas & Plotly | Performance tracking and visual mastery charts |

---

## Project Structure

```text
ScholarAI/
├── app.py                     # Main application entry point and UI controller
├── researchmate/
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
└── README.md                  # Project documentation and guide
```

---

## Installation & Setup

### 1. Prerequisites
- Python 3.10 or newer
- A Google Gemini API key ([Google AI Studio](https://aistudio.google.com/))

### 2. Environment Setup

Clone or navigate into your project folder:

```bash
# Create a virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Windows (CMD):
.venv\Scripts\activate.bat
# Linux / macOS:
source .venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure API Key

Copy the example environment file and add your Gemini API key:

```bash
# Windows:
copy .env.example .env

# Linux / macOS:
cp .env.example .env
```

Open `.env` and configure your API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
GEMINI_EMBEDDING_MODEL=text-embedding-004
```

### 4. Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## Usage Workflow

1. **Upload Paper**: Go to the ingestion section and upload any research paper in PDF format.
2. **Review Synthesis**: Check the structured summary and key conceptual takeaways.
3. **Ask Questions**: Query the paper using natural language; responses provide precise page citations.
4. **Export Slides**: Generate PowerPoint slides and review them in the slide presenter.
5. **Simulate Defense**: Start a viva session to test your knowledge against AI-generated examination questions.
