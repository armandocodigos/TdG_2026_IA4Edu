from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.auth_session import AuthSession
from app.models.enums import SessionStatus


class AuthSessionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, session: AuthSession) -> AuthSession:
        self.db.add(session)
        self.db.flush()
        self.db.refresh(session)
        return session

    def get_by_token_hash(self, token_hash: str) -> AuthSession | None:
        stmt = select(AuthSession).where(AuthSession.refresh_token_hash == token_hash)
        return self.db.execute(stmt).scalar_one_or_none()

    def revoke(self, session: AuthSession) -> AuthSession:
        session.status = SessionStatus.REVOKED
        session.revoked_at = datetime.now(timezone.utc)
        self.db.add(session)
        self.db.flush()
        self.db.refresh(session)
        return session
