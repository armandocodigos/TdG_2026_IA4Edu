from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from app.models.enums import ExamDifficulty, Subject
from app.schemas.diagnostic import TopicResultRead


class ExamQuestionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str
    topic: str
    difficulty: ExamDifficulty
    skill: str
    question_text: str = Field(validation_alias=AliasChoices("question_text", "prompt"))
    options: list[str]
    weight: float


class ExamStartRequest(BaseModel):
    topics: list[str]
    difficulty: ExamDifficulty
    question_count: int = 10


class ExamAttemptRead(BaseModel):
    id: str
    subject: Subject
    title: str
    topics: list[str] = Field(default_factory=list)
    difficulty: ExamDifficulty | None = None
    question_count: int
    questions: list[ExamQuestionRead]


class ExamAnswerRequest(BaseModel):
    question_id: str
    answer: str


class AnswerFeedbackRead(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    question_id: str
    topic: str
    difficulty: ExamDifficulty
    skill: str
    question_text: str = Field(validation_alias=AliasChoices("question_text", "prompt"))
    student_answer: str
    correct_answer: str
    is_correct: bool = False
    explanation: str | None = None


class IncorrectAnswerFeedbackRead(AnswerFeedbackRead):
    pass


class ExamResultRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    exam_attempt_id: str
    score_global: float
    topic_breakdown: dict[str, TopicResultRead]
    strengths: list[str]
    weaknesses: list[str]
    positive_recommendations: list[str] = Field(default_factory=list)
    improvement_recommendations: list[str] = Field(default_factory=list)
    incorrect_answers: list[IncorrectAnswerFeedbackRead] = Field(default_factory=list)
    answers_feedback: list[AnswerFeedbackRead] = Field(default_factory=list)


class ExamAvailabilityItem(BaseModel):
    topic: str
    difficulty: ExamDifficulty
    question_count: int


class ExamAvailabilityResponse(BaseModel):
    subject: Subject
    items: list[ExamAvailabilityItem]


class ExamFinishResponse(BaseModel):
    attempt_id: str
    score_global: float
    result: ExamResultRead


class LastExamResultRead(BaseModel):
    attempt_id: str
    subject: Subject
    title: str
    topics: list[str] = Field(default_factory=list)
    difficulty: ExamDifficulty | None = None
    completed_at: str
    result: ExamResultRead
