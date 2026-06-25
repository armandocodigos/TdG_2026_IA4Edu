import type { ExamAttempt } from "@/app/features/exams/types";

function buildStorageKey(attemptId: string) {
  return `exam-attempt:${attemptId}`;
}

export function storeExamAttempt(attempt: ExamAttempt) {
  if (typeof window === "undefined") {
    return;
  }

  window.sessionStorage.setItem(buildStorageKey(attempt.id), JSON.stringify(attempt));
}

export function getStoredExamAttempt(attemptId: string) {
  if (typeof window === "undefined") {
    return null;
  }

  const rawValue = window.sessionStorage.getItem(buildStorageKey(attemptId));
  if (!rawValue) {
    return null;
  }

  try {
    return JSON.parse(rawValue) as ExamAttempt;
  } catch {
    window.sessionStorage.removeItem(buildStorageKey(attemptId));
    return null;
  }
}

export function clearStoredExamAttempt(attemptId: string) {
  if (typeof window === "undefined") {
    return;
  }

  window.sessionStorage.removeItem(buildStorageKey(attemptId));
}
