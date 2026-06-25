import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate, useParams } from "react-router";
import { CheckCircle2, TrendingUp } from "lucide-react";

import { ExamView } from "@/app/components/ExamView";
import { MathText } from "@/app/components/ui/MathText";
import { abandonExam, fetchExamResult, finishExam, submitExamAnswer } from "@/app/features/exams/api";
import { ExamRecommendationPanels } from "@/app/features/exams/components/ExamRecommendationPanels";
import { clearStoredExamAttempt, getStoredExamAttempt, storeExamAttempt } from "@/app/features/exams/storage";
import type { ExamAttempt, ExamFinishResult } from "@/app/features/exams/types";
import { getErrorMessage } from "@/app/shared/api/errors";
import type { MasteryLevel } from "@/app/shared/types/domain";

const MASTERY_LABELS: Record<MasteryLevel, string> = {
  high: "Dominado",
  medium: "En progreso",
  low: "Por reforzar",
};

const MASTERY_BAR: Record<MasteryLevel, string> = {
  high: "bg-emerald-500",
  medium: "bg-amber-400",
  low: "bg-red-400",
};

const MASTERY_BADGE: Record<MasteryLevel, string> = {
  high: "border-emerald-200 bg-emerald-50 text-emerald-700",
  medium: "border-amber-200 bg-amber-50 text-amber-700",
  low: "border-red-200 bg-red-50 text-red-600",
};

const DIFFICULTY_LABELS = {
  basic: "Básico",
  intermediate: "Intermedio",
  advanced: "Avanzado",
};

