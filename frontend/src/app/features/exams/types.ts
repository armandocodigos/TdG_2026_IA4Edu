import type { MasteryLevel, Subject } from "@/app/shared/types/domain";

export type ExamDifficulty = "basic" | "intermediate" | "advanced";

export interface ExamQuestion {
  id: string;
  topic: string;
  difficulty: ExamDifficulty;
  skill: string;
  questionText: string;
  options: string[];
  weight: number;
}

export interface ExamAttempt {
  id: string;
  subject: Subject;
  title: string;
  topics: string[];
  difficulty: ExamDifficulty | null;
  questionCount: number;
  questions: ExamQuestion[];
  answers?: Record<string, string>;
}

export interface ExamBreakdown {
  mastery: MasteryLevel;
  correctAnswers: number;
  totalQuestions: number;
  scorePercentage: number;
}

export interface ExamResult {
  id: string;
  examAttemptId: string;
  scoreGlobal: number;
  topicBreakdown: Record<string, ExamBreakdown>;
  strengths: string[];
  weaknesses: string[];
  positiveRecommendations: string[];
  improvementRecommendations: string[];
  answersFeedback: IncorrectAnswerFeedback[];
}

export interface ExamFinishResult {
  attemptId: string;
  scoreGlobal: number;
  result: ExamResult;
}

export interface IncorrectAnswerFeedback {
  questionId: string;
  topic: string;
  difficulty: ExamDifficulty;
  skill: string;
  questionText: string;
  studentAnswer: string;
  correctAnswer: string;
  isCorrect: boolean;
  explanation: string | null;
}

export interface ExamAvailabilityItem {
  topic: string;
  difficulty: ExamDifficulty;
  questionCount: number;
}

export interface ExamAvailability {
  subject: Subject;
  items: ExamAvailabilityItem[];
}

export interface StartCustomExamPayload {
  topics: string[];
  difficulty: ExamDifficulty;
  questionCount: number;
}

export interface LastExamResult {
  attemptId: string;
  subject: Subject;
  title: string;
  topics: string[];
  difficulty: ExamDifficulty | null;
  completedAt: string;
  result: ExamResult;
}
