from enum import Enum


class Subject(str, Enum):
    PRECALCULO = "precalculo"
    PREUNIVERSITARIO = "preuniversitario"


class UserRole(str, Enum):
    STUDENT = "student"
    ADMIN = "admin"


class MasteryLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class BloomLevel(str, Enum):
    REMEMBER = "remember"
    UNDERSTAND = "understand"
    APPLY = "apply"
    ANALYZE = "analyze"
    EVALUATE = "evaluate"
    CREATE = "create"


class AttemptStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"


class ExamDifficulty(str, Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class SessionStatus(str, Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"


class ConversationStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


BLOOM_LEVEL_ORDER = [
    BloomLevel.REMEMBER,
    BloomLevel.UNDERSTAND,
    BloomLevel.APPLY,
    BloomLevel.ANALYZE,
    BloomLevel.EVALUATE,
    BloomLevel.CREATE,
]

BLOOM_WEIGHTS = {
    BloomLevel.REMEMBER: 1.0,
    BloomLevel.UNDERSTAND: 1.0,
    BloomLevel.APPLY: 1.25,
    BloomLevel.ANALYZE: 1.5,
    BloomLevel.EVALUATE: 1.75,
    BloomLevel.CREATE: 2.0,
}


def get_bloom_rank(level: BloomLevel) -> int:
    return BLOOM_LEVEL_ORDER.index(level)


def get_bloom_weight(level: BloomLevel) -> float:
    return BLOOM_WEIGHTS[level]


def enum_values(enum_cls: type[Enum]) -> list[str]:
    return [member.value for member in enum_cls]
