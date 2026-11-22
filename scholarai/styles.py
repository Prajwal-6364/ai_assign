"""Ultra-modern dark glassmorphic design system and UI components for ScholarAI Studio."""

import urllib.parse

# Futuristic ambient technical mesh background with subtle glow points
_BACKGROUND_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice">
<defs>
  <radialGradient id="meshGradient" cx="50%" cy="10%" r="70%">
    <stop offset="0%" stop-color="#1e1b4b" stop-opacity="0.85"/>
    <stop offset="35%" stop-color="#0f172a" stop-opacity="0.95"/>
    <stop offset="100%" stop-color="#070a12" stop-opacity="1"/>
  </radialGradient>
  <radialGradient id="glowTopLeft" cx="15%" cy="15%" r="40%">
    <stop offset="0%" stop-color="#4f46e5" stop-opacity="0.22"/>
    <stop offset="100%" stop-color="#070a12" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowTopRight" cx="85%" cy="10%" r="45%">
    <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.18"/>
    <stop offset="100%" stop-color="#070a12" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowBottomCenter" cx="50%" cy="90%" r="50%">
    <stop offset="0%" stop-color="#6366f1" stop-opacity="0.12"/>
    <stop offset="100%" stop-color="#070a12" stop-opacity="0"/>
  </radialGradient>
  <pattern id="dotGrid" width="32" height="32" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.1" fill="rgba(255, 255, 255, 0.04)"/>
  </pattern>
</defs>

<rect width="1440" height="900" fill="url(#meshGradient)"/>
<rect width="1440" height="900" fill="url(#dotGrid)"/>
<rect width="1440" height="900" fill="url(#glowTopLeft)"/>
<rect width="1440" height="900" fill="url(#glowTopRight)"/>
<rect width="1440" height="900" fill="url(#glowBottomCenter)"/>
</svg>"""

_ENCODED_SVG = urllib.parse.quote(_BACKGROUND_SVG.replace("\n", " ").strip())

CUSTOM_CSS = f"""
<style>
/* ====================================================================
   SCHOLARAI STUDIO — NEXT-GEN ACADEMIC RESEARCH & DEFENSE INTELLIGENCE
   ==================================================================== */

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {{
    --primary: #6366f1;
    --primary-light: #818cf8;
    --primary-glow: rgba(99, 102, 241, 0.35);
    --cyan: #06b6d4;
    --cyan-glow: rgba(6, 182, 212, 0.35);
    --emerald: #10b981;
    --amber: #f59e0b;
    --rose: #f43f5e;
    --bg-deep: #070a12;
    --bg-card: rgba(15, 23, 42, 0.72);
    --bg-card-hover: rgba(22, 33, 62, 0.85);
    --border-subtle: rgba(255, 255, 255, 0.08);
    --border-highlight: rgba(99, 102, 241, 0.32);
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
}}

.stApp {{
    background-color: var(--bg-deep) !important;
    background-image: url("data:image/svg+xml,{_ENCODED_SVG}") !important;
    background-size: cover !important;
    background-position: center top !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important;
    color: var(--text-main) !important;
    font-family: var(--font-sans) !important;
}}

header[data-testid="stHeader"] {{
    background: transparent !important;
}}

.block-container {{
    max-width: 1260px !important;
    padding-top: 1.2rem !important;
    padding-bottom: 4.5rem !important;
}}

/* Top Navigation Bar */
.sai-top-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(99, 102, 241, 0.22);
    padding: 0.6rem 0.4rem 1rem 0.4rem;
    margin-bottom: 1.8rem;
    font-family: var(--font-mono);
    font-size: 0.78rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}}

.sai-brand-badge {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}

.sai-logo-gem {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 8px;
    background: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%);
    color: #ffffff;
    font-size: 0.85rem;
    font-weight: 800;
    box-shadow: 0 0 14px rgba(99, 102, 241, 0.5);
}}

.sai-meta-group {{
    display: flex;
    gap: 2.2rem;
    align-items: center;
    flex-wrap: wrap;
}}

.sai-meta-item {{
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}}

.sai-meta-label {{
    color: #64748b;
    font-size: 0.66rem;
    letter-spacing: 0.12em;
}}

