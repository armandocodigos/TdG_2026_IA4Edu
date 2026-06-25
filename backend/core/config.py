import os
from pathlib import Path


def load_env_file() -> None:
    candidate_paths = [
        Path.cwd() / ".env",
        Path(__file__).resolve().parents[1] / ".env",
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


load_env_file()


# ============================================================
# OLLAMA
# ============================================================

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")

OLLAMA_URL = os.getenv("OLLAMA_URL", f"{OLLAMA_BASE_URL}/api/generate")

MODEL = os.getenv(
    "SOCRATIC_CHAT_MODEL",
    "gemma3",
)


# ============================================================
# GENERACIÓN TUTOR
# ============================================================

TUTOR_TEMPERATURE = 0.4

TUTOR_TOP_P = 0.9

TUTOR_REPEAT_PENALTY = 1.1

TUTOR_NUM_PREDICT = 120

TUTOR_TIMEOUT_SECONDS = int(
    os.getenv(
        "SOCRATIC_TIMEOUT_SECONDS",
        "300",
    )
)
