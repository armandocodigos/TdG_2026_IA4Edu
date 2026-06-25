from fastapi import APIRouter, Depends, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.exam import (
    ExamAnswerRequest,
    ExamAttemptRead,
    ExamAvailabilityResponse,
    ExamFinishResponse,
    ExamResultRead,
    ExamStartRequest,
    LastExamResultRead,
)
from app.services.exam_service import ExamService


router = APIRouter(prefix="/api/exams", tags=["exams"])
bearer_scheme = HTTPBearer(auto_error=False)


def _build_authorization(credentials: HTTPAuthorizationCredentials | None) -> str | None:
    if not credentials:
        return None
    return f"{credentials.scheme} {credentials.credentials}"


@router.get("/availability", response_model=ExamAvailabilityResponse)
def read_exam_availability(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> ExamAvailabilityResponse:
    user = get_current_user(db=db, authorization=_build_authorization(credentials))
    return ExamService(db).get_availability(user)


@router.post("/start", response_model=ExamAttemptRead)
def start_custom_exam(
    payload: ExamStartRequest,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> ExamAttemptRead:
    user = get_current_user(db=db, authorization=_build_authorization(credentials))
    return ExamService(db).start_custom(user=user, payload=payload)


@router.get("/latest-result", response_model=LastExamResultRead)
def read_latest_exam_result(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> LastExamResultRead:
    user = get_current_user(db=db, authorization=_build_authorization(credentials))
    return ExamService(db).get_latest_result(user=user)


@router.post("/{attempt_id}/answer", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def answer_exam(
    attempt_id: str,
    payload: ExamAnswerRequest,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Response:
    user = get_current_user(db=db, authorization=_build_authorization(credentials))
    ExamService(db).answer(user=user, attempt_id=attempt_id, question_id=payload.question_id, answer=payload.answer)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{attempt_id}/finish", response_model=ExamFinishResponse)
def finish_exam(
    attempt_id: str,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> ExamFinishResponse:
    user = get_current_user(db=db, authorization=_build_authorization(credentials))
    return ExamService(db).finish(user=user, attempt_id=attempt_id)


@router.post("/{attempt_id}/abandon", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def abandon_exam(
    attempt_id: str,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Response:
    user = get_current_user(db=db, authorization=_build_authorization(credentials))
    ExamService(db).abandon(user=user, attempt_id=attempt_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{attempt_id}/result", response_model=ExamResultRead)
def read_exam_result(
    attempt_id: str,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> ExamResultRead:
    user = get_current_user(db=db, authorization=_build_authorization(credentials))
    return ExamService(db).get_result(user=user, attempt_id=attempt_id)