.sai-meta-val {{
    color: #e2e8f0;
    font-weight: 600;
    letter-spacing: 0.08em;
}}

.sai-meta-val.cyan {{
    color: #38bdf8;
    text-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
}}

.sai-meta-val.indigo {{
    color: #a5b4fc;
    text-shadow: 0 0 10px rgba(99, 102, 241, 0.4);
}}

/* Hero Section */
.sai-hero {{
    text-align: center;
    padding: 2.2rem 1.5rem 2.6rem 1.5rem;
    margin-bottom: 2.2rem;
    position: relative;
    background: linear-gradient(180deg, rgba(30, 27, 75, 0.35) 0%, rgba(15, 23, 42, 0.45) 100%);
    border: 1px solid rgba(99, 102, 241, 0.18);
    border-radius: 18px;
    backdrop-filter: blur(14px);
    box-shadow: 0 12px 35px -8px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
}}

.sai-hero-emblem {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 64px;
    height: 64px;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(6, 182, 212, 0.2) 100%);
    border: 1px solid rgba(129, 140, 248, 0.4);
    box-shadow: 0 4px 25px rgba(99, 102, 241, 0.35);
    margin-bottom: 1.1rem;
    font-size: 1.85rem;
}}

.sai-hero-title {{
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    margin: 0;
    padding: 0;
    background: linear-gradient(180deg, #ffffff 40%, #c7d2fe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 2px 14px rgba(99, 102, 241, 0.3));
}}

.sai-hero-subtitle {{
    font-size: 1.05rem;
    color: #94a3b8;
    max-width: 720px;
    margin: 0.8rem auto 1.4rem auto;
    line-height: 1.6;
    font-weight: 400;
}}

.sai-hero-badges {{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.9rem;
    flex-wrap: wrap;
}}

.sai-badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(99, 102, 241, 0.28);
    padding: 0.4rem 1.05rem;
    border-radius: 9999px;
    font-size: 0.76rem;
    color: #c7d2fe;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 600;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 14px rgba(2, 6, 23, 0.4);
}}

.sai-pulse-dot {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #6366f1;
    box-shadow: 0 0 10px #6366f1;
}}

.sai-pulse-dot.cyan {{
    background: #06b6d4;
    box-shadow: 0 0 10px #06b6d4;
}}

.sai-pulse-dot.emerald {{
    background: #10b981;
    box-shadow: 0 0 10px #10b981;
}}

/* Containers & Glassmorphic Cards */
div[data-testid="stContainer"][border="true"],
div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] {{
    background: var(--bg-card) !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 14px !important;
    box-shadow: 0 10px 28px -5px rgba(0, 0, 0, 0.5) !important;
    transition: all 0.25s ease !important;
}}

div[data-testid="stContainer"][border="true"]:hover {{
    border-color: var(--border-highlight) !important;
    box-shadow: 0 14px 34px -5px rgba(0, 0, 0, 0.6), 0 0 20px rgba(99, 102, 241, 0.12) !important;
}}

/* Interactive Step / Feature Cards */
.sai-card-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.25rem;
    margin: 1.2rem 0 1.8rem 0;
}}

.sai-card {{
    background: rgba(17, 24, 39, 0.68);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 1.5rem 1.3rem;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.45);
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    height: 100%;
    position: relative;
    overflow: hidden;
}}

.sai-card:hover {{
    transform: translateY(-3px);
    border-color: rgba(99, 102, 241, 0.45);
    box-shadow: 0 14px 30px -6px rgba(0, 0, 0, 0.6), 0 0 22px rgba(99, 102, 241, 0.16);
}}

.sai-card-num {{
    font-family: var(--font-mono);
    font-size: 0.74rem;
    color: #818cf8;
    font-weight: 700;
    letter-spacing: 0.12em;
    margin-bottom: 0.5rem;
}}

.sai-card-title {{
    font-size: 1.15rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 0.5rem;
}}

.sai-card-desc {{
    font-size: 0.88rem;
    color: #94a3b8;
    line-height: 1.55;
}}

/* Tabs Styling */
div[data-testid="stTabs"] {{
    margin-top: 0.6rem;
}}

