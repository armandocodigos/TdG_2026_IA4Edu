import type { DiagnosticAttempt } from "@/app/features/diagnostic/types";

function buildStorageKey(attemptId: string) {
  return `diagnostic-attempt:${attemptId}`;
}

export function storeDiagnosticAttempt(attempt: DiagnosticAttempt) {
  if (typeof window === "undefined") {
    return;
  }

  window.sessionStorage.setItem(buildStorageKey(attempt.id), JSON.stringify(attempt));
}

export function getStoredDiagnosticAttempt(attemptId: string) {
  if (typeof window === "undefined") {
    return null;
  }

  const rawValue = window.sessionStorage.getItem(buildStorageKey(attemptId));
  if (!rawValue) {
    return null;
  }

  try {
    return JSON.parse(rawValue) as DiagnosticAttempt;
  } catch {
    window.sessionStorage.removeItem(buildStorageKey(attemptId));
    return null;
  }
}

export function clearStoredDiagnosticAttempt(attemptId: string) {
  if (typeof window === "undefined") {
    return;
  }

  window.sessionStorage.removeItem(buildStorageKey(attemptId));
}
