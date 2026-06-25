from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models
from app.core.config import get_settings
from app.routers import auth, diagnostic, exams, fast_chat, health, multimodal, solve, users


settings = get_settings()

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_allowed_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(solve.router)
app.include_router(fast_chat.router)
app.include_router(diagnostic.router)
app.include_router(exams.router)
app.include_router(multimodal.router, prefix="/api/multimodal", tags=["Multimodal"])


# Initialize TopicManager at startup to prepare topic dictionary and embeddings
from app.services.topic_manager import get_topic_manager


@app.on_event("startup")
def _initialize_topic_manager() -> None:
    try:
        tm = get_topic_manager()
        tm.initialize()
    except Exception:
        # Do not crash the app if the topic manager initialization fails; log for debugging
        import logging

        logging.getLogger(__name__).exception("Failed to initialize TopicManager on startup")
