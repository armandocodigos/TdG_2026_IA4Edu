from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_token, verify_password
from app.models.enums import SessionStatus
from app.repositories.auth_session_repository import AuthSessionRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, TokenPair
from app.schemas.user import UserCreate
from app.services.token_service import TokenService
from app.services.user_service import UserService


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repository = UserRepository(db)
        self.auth_session_repository = AuthSessionRepository(db)
        self.user_service = UserService(self.user_repository)
        self.token_service = TokenService()

    def register(self, payload: UserCreate) -> TokenPair:
        if self.user_repository.get_by_email(payload.email.lower()):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

        user = self.user_service.create_user(payload)
        refresh_token, session = self.token_service.build_refresh_session(user)
        self.auth_session_repository.create(session)
        self.db.commit()

        return TokenPair(
            access_token=self.token_service.build_access_token(user),
            refresh_token=refresh_token,
            user=user,
        )

    def login(self, payload: LoginRequest) -> TokenPair:
        user = self.user_repository.get_by_email(payload.email.lower())
        if not user or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")

        refresh_token, session = self.token_service.build_refresh_session(user)
        self.auth_session_repository.create(session)
        self.db.commit()

        return TokenPair(
            access_token=self.token_service.build_access_token(user),
            refresh_token=refresh_token,
            user=user,
        )

    def refresh(self, refresh_token: str) -> TokenPair:
        session = self.auth_session_repository.get_by_token_hash(hash_token(refresh_token))
        if not session:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        if session.status != SessionStatus.ACTIVE:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked")

        expires_at = session.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if expires_at <= datetime.now(timezone.utc):
            session.status = SessionStatus.EXPIRED
            self.db.add(session)
            self.db.commit()
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")

        user = self.user_repository.get_by_id(session.user_id)
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not available")

        self.auth_session_repository.revoke(session)
        new_refresh_token, new_session = self.token_service.build_refresh_session(user)
        self.auth_session_repository.create(new_session)
        self.db.commit()

        return TokenPair(
            access_token=self.token_service.build_access_token(user),
            refresh_token=new_refresh_token,
            user=user,
        )

    def logout(self, refresh_token: str) -> None:
        session = self.auth_session_repository.get_by_token_hash(hash_token(refresh_token))
        if not session:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        self.auth_session_repository.revoke(session)
        self.db.commit()
