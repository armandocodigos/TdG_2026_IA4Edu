from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.user import UserRead, UserSubjectUpdate


router = APIRouter(prefix="/api/users", tags=["users"])
bearer_scheme = HTTPBearer(auto_error=False)


@router.get("/me", response_model=UserRead)
def read_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> UserRead:
    authorization = None
    if credentials:
        authorization = f"{credentials.scheme} {credentials.credentials}"
    user = get_current_user(db=db, authorization=authorization)
    return UserRead.model_validate(user)


@router.patch("/me/subject", response_model=UserRead)
def update_current_user_subject(
    payload: UserSubjectUpdate,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> UserRead:
    authorization = None
    if credentials:
        authorization = f"{credentials.scheme} {credentials.credentials}"
    user = get_current_user(db=db, authorization=authorization)
    user.subject = payload.subject
    db.commit()
    db.refresh(user)
    return UserRead.model_validate(user)
