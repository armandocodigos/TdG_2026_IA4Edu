from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import AttemptStatus, BloomLevel, MasteryLevel, Subject


class DiagnosticQuestionRead(BaseModel):
    id: str
    topic: str
    skill: str
    question_text: str
    bloom_level: BloomLevel
    options: list[str]


class DiagnosticAttemptRead(BaseModel):
    id: str
    subject: Subject
    status: AttemptStatus = AttemptStatus.IN_PROGRESS
    questions: list[DiagnosticQuestionRead]
    answers: dict[str, str] = Field(default_factory=dict)


class DiagnosticAnswerRequest(BaseModel):
    question_id: str
    answer: str


class TopicResultRead(BaseModel):
    mastery: MasteryLevel
    correct_answers: int
    total_questions: int
    score_percentage: float


class BloomResultRead(BaseModel):
    mastery: MasteryLevel
    correct_answers: int
    total_questions: int
    score_percentage: float


class DiagnosticProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    subject: Subject
    topic_results: dict[str, TopicResultRead]
    bloom_results: dict[str, BloomResultRead]
    strengths: list[str]
    weaknesses: list[str]
    positive_recommendations: list[str] = Field(default_factory=list)
    improvement_recommendations: list[str] = Field(default_factory=list)


class DiagnosticAnswerFeedbackRead(BaseModel):
    question_id: str
    topic: str
    skill: str
    bloom_level: BloomLevel
    question_text: str
    student_answer: str
    correct_answer: str
    is_correct: bool
    explanation: str | None = None


class DiagnosticFinishResponse(BaseModel):
    attempt_id: str
    score_global: float
    profile: DiagnosticProfileRead
    answers_feedback: list[DiagnosticAnswerFeedbackRead] = Field(default_factory=list)


class DiagnosticAttemptReviewRead(BaseModel):
    attempt_id: str
    subject: Subject
    score_global: float
    answers_feedback: list[DiagnosticAnswerFeedbackRead]
