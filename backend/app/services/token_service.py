from datetime import datetime, timedelta, timezone

from app.core.config import get_settings
from app.core.security import create_access_token, create_refresh_token, hash_token
from app.models.auth_session import AuthSession
from app.models.user import User


class TokenService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def build_access_token(self, user: User) -> str:
        payload = {
            "sub": user.id,
            "email": user.email,
            "role": user.role.value,
            "subject": user.subject.value,
        }
        return create_access_token(payload)

    def build_refresh_session(self, user: User) -> tuple[str, AuthSession]:
        refresh_token = create_refresh_token()
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=self.settings.refresh_token_expire_days
        )
        session = AuthSession(
            user_id=user.id,
            refresh_token_hash=hash_token(refresh_token),
            expires_at=expires_at,
        )
        return refresh_token, session
