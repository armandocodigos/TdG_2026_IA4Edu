import type { AttemptStatus, BloomLevel, MasteryLevel, Subject } from "@/app/shared/types/domain";

export interface DiagnosticQuestion {
  id: string;
  topic: string;
  skill: string;
  questionText: string;
  bloomLevel: BloomLevel;
  options: string[];
}

export interface DiagnosticAttempt {
  id: string;
  subject: Subject;
  status: AttemptStatus;
  questions: DiagnosticQuestion[];
  answers: Record<string, string>;
}

export interface DiagnosticBreakdown {
  mastery: MasteryLevel;
  correctAnswers: number;
  totalQuestions: number;
  scorePercentage: number;
}

export interface DiagnosticProfile {
  id: string;
  userId: string;
  subject: Subject;
  topicResults: Record<string, DiagnosticBreakdown>;
  bloomResults: Record<string, DiagnosticBreakdown>;
  strengths: string[];
  weaknesses: string[];
  positiveRecommendations: string[];
  improvementRecommendations: string[];
}

export interface DiagnosticFinishResult {
  attemptId: string;
  scoreGlobal: number;
  profile: DiagnosticProfile;
  answersFeedback: DiagnosticAnswerFeedback[];
}

export interface DiagnosticAttemptReview {
  attemptId: string;
  subject: Subject;
  scoreGlobal: number;
  answersFeedback: DiagnosticAnswerFeedback[];
}

export interface DiagnosticAnswerFeedback {
  questionId: string;
  topic: string;
  skill: string;
  bloomLevel: BloomLevel;
  questionText: string;
  studentAnswer: string;
  correctAnswer: string;
  isCorrect: boolean;
  explanation: string | null;
}
