import { apiRequest } from "@/app/shared/api/http";
import type {
  ExamAttempt,
  ExamAvailability,
  ExamAvailabilityItem,
  ExamBreakdown,
  ExamDifficulty,
  ExamFinishResult,
  LastExamResult,
  ExamResult,
  StartCustomExamPayload,
} from "@/app/features/exams/types";
import type { MasteryLevel, Subject } from "@/app/shared/types/domain";

interface ExamQuestionResponse {
  id: string;
  topic: string;
  difficulty: ExamDifficulty;
  skill: string;
  question_text: string;
  options: string[];
  weight: number;
}

interface ExamAttemptResponse {
  id: string;
  subject: Subject;
  title: string;
  topics: string[];
  difficulty: ExamDifficulty | null;
  question_count: number;
  questions: ExamQuestionResponse[];
}

interface ExamBreakdownResponse {
  mastery: MasteryLevel;
  correct_answers: number;
  total_questions: number;
  score_percentage: number;
}

interface ExamResultResponse {
  id: string;
  exam_attempt_id: string;
  score_global: number;
  topic_breakdown: Record<string, ExamBreakdownResponse>;
  strengths: string[];
  weaknesses: string[];
  positive_recommendations?: string[];
  improvement_recommendations?: string[];
  incorrect_answers: IncorrectAnswerFeedbackResponse[];
  answers_feedback?: IncorrectAnswerFeedbackResponse[];
}

interface ExamFinishResponse {
  attempt_id: string;
  score_global: number;
  result: ExamResultResponse;
}

interface LastExamResultResponse {
  attempt_id: string;
  subject: Subject;
  title: string;
  topics: string[];
  difficulty: ExamDifficulty | null;
  completed_at: string;
  result: ExamResultResponse;
}

interface IncorrectAnswerFeedbackResponse {
  question_id: string;
  topic: string;
  difficulty: ExamDifficulty;
  skill: string;
  question_text: string;
  student_answer: string;
  correct_answer: string;
  is_correct?: boolean;
  explanation: string | null;
}

interface ExamAvailabilityResponse {
  subject: Subject;
  items: Array<{
    topic: string;
    difficulty: ExamDifficulty;
    question_count: number;
  }>;
}

function mapBreakdown(payload: ExamBreakdownResponse): ExamBreakdown {
  return {
    mastery: payload.mastery,
    correctAnswers: payload.correct_answers,
    totalQuestions: payload.total_questions,
    scorePercentage: payload.score_percentage,
  };
}

function mapBreakdownRecord(payload: Record<string, ExamBreakdownResponse>) {
  return Object.fromEntries(Object.entries(payload).map(([key, value]) => [key, mapBreakdown(value)]));
}

function mapExamResult(payload: ExamResultResponse): ExamResult {
  const answersFeedback = (payload.answers_feedback ?? payload.incorrect_answers ?? []).map(mapAnswerFeedback);
  return {
    id: payload.id,
    examAttemptId: payload.exam_attempt_id,
    scoreGlobal: payload.score_global,
    topicBreakdown: mapBreakdownRecord(payload.topic_breakdown),
    strengths: payload.strengths,
    weaknesses: payload.weaknesses,
    positiveRecommendations: payload.positive_recommendations ?? [],
    improvementRecommendations: payload.improvement_recommendations ?? [],
    answersFeedback,
  };
}

function mapAnswerFeedback(item: IncorrectAnswerFeedbackResponse) {
  return {
    questionId: item.question_id,
    topic: item.topic,
    difficulty: item.difficulty,
    skill: item.skill,
    questionText: item.question_text,
    studentAnswer: item.student_answer,
    correctAnswer: item.correct_answer,
    isCorrect: item.is_correct ?? false,
    explanation: item.explanation,
  };
}

function mapAvailabilityItem(item: ExamAvailabilityResponse["items"][number]): ExamAvailabilityItem {
  return {
    topic: item.topic,
    difficulty: item.difficulty,
    questionCount: item.question_count,
  };
}

export function fetchExamAvailability() {
  return apiRequest<ExamAvailabilityResponse>("/api/exams/availability").then(
    (payload): ExamAvailability => ({
      subject: payload.subject,
      items: payload.items.map(mapAvailabilityItem),
    }),
  );
}

export function startCustomExam(payload: StartCustomExamPayload) {
  return apiRequest<ExamAttemptResponse>("/api/exams/start", {
    method: "POST",
    body: JSON.stringify({
      topics: payload.topics,
      difficulty: payload.difficulty,
      question_count: payload.questionCount,
    }),
  }).then(
    (response): ExamAttempt => ({
      id: response.id,
      subject: response.subject,
      title: response.title,
      topics: response.topics ?? [],
      difficulty: response.difficulty,
      questionCount: response.question_count,
      questions: response.questions.map((question) => ({
        id: question.id,
        topic: question.topic,
        difficulty: question.difficulty,
        skill: question.skill,
        questionText: question.question_text,
        options: question.options,
        weight: question.weight,
      })),
      answers: {},
    }),
  );
}

export function submitExamAnswer(attemptId: string, questionId: string, answer: string) {
  return apiRequest<void>(`/api/exams/${attemptId}/answer`, {
    method: "POST",
    body: JSON.stringify({
      question_id: questionId,
      answer,
    }),
  });
}

export function finishExam(attemptId: string) {
  return apiRequest<ExamFinishResponse>(`/api/exams/${attemptId}/finish`, {
    method: "POST",
  }).then(
    (payload): ExamFinishResult => ({
      attemptId: payload.attempt_id,
      scoreGlobal: payload.score_global,
      result: mapExamResult(payload.result),
    }),
  );
}

export function abandonExam(attemptId: string) {
  return apiRequest<void>(`/api/exams/${attemptId}/abandon`, {
    method: "POST",
  });
}

export function fetchExamResult(attemptId: string) {
  return apiRequest<ExamResultResponse>(`/api/exams/${attemptId}/result`).then(mapExamResult);
}

export function fetchLatestExamResult() {
  return apiRequest<LastExamResultResponse>("/api/exams/latest-result").then(
    (payload): LastExamResult => ({
      attemptId: payload.attempt_id,
      subject: payload.subject,
      title: payload.title,
      topics: payload.topics ?? [],
      difficulty: payload.difficulty,
      completedAt: payload.completed_at,
      result: mapExamResult(payload.result),
    }),
  );
}
