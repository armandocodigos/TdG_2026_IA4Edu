from fastapi import APIRouter, Depends, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.diagnostic import (
    DiagnosticAnswerRequest,
    DiagnosticAttemptRead,
    DiagnosticAttemptReviewRead,
    DiagnosticFinishResponse,
    DiagnosticProfileRead,
)
from app.services.diagnostic_service import DiagnosticService




router = APIRouter(prefix="/api/diagnostic", tags=["diagnostic"])
bearer_scheme = HTTPBearer(auto_error=False)


def _build_authorization(credentials: HTTPAuthorizationCredentials | None) -> str | None:
    if not credentials:
        return None
    return f"{credentials.scheme} {credentials.credentials}"


@router.post("/start", response_model=DiagnosticAttemptRead)
def start_diagnostic(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> DiagnosticAttemptRead:
    user = get_current_user(db=db, authorization=_build_authorization(credentials))
    return DiagnosticService(db).start(user)


@router.get("/profile", response_model=DiagnosticProfileRead | None)
def read_diagnostic_profile(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> DiagnosticProfileRead | None:
    user = get_current_user(db=db, authorization=_build_authorization(credentials))
    return DiagnosticService(db).get_profile(user)


@router.get("/latest-review", response_model=DiagnosticAttemptReviewRead | None)
def read_latest_diagnostic_review(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> DiagnosticAttemptReviewRead | None:
    user = get_current_user(db=db, authorization=_build_authorization(credentials))
    return DiagnosticService(db).get_latest_attempt_review(user)


@router.get("/{attempt_id}/result", response_model=DiagnosticFinishResponse)
def read_diagnostic_result(
    attempt_id: str,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> DiagnosticFinishResponse:
    user = get_current_user(db=db, authorization=_build_authorization(credentials))
    return DiagnosticService(db).get_result(user=user, attempt_id=attempt_id)


@router.get("/{attempt_id}", response_model=DiagnosticAttemptRead)
def read_diagnostic_attempt(
    attempt_id: str,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> DiagnosticAttemptRead:
    user = get_current_user(db=db, authorization=_build_authorization(credentials))
    return DiagnosticService(db).get_attempt(user=user, attempt_id=attempt_id)


@router.post("/{attempt_id}/answer", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def answer_diagnostic(
    attempt_id: str,
    payload: DiagnosticAnswerRequest,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Response:
    user = get_current_user(db=db, authorization=_build_authorization(credentials))
    DiagnosticService(db).answer(user=user, attempt_id=attempt_id, question_id=payload.question_id, answer=payload.answer)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{attempt_id}/finish", response_model=DiagnosticFinishResponse)
def finish_diagnostic(
    attempt_id: str,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> DiagnosticFinishResponse:
    user = get_current_user(db=db, authorization=_build_authorization(credentials))
    return DiagnosticService(db).finish(user=user, attempt_id=attempt_id)


@router.post("/{attempt_id}/abandon", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def abandon_diagnostic(
    attempt_id: str,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Response:
    user = get_current_user(db=db, authorization=_build_authorization(credentials))
    DiagnosticService(db).abandon(user=user, attempt_id=attempt_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