div[data-testid="stTabs"] button[role="tab"] {{
    background: transparent !important;
    border: none !important;
    color: #94a3b8 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1.4rem !important;
    border-radius: 8px 8px 0 0 !important;
    transition: all 0.2s ease !important;
}}

div[data-testid="stTabs"] button[role="tab"]:hover {{
    color: #c7d2fe !important;
    background: rgba(99, 102, 241, 0.08) !important;
}}

div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {{
    color: #ffffff !important;
    border-bottom: 2px solid #6366f1 !important;
    background: rgba(99, 102, 241, 0.12) !important;
    text-shadow: 0 0 12px rgba(99, 102, 241, 0.5);
}}

/* Buttons Styling */
button[data-testid="baseButton-primary"] {{
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border: 1px solid rgba(129, 140, 248, 0.4) !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.35) !important;
    transition: all 0.2s ease !important;
}}

button[data-testid="baseButton-primary"]:hover {{
    background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%) !important;
    box-shadow: 0 6px 22px rgba(99, 102, 241, 0.5) !important;
    transform: translateY(-1px);
}}

button[data-testid="baseButton-secondary"] {{
    background: rgba(17, 24, 39, 0.7) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
}}

button[data-testid="baseButton-secondary"]:hover {{
    border-color: rgba(99, 102, 241, 0.4) !important;
    background: rgba(30, 41, 59, 0.8) !important;
    color: #ffffff !important;
    transform: translateY(-1px);
}}

/* Metrics Tiles */
div[data-testid="stMetric"] {{
    background: rgba(17, 24, 39, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    padding: 1.1rem !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35) !important;
}}

