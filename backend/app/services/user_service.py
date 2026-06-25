from app.core.config import get_settings
from app.core.security import get_password_hash
from app.models.enums import Subject, UserRole
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository
        self.settings = get_settings()

    def create_user(self, payload: UserCreate) -> User:
        return self.user_repository.create(
            User(
                email=payload.email.lower(),
                hashed_password=get_password_hash(payload.password),
                full_name=payload.full_name,
                subject=payload.subject or Subject(self.settings.default_user_subject),
                role=UserRole(self.settings.default_user_role),
            )
        )
