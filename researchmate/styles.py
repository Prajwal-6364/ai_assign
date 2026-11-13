"""Modern indigo/slate glassmorphic theme for ScholarAI."""

import urllib.parse

# Crisp modern minimalist technical grid SVG
_BACKGROUND_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice">
<defs>
  <radialGradient id="meshGradient" cx="50%" cy="15%" r="65%">
    <stop offset="0%" stop-color="#1e1b4b" stop-opacity="0.75"/>
    <stop offset="40%" stop-color="#0f172a" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="#090d16" stop-opacity="1"/>
  </radialGradient>
  <radialGradient id="glowTopRight" cx="85%" cy="10%" r="35%">
    <stop offset="0%" stop-color="#6366f1" stop-opacity="0.18"/>
    <stop offset="100%" stop-color="#090d16" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowBottomLeft" cx="15%" cy="85%" r="40%">
    <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.14"/>
    <stop offset="100%" stop-color="#090d16" stop-opacity="0"/>
  </radialGradient>
  <pattern id="dotGrid" width="36" height="36" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.2" fill="rgba(255, 255, 255, 0.05)"/>
  </pattern>
</defs>

<rect width="1440" height="900" fill="url(#meshGradient)"/>
<rect width="1440" height="900" fill="url(#dotGrid)"/>
<rect width="1440" height="900" fill="url(#glowTopRight)"/>
<rect width="1440" height="900" fill="url(#glowBottomLeft)"/>
</svg>"""

_ENCODED_SVG = urllib.parse.quote(_BACKGROUND_SVG.replace("\n", " ").strip())

CUSTOM_CSS = f"""
<style>
/* ====================================================================
   SCHOLARAI — CLEAN MODERN SLATE & INDIGO WORKSPACE
   ==================================================================== */

.stApp {{
    background-color: #0b0f19 !important;
    background-image: url("data:image/svg+xml,{_ENCODED_SVG}") !important;
    background-size: cover !important;
    background-position: center top !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important;
    color: #f3f4f6 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif !important;
}}

header[data-testid="stHeader"] {{
    background: transparent !important;
}}

.block-container {{
    max-width: 1220px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 4rem !important;
}}

.rm-corner-star {{
    color: #818cf8;
    font-size: 1.25rem;
    line-height: 1;
    display: inline-block;
    filter: drop-shadow(0 0 8px rgba(129, 140, 248, 0.6));
    user-select: none;
}}

.rm-top-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(99, 102, 241, 0.2);
    padding: 0.6rem 0.2rem 1rem 0.2rem;
    margin-bottom: 1.8rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}}

.rm-meta-group {{
    display: flex;
    gap: 2rem;
    align-items: center;
    flex-wrap: wrap;
}}

.rm-meta-item {{
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}}

.rm-meta-label {{
    color: #64748b;
    font-size: 0.68rem;
}}

.rm-meta-val {{
    color: #e2e8f0;
    font-weight: 600;
    letter-spacing: 0.08em;
}}

.rm-meta-val.cyan {{
    color: #818cf8;
    text-shadow: 0 0 10px rgba(99, 102, 241, 0.4);
}}

/* Central Hero Banner */
.rm-hero {{
    text-align: center;
    padding: 1.8rem 1rem 2.2rem 1rem;
    margin-bottom: 2rem;
    position: relative;
}}

.rm-hero-emblem {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 58px;
    height: 58px;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(59, 130, 246, 0.15) 100%);
    border: 1px solid rgba(129, 140, 248, 0.35);
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.25);
    margin-bottom: 1rem;
    font-size: 1.6rem;
}}

.rm-hero-title {{
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin: 0;
    padding: 0;
    background: linear-gradient(180deg, #ffffff 40%, #c7d2fe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 2px 12px rgba(99, 102, 241, 0.25));
}}

.rm-hero-subtitle {{
    font-size: 1.02rem;
    color: #94a3b8;
    max-width: 660px;
    margin: 0.6rem auto 1.2rem auto;
    line-height: 1.55;
    font-weight: 400;
}}

.rm-hero-badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid rgba(99, 102, 241, 0.3);
    padding: 0.35rem 0.95rem;
    border-radius: 9999px;
    font-size: 0.76rem;
    color: #a5b4fc;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 600;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 14px rgba(2, 6, 23, 0.35);
}}

