from fastapi import APIRouter, Depends, Form, File, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.fast_chat import FastChatRequest, FastChatResponse
from app.services.fast_chat_service import FastChatService
from app.services.multimodal_service import MultimodalService, get_multimodal_service
from app.services.socratic_tutor_service import SocraticTutorService


router = APIRouter(prefix="/api/fast-chat", tags=["fast-chat"])
bearer_scheme = HTTPBearer(auto_error=False)


def _build_authorization(credentials: HTTPAuthorizationCredentials | None) -> str | None:
    if not credentials:
        return None
    return f"{credentials.scheme} {credentials.credentials}"


@router.post("", response_model=FastChatResponse)
async def fast_chat(
    query: str = Form(..., min_length=3, max_length=4000),
    topic: str | None = Form(None, max_length=200),
    use_rag: bool = Form(False),
    mode: str | None = Form(None, max_length=50),
    file: UploadFile | None = File(None),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
    multimodal_service: MultimodalService = Depends(get_multimodal_service),
) -> FastChatResponse:
    print(f"[FastChat API] Received payload from frontend: query={query}, use_rag={use_rag}, file={file.filename if file else None}")
    user = get_current_user(db=db, authorization=_build_authorization(credentials))
    print(f"[FastChat API] User: {user}")

    extracted_content = None
    if file:
        try:
            content = await file.read()
            ext = file.filename.lower()
            if ext.endswith(('.png', '.jpg', '.jpeg', '.webp')):
                extracted_content, _, _ = await multimodal_service.process_image(content, file.filename)
            elif ext.endswith(('.wav', '.mp3', '.m4a', '.ogg')):
                extracted_content, _, _ = await multimodal_service.process_audio(content, file.filename)
            elif ext.endswith('.pdf'):
                extracted_content, _, _ = await multimodal_service.process_document(content, file.filename)
        except Exception as e:
            print(f"[FastChat API] Error reading file: {e}")
            return FastChatResponse(
                answer="No se pudo leer el archivo claramente",
                model_used="multimodal-service",
                rag_enabled=use_rag,
                context_count=0,
                sources=[],
                rag_metadata=[],
                latency_ms=0,
            )

    payload = FastChatRequest(query=query, topic=topic, use_rag=use_rag)
    if mode == "socratic":
        return await run_in_threadpool(
            SocraticTutorService().answer,
            user=user,
            payload=payload,
            extracted_content=extracted_content,
        )

    return await run_in_threadpool(
        FastChatService(db).answer, user=user, payload=payload, extracted_content=extracted_content
    )
