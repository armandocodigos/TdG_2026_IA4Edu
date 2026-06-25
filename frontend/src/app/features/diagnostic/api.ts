import { apiRequest } from "@/app/shared/api/http";
import type {
  DiagnosticAnswerFeedback,
  DiagnosticAttemptReview,
  DiagnosticAttempt,
  DiagnosticFinishResult,
  DiagnosticProfile,
  DiagnosticBreakdown,
} from "@/app/features/diagnostic/types";
import type { AttemptStatus, BloomLevel, MasteryLevel, Subject } from "@/app/shared/types/domain";

interface DiagnosticQuestionResponse {
  id: string;
  topic: string;
  skill: string;
  question_text: string;
  bloom_level: BloomLevel;
  options: string[];
}

interface DiagnosticAttemptResponse {
  id: string;
  subject: Subject;
  status: AttemptStatus;
  questions: DiagnosticQuestionResponse[];
  answers: Record<string, string>;
}

interface DiagnosticBreakdownResponse {
  mastery: MasteryLevel;
  correct_answers: number;
  total_questions: number;
  score_percentage: number;
}

interface DiagnosticProfileResponse {
  id: string;
  user_id: string;
  subject: Subject;
  topic_results: Record<string, DiagnosticBreakdownResponse>;
  bloom_results: Record<string, DiagnosticBreakdownResponse>;
  strengths: string[];
  weaknesses: string[];
  positive_recommendations?: string[];
  improvement_recommendations?: string[];
}

interface DiagnosticFinishResponse {
  attempt_id: string;
  score_global: number;
  profile: DiagnosticProfileResponse;
  answers_feedback: DiagnosticAnswerFeedbackResponse[];
}

interface DiagnosticAttemptReviewResponse {
  attempt_id: string;
  subject: Subject;
  score_global: number;
  answers_feedback: DiagnosticAnswerFeedbackResponse[];
}

interface DiagnosticAnswerFeedbackResponse {
  question_id: string;
  topic: string;
  skill: string;
  bloom_level: BloomLevel;
  question_text: string;
  student_answer: string;
  correct_answer: string;
  is_correct: boolean;
  explanation: string | null;
}

function mapBreakdown(payload: DiagnosticBreakdownResponse): DiagnosticBreakdown {
  return {
    mastery: payload.mastery,
    correctAnswers: payload.correct_answers,
    totalQuestions: payload.total_questions,
    scorePercentage: payload.score_percentage,
  };
}

function mapBreakdownRecord(payload: Record<string, DiagnosticBreakdownResponse>) {
  return Object.fromEntries(Object.entries(payload).map(([key, value]) => [key, mapBreakdown(value)]));
}

function mapAttempt(payload: DiagnosticAttemptResponse): DiagnosticAttempt {
  return {
    id: payload.id,
    subject: payload.subject,
    status: payload.status,
    answers: payload.answers ?? {},
    questions: payload.questions.map((question) => ({
      id: question.id,
      topic: question.topic,
      skill: question.skill,
      questionText: question.question_text,
      bloomLevel: question.bloom_level,
      options: question.options,
    })),
  };
}

function mapAnswerFeedback(payload: DiagnosticAnswerFeedbackResponse): DiagnosticAnswerFeedback {
  return {
    questionId: payload.question_id,
    topic: payload.topic,
    skill: payload.skill,
    bloomLevel: payload.bloom_level,
    questionText: payload.question_text,
    studentAnswer: payload.student_answer,
    correctAnswer: payload.correct_answer,
    isCorrect: payload.is_correct,
    explanation: payload.explanation,
  };
}

function mapProfile(payload: DiagnosticProfileResponse): DiagnosticProfile {
  return {
    id: payload.id,
    userId: payload.user_id,
    subject: payload.subject,
    topicResults: mapBreakdownRecord(payload.topic_results),
    bloomResults: mapBreakdownRecord(payload.bloom_results),
    strengths: payload.strengths,
    weaknesses: payload.weaknesses,
    positiveRecommendations: payload.positive_recommendations ?? [],
    improvementRecommendations: payload.improvement_recommendations ?? [],
  };
}

export function startDiagnostic() {
  return apiRequest<DiagnosticAttemptResponse>("/api/diagnostic/start", {
    method: "POST",
  }).then(mapAttempt);
}

export function fetchDiagnosticAttempt(attemptId: string) {
  return apiRequest<DiagnosticAttemptResponse>(`/api/diagnostic/${attemptId}`).then(mapAttempt);
}

export function submitDiagnosticAnswer(attemptId: string, questionId: string, answer: string) {
  return apiRequest<void>(`/api/diagnostic/${attemptId}/answer`, {
    method: "POST",
    body: JSON.stringify({
      question_id: questionId,
      answer,
    }),
  });
}

export function finishDiagnostic(attemptId: string) {
  return apiRequest<DiagnosticFinishResponse>(`/api/diagnostic/${attemptId}/finish`, {
    method: "POST",
  }).then(mapFinishResponse);
}

export function fetchDiagnosticResult(attemptId: string) {
  return apiRequest<DiagnosticFinishResponse>(`/api/diagnostic/${attemptId}/result`).then(mapFinishResponse);
}

function mapFinishResponse(payload: DiagnosticFinishResponse): DiagnosticFinishResult {
  return {
    attemptId: payload.attempt_id,
    scoreGlobal: payload.score_global,
    profile: mapProfile(payload.profile),
    answersFeedback: (payload.answers_feedback ?? []).map(mapAnswerFeedback),
  };
}

export function abandonDiagnostic(attemptId: string) {
  return apiRequest<void>(`/api/diagnostic/${attemptId}/abandon`, {
    method: "POST",
  });
}

export function fetchDiagnosticProfile() {
  return apiRequest<DiagnosticProfileResponse | null>("/api/diagnostic/profile").then((payload) => {
    if (!payload) return null;
    return mapProfile(payload);
  });
}

export function fetchLatestDiagnosticReview() {
  return apiRequest<DiagnosticAttemptReviewResponse | null>("/api/diagnostic/latest-review").then((payload) => {
    if (!payload) return null;
    return {
      attemptId: payload.attempt_id,
      subject: payload.subject,
      scoreGlobal: payload.score_global,
      answersFeedback: (payload.answers_feedback ?? []).map(mapAnswerFeedback),
    } satisfies DiagnosticAttemptReview;
  });
}