.rm-pulse-dot {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #6366f1;
    box-shadow: 0 0 8px #6366f1;
}}

/* Clean containers */
div[data-testid="stContainer"],
div.st-emotion-cache-16txtl3,
div.st-emotion-cache-ocqkz7 {{
    border-radius: 12px !important;
}}

div[data-testid="stContainer"][border="true"],
div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] {{
    background: rgba(17, 24, 39, 0.65) !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.45) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}}

div[data-testid="stContainer"][border="true"]:hover {{
    border-color: rgba(99, 102, 241, 0.35) !important;
    box-shadow: 0 12px 30px -5px rgba(0, 0, 0, 0.55), 0 0 15px rgba(99, 102, 241, 0.1) !important;
}}

/* Workflow Step Cards in Overview Tab */
.rm-step-card {{
    background: rgba(17, 24, 39, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 1.4rem 1.2rem;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.4);
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    height: 100%;
}}

.rm-step-card:hover {{
    transform: translateY(-2px);
    border-color: rgba(99, 102, 241, 0.4);
    box-shadow: 0 12px 28px -6px rgba(0, 0, 0, 0.5), 0 0 18px rgba(99, 102, 241, 0.15);
}}

.rm-step-num {{
    font-family: ui-monospace, monospace;
    font-size: 0.78rem;
    color: #818cf8;
    font-weight: 700;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}}

.rm-step-title {{
    font-size: 1.12rem;
    font-weight: 700;
    color: #f9fafb;
    margin-bottom: 0.4rem;
}}

.rm-step-desc {{
    font-size: 0.86rem;
    color: #94a3b8;
    line-height: 1.5;
}}

/* Tabs Styling */
div[data-testid="stTabs"] {{
    margin-top: 0.5rem;
}}

div[data-testid="stTabs"] button[role="tab"] {{
    background: transparent !important;
    color: #94a3b8 !important;
    border-radius: 8px 8px 0 0 !important;
    border: none !important;
    font-size: 0.94rem !important;
    font-weight: 500 !important;
    padding: 0.65rem 1.25rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
}}

div[data-testid="stTabs"] button[role="tab"]:hover {{
    color: #e5e7eb !important;
    background: rgba(99, 102, 241, 0.08) !important;
}}

div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {{
    color: #818cf8 !important;
    font-weight: 700 !important;
    background: rgba(30, 27, 75, 0.4) !important;
    border-bottom: 2px solid #6366f1 !important;
}}

/* File Uploader styling */
div[data-testid="stFileUploader"] {{
    background: rgba(17, 24, 39, 0.6) !important;
    border: 1px dashed rgba(99, 102, 241, 0.35) !important;
    border-radius: 12px !important;
    padding: 1.2rem !important;
    backdrop-filter: blur(10px) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}}

div[data-testid="stFileUploader"]:hover {{
    border-color: #818cf8 !important;
    box-shadow: 0 0 16px rgba(99, 102, 241, 0.2) !important;
}}

div[data-testid="stFileUploader"] section {{
    background: transparent !important;
    border: none !important;
}}

/* Alert Banners */
div[data-testid="stAlert"] {{
    border-radius: 10px !important;
    backdrop-filter: blur(12px) !important;
    padding: 0.9rem 1.1rem !important;
    font-weight: 500 !important;
}}

div[data-testid="stAlert"] div[role="alert"] {{
    background: transparent !important;
    color: #f9fafb !important;
}}

/* Extracted Text Content Box */
.rm-text-preview-box {{
    background: rgba(11, 15, 25, 0.95) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 10px !important;
    padding: 1.2rem !important;
    color: #f3f4f6 !important;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
    font-size: 0.88rem !important;
    line-height: 1.65 !important;
    white-space: pre-wrap !important;
    word-break: break-word !important;
    box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.5) !important;
}}