div[data-testid="stMetricLabel"] {{
    color: #94a3b8 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}}

div[data-testid="stMetricValue"] {{
    color: #f8fafc !important;
    font-size: 1.7rem !important;
    font-weight: 800 !important;
}}

/* Sidebar styling */
section[data-testid="stSidebar"] {{
    background: #070a12 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}}

section[data-testid="stSidebar"] div.block-container {{
    padding-top: 1.8rem !important;
}}

/* Status and info callouts */
div[data-testid="stAlert"] {{
    background: rgba(17, 24, 39, 0.75) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
}}

div[data-testid="stAlert"][data-baseweb="notification"] {{
    background: rgba(17, 24, 39, 0.75) !important;
}}

/* Expanders */
div[data-testid="stExpander"] {{
    background: rgba(17, 24, 39, 0.55) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 10px !important;
    margin-top: 0.45rem !important;
    margin-bottom: 0.45rem !important;
}}

div[data-testid="stExpander"]:hover {{
    border-color: rgba(99, 102, 241, 0.35) !important;
}}

/* Form inputs */
div[data-baseweb="input"] > div {{
    background: rgba(17, 24, 39, 0.85) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 8px !important;
}}

div[data-baseweb="textarea"] > div {{
    background: rgba(17, 24, 39, 0.85) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 8px !important;
}}

div[data-baseweb="select"] > div {{
    background: rgba(17, 24, 39, 0.85) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 8px !important;
}}

/* Custom scrollbars */
::-webkit-scrollbar {{
    width: 7px;
    height: 7px;
}}

::-webkit-scrollbar-track {{
    background: rgba(7, 10, 18, 0.6);
}}

::-webkit-scrollbar-thumb {{
    background: rgba(99, 102, 241, 0.35);
    border-radius: 4px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: rgba(99, 102, 241, 0.55);
}}

/* Responsive adjustments */
@media (max-width: 768px) {{
    .sai-top-bar {{
        flex-direction: column;
        align-items: flex-start;
        gap: 0.9rem;
    }}
    .sai-meta-group {{
        gap: 1.2rem;
    }}
    .sai-hero-title {{
        font-size: 1.9rem;
    }}
    .sai-hero-subtitle {{
        font-size: 0.94rem;
    }}
}}
</style>
"""


def get_header_html() -> str:
    """Generate the top navigation and metadata header."""
    return """
    <div class="sai-top-bar">
      <div class="sai-brand-badge">
        <span class="sai-logo-gem">✦</span>
        <div class="sai-meta-item">
          <span class="sai-meta-label">APPLICATION</span>
          <span class="sai-meta-val cyan">SCHOLARAI STUDIO</span>
        </div>
      </div>
      <div class="sai-meta-group">
        <div class="sai-meta-item">
          <span class="sai-meta-label">DEVELOPER</span>
          <span class="sai-meta-val indigo">PRAJWAL</span>
        </div>
        <div class="sai-meta-item">
          <span class="sai-meta-label">ARCHITECTURE</span>
          <span class="sai-meta-val">GROUNDED RAG & VIVA</span>
        </div>
        <div class="sai-meta-item">
          <span class="sai-meta-label">STATUS</span>
          <span class="sai-meta-val cyan">● ACTIVE</span>
        </div>
      </div>
    </div>
    """


def get_hero_html() -> str:
    """Generate the central visual hero banner."""
    return """
    <div class="sai-hero">
      <div class="sai-hero-emblem">🎓</div>
      <h1 class="sai-hero-title">SCHOLARAI STUDIO</h1>
      <p class="sai-hero-subtitle">
        Intelligent paper synthesis, page-grounded retrieval Q&A, automated widescreen presentation decks, 
        and real-time oral defense (viva) simulation.
      </p>
      <div class="sai-hero-badges">
        <div class="sai-badge">
          <span class="sai-pulse-dot"></span>
          <span>Vector RAG</span>
        </div>
        <div class="sai-badge">
          <span class="sai-pulse-dot cyan"></span>
          <span>6-Section Synthesis</span>
        </div>
        <div class="sai-badge">
          <span class="sai-pulse-dot emerald"></span>
          <span>Oral Defense Simulator</span>
        </div>
        <div class="sai-badge">
          <span class="sai-pulse-dot"></span>
          <span>PowerPoint Engine</span>
        </div>
      </div>
    </div>
    """


def get_workflow_cards_html() -> str:
    """Generate the 4 interactive workflow overview cards."""
    return """
    <div class="sai-card-grid">
      <div class="sai-card">
        <div class="sai-card-num">STAGE 01 · EXTRACTION</div>
        <div class="sai-card-title">Page-Aware Ingestion</div>
        <div class="sai-card-desc">
          Upload any digital PDF research paper. PyMuPDF extracts text per page while preserving 1-based page coordinates for strict citation provenance.
        </div>
      </div>
      <div class="sai-card">
        <div class="sai-card-num">STAGE 02 · SYNTHESIS</div>
        <div class="sai-card-title">Academic Synthesis</div>
        <div class="sai-card-desc">
          Synthesize full-paper executive summaries across 6 core academic dimensions and extract distinct conceptual frameworks with verifiable citations.
        </div>
      </div>
      <div class="sai-card">
        <div class="sai-card-num">STAGE 03 · GROUNDED RAG</div>
        <div class="sai-card-title">Grounded Vector Q&A</div>
        <div class="sai-card-desc">
          Query the active paper using Gemini embeddings and ChromaDB vector store. Every answer is strictly anchored to retrieved excerpt passages.
        </div>
      </div>
      <div class="sai-card">
        <div class="sai-card-num">STAGE 04 · DEFENSE & DECK</div>
        <div class="sai-card-title">Viva Exam & Slides</div>
        <div class="sai-card-desc">
          Practice adaptive 6-turn oral defense examinations with rubric scoring, and generate widescreen 16:9 presentation slide decks with notes.
        </div>
      </div>
    </div>
    """


def get_footer_html() -> str:
    """Generate the clean, professional application footer."""
    return """
    <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid rgba(99,102,241,0.2); padding-top:1.6rem; margin-top:3.5rem; font-family:var(--font-mono); font-size:0.75rem; color:#64748b;">
      <span style="color:#818cf8; font-size:1.1rem;">◈</span>
      <span style="letter-spacing:0.1em; text-transform:uppercase;">SCHOLARAI STUDIO · ENGINEERED BY PRAJWAL · ALL RIGHTS RESERVED</span>
      <span style="color:#818cf8; font-size:1.1rem;">◈</span>
    </div>
    """
