from functools import lru_cache

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
    app_version: str = "0.1.0"
    crossref_mailto: str = "peerlens@example.com"
    request_timeout_seconds: float = 30.0
    max_upload_bytes: int = 10 * 1024 * 1024
    fetch_arxiv_pdf: bool = True
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
