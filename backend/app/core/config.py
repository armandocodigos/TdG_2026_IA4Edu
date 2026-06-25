import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


def load_env_file() -> None:
    candidate_paths = [
        Path.cwd() / ".env",
        Path(__file__).resolve().parents[2] / ".env",
        Path.cwd().parent / "backend" / ".env",
    ]

    for path in candidate_paths:
        if not path.exists():
            continue

        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())
        return


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_version: str
    database_url: str
    cors_allowed_origins: tuple[str, ...]
    secret_key: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    default_user_role: str
    default_user_subject: str
    embedding_dimensions: int
    jwt_algorithm: str
    ollama_base_url: str
    default_llm_model: str
    fast_llm_model: str
    fast_chat_model: str
    embedding_model: str
    rag_top_k: int
    rag_chunk_size: int
    rag_chunk_overlap: int
    ollama_timeout_seconds: float
    whisper_model_size: str


@lru_cache
def get_settings() -> Settings:
    load_env_file()
    cors_allowed_origins = tuple(
        origin.strip()
        for origin in os.getenv(
            "CORS_ALLOWED_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if origin.strip()
    )
    return Settings(
        app_name=os.getenv("APP_NAME", "Math Tutor Backend"),
        app_version=os.getenv("APP_VERSION", "0.1.0"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///./app.db"),
        cors_allowed_origins=cors_allowed_origins,
        secret_key=os.getenv("SECRET_KEY", "change-this-in-production"),
        access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
        refresh_token_expire_days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30")),
        default_user_role=os.getenv("DEFAULT_USER_ROLE", "student"),
        default_user_subject=os.getenv("DEFAULT_USER_SUBJECT", "precalculo"),
        embedding_dimensions=int(os.getenv("EMBEDDING_DIMENSIONS", "768")),
        jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        default_llm_model=os.getenv("DEFAULT_LLM_MODEL", "deepseek-r1:7b"),
        fast_llm_model=os.getenv("FAST_LLM_MODEL", "phi4-mini"),
        fast_chat_model=os.getenv("FAST_CHAT_MODEL", os.getenv("FAST_LLM_MODEL", "phi4-mini")),
        embedding_model=os.getenv("EMBEDDING_MODEL", "nomic-embed-text"),
        rag_top_k=int(os.getenv("RAG_TOP_K", "3")),
        rag_chunk_size=int(os.getenv("RAG_CHUNK_SIZE", "1200")),
        rag_chunk_overlap=int(os.getenv("RAG_CHUNK_OVERLAP", "150")),
        ollama_timeout_seconds=float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "60")),
        whisper_model_size=os.getenv("WHISPER_MODEL_SIZE", "small"),
    )