/* Sidebar styling */
section[data-testid="stSidebar"] {{
    background: #080c14 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}}

section[data-testid="stSidebar"] div.block-container {{
    padding-top: 2rem !important;
}}

/* Form elements, selects, buttons */
div[data-baseweb="select"] > div {{
    background: rgba(17, 24, 39, 0.85) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 8px !important;
    color: #f9fafb !important;
}}

div[data-baseweb="select"] * {{
    color: #f9fafb !important;
}}

div[data-baseweb="popover"] {{
    background: #111827 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
}}

div[data-baseweb="popover"] li {{
    color: #f3f4f6 !important;
}}

div[data-baseweb="popover"] li:hover {{
    background: rgba(99, 102, 241, 0.2) !important;
}}

/* Expandable Citations */
div[data-testid="stExpander"] {{
    background: rgba(17, 24, 39, 0.55) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 10px !important;
    margin-top: 0.4rem !important;
    margin-bottom: 0.4rem !important;
}}

div[data-testid="stExpander"]:hover {{
    border-color: rgba(99, 102, 241, 0.35) !important;
}}

div[data-testid="stExpander"] summary {{
    color: #e5e7eb !important;
    font-size: 0.88rem !important;
}}

/* Custom scrollbars */
::-webkit-scrollbar {{
    width: 7px;
    height: 7px;
}}

::-webkit-scrollbar-track {{
    background: rgba(11, 15, 25, 0.6);
}}

::-webkit-scrollbar-thumb {{
    background: rgba(99, 102, 241, 0.3);
    border-radius: 4px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: rgba(99, 102, 241, 0.5);
}}

/* Responsive adjustments */
@media (max-width: 768px) {{
    .rm-top-bar {{
        flex-direction: column;
        align-items: flex-start;
        gap: 0.8rem;
    }}
    .rm-meta-group {{
        gap: 1rem;
    }}
    .rm-hero-title {{
        font-size: 1.8rem;
    }}
    .rm-hero-subtitle {{
        font-size: 0.92rem;
    }}
    .rm-step-card {{
        margin-bottom: 0.8rem;
    }}
}}
</style>
"""


def get_header_html() -> str:
    """Generate the top metadata bar."""
    return """
    <div class="rm-top-bar">
      <div style="display:flex; align-items:center; gap:0.6rem;">
        <span class="rm-corner-star">◈</span>
        <div class="rm-meta-item">
          <span class="rm-meta-label">SYSTEM</span>
          <span class="rm-meta-val cyan">SCHOLARAI WORKBENCH</span>
        </div>
      </div>
      <div class="rm-meta-group">
        <div class="rm-meta-item">
          <span class="rm-meta-label">MODULES</span>
          <span class="rm-meta-val">PAPER SYNTHESIS & VIVA</span>
        </div>
        <div class="rm-meta-item">
          <span class="rm-meta-label">ENGINE</span>
          <span class="rm-meta-val">GROUNDED VECTOR RAG</span>
        </div>
      </div>
      <span class="rm-corner-star">◈</span>
    </div>
    """


def get_hero_html() -> str:
    """Generate the central modern hero banner."""
    return """
    <div class="rm-hero">
      <div class="rm-hero-emblem">🎓</div>
      <h1 class="rm-hero-title">SCHOLARAI</h1>
      <p class="rm-hero-subtitle">
        Accelerate academic reading, convert research papers into presentation decks, 
        and prepare for your defense with interactive viva practice.
      </p>
      <div class="rm-hero-badge">
        <span class="rm-pulse-dot"></span>
        <span>Academic Assistant · Document Intelligence</span>
      </div>
    </div>
    """


def get_workflow_cards_html() -> str:
    """Generate 3 workflow cards for the Overview tab."""
    return """
    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:1.2rem; margin:1rem 0 1.5rem 0;">
      <div class="rm-step-card">
        <div class="rm-step-num">STEP 01</div>
        <div class="rm-step-title">Document Parsing</div>
        <div class="rm-step-desc">
          Upload any academic paper in PDF format. Text and structure are extracted with 1-based page coordinates.
        </div>
      </div>
      <div class="rm-step-card">
        <div class="rm-step-num">STEP 02</div>
        <div class="rm-step-title">Grounded Q&A</div>
        <div class="rm-step-desc">
          Ask questions against indexed embeddings. Every answer is grounded directly in citations.
        </div>
      </div>
      <div class="rm-step-card">
        <div class="rm-step-num">STEP 03</div>
        <div class="rm-step-title">Defense & Slides</div>
        <div class="rm-step-desc">
          Generate presentation slides and test your understanding with simulated mock viva sessions.
        </div>
      </div>
    </div>
    """
