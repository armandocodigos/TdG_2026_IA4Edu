import { useEffect, useRef, useState } from "react";
import { Link, useLocation, useNavigate, useParams } from "react-router";
import {
  AlertTriangle,
  ArrowRight,
  CheckCircle2,
  PartyPopper,
  Target,
  TrendingUp,
} from "lucide-react";
import confetti from "canvas-confetti";

import { ExamView } from "@/app/components/ExamView";
import { MathText } from "@/app/components/ui/MathText";
import { DiagnosticRecommendationPanels } from "@/app/features/diagnostic/components/DiagnosticRecommendationPanels";
import { abandonDiagnostic, fetchDiagnosticAttempt, fetchDiagnosticResult, finishDiagnostic, submitDiagnosticAnswer } from "@/app/features/diagnostic/api";
import { clearStoredDiagnosticAttempt, getStoredDiagnosticAttempt, storeDiagnosticAttempt } from "@/app/features/diagnostic/storage";
import type { DiagnosticAttempt, DiagnosticFinishResult } from "@/app/features/diagnostic/types";
import { getErrorMessage } from "@/app/shared/api/errors";
import type { MasteryLevel } from "@/app/shared/types/domain";

type AttemptLocationState = {
  attempt?: DiagnosticAttempt;
};

const MASTERY_CONFIG: Record<MasteryLevel, { label: string; color: string; bg: string; border: string }> = {
  high: { label: "Dominado", color: "text-emerald-700", bg: "bg-emerald-50", border: "border-emerald-200" },
  medium: { label: "En progreso", color: "text-amber-700", bg: "bg-amber-50", border: "border-amber-200" },
  low: { label: "Por reforzar", color: "text-red-600", bg: "bg-red-50", border: "border-red-200" },
};

function getMasteryStyle(mastery: MasteryLevel) {
  return MASTERY_CONFIG[mastery];
}

function getScoreBarColor(score: number) {
  if (score >= 75) return "bg-emerald-500";
  if (score >= 40) return "bg-amber-400";
  return "bg-red-400";
}

function getScoreRingColor(score: number) {
  if (score >= 75) return "#10b981";
  if (score >= 40) return "#f59e0b";
  return "#ef4444";
}

function getScoreLabel(score: number) {
  if (score >= 90) return "¡Excelente!";
  if (score >= 75) return "¡Muy bien!";
  if (score >= 60) return "Buen trabajo";
  if (score >= 40) return "Puedes mejorar";
  return "Sigue practicando";
}

const MASTERY_ORDER: Record<MasteryLevel, number> = {
  high: 0,
  medium: 1,
  low: 2,
};

function sortByMastery<T extends { mastery: MasteryLevel; scorePercentage: number }>(entries: Array<[string, T]>) {
  return [...entries].sort(([, a], [, b]) => {
    const masteryDiff = MASTERY_ORDER[a.mastery] - MASTERY_ORDER[b.mastery];
    if (masteryDiff !== 0) return masteryDiff;
    return b.scorePercentage - a.scorePercentage;
  });
}

