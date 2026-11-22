"""Application settings loaded from environment variables or a local .env."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


def _get_setting(key: str, default: str | None = None) -> str | None:
    """Retrieve setting from environment variables or Streamlit secrets."""
    val = os.getenv(key)
    if val and val.strip():
        return val.strip()
    try:
        import streamlit as st

        if key in st.secrets and str(st.secrets[key]).strip():
            return str(st.secrets[key]).strip()
    except Exception:
        pass
    return default


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str | None = _get_setting("GEMINI_API_KEY")
    gemini_model: str = _get_setting("GEMINI_MODEL", "gemini-3.5-flash-lite")
    gemini_embedding_model: str = _get_setting(
        "GEMINI_EMBEDDING_MODEL", "models/gemini-embedding-001"
    )
    chroma_dir: str = _get_setting("CHROMA_DIR", "./chroma_db")


settings = Settings()
