from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.solve import SolveRequest, SolveResponse
from app.services.rag_service import RAGService


router = APIRouter(prefix="/api/solve", tags=["solve"])
bearer_scheme = HTTPBearer(auto_error=False)


@router.post("", response_model=SolveResponse)
def solve(
    payload: SolveRequest,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> SolveResponse:
    authorization = None
    if credentials:
        authorization = f"{credentials.scheme} {credentials.credentials}"
    user = get_current_user(db=db, authorization=authorization)
    return RAGService(db).solve(user=user, payload=payload)