export function DiagnosticAttemptPage() {
  const params = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const confettiFired = useRef(false);
  const locationState = (location.state as AttemptLocationState | null) ?? null;

  const [attempt, setAttempt] = useState<DiagnosticAttempt | null>(null);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [savingQuestionId, setSavingQuestionId] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLoadingAttempt, setIsLoadingAttempt] = useState(true);
  const [finishResult, setFinishResult] = useState<DiagnosticFinishResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const attemptId = params.attemptId;
    const stateAttempt = locationState?.attempt;
    let isCurrent = true;

    if (!attemptId) {
      setIsLoadingAttempt(false);
      return;
    }

    async function loadAttemptState() {
      setIsLoadingAttempt(true);

      // 1. Intentar recuperar el resultado si el intento ya fue finalizado
      try {
        const result = await fetchDiagnosticResult(attemptId!);
        if (!isCurrent) return;
        clearStoredDiagnosticAttempt(attemptId!);
        setAttempt(null);
        setFinishResult(result);
        setIsLoadingAttempt(false);
        return;
      } catch {
        if (!isCurrent) return;
      }

      // 2. Cargar intento en curso: sessionStorage → state → API
      const storedAttempt = getStoredDiagnosticAttempt(attemptId!);
      const initial =
        storedAttempt ?? (stateAttempt && stateAttempt.id === attemptId ? stateAttempt : null);
      if (initial && isCurrent) {
        setAttempt(initial);
        setAnswers(initial.answers ?? {});
      }

      try {
        const nextAttempt = await fetchDiagnosticAttempt(attemptId!);
        if (!isCurrent) return;
        setAttempt(nextAttempt);
        setAnswers(nextAttempt.answers ?? {});
        storeDiagnosticAttempt(nextAttempt);
      } catch (loadError: unknown) {
        if (!isCurrent) return;
        setError(getErrorMessage(loadError, "No se pudo recuperar el intento de diagnóstico."));
      } finally {
        if (isCurrent) setIsLoadingAttempt(false);
      }
    }

    void loadAttemptState();

    return () => {
      isCurrent = false;
    };
  }, [locationState, params.attemptId]);

  /* fire confetti once when results appear */
  useEffect(() => {
    if (finishResult && !confettiFired.current) {
      confettiFired.current = true;
      void confetti({
        particleCount: 120,
        spread: 80,
        origin: { y: 0.55 },
        colors: ["#3b82f6", "#8b5cf6", "#10b981", "#f59e0b"],
      });
    }
  }, [finishResult]);

  async function handleAnswer(questionId: string, answer: string) {
    if (!attempt) {
      return;
    }

    setError(null);
    setSavingQuestionId(questionId);
    try {
      await submitDiagnosticAnswer(attempt.id, questionId, answer);
      setAnswers((current) => ({ ...current, [questionId]: answer }));
      setAttempt((current) => {
        if (!current) return current;
        const nextAttempt = { ...current, answers: { ...current.answers, [questionId]: answer } };
        storeDiagnosticAttempt(nextAttempt);
        return nextAttempt;
      });
    } catch (submitError) {
      setError(getErrorMessage(submitError, "No se pudo guardar la respuesta."));
    } finally {
      setSavingQuestionId(null);
    }
  }

  async function handleSubmit() {
    if (!attempt) {
      return;
    }

    setError(null);
    setIsSubmitting(true);
    try {
      const result = await finishDiagnostic(attempt.id);
      clearStoredDiagnosticAttempt(attempt.id);
      setFinishResult(result);
    } catch (submitError) {
      setError(getErrorMessage(submitError, "No se pudo finalizar el diagnóstico."));
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleExit() {
    if (!attempt) {
      navigate("/diagnostic");
      return;
    }

    try {
      await abandonDiagnostic(attempt.id);
    } catch {
    } finally {
      clearStoredDiagnosticAttempt(attempt.id);
      navigate("/diagnostic");
    }
  }

  /* ── loading ── */
  if (isLoadingAttempt && !finishResult && !attempt) {
    return (
      <div className="px-8 py-8">
        <div className="mx-auto max-w-3xl rounded-lg border border-[#e5e5e5] bg-white p-8">
          <h2 className="mb-2 text-xl font-semibold text-[#171717]">Cargando diagnóstico</h2>
          <p className="text-[13px] leading-6 text-[#737373]">Estamos revisando si este diagnóstico ya fue finalizado.</p>
        </div>
      </div>
    );
  }

  /* ── no attempt ── */
  if (!attempt && !finishResult) {
    return (
      <div className="flex h-full items-center justify-center bg-[#fafafa] p-8">
        <div className="w-full max-w-md rounded-xl border border-[#e5e5e5] bg-white p-8 text-center">
          <AlertTriangle className="mx-auto mb-4 h-10 w-10 text-amber-400" />
          <h2 className="mb-2 text-xl font-semibold text-[#171717]">No se encontró un examen activo</h2>
          <p className="mb-6 text-[13px] leading-6 text-[#737373]">
            Inicia un nuevo examen desde la página de diagnóstico para evaluar tu nivel.
          </p>
          <Link
            to="/diagnostic"
            className="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 px-5 py-2.5 text-[13px] font-medium text-white transition-all hover:from-blue-700 hover:to-indigo-700"
          >
            Ir al diagnóstico
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </div>
    );
  }

  /* ── results ── */
  if (finishResult) {
    const profile = finishResult.profile;
    const score = finishResult.scoreGlobal;
    const circumference = 2 * Math.PI * 54;
    const dashOffset = circumference - (score / 100) * circumference;

    return (
      <div className="px-8 py-8">
        <div className="mx-auto max-w-5xl">
          {/* Header */}
          <div className="mb-8 rounded-xl border border-blue-100 bg-gradient-to-r from-blue-50 to-indigo-50 p-6 text-center">
            <PartyPopper className="mx-auto mb-3 h-8 w-8 text-blue-600" />
            <h1 className="mb-1 text-[24px] font-semibold text-[#171717]">¡Diagnóstico completado!</h1>
            <p className="text-[14px] text-[#737373]">
              Aquí están tus resultados. Usa esta información para enfocar tu estudio.
            </p>
          </div>

          {/* Score + summary row */}
          <div className="mb-6 grid gap-6 md:grid-cols-[auto_1fr]">
            {/* Score circle */}
            <div className="flex flex-col items-center justify-center rounded-xl border border-[#e5e5e5] bg-white px-8 py-6">
              <div className="relative flex h-32 w-32 items-center justify-center">
                <svg className="h-32 w-32 -rotate-90" viewBox="0 0 128 128">
                  <circle cx="64" cy="64" r="54" fill="none" stroke="#f0f0f0" strokeWidth="8" />
                  <circle
                    cx="64"
                    cy="64"
                    r="54"
                    fill="none"
                    stroke={getScoreRingColor(score)}
                    strokeWidth="8"
                    strokeDasharray={`${circumference}`}
                    strokeDashoffset={dashOffset}
                    strokeLinecap="round"
                    className="transition-all duration-1000 ease-out"
                  />
                </svg>
                <div className="absolute text-center">
                  <span className="block text-[28px] font-bold text-[#171717]">{Math.round(score)}%</span>
                </div>
              </div>
              <p className="mt-3 text-[14px] font-medium text-[#171717]">{getScoreLabel(score)}</p>
              <p className="mt-0.5 text-[12px] text-[#737373]">Puntaje global</p>
            </div>

            {/* Topic results */}
            <div className="rounded-xl border border-[#e5e5e5] bg-white p-6">
              <div className="mb-4 flex items-center gap-2">
                <Target className="h-4 w-4 text-blue-600" />
                <h2 className="text-[16px] font-semibold text-[#171717]">Resultados por tema</h2>
              </div>
              <div className="space-y-4">
                {sortByMastery(Object.entries(profile.topicResults)).map(([topic, result]) => {
                  const style = getMasteryStyle(result.mastery);
                  return (
                    <div key={topic}>
                      <div className="mb-1.5 flex items-center justify-between">
                        <span className="text-[13px] font-medium capitalize text-[#525252]">{topic.replace(/_/g, " ")}</span>
                        <div className="flex items-center gap-2">
                          <span className="text-[12px] font-medium text-[#737373]">
                            {result.correctAnswers}/{result.totalQuestions} correctas
                          </span>
                          <span
                            className={`rounded-full border px-2 py-0.5 text-[10px] font-medium ${style.color} ${style.bg} ${style.border}`}
                          >
                            {style.label}
                          </span>
                        </div>
                      </div>
                      <div className="h-2.5 w-full overflow-hidden rounded-full bg-[#f0f0f0]">
                        <div
                          className={`h-full rounded-full transition-all duration-1000 ease-out ${getScoreBarColor(result.scorePercentage)}`}
                          style={{ width: `${result.scorePercentage}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Strengths & weaknesses row */}
          <div className="mb-6 grid gap-6 md:grid-cols-2">
            <div className="rounded-xl border border-[#e5e5e5] bg-white p-6">
              <div className="mb-3 flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 text-emerald-500" />
                <h2 className="text-[16px] font-semibold text-[#171717]">Fortalezas</h2>
              </div>
              {profile.strengths.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {profile.strengths.map((s) => (
                    <span
                      key={s}
                      className="rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1.5 text-[12px] font-medium capitalize text-emerald-700"
                    >
                      {s.replace(/_/g, " ")}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-[13px] text-[#737373]">Completa más preguntas para identificar fortalezas.</p>
              )}
            </div>

            <div className="rounded-xl border border-[#e5e5e5] bg-white p-6">
              <div className="mb-3 flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-amber-500" />
                <h2 className="text-[16px] font-semibold text-[#171717]">Áreas de mejora</h2>
              </div>
              {profile.weaknesses.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {profile.weaknesses.map((w) => (
                    <span
                      key={w}
                      className="rounded-full border border-amber-200 bg-amber-50 px-3 py-1.5 text-[12px] font-medium capitalize text-amber-700"
                    >
                      {w.replace(/_/g, " ")}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-[13px] text-[#737373]">¡Buen trabajo! No se detectaron áreas débiles.</p>
              )}
            </div>
          </div>

          <DiagnosticRecommendationPanels
            positiveRecommendations={profile.positiveRecommendations}
            improvementRecommendations={profile.improvementRecommendations}
          />

          {finishResult.answersFeedback.length ? (
            <div className="rounded-xl border border-[#e5e5e5] bg-white p-6">
              <div className="mb-4 flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 text-blue-600" />
                <h2 className="text-[16px] font-semibold text-[#171717]">Revisión de preguntas</h2>
              </div>
              <div className="space-y-3">
                {finishResult.answersFeedback.map((item, index) => (
                  <div
                    key={item.questionId}
                    className={`rounded-lg border p-4 ${
                      item.isCorrect ? "border-emerald-100 bg-emerald-50/30" : "border-red-100 bg-red-50/30"
                    }`}
                  >
                    <div className="mb-2 flex items-start justify-between gap-3">
                      <div className="flex flex-wrap gap-2">
                        <span className="rounded-full bg-white px-2 py-0.5 text-[11px] font-medium capitalize text-[#525252]">
                          {item.topic.replace(/_/g, " ")}
                        </span>
                      </div>
                      <div className="flex flex-shrink-0 items-center gap-2">
                        <span
                          className={`rounded-full bg-white px-2 py-0.5 text-[11px] font-medium ${
                            item.isCorrect ? "text-emerald-700" : "text-red-600"
                          }`}
                        >
                          {item.isCorrect ? "Correcta" : "Incorrecta"}
                        </span>
                        <span className="flex h-7 w-7 items-center justify-center rounded-full border border-[#e5e5e5] bg-white text-[12px] font-semibold text-[#171717] shadow-sm">
                          {index + 1}
                        </span>
                      </div>
                    </div>
                    <MathText content={item.questionText} className="text-[13px] font-medium leading-6 text-[#171717]" />
                    <div className="mt-3 grid gap-3 md:grid-cols-2">
                      <div className="rounded-md bg-white p-3">
                        <p
                          className={`text-[11px] font-semibold uppercase tracking-[0.12em] ${
                            item.isCorrect ? "text-emerald-600" : "text-red-500"
                          }`}
                        >
                          Tu respuesta
                        </p>
                        <MathText
                          content={item.studentAnswer}
                          className={`mt-1 text-[13px] ${item.isCorrect ? "text-emerald-700" : "text-red-600"}`}
                        />
                      </div>
                      <div className="rounded-md bg-white p-3">
                        <p className="text-[11px] font-semibold uppercase tracking-[0.12em] text-emerald-600">Opción correcta</p>
                        <MathText content={item.correctAnswer} className="mt-1 text-[13px] text-[#525252]" />
                      </div>
                    </div>
                    {item.explanation ? (
                      <div className="mt-3 rounded-md border border-blue-100 bg-blue-50 p-3">
                        <p className="text-[12px] font-semibold text-blue-800">Explicación</p>
                        <MathText content={item.explanation} className="mt-1 text-[13px] leading-6 text-blue-900" />
                      </div>
                    ) : null}
                  </div>
                ))}
              </div>
            </div>
          ) : null}

          <div className="mt-6 flex justify-end">
            <Link
              to="/diagnostic"
              className="inline-flex items-center gap-2 rounded-lg bg-[#171717] px-5 py-2.5 text-[13px] font-medium text-white transition-colors hover:bg-[#404040]"
            >
              Volver al diagnóstico
            </Link>
          </div>
        </div>
      </div>
    );
  }

  /* ── active exam ── */
  return (
    <>
      {error ? (
        <div className="border-b border-[#fecaca] bg-[#fef2f2] px-6 py-3 text-[13px] text-[#b91c1c]">
          <div className="mx-auto max-w-5xl">{error}</div>
        </div>
      ) : null}
      <ExamView
        title="Examen de Diagnóstico"
        subtitle=""
        questions={attempt.questions.map((question) => ({
          id: question.id,
          question: question.questionText,
          options: question.options,
          meta: [question.topic],
        }))}
        answers={answers}
        onAnswer={handleAnswer}
        onComplete={handleSubmit}
        onExit={() => void handleExit()}
        submitLabel="Finalizar diagnóstico"
        submittingTitle="Finalizando tu diagnóstico"
        submittingDescription="Estamos procesando tus respuestas y preparando tu resultado."
        isSubmitting={isSubmitting}
        savingQuestionId={savingQuestionId}
      />
    </>
  );
}
