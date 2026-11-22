"""Application settings loaded from environment variables or Streamlit secrets."""

import os
from dotenv import load_dotenv

load_dotenv()


def _get_setting(key: str, default: str | None = None) -> str | None:
    """Retrieve setting from environment variables or Streamlit secrets dynamically."""
    val = os.getenv(key)
    if val and val.strip():
        return val.strip()
    try:
        import streamlit as st

        # Direct key lookup
        if hasattr(st, "secrets") and st.secrets is not None:
            if key in st.secrets and str(st.secrets[key]).strip():
                return str(st.secrets[key]).strip()
            # Case-insensitive lookup
            for k in (key.lower(), key.upper()):
                if k in st.secrets and str(st.secrets[k]).strip():
                    return str(st.secrets[k]).strip()
    except Exception:
        pass
    return default


class Settings:
    @property
    def gemini_api_key(self) -> str | None:
        return _get_setting("GEMINI_API_KEY")

    @property
    def gemini_model(self) -> str:
        return _get_setting("GEMINI_MODEL", "gemini-3.5-flash-lite") or "gemini-3.5-flash-lite"

    @property
    def gemini_embedding_model(self) -> str:
        return (
            _get_setting("GEMINI_EMBEDDING_MODEL", "models/gemini-embedding-001")
            or "models/gemini-embedding-001"
        )

    @property
    def chroma_dir(self) -> str:
        return _get_setting("CHROMA_DIR", "./chroma_db") or "./chroma_db"


settings = Settings()
