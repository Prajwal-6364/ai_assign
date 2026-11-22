"""ScholarAI Studio: Next-Generation Academic Research & Defense Intelligence Copilot."""

import html
import random
import streamlit as st
import pandas as pd
import plotly.express as px
from collections import defaultdict

from scholarai.analysis import (
    extract_paper_concepts,
    generate_paper_summary,
)
from scholarai.config import settings
from scholarai.pdf import PDFProcessingError, extract_pages_from_pdf
from scholarai.presentation import (
    THEMES,
    PresentationError,
    generate_presentation,
    render_slide_html,
)
from scholarai.rag import (
    EmbeddingError,
    GenerationError,
    MissingAPIKeyError,
    RAGError,
    RetrievalError,
    format_actionable_error,
    is_paper_fully_indexed,
)
from scholarai.router import execute_routed_request
from scholarai.viva import evaluate_viva_answer, start_viva
from scholarai.flashcards import generate_flashcards
from scholarai.progress import load_viva_history, save_completed_viva
from scholarai.styles import (
    CUSTOM_CSS,
    get_header_html,
    get_hero_html,
    get_workflow_cards_html,
    get_footer_html,
)

# Page configuration
st.set_page_config(
    page_title="ScholarAI Studio — Research & Defense Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject custom modern glassmorphic stylesheet
st.html(CUSTOM_CSS)

# Initialize session state variables
if "extracted_pages" not in st.session_state:
    st.session_state["extracted_pages"] = None
if "paper_pages" not in st.session_state:
    st.session_state["paper_pages"] = None
if "uploaded_paper_name" not in st.session_state:
    st.session_state["uploaded_paper_name"] = None
if "pdf_error" not in st.session_state:
    st.session_state["pdf_error"] = None
if "last_uploaded_file_id" not in st.session_state:
    st.session_state["last_uploaded_file_id"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "paper_summary_data" not in st.session_state:
    st.session_state["paper_summary_data"] = None
if "paper_concepts_data" not in st.session_state:
    st.session_state["paper_concepts_data"] = None
if "presentation_data" not in st.session_state:
    st.session_state["presentation_data"] = None
if "presenter_mode" not in st.session_state:
    st.session_state["presenter_mode"] = False
if "current_slide_idx" not in st.session_state:
    st.session_state["current_slide_idx"] = 0
if "viva_session" not in st.session_state:
    st.session_state["viva_session"] = None
if "flashcard_deck" not in st.session_state:
    st.session_state["flashcard_deck"] = None
if "flashcard_index" not in st.session_state:
    st.session_state["flashcard_index"] = 0
if "flashcard_revealed" not in st.session_state:
    st.session_state["flashcard_revealed"] = False

VIVA_QUESTION_LIMIT = 6


def reset_paper_features():
    """Reset downstream analysis and chat states when a new paper is loaded."""
    st.session_state["chat_history"] = []
    st.session_state["paper_summary_data"] = None
    st.session_state["paper_concepts_data"] = None
    st.session_state["presentation_data"] = None
    st.session_state["presenter_mode"] = False
    st.session_state["current_slide_idx"] = 0
    st.session_state["viva_session"] = None
    st.session_state["flashcard_deck"] = None
    st.session_state["flashcard_index"] = 0
    st.session_state["flashcard_revealed"] = False


# Top navigation metadata bar
st.html(get_header_html())

# Central hero banner
st.html(get_hero_html())

# Sidebar Configuration & Telemetry
with st.sidebar:
    st.markdown("### 🎓 ScholarAI Studio")
    st.caption("Engineered by **Prajwal** (`Prajwal-6364`)")
    st.divider()

    st.subheader("System Telemetry")
    if settings.gemini_api_key and settings.gemini_api_key.strip() not in ("", "your_gemini_api_key_here"):
        st.success("Gemini API Online", icon=":material/check_circle:")
    else:
        st.info("Add GEMINI_API_KEY in local .env to activate reasoning.", icon=":material/key:")
    
    st.markdown(f"**Reasoning Engine:** `{settings.gemini_model}`")
    st.markdown(f"**Embedding Model:** `{settings.gemini_embedding_model}`")
    st.markdown(f"**Vector Database:** `ChromaDB (Local)`")

    if st.session_state.get("uploaded_paper_name") and st.session_state.get("extracted_pages"):
        st.divider()
        st.subheader("Active Document")
        pages = st.session_state["extracted_pages"]
        total_p = len(pages)
        total_words = sum(p.word_count for p in pages)
        est_read_min = max(1, round(total_words / 200))

        st.markdown(f"📄 **{st.session_state['uploaded_paper_name']}**")
        st.caption(f"{total_p} pages · {total_words:,} words · ~{est_read_min} min read")

        if is_paper_fully_indexed(st.session_state["uploaded_paper_name"], pages=pages):
            st.success("Vector Index: Indexed & Grounded", icon=":material/verified:")
        else:
            st.caption("⚡ Vector Index: Ready (On Demand)")

        st.markdown("##### Artifacts Status")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.caption("📑 Summary: " + ("✅ Ready" if st.session_state.get("paper_summary_data") else "— Pending"))
            st.caption("📊 Slides: " + ("✅ Ready" if st.session_state.get("presentation_data") else "— Pending"))
        with col_s2:
            st.caption("💡 Concepts: " + ("✅ Ready" if st.session_state.get("paper_concepts_data") else "— Pending"))
            st.caption("🃏 Cards: " + ("✅ Ready" if st.session_state.get("flashcard_deck") else "— Pending"))

        st.divider()
        if st.button("Unload Active Paper", icon=":material/close:", width="stretch"):
            st.session_state["extracted_pages"] = None
            st.session_state["paper_pages"] = None
            st.session_state["uploaded_paper_name"] = None
            st.session_state["last_uploaded_file_id"] = None
            reset_paper_features()
            st.rerun()

# Main Application Tabs
tab_overview, tab_intake, tab_chat, tab_viva, tab_slides, tab_cards, tab_dashboard = st.tabs(
    [
        "🌟 Overview",
        "📄 Intake & Analysis",
        "💬 Grounded Q&A",
        "🎓 Viva Simulator",
        "📊 Presentation Studio",
        "🃏 Flashcards",
        "📈 Learning Analytics",
    ]
)

# ====================================================================
# TAB 1: OVERVIEW & ARCHITECTURE
# ====================================================================
with tab_overview:
    st.subheader("Architectural Foundation & Capabilities")
    st.html(get_workflow_cards_html())

    with st.container(border=True):
        st.markdown("#### ⚡ Core Capabilities Matrix")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            - **Page-Aware Ingestion**: PyMuPDF parses documents preserving exact 1-based page numbers.
            - **6-Dimension Academic Synthesis**: Problem, Objective, Methodology, Findings, Conclusion, Limitations.
            - **Grounded Vector RAG**: Scoped ChromaDB collections with strict document isolation.
            """)
        with c2:
            st.markdown("""
            - **Widescreen Slide Builder**: Generates 16:9 PowerPoint decks with presenter notes and citations.
            - **Adaptive Viva Simulator**: Multi-turn oral exam agent with rubric evaluation and scoring.
            - **Revision Cards & Analytics**: Topic-mastery tracking and paper-grounded flashcards.
            """)

    st.info(
        "Upload any academic paper in the **Intake & Analysis** tab to start analyzing, asking questions, "
        "and preparing your defense presentation.",
        icon=":material/lightbulb:",
    )

# ====================================================================
# TAB 2: PAPER INTAKE & FULL SYNTHESIS
# ====================================================================
with tab_intake:
    st.subheader("Research Paper Intake & Document Inspector")
    st.caption("Upload your PDF research paper to inspect page text, generate comprehensive summaries, and extract conceptual frameworks.")

    uploaded_file = st.file_uploader(
        "Upload a research paper (PDF)",
        type=["pdf"],
        key="pdf_uploader",
        help="Upload an academic research paper PDF containing digital selectable text.",
    )

    if uploaded_file is not None:
        file_id = (uploaded_file.name, uploaded_file.size)
        if st.session_state["last_uploaded_file_id"] != file_id:
            st.session_state["last_uploaded_file_id"] = file_id
            try:
                pages = extract_pages_from_pdf(
                    uploaded_file.getvalue(), filename=uploaded_file.name
                )
                st.session_state["extracted_pages"] = pages
                st.session_state["paper_pages"] = pages
                st.session_state["uploaded_paper_name"] = uploaded_file.name
                st.session_state["pdf_error"] = None
                reset_paper_features()
            except PDFProcessingError as err:
                st.session_state["extracted_pages"] = None
                st.session_state["paper_pages"] = None
                st.session_state["uploaded_paper_name"] = None
                st.session_state["pdf_error"] = str(err)
                reset_paper_features()
            except Exception as err:
                st.session_state["extracted_pages"] = None
                st.session_state["paper_pages"] = None
                st.session_state["uploaded_paper_name"] = None
                st.session_state["pdf_error"] = f"Unexpected error reading '{uploaded_file.name}': {err}"
                reset_paper_features()
    else:
        if st.session_state.get("last_uploaded_file_id") is not None:
            st.session_state["extracted_pages"] = None
            st.session_state["paper_pages"] = None
            st.session_state["uploaded_paper_name"] = None
            st.session_state["pdf_error"] = None
            st.session_state["last_uploaded_file_id"] = None
            reset_paper_features()

    if st.session_state["pdf_error"]:
        st.error(st.session_state["pdf_error"], icon=":material/error:")
    elif st.session_state["extracted_pages"]:
        pages = st.session_state["extracted_pages"]
        total_pages = len(pages)
        st.success(
            f"Successfully processed **{st.session_state['uploaded_paper_name']}** ({total_pages} pages parsed with coordinates).",
            icon=":material/check_circle:",
        )

        # Page Reader Workspace
        with st.container(border=True):
            col_sel, col_stats = st.columns([2, 1], vertical_alignment="center")
            with col_sel:
                selected_page_num = st.selectbox(
                    "Inspect Page Content",
                    options=list(range(1, total_pages + 1)),
                    format_func=lambda p: f"Page {p} of {total_pages}",
                    key="page_inspector_select",
                )
            with col_stats:
                cur_page = pages[selected_page_num - 1]
                st.markdown(f"**Word Count:** {cur_page.word_count:,} · **Characters:** {cur_page.char_count:,}")

            if cur_page.text.strip():
                st.text_area(
                    label=f"Page {selected_page_num} Text",
                    value=cur_page.text,
                    height=280,
                    disabled=True,
                    label_visibility="collapsed",
                )
            else:
                st.info("No readable text detected on this page. It may contain figures or tables.", icon=":material/info:")

        # Full-Paper Synthesis Area
        st.divider()
        st.subheader("Academic Synthesis Engine")
        st.caption("Full-paper synthesis grounded strictly in page excerpts with evidence citations.")

        syn_tab_summary, syn_tab_concepts = st.tabs(["📑 6-Section Academic Summary", "💡 Key Conceptual Frameworks"])

        with syn_tab_summary:
            st.markdown("##### Executive Academic Summary")
            st.caption("Synthesizes Problem, Objective, Methodology & Data, Key Findings, Conclusion, and Limitations.")
            
            c_s_btn, c_s_time = st.columns([1, 2], vertical_alignment="center")
            with c_s_btn:
                btn_summary = st.button(
                    "Generate Summary" if not st.session_state.get("paper_summary_data") else "Regenerate Summary",
                    key="btn_generate_summary",
                    type="primary",
                    icon=":material/summarize:",
                )
            with c_s_time:
                if st.session_state.get("paper_summary_data"):
                    s_sec = st.session_state["paper_summary_data"].get("total_elapsed", 0.0)
                    st.caption(f"⚡ Synthesized in {s_sec:.1f}s")

            if btn_summary:
                if not settings.gemini_api_key or settings.gemini_api_key.strip() in ("", "your_gemini_api_key_here"):
                    st.error("Please add your GEMINI_API_KEY to .env to enable academic synthesis.", icon=":material/key:")
                else:
                    with st.status("Analyzing entire paper text & synthesizing...", expanded=True) as status_box:
                        def sum_prog(stage, msg, elapsed, extra=None):
                            status_box.write(f"⏱️ **[{elapsed:.1f}s]** {msg}")
                        try:
                            summary_res = generate_paper_summary(
                                filename=st.session_state["uploaded_paper_name"],
                                pages=pages,
                                on_progress=sum_prog,
                            )
                            status_box.update(label=f"Summary complete in {summary_res.get('total_elapsed', 0.0):.1f}s", state="complete", expanded=False)
                            st.session_state["paper_summary_data"] = summary_res
                        except Exception as exc:
                            status_box.update(label="Synthesis failed", state="error", expanded=True)
                            st.error(format_actionable_error(exc), icon=":material/error:")

            if st.session_state.get("paper_summary_data"):
                s_data = st.session_state["paper_summary_data"]
                with st.container(border=True):
                    st.markdown("#### 📄 Executive Summary")
                    st.markdown(s_data["summary"])

                    cited_p = s_data.get("cited_pages", [])
                    p_sources = s_data.get("page_sources", {})
                    if cited_p and p_sources:
                        st.divider()
                        st.caption("🔍 **Verifiable Evidence & Source Passages:**")
                        for p_num in cited_p:
                            if p_num in p_sources:
                                with st.expander(f"📄 Page {p_num} Evidence Source", expanded=False):
                                    st.caption(f"Document: {st.session_state['uploaded_paper_name']} · Page {p_num}")
                                    st.text(p_sources[p_num], wrap=True)

        with syn_tab_concepts:
            st.markdown("##### Key Concepts & Theoretical Frameworks")
            st.caption("Extracts 5–7 foundational and study-specific conceptual frameworks with plain-language definitions.")

            c_c_btn, c_c_time = st.columns([1, 2], vertical_alignment="center")
            with c_c_btn:
                btn_concepts = st.button(
                    "Extract Concepts" if not st.session_state.get("paper_concepts_data") else "Re-extract Concepts",
                    key="btn_extract_concepts",
                    type="primary",
                    icon=":material/lightbulb:",
                )
            with c_c_time:
                if st.session_state.get("paper_concepts_data"):
                    c_sec = st.session_state["paper_concepts_data"].get("total_elapsed", 0.0)
                    st.caption(f"⚡ Extracted in {c_sec:.1f}s")

            if btn_concepts:
                if not settings.gemini_api_key or settings.gemini_api_key.strip() in ("", "your_gemini_api_key_here"):
                    st.error("Please add your GEMINI_API_KEY to .env to enable concept extraction.", icon=":material/key:")
                else:
                    with st.status("Extracting key conceptual frameworks...", expanded=True) as status_box:
                        def con_prog(stage, msg, elapsed, extra=None):
                            status_box.write(f"⏱️ **[{elapsed:.1f}s]** {msg}")
                        try:
                            concepts_res = extract_paper_concepts(
                                filename=st.session_state["uploaded_paper_name"],
                                pages=pages,
                                on_progress=con_prog,
                            )
                            status_box.update(label=f"Concepts extracted in {concepts_res.get('total_elapsed', 0.0):.1f}s", state="complete", expanded=False)
                            st.session_state["paper_concepts_data"] = concepts_res
                        except Exception as exc:
                            status_box.update(label="Concept extraction failed", state="error", expanded=True)
                            st.error(format_actionable_error(exc), icon=":material/error:")

            if st.session_state.get("paper_concepts_data"):
                c_data = st.session_state["paper_concepts_data"]
                with st.container(border=True):
                    st.markdown("#### 💡 Key Concepts & Frameworks")
                    st.markdown(c_data["concepts"])

                    cited_p = c_data.get("cited_pages", [])
                    p_sources = c_data.get("page_sources", {})
                    if cited_p and p_sources:
                        st.divider()
                        st.caption("🔍 **Verifiable Concept Evidence Passages:**")
                        for p_num in cited_p:
                            if p_num in p_sources:
                                with st.expander(f"📄 Page {p_num} Evidence Source", expanded=False):
                                    st.caption(f"Document: {st.session_state['uploaded_paper_name']} · Page {p_num}")
                                    st.text(p_sources[p_num], wrap=True)

    else:
        st.info("Upload an academic research paper PDF above to preview pages and generate synthesis.", icon=":material/upload_file:")

# ====================================================================
# TAB 3: GROUNDED Q&A ASSISTANT (CONVERSATIONAL RAG & ROUTING)
# ====================================================================
with tab_chat:
    st.subheader("Grounded Paper Q&A Assistant")
    st.caption("Ask questions, explore specific methodologies, or request actions. ScholarAI automatically classifies your intent.")

    if not st.session_state.get("extracted_pages"):
        st.info("Upload a research paper in the Intake & Analysis tab first to enable Grounded Q&A.", icon=":material/info:")
    else:
        # Prompt Suggestion Chips
        st.markdown("##### Suggested Queries")
        chip_col1, chip_col2, chip_col3, chip_col4 = st.columns(4)
        selected_prompt = None
        with chip_col1:
            if st.button("🎯 Research Problem", width="stretch", key="chip_prob"):
                selected_prompt = "What is the primary research problem and motivating challenge of this paper?"
        with chip_col2:
            if st.button("⚙️ Methodology", width="stretch", key="chip_meth"):
                selected_prompt = "Describe the methodology, algorithm, or experimental setup in detail."
        with chip_col3:
            if st.button("📊 Empirical Findings", width="stretch", key="chip_find"):
                selected_prompt = "What were the key quantitative findings, benchmarks, and results?"
        with chip_col4:
            if st.button("⚠️ Limitations", width="stretch", key="chip_limit"):
                selected_prompt = "What are the acknowledged limitations and potential threats to validity?"

        with st.form("scholar_qa_form", clear_on_submit=True):
            user_question = st.text_input(
                "Ask a question or request an action",
                value=selected_prompt or "",
                placeholder="e.g. 'What dataset was used?', 'Summarize this paper', 'Extract key concepts', 'Can we practice viva?'",
                key="qa_input_box",
            )
            c_sub, c_stat = st.columns([1, 3], vertical_alignment="center")
            with c_sub:
                submit_qa = st.form_submit_button("Ask ScholarAI", type="primary", icon=":material/send:")
            with c_stat:
                if is_paper_fully_indexed(st.session_state["uploaded_paper_name"], pages=st.session_state["extracted_pages"]):
                    st.caption("⚡ ChromaDB Vector Index: Active (Fully Indexed)")
                else:
                    st.caption("ChromaDB Vector Index: Ready (Indexes on Query)")

        if submit_qa:
            if not user_question.strip():
                st.warning("Please type a question or request before submitting.", icon=":material/warning:")
            elif not settings.gemini_api_key or settings.gemini_api_key.strip() in ("", "your_gemini_api_key_here"):
                st.error("Gemini API key is missing. Add GEMINI_API_KEY in .env to query.", icon=":material/key:")
            else:
                with st.status("Routing request & querying vector knowledge...", expanded=True) as status_box:
                    def qa_prog(stage, msg, elapsed, extra=None):
                        status_box.write(f"⏱️ **[{elapsed:.1f}s]** {msg}")

                    try:
                        routed_res = execute_routed_request(
                            user_input=user_question.strip(),
                            filename=st.session_state["uploaded_paper_name"],
                            pages=st.session_state["extracted_pages"],
                            on_progress=qa_prog,
                            existing_summary_data=st.session_state.get("paper_summary_data"),
                            existing_concepts_data=st.session_state.get("paper_concepts_data"),
                            existing_presentation_data=st.session_state.get("presentation_data"),
                        )
                        total_time = routed_res.get("total_elapsed", 0.0)
                        route_lbl = routed_res.get("route_label", "Grounded Paper Chat")
                        status_box.update(label=f"Handled via {route_lbl} in {total_time:.1f}s", state="complete", expanded=False)

                        if routed_res.get("updated_summary_data"):
                            st.session_state["paper_summary_data"] = routed_res["updated_summary_data"]
                        if routed_res.get("updated_concepts_data"):
                            st.session_state["paper_concepts_data"] = routed_res["updated_concepts_data"]
                        if routed_res.get("updated_presentation_data"):
                            st.session_state["presentation_data"] = routed_res["updated_presentation_data"]

                        st.session_state["chat_history"].append({
                            "question": user_question.strip(),
                            "answer": routed_res["answer"],
                            "intent": routed_res["intent"],
                            "route_label": route_lbl,
                            "sources": routed_res.get("sources", []),
                            "cited_pages": routed_res.get("cited_pages", []),
                            "page_sources": routed_res.get("page_sources", {}),
                            "elapsed": total_time,
                        })
                    except Exception as exc:
                        status_box.update(label="Request failed", state="error", expanded=True)
                        st.error(format_actionable_error(exc), icon=":material/error:")

        # Conversation History
        if st.session_state.get("chat_history"):
            st.divider()
            c_hdr, c_clr = st.columns([3, 1], vertical_alignment="center")
            with c_hdr:
                st.markdown("#### Conversation History")
            with c_clr:
                if st.button("Clear History", icon=":material/delete:", key="btn_clear_chat"):
                    st.session_state["chat_history"] = []
                    st.rerun()

            for idx, item in enumerate(reversed(st.session_state["chat_history"])):
                with st.container(border=True):
                    col_q, col_tag = st.columns([3, 1], vertical_alignment="center")
                    with col_q:
                        st.markdown(f"**Query:** {item['question']}")
                    with col_tag:
                        st.caption(f":material/alt_route: **Route:** `{item.get('route_label', 'Grounded Chat')}`")

                    st.markdown(f"**ScholarAI:**\n\n{item['answer']}")
                    if item.get("elapsed"):
                        st.caption(f"⚡ Generated in {item['elapsed']:.1f}s")

                    # Chunk sources for paper_question
                    sources = item.get("sources", [])
                    if sources:
                        with st.expander(f"🔍 Retrieved Evidence Passages ({len(sources)} Chunks)", expanded=False):
                            for s_i, src in enumerate(sources, 1):
                                p_num = src.metadata.get("page", "?")
                                st.markdown(f"**Passage {s_i} (Page {p_num}):**")
                                st.text(src.page_content, wrap=True)

                    # Full-paper citations
                    cited_pages = item.get("cited_pages", [])
                    page_sources = item.get("page_sources", {})
                    if cited_pages and page_sources:
                        with st.expander(f"🔍 Cited Document Pages ({len(cited_pages)} Pages)", expanded=False):
                            for p_num in cited_pages:
                                if p_num in page_sources:
                                    st.markdown(f"**Page {p_num} Source Excerpt:**")
                                    st.text(page_sources[p_num], wrap=True)

# ====================================================================
# TAB 4: VIVA DEFENSE SIMULATOR
# ====================================================================
with tab_viva:
    st.subheader("Oral Defense (Viva) Simulator")
    st.caption(f"Simulate a rigorous, paper-grounded defense examination with up to {VIVA_QUESTION_LIMIT} adaptive questions.")

    if not st.session_state.get("extracted_pages"):
        st.info("Upload a research paper in the Intake & Analysis tab first to start oral defense practice.", icon=":material/upload_file:")
    elif not settings.gemini_api_key:
        st.warning("Add GEMINI_API_KEY in .env to enable the viva simulator agent.", icon=":material/key:")
    else:
        viva_session = st.session_state.get("viva_session")
        start_lbl = "Initiate Viva Defense" if not viva_session else "Restart Defense Session"
        if st.button(start_lbl, type="primary", icon=":material/play_arrow:", key="btn_start_viva"):
            try:
                with st.spinner("Academic examiner is reviewing paper to prepare defense question 1..."):
                    first_q = start_viva(
                        st.session_state["extracted_pages"],
                        st.session_state["uploaded_paper_name"],
                    )
                st.session_state["viva_session"] = {
                    "turns": [],
                    "current_question": first_q["question"],
                    "current_focus": first_q["focus"],
                    "current_citation": first_q["citation"],
                    "total_score": 0,
                }
                st.rerun()
            except Exception as exc:
                st.error(f"Could not initialize defense session: {format_actionable_error(exc)}", icon=":material/error:")

        viva_session = st.session_state.get("viva_session")
        if viva_session:
            turns = viva_session["turns"]
            answered = len(turns)
            avg_score = viva_session["total_score"] / answered if answered else 0

            # Telemetry metrics
            vm1, vm2, vm3 = st.columns(3)
            vm1.metric("Questions Completed", f"{answered} / {VIVA_QUESTION_LIMIT}")
            vm2.metric("Mean Defense Score", f"{avg_score:.1f} / 5" if answered else "—")
            vm3.metric("Paper Under Defense", st.session_state.get("uploaded_paper_name", "Paper"))

            if answered:
                st.progress(min(1.0, answered / VIVA_QUESTION_LIMIT), text=f"Defense Progression: Question {min(answered + 1, VIVA_QUESTION_LIMIT)} of {VIVA_QUESTION_LIMIT}")

            if answered >= VIVA_QUESTION_LIMIT:
                # Honors classification
                grade = "High Honors (Pass with Distinction)" if avg_score >= 4.5 else "Honors Pass" if avg_score >= 3.8 else "Pass" if avg_score >= 3.0 else "Revision Recommended"
                st.success(f"🎓 **Defense Examination Complete!** Final Score: **{avg_score:.1f} / 5** — *{grade}*", icon=":material/celebration:")

                if not viva_session.get("history_saved"):
                    try:
                        save_completed_viva(st.session_state.get("uploaded_paper_name", "Research Paper"), turns)
                        viva_session["history_saved"] = True
                    except Exception:
                        viva_session["history_saved"] = True
                        viva_session["history_save_failed"] = True

                if viva_session.get("history_saved"):
                    st.caption("Session metrics recorded to your local Learning Analytics dashboard.")
            else:
                # Active Examination Question Card
                with st.container(border=True):
                    st.markdown(f"#### Question {answered + 1} of {VIVA_QUESTION_LIMIT} · Focus: `{viva_session.get('current_focus', 'Core Concept')}`")
                    st.info(viva_session["current_question"], icon=":material/record_voice_over:")
                    if viva_session.get("current_citation"):
                        st.caption(f"📄 Target Paper Evidence: {viva_session['current_citation']}")

                    student_answer = st.text_area(
                        "Your Verbal Defense Answer:",
                        placeholder="State your answer clearly with theoretical and methodological justification as if speaking to faculty examiners...",
                        height=140,
                        key=f"viva_ans_input_{answered}",
                    )

                    if st.button("Submit Defense Answer", type="primary", icon=":material/send:", key=f"btn_viva_sub_{answered}", disabled=not student_answer.strip()):
                        try:
                            with st.spinner("Faculty examiner is evaluating your defense against paper evidence..."):
                                eval_res = evaluate_viva_answer(
                                    st.session_state["extracted_pages"],
                                    st.session_state["uploaded_paper_name"],
                                    viva_session["current_question"],
                                    student_answer,
                                    turns,
                                )
                            turns.append({
                                "question": viva_session["current_question"],
                                "focus": viva_session.get("current_focus", "Defense"),
                                "answer": student_answer.strip(),
                                **eval_res,
                            })
                            viva_session["total_score"] += eval_res["score"]
                            if len(turns) < VIVA_QUESTION_LIMIT:
                                viva_session["current_question"] = eval_res["next_question"]
                                viva_session["current_focus"] = eval_res["next_focus"]
                                viva_session["current_citation"] = eval_res["next_citation"]
                            st.rerun()
                        except Exception as exc:
                            st.error(f"Evaluation error: {format_actionable_error(exc)}", icon=":material/error:")

            # Historical Turn Feedback
            if turns:
                st.markdown("#### Examiner Rubric Feedback History")
                for t_num, t in enumerate(turns, start=1):
                    score_stars = "★" * t['score'] + "☆" * (5 - t['score'])
                    with st.expander(f"Question {t_num}: {t['focus']} · Score: {t['score']}/5 ({score_stars})", expanded=(t_num == answered)):
                        st.markdown(f"**Question:** {t['question']}")
                        st.markdown(f"**Your Answer:** {t['answer']}")
                        st.markdown(f"**✅ Strengths:** {t['strengths']}")
                        st.markdown(f"**⚠️ Improvement Areas:** {t['improve']}")
                        st.markdown(f"**🎙️ Examiner Commentary:** {t['feedback']}")
                        if t.get("citation"):
                            st.caption(f"📄 Paper Evidence Anchor: {t['citation']}")

# ====================================================================
# TAB 5: PRESENTATION STUDIO & SLIDE BUILDER
# ====================================================================
with tab_slides:
    if st.session_state.get("presenter_mode") and st.session_state.get("presentation_data"):
        # Immersive Presenter Mode
        st.html("""<div id="sai-presenter-mode"></div>
        <style>
        body:has(#sai-presenter-mode) [data-testid="stSidebar"],
        body:has(#sai-presenter-mode) header[data-testid="stHeader"],
        body:has(#sai-presenter-mode) .sai-top-bar,
        body:has(#sai-presenter-mode) .sai-hero,
        body:has(#sai-presenter-mode) [data-testid="stTabsHeader"] { display: none !important; }
        body:has(#sai-presenter-mode) .block-container {
            max-width: none !important; width: 100% !important;
            padding: 0.6rem 1.2rem 0.5rem !important;
        }
        body:has(#sai-presenter-mode) [data-testid="stAppViewContainer"] { overflow: hidden; }
        </style>""")

        pres_data = st.session_state["presentation_data"]
        slides_list = pres_data["slides"]
        total_slides = len(slides_list)
        cur_idx = max(0, min(st.session_state.get("current_slide_idx", 0), total_slides - 1))
        st.session_state["current_slide_idx"] = cur_idx
        cur_slide = slides_list[cur_idx]

        # Presenter Controls
        cp_exit, cp_prev, cp_stat, cp_next, cp_jump = st.columns([1.5, 1, 2.5, 1, 2.5], vertical_alignment="center")
        with cp_exit:
            if st.button("Exit Presenter", icon=":material/close:", width="stretch", key="btn_exit_pres"):
                st.session_state["presenter_mode"] = False
                st.rerun()
        with cp_prev:
            if st.button("Previous", icon=":material/arrow_back:", disabled=(cur_idx == 0), width="stretch", key="btn_pres_prev"):
                st.session_state["current_slide_idx"] = cur_idx - 1
                st.rerun()
        with cp_stat:
            cat_tag = html.escape(str(cur_slide.get("category", "")).upper())
            st.markdown(f"<div style='text-align:center; font-weight:700; color:#818cf8;'>Slide {cur_idx + 1} of {total_slides} · <span style='color:#38bdf8;'>{cat_tag}</span></div>", unsafe_allow_html=True)
        with cp_next:
            if st.button("Next", icon=":material/arrow_forward:", disabled=(cur_idx >= total_slides - 1), type="primary", width="stretch", key="btn_pres_next"):
                st.session_state["current_slide_idx"] = cur_idx + 1
                st.rerun()
        with cp_jump:
            slide_opts = [f"{s['slide_number']}. [{s['category']}] {s['title'][:20]}..." for s in slides_list]
            chosen_jump = st.selectbox("Jump to Slide", options=list(range(total_slides)), format_func=lambda i: slide_opts[i], index=cur_idx, label_visibility="collapsed", key=f"pres_jump_{cur_idx}")
            if chosen_jump != cur_idx:
                st.session_state["current_slide_idx"] = chosen_jump
                st.rerun()

        # Render Slide Canvas
        st.html(render_slide_html(
            slide_info=cur_slide,
            theme_name=pres_data.get("theme_name", "Obsidian Indigo (ScholarAI Dark)"),
            total_slides=total_slides,
            duration=pres_data.get("duration", "10 minutes"),
            audience_level=pres_data.get("audience_level", "General academic"),
            is_presentation_mode=True,
        ))

        if cur_slide.get("speaker_notes") or cur_slide.get("citation"):
            with st.expander("🎙️ Presenter Notes & Talking Points", expanded=True):
                if cur_slide.get("speaker_notes"):
                    st.write(cur_slide["speaker_notes"])
                if cur_slide.get("citation"):
                    st.caption(f"📄 Grounded Evidence: {cur_slide['citation']}")

    else:
        st.subheader("Paper-to-PowerPoint Presentation Studio")
        st.caption("Generate grounded, 16:9 widescreen presentation slide decks with verifiable citations and presenter speaker notes.")

        if not st.session_state.get("extracted_pages"):
            st.info("Upload a research paper in the Intake & Analysis tab to configure and generate presentations.", icon=":material/upload_file:")
        else:
            pages = st.session_state["extracted_pages"]
            filename = st.session_state["uploaded_paper_name"]

            with st.container(border=True):
                c_p1, c_p2 = st.columns(2)
                with c_p1:
                    slide_count = st.slider("Target Slide Count", min_value=5, max_value=15, value=8, key="pres_slide_count")
                    duration = st.selectbox("Presentation Duration", ["5 minutes (Lightning)", "10 minutes (Conference)", "15 minutes (Seminar)", "20 minutes (Thesis Defense)"], index=1, key="pres_duration")
                with c_p2:
                    audience_level = st.selectbox("Target Technical Level", ["General academic (undergrad / interdisciplinary)", "Specialist / Peer review (faculty, examiners, viva)", "Executive / High-level (industry, overview)"], index=0, key="pres_audience")
                    theme_name = st.selectbox("Visual Theme", list(THEMES.keys()), index=0, key="pres_theme")

                c_gen_btn, c_gen_stat = st.columns([1, 2], vertical_alignment="center")
                with c_gen_btn:
                    btn_gen_presentation = st.button(
                        "Generate PowerPoint" if not st.session_state.get("presentation_data") else "Regenerate PowerPoint",
                        type="primary",
                        icon=":material/slideshow:",
                        key="btn_generate_presentation",
                    )
                with c_gen_stat:
                    if st.session_state.get("presentation_data"):
                        pres = st.session_state["presentation_data"]
                        st.caption(f"⚡ Deck generated: {pres['slide_count']} slides in {pres['total_elapsed']:.1f}s ({len(pres['pptx_bytes']):,} bytes)")

            if btn_gen_presentation:
                if not settings.gemini_api_key or settings.gemini_api_key.strip() in ("", "your_gemini_api_key_here"):
                    st.error("Please add your GEMINI_API_KEY to .env to generate presentations.", icon=":material/key:")
                else:
                    with st.status("Synthesizing slide outline & rendering widescreen deck...", expanded=True) as status_box:
                        def pres_prog(stage, msg, elapsed, extra=None):
                            status_box.write(f"⏱️ **[{elapsed:.1f}s]** {msg}")
                        try:
                            pres_data = generate_presentation(
                                filename=filename,
                                pages=pages,
                                slide_count=slide_count,
                                duration=duration,
                                audience_level=audience_level,
                                theme_name=theme_name,
                                on_progress=pres_prog,
                            )
                            status_box.update(label=f"Deck ready in {pres_data['total_elapsed']:.1f}s ({pres_data['slide_count']} slides)", state="complete", expanded=False)
                            st.session_state["presentation_data"] = pres_data
                            st.session_state["current_slide_idx"] = 0
                            st.session_state["presenter_mode"] = False
                            st.rerun()
                        except Exception as exc:
                            status_box.update(label="Presentation generation failed", state="error", expanded=True)
                            st.error(format_actionable_error(exc), icon=":material/error:")

            if st.session_state.get("presentation_data"):
                pres_data = st.session_state["presentation_data"]
                slides_list = pres_data["slides"]
                total_slides = len(slides_list)
                cur_idx = max(0, min(st.session_state.get("current_slide_idx", 0), total_slides - 1))
                st.session_state["current_slide_idx"] = cur_idx
                cur_slide = slides_list[cur_idx]
                clean_f = filename.replace(".pdf", "").replace(" ", "_")

                st.divider()
                col_live_pres, col_dl_pptx = st.columns(2)
                with col_live_pres:
                    if st.button("Present Slides (Full Screen)", type="primary", icon=":material/play_circle:", width="stretch", key="btn_run_pres_mode"):
                        st.session_state["presenter_mode"] = True
                        st.rerun()
                with col_dl_pptx:
                    st.download_button(
                        label="Download PowerPoint (.pptx)",
                        data=pres_data["pptx_bytes"],
                        file_name=f"{clean_f}_presentation.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        icon=":material/download:",
                        width="stretch",
                        key="btn_dl_pptx",
                    )

                st.divider()
                st.markdown("#### 🖥️ Interactive Slide Canvas Preview")

                # Navigator Bar
                nav_prev, nav_ind, nav_next, nav_jump = st.columns([1, 2.2, 1, 2.8], vertical_alignment="center")
                with nav_prev:
                    if st.button("Previous Slide", icon=":material/arrow_back:", disabled=(cur_idx == 0), width="stretch", key="btn_pv_prev"):
                        st.session_state["current_slide_idx"] = cur_idx - 1
                        st.rerun()
                with nav_ind:
                    cat_lbl = html.escape(str(cur_slide.get("category", "")).upper())
                    st.markdown(f"<div style='text-align:center; font-weight:700; color:#818cf8;'>Slide {cur_idx + 1} of {total_slides} · <span style='color:#38bdf8;'>{cat_lbl}</span></div>", unsafe_allow_html=True)
                with nav_next:
                    if st.button("Next Slide", icon=":material/arrow_forward:", disabled=(cur_idx >= total_slides - 1), width="stretch", key="btn_pv_next"):
                        st.session_state["current_slide_idx"] = cur_idx + 1
                        st.rerun()
                with nav_jump:
                    s_opts = [f"{s['slide_number']}. [{s['category']}] {s['title'][:22]}..." for s in slides_list]
                    chosen_pv = st.selectbox("Select Slide", options=list(range(total_slides)), format_func=lambda i: s_opts[i], index=cur_idx, label_visibility="collapsed", key=f"pv_jump_{cur_idx}")
                    if chosen_pv != cur_idx:
                        st.session_state["current_slide_idx"] = chosen_pv
                        st.rerun()

                # Render Canvas
                st.html(render_slide_html(
                    slide_info=cur_slide,
                    theme_name=pres_data.get("theme_name", "Obsidian Indigo (ScholarAI Dark)"),
                    total_slides=total_slides,
                    duration=pres_data.get("duration", "10 minutes"),
                    audience_level=pres_data.get("audience_level", "General academic"),
                    is_presentation_mode=False,
                ))

                if cur_slide.get("speaker_notes") or cur_slide.get("citation"):
                    col_n1, col_n2 = st.columns([2, 1])
                    with col_n1:
                        if cur_slide.get("speaker_notes"):
                            st.caption(f"🎙️ **Presenter Notes:** {cur_slide['speaker_notes']}")
                    with col_n2:
                        if cur_slide.get("citation"):
                            st.info(f"📄 **Grounded Citation:** {cur_slide['citation']}", icon=":material/menu_book:")

# ====================================================================
# TAB 6: FLASHCARDS REVISION LAB
# ====================================================================
with tab_cards:
    st.subheader("Paper-Grounded Revision Flashcards")
    st.caption("Test your recall with question-and-answer study cards grounded in paper excerpts with verifiable page citations.")

    if not st.session_state.get("extracted_pages"):
        st.info("Upload a research paper in the Intake & Analysis tab first to create flashcards.", icon=":material/upload_file:")
    elif not settings.gemini_api_key:
        st.warning("Add GEMINI_API_KEY to your local .env file to generate flashcards.", icon=":material/key:")
    else:
        deck = st.session_state.get("flashcard_deck")
        if not deck:
            if st.button("Generate 10 Flashcards", type="primary", icon=":material/auto_awesome:", key="btn_gen_cards"):
                try:
                    with st.spinner("Authoring paper-grounded study flashcards..."):
                        deck = generate_flashcards(
                            st.session_state["extracted_pages"],
                            st.session_state["uploaded_paper_name"],
                            count=10,
                        )
                    st.session_state["flashcard_deck"] = deck
                    st.session_state["flashcard_index"] = 0
                    st.session_state["flashcard_revealed"] = False
                    st.rerun()
                except Exception as exc:
                    st.error(f"Could not generate flashcard deck: {format_actionable_error(exc)}", icon=":material/error:")
        else:
            total_cards = len(deck)
            idx = max(0, min(st.session_state.get("flashcard_index", 0), total_cards - 1))
            st.session_state["flashcard_index"] = idx
            card = deck[idx]

            st.progress((idx + 1) / total_cards, text=f"Flashcard {idx + 1} of {total_cards}")

            with st.container(border=True):
                if st.session_state.get("flashcard_revealed"):
                    st.caption("ANSWER SIDE · REVEALED")
                    st.markdown(f"### {card['answer']}")
                    if card.get("citation"):
                        st.caption(f"📄 Verified Paper Evidence: {card['citation']}")
                else:
                    st.caption("QUESTION SIDE · THINK FIRST")
                    st.markdown(f"### {card['question']}")
                    st.caption("Formulate your answer, then click Reveal Answer below.")

            fc_prev, fc_flip, fc_next, fc_shuf = st.columns([1, 1.4, 1, 1.2], vertical_alignment="center")
            with fc_prev:
                if st.button("Previous Card", icon=":material/arrow_back:", disabled=(idx == 0), width="stretch", key="btn_fc_prev"):
                    st.session_state["flashcard_index"] = idx - 1
                    st.session_state["flashcard_revealed"] = False
                    st.rerun()
            with fc_flip:
                flip_lbl = "Show Question" if st.session_state.get("flashcard_revealed") else "Reveal Answer"
                if st.button(flip_lbl, type="primary", icon=":material/flip:", width="stretch", key="btn_fc_flip"):
                    st.session_state["flashcard_revealed"] = not st.session_state.get("flashcard_revealed", False)
                    st.rerun()
            with fc_next:
                if st.button("Next Card", icon=":material/arrow_forward:", disabled=(idx >= total_cards - 1), width="stretch", key="btn_fc_next"):
                    st.session_state["flashcard_index"] = idx + 1
                    st.session_state["flashcard_revealed"] = False
                    st.rerun()
            with fc_shuf:
                if st.button("Shuffle Deck", icon=":material/shuffle:", width="stretch", key="btn_fc_shuf"):
                    random.shuffle(deck)
                    st.session_state["flashcard_index"] = 0
                    st.session_state["flashcard_revealed"] = False
                    st.rerun()

            st.divider()
            if st.button("Generate Fresh Deck", key="btn_regen_deck"):
                st.session_state["flashcard_deck"] = None
                st.session_state["flashcard_index"] = 0
                st.session_state["flashcard_revealed"] = False
                st.rerun()

# ====================================================================
# TAB 7: LEARNING ANALYTICS DASHBOARD
# ====================================================================
with tab_dashboard:
    st.subheader("Defense Performance Analytics & Progress")
    st.caption("Track defense mastery, topic strengths, and historical viva exam performance stored privately in local SQLite.")

    try:
        history = load_viva_history()
    except Exception as exc:
        history = []
        st.error(f"Could not load local session database: {format_actionable_error(exc)}")

    if not history:
        st.info("Complete an oral defense session in the Viva Simulator tab to generate learning analytics here.", icon=":material/insights:")
    else:
        total_sessions = len(history)
        overall_avg = sum(item["average_score"] for item in history) / total_sessions
        total_ans = sum(item["question_count"] for item in history)
        best_score = max(item["average_score"] for item in history)

        d1, d2, d3, d4 = st.columns(4)
        d1.metric("Completed Defenses", total_sessions)
        d2.metric("Overall Mean Score", f"{overall_avg:.1f} / 5")
        d3.metric("Peak Session Score", f"{best_score:.1f} / 5")
        d4.metric("Questions Evaluated", total_ans)

        topic_vals = defaultdict(list)
        for item in history:
            for top, sc in item["topic_scores"].items():
                topic_vals[top].append(sc)

        topic_df = pd.DataFrame([
            {"Topic": t, "Average Score": sum(scs) / len(scs), "Sessions": len(scs)}
            for t, scs in topic_vals.items()
        ]).sort_values("Average Score", ascending=True)

        if not topic_df.empty:
            st.markdown("#### Topic Mastery & Comprehension Breakdown")
            fig = px.bar(
                topic_df,
                x="Average Score",
                y="Topic",
                orientation="h",
                range_x=[0, 5],
                color="Average Score",
                color_continuous_scale=[[0, "#f59e0b"], [0.6, "#38bdf8"], [1, "#10b981"]],
                hover_data={"Sessions": True, "Average Score": ":.1f"},
            )
            fig.update_layout(
                template="plotly_dark",
                height=max(320, 50 * len(topic_df)),
                margin=dict(l=10, r=10, t=10, b=10),
                coloraxis_showscale=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis_title="Average Viva Defense Score (out of 5)",
                yaxis_title="",
            )
            st.plotly_chart(fig, width="stretch")

            strong_t = topic_df[topic_df["Average Score"] >= 4.0]["Topic"].tolist()
            review_t = topic_df[topic_df["Average Score"] < 3.2]["Topic"].tolist()

            cs_col1, cs_col2 = st.columns(2)
            with cs_col1:
                st.markdown("##### 🏆 Current Demonstrated Strengths")
                st.write(", ".join(strong_t) if strong_t else "Practice more sessions to build consistent topic strengths.")
            with cs_col2:
                st.markdown("##### 🎯 Priority Revision Areas")
                st.write(", ".join(review_t) if review_t else "No topics currently below 3.2 in saved defense sessions.")

        st.markdown("#### Recent Defense Sessions History")
        recent_df = pd.DataFrame([
            {
                "Paper Title": item["paper_name"],
                "Timestamp": item["completed_at"].replace("T", " "),
                "Questions Answered": item["question_count"],
                "Session Score": f"{item['average_score']:.1f} / 5",
            }
            for item in history[:12]
        ])
        st.dataframe(recent_df, hide_index=True, width="stretch")

# Footer
st.html(get_footer_html())
