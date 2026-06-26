from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PEERLENS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    env: str = "development"
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "info"
    app_name: str = "PeerLens"
    app_version: str = "0.3.0"
    crossref_mailto: str = "peerlens@example.com"
    request_timeout_seconds: float = 30.0
    max_upload_bytes: int = 10 * 1024 * 1024
    fetch_arxiv_pdf: bool = True
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    openai_api_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("OPENAI_API_KEY", "PEERLENS_OPENAI_API_KEY"),
    )
    openai_base_url: str = "https://api.openai.com/v1"
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4o-mini"
    rag_top_k: int = 5
    rag_chunk_size: int = 900
    rag_chunk_overlap: int = 120
    rag_demo_mode: bool = False
    rag_demo_message: str = (
        "This is a demo version of PeerLens — LLM responses are disabled on this deployment. "
        "Paper analysis and quality signals still work. To enable Q&A, set OPENAI_API_KEY and "
        "set PEERLENS_RAG_DEMO_MODE=false on the server."
    )

    def rag_uses_llm(self) -> bool:
        if self.rag_demo_mode:
            return False
        return bool(self.openai_api_key)

@lru_cache
def get_settings() -> Settings:
    return Settings()