function formatLabel(value: string) {
  return value.replace(/_/g, " ");
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

export function ExamAttemptPage() {
  const params = useParams();
  const navigate = useNavigate();
  const location = useLocation();

  const [attempt, setAttempt] = useState<ExamAttempt | null>(null);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [savingQuestionId, setSavingQuestionId] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLoadingAttempt, setIsLoadingAttempt] = useState(true);
  const [finishResult, setFinishResult] = useState<ExamFinishResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const attemptId = params.attemptId;
    const stateAttempt = location.state?.attempt as ExamAttempt | undefined;

    if (!attemptId) {
      setIsLoadingAttempt(false);
      return;
    }

    const resolvedAttemptId = attemptId;
    let isCurrent = true;

    async function loadAttemptState() {
      setIsLoadingAttempt(true);
      try {
        const result = await fetchExamResult(resolvedAttemptId);
        if (!isCurrent) {
          return;
        }
        clearStoredExamAttempt(resolvedAttemptId);
        setAttempt(null);
        setFinishResult({
          attemptId: resolvedAttemptId,
          scoreGlobal: result.scoreGlobal,
          result,
        });
        setIsLoadingAttempt(false);
        return;
      } catch {
        if (!isCurrent) {
          return;
        }
      }

      const storedAttempt = getStoredExamAttempt(resolvedAttemptId);
      const nextAttempt =
        storedAttempt && stateAttempt && stateAttempt.id === resolvedAttemptId
          ? { ...stateAttempt, ...storedAttempt, answers: storedAttempt.answers ?? stateAttempt.answers ?? {} }
          : storedAttempt ?? (stateAttempt && stateAttempt.id === resolvedAttemptId ? stateAttempt : null);

      setAttempt(nextAttempt);
      setAnswers(nextAttempt?.answers ?? {});
      setFinishResult(null);
      setIsLoadingAttempt(false);
    }

    void loadAttemptState();

    return () => {
      isCurrent = false;
    };
  }, [location.state, params.attemptId]);

  async function handleAnswer(questionId: string, answer: string) {
    if (!attempt) {
      return;
    }

    setError(null);
    setSavingQuestionId(questionId);
    try {
      await submitExamAnswer(attempt.id, questionId, answer);
      setAnswers((current) => ({ ...current, [questionId]: answer }));
      setAttempt((current) => {
        if (!current) return current;
        const nextAttempt = { ...current, answers: { ...(current.answers ?? {}), [questionId]: answer } };
        storeExamAttempt(nextAttempt);
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
      const result = await finishExam(attempt.id);
      clearStoredExamAttempt(attempt.id);
      setFinishResult(result);
      navigate(`/exams/${attempt.id}`, { replace: true, state: null });
    } catch (submitError) {
      setError(getErrorMessage(submitError, "No se pudo finalizar el examen."));
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleExit() {
    if (!attempt) {
      navigate("/exams");
      return;
    }

    setError(null);
    try {
      await abandonExam(attempt.id);
      clearStoredExamAttempt(attempt.id);
    } catch (exitError) {
      setError(getErrorMessage(exitError, "No se pudo cerrar el intento."));
      return;
    }
    navigate("/exams");
  }

  if (isLoadingAttempt && !finishResult && !attempt) {
    return (
      <div className="px-8 py-8">
        <div className="mx-auto max-w-3xl rounded-lg border border-[#e5e5e5] bg-white p-8">
          <h2 className="mb-2 text-xl font-semibold text-[#171717]">Cargando intento</h2>
          <p className="text-[13px] leading-6 text-[#737373]">Estamos revisando si este examen ya fue finalizado.</p>
        </div>
      </div>
    );
  }

  if (!attempt && !finishResult) {
    return (
      <div className="px-8 py-8">
        <div className="mx-auto max-w-3xl rounded-lg border border-[#e5e5e5] bg-white p-8">
          <h2 className="mb-2 text-xl font-semibold text-[#171717]">No se encontró el intento</h2>
          <p className="mb-6 text-[13px] leading-6 text-[#737373]">
            No se encontró el intento local. Inicia un nuevo examen desde la pantalla principal.
          </p>
          <Link
            to="/exams"
            className="inline-flex rounded-md bg-[#171717] px-4 py-2.5 text-[13px] font-medium text-white transition-colors hover:bg-[#404040]"
          >
            Volver a exámenes
          </Link>
        </div>
      </div>
    );
  }

  if (finishResult) {
    return (
      <div className="px-8 py-8">
        <div className="mx-auto max-w-6xl">
          <div className="mb-6 rounded-lg border border-[#e5e5e5] bg-white p-6">
            <h1 className="mb-2 text-[28px] font-semibold text-[#171717]">Examen completado</h1>
            <p className="text-[14px] text-[#737373]">
              El intento fue finalizado y el resultado quedó guardado.
            </p>
          </div>

          <div className="mb-6 grid gap-4 md:grid-cols-3">
            <div className="rounded-lg border border-[#e5e5e5] bg-white p-5">
              <p className="text-[11px] uppercase tracking-[0.16em] text-[#a3a3a3]">Puntaje global</p>
              <p className="mt-3 text-3xl font-semibold text-[#171717]">{Math.round(finishResult.scoreGlobal)}%</p>
            </div>
            <div className="rounded-lg border border-emerald-100 bg-emerald-50/60 p-5">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 text-emerald-600" />
                <p className="text-[12px] font-semibold text-emerald-800">Fortalezas</p>
              </div>
              <p className="mt-3 text-[13px] capitalize text-emerald-700">
                {finishResult.result.strengths.length ? finishResult.result.strengths.map(formatLabel).join(", ") : "Aún por consolidar"}
              </p>
            </div>
            <div className="rounded-lg border border-amber-100 bg-amber-50/60 p-5">
              <div className="flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-amber-600" />
                <p className="text-[12px] font-semibold text-amber-800">Áreas de mejora</p>
              </div>
              <p className="mt-3 text-[13px] capitalize text-amber-700">
                {finishResult.result.weaknesses.length ? finishResult.result.weaknesses.map(formatLabel).join(", ") : "Sin áreas críticas"}
              </p>
            </div>
          </div>

          <div className="mb-6 rounded-lg border border-[#e5e5e5] bg-white p-6">
            <h2 className="mb-4 text-[18px] font-semibold text-[#171717]">Resultados por tema</h2>
            <div className="space-y-4">
              {sortByMastery(Object.entries(finishResult.result.topicBreakdown)).map(([topic, result]) => (
                <div key={topic} className="rounded-md border border-[#e5e5e5] bg-[#fafafa] p-4 text-[13px] text-[#737373]">
                  <div className="mb-2 flex items-center justify-between gap-4">
                    <p className="font-medium capitalize text-[#171717]">{formatLabel(topic)}</p>
                    <span className={`rounded-full border px-2 py-0.5 text-[11px] font-medium ${MASTERY_BADGE[result.mastery]}`}>
                      {MASTERY_LABELS[result.mastery]}
                    </span>
                  </div>
                  <div className="h-2 w-full overflow-hidden rounded-full bg-[#e5e5e5]">
                    <div className={`h-full rounded-full ${MASTERY_BAR[result.mastery]}`} style={{ width: `${result.scorePercentage}%` }} />
                  </div>
                  <p className="mt-2">
                    {result.correctAnswers}/{result.totalQuestions} correctas · {Math.round(result.scorePercentage)}%
                  </p>
                </div>
              ))}
            </div>
          </div>

          <ExamRecommendationPanels
            positiveRecommendations={finishResult.result.positiveRecommendations}
            improvementRecommendations={finishResult.result.improvementRecommendations}
          />

          <div className="rounded-lg border border-[#e5e5e5] bg-white p-6">
            <div className="mb-4 flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-blue-600" />
              <h2 className="text-[18px] font-semibold text-[#171717]">Revisión de preguntas</h2>
            </div>
            {finishResult.result.answersFeedback.length ? (
              <div className="space-y-3">
                {finishResult.result.answersFeedback.map((item, index) => (
                  <div
                    key={item.questionId}
                    className={`rounded-lg border p-4 ${
                      item.isCorrect ? "border-emerald-100 bg-emerald-50/30" : "border-red-100 bg-red-50/30"
                    }`}
                  >
                    <div className="mb-2 flex items-start justify-between gap-3">
                      <div className="flex flex-wrap gap-2">
                        <span className="rounded-full bg-white px-2 py-0.5 text-[11px] font-medium capitalize text-[#525252]">{formatLabel(item.topic)}</span>
                        <span className="rounded-full bg-white px-2 py-0.5 text-[11px] font-medium text-[#525252]">{DIFFICULTY_LABELS[item.difficulty]}</span>
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
            ) : (
              <p className="rounded-lg border border-emerald-100 bg-emerald-50 px-4 py-3 text-[13px] text-emerald-700">
                No hay preguntas para revisar en este intento.
              </p>
            )}
            <div className="mt-6 flex justify-end">
              <Link
                to="/exams"
                className="inline-flex rounded-md bg-[#171717] px-4 py-2.5 text-[13px] font-medium text-white transition-colors hover:bg-[#404040]"
              >
                Volver a exámenes
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const activeAttempt = attempt;
  if (!activeAttempt) {
    return null;
  }

  return (
    <>
      {error ? (
        <div className="border-b border-[#fecaca] bg-[#fef2f2] px-6 py-3 text-[13px] text-[#b91c1c]">
          <div className="mx-auto max-w-5xl">{error}</div>
        </div>
      ) : null}
      <ExamView
        title={activeAttempt.difficulty ? `Examen nivel ${DIFFICULTY_LABELS[activeAttempt.difficulty].toLowerCase()}` : "Examen personalizado"}
        contextTags={activeAttempt.topics.map(formatLabel)}
        questions={activeAttempt.questions.map((question) => ({
          id: question.id,
          question: question.questionText,
          options: question.options,
        }))}
        answers={answers}
        onAnswer={handleAnswer}
        onComplete={handleSubmit}
        onExit={() => void handleExit()}
        submitLabel="Finalizar examen"
        submittingTitle="Finalizando tu examen"
        submittingDescription="Estamos procesando tus respuestas y preparando tu resultado."
        isSubmitting={isSubmitting}
        savingQuestionId={savingQuestionId}
      />
    </>
  );
}
