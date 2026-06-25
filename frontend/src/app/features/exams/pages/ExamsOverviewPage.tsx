import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router";
import { ArrowRight, BookOpenCheck, Calculator, Check, ClipboardList, Eye, FileQuestion, History, Lightbulb, X } from "lucide-react";

import { MathText } from "@/app/components/ui/MathText";
import { useAuth } from "@/app/features/auth/AuthProvider";
import { fetchExamAvailability, fetchLatestExamResult, startCustomExam } from "@/app/features/exams/api";
import { ExamRecommendationPanels } from "@/app/features/exams/components/ExamRecommendationPanels";
import { storeExamAttempt } from "@/app/features/exams/storage";
import type { ExamAvailability, ExamDifficulty, LastExamResult } from "@/app/features/exams/types";
import { getErrorMessage } from "@/app/shared/api/errors";
import type { MasteryLevel } from "@/app/shared/types/domain";

const SUBJECT_LABELS: Record<string, string> = {
  precalculo: "Precálculo",
  preuniversitario: "Preuniversitario",
};

const DIFFICULTY_LABELS: Record<ExamDifficulty, string> = {
  basic: "Básico",
  intermediate: "Intermedio",
  advanced: "Avanzado",
};

const DIFFICULTY_HELP: Record<ExamDifficulty, string> = {
  basic: "Conceptos esenciales y ejercicios directos.",
  intermediate: "Aplicación con varios pasos y lectura de contexto.",
  advanced: "Análisis, restricciones y conexiones entre ideas.",
};

const DEFAULT_DIFFICULTY: ExamDifficulty = "basic";

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

function formatTopic(topic: string) {
  return topic.replace(/_/g, " ");
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

export function ExamsOverviewPage() {
  const [availability, setAvailability] = useState<ExamAvailability | null>(null);
  const [selectedTopics, setSelectedTopics] = useState<string[]>([]);
  const [useAllTopics, setUseAllTopics] = useState(true);
  const [selectedDifficulty, setSelectedDifficulty] = useState<ExamDifficulty>(DEFAULT_DIFFICULTY);
  const [questionCount, setQuestionCount] = useState(10);
  const [latestResult, setLatestResult] = useState<LastExamResult | null>(null);
  const [isLatestOpen, setIsLatestOpen] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isStarting, setIsStarting] = useState(false);

  const navigate = useNavigate();
  const { user } = useAuth();
  const currentSubject = user?.subject;

  useEffect(() => {
    if (!currentSubject) return;
    let isActive = true;

    setIsLoading(true);
    setAvailability(null);
    setSelectedTopics([]);
    setUseAllTopics(true);
    setLatestResult(null);
    setIsLatestOpen(false);
    setError(null);

    Promise.allSettled([fetchExamAvailability(), fetchLatestExamResult()])
      .then((payload) => {
        if (!isActive) return;
        const [availabilityResult, latestResultResponse] = payload;
        if (availabilityResult.status === "fulfilled") {
          setAvailability(availabilityResult.value);
          const initialTopics = Array.from(new Set(availabilityResult.value.items.map((item) => item.topic))).sort();
          setSelectedTopics(initialTopics);
        } else {
          setError(getErrorMessage(availabilityResult.reason, "No se pudo cargar el banco de preguntas."));
        }
        if (latestResultResponse.status === "fulfilled") {
          setLatestResult(latestResultResponse.value);
        }
      })
      .finally(() => {
        if (isActive) {
          setIsLoading(false);
        }
      });

    return () => {
      isActive = false;
    };
  }, [currentSubject]);

  const topics = useMemo(() => {
    return Array.from(new Set((availability?.items ?? []).map((item) => item.topic))).sort();
  }, [availability]);

  const activeTopics = useAllTopics ? topics : selectedTopics;
  const minimumQuestionCount = Math.max(activeTopics.length, 1);

  const availabilityByDifficulty = useMemo(() => {
    const totals: Partial<Record<ExamDifficulty, number>> = {};
    for (const item of availability?.items ?? []) {
      if (!activeTopics.includes(item.topic)) continue;
      totals[item.difficulty] = (totals[item.difficulty] ?? 0) + item.questionCount;
    }
    return totals;
  }, [availability, activeTopics]);

  const availabilityByTopicAndDifficulty = useMemo(() => {
    const counts: Record<string, Partial<Record<ExamDifficulty, number>>> = {};
    for (const item of availability?.items ?? []) {
      counts[item.topic] = counts[item.topic] ?? {};
      counts[item.topic][item.difficulty] = item.questionCount;
    }
    return counts;
  }, [availability]);

  const availableQuestions = availabilityByDifficulty[selectedDifficulty] ?? 0;
  const unavailableTopics = activeTopics.filter((topic) => (availabilityByTopicAndDifficulty[topic]?.[selectedDifficulty] ?? 0) < 1);
  const hasBank = (availability?.items.length ?? 0) > 0;
  const canStart =
    activeTopics.length > 0 &&
    unavailableTopics.length === 0 &&
    availableQuestions >= questionCount &&
    questionCount >= minimumQuestionCount &&
    questionCount <= 15;

  useEffect(() => {
    setQuestionCount((current) => {
      if (current < minimumQuestionCount) return minimumQuestionCount;
      if (current > 15) return 15;
      return current;
    });
  }, [minimumQuestionCount]);

  function toggleTopic(topic: string) {
    if (useAllTopics) {
      setUseAllTopics(false);
      setSelectedTopics([topic]);
      return;
    }

    setUseAllTopics(false);
    setSelectedTopics((current) => {
      if (current.includes(topic)) {
        return current.filter((item) => item !== topic);
      }
      return [...current, topic].sort();
    });
  }

  function handleUseAllTopics() {
    setUseAllTopics(true);
    setSelectedTopics(topics);
  }

  async function handleStartExam() {
    if (!activeTopics.length) return;

    setError(null);
    setIsStarting(true);
    try {
      const attempt = await startCustomExam({
        topics: activeTopics,
        difficulty: selectedDifficulty,
        questionCount,
      });
      storeExamAttempt(attempt);
      navigate(`/exams/${attempt.id}`, {
        state: { attempt },
      });
    } catch (startError) {
      setError(getErrorMessage(startError, "No se pudo iniciar el examen."));
    } finally {
      setIsStarting(false);
    }
  }

  return (
    <div className="px-8 py-8">
      <div className="mx-auto max-w-7xl">
        <div className="mb-8 rounded-xl border border-blue-100 bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 px-8 py-8">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
            <div className="max-w-2xl">
              <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-blue-200 bg-white/70 px-3 py-1 text-[12px] font-medium text-blue-700">
                <FileQuestion className="h-3.5 w-3.5" />
                Exámenes
              </div>
              <h1 className="mb-2 text-[28px] font-bold tracking-tight text-[#171717]">Prepara un examen a tu medida</h1>
              <p className="text-[14px] leading-relaxed text-[#525252]">
                Elige todos los temas o combina solo los que quieras. Al finalizar verás tu puntaje, resultados por tema y una revisión de las preguntas incorrectas.
              </p>
            </div>
            <div className="grid grid-cols-3 gap-3">
              <div className="flex h-20 w-20 items-center justify-center rounded-xl bg-white/80 shadow-sm">
                <Lightbulb className="h-7 w-7 text-amber-500" />
              </div>
              <div className="flex h-20 w-20 items-center justify-center rounded-xl bg-white/80 shadow-sm">
                <Calculator className="h-7 w-7 text-blue-500" />
              </div>
              <div className="flex h-20 w-20 items-center justify-center rounded-xl bg-white/80 shadow-sm">
                <BookOpenCheck className="h-7 w-7 text-emerald-500" />
              </div>
            </div>
          </div>
        </div>

        {error ? (
          <div className="mb-6 rounded-lg border border-[#fecaca] bg-[#fef2f2] px-4 py-3 text-[13px] text-[#b91c1c]">
            {error}
          </div>
        ) : null}

        <div className="grid gap-6 lg:grid-cols-[1fr_360px]">
          <section className="rounded-xl border border-[#e5e5e5] bg-white">
            <div className="border-b border-[#f0f0f0] px-6 py-4">
              <div className="flex items-center gap-2">
                <ClipboardList className="h-4 w-4 text-blue-600" />
                <h2 className="text-[16px] font-semibold text-[#171717]">Configura tu examen</h2>
              </div>
            </div>

            <div className="space-y-6 p-6">
              {isLoading ? <p className="text-[13px] text-[#737373]">Cargando banco de preguntas...</p> : null}

              {!isLoading && !hasBank ? (
                <div className="rounded-xl border border-dashed border-[#e5e5e5] bg-[#fafafa] px-6 py-10 text-center">
                  <p className="text-[14px] font-medium text-[#525252]">Aún no hay preguntas disponibles</p>
                  <p className="mt-1 text-[13px] text-[#a3a3a3]">Ejecuta el seed académico para cargar el banco inicial.</p>
                </div>
              ) : null}

              {hasBank ? (
                <>
                  <div>
                    <p className="mb-2 text-[13px] font-semibold text-[#171717]">Temas</p>
                    <button
                      type="button"
                      onClick={handleUseAllTopics}
                      className={`mb-3 flex w-full items-center justify-between rounded-lg border px-4 py-3 text-left transition-all ${
                        useAllTopics ? "border-blue-500 bg-blue-50" : "border-[#e5e5e5] bg-white hover:border-[#d4d4d4]"
                      }`}
                    >
                      <span>
                        <span className="block text-[13px] font-semibold text-[#171717]">Todos los temas</span>
                        <span className="mt-0.5 block text-[12px] text-[#737373]">Mezcla preguntas de todos los temas</span>
                      </span>
                      {useAllTopics ? <Check className="h-4 w-4 text-blue-600" /> : null}
                    </button>
                    <div className="grid gap-2 md:grid-cols-2">
                      {topics.map((topic) => (
                        <button
                          key={topic}
                          type="button"
                          onClick={() => toggleTopic(topic)}
                          className={`flex items-center justify-between rounded-lg border px-3 py-2.5 text-left transition-all ${
                            !useAllTopics && selectedTopics.includes(topic)
                              ? "border-blue-500 bg-blue-50"
                              : "border-[#e5e5e5] bg-white hover:border-[#d4d4d4]"
                          }`}
                        >
                          <span className="text-[13px] font-medium capitalize text-[#171717]">{formatTopic(topic)}</span>
                          {!useAllTopics && selectedTopics.includes(topic) ? <Check className="h-4 w-4 text-blue-600" /> : null}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <p className="mb-2 text-[13px] font-semibold text-[#171717]">Dificultad</p>
                    <div className="grid gap-3 md:grid-cols-3">
                      {(Object.keys(DIFFICULTY_LABELS) as ExamDifficulty[]).map((difficulty) => {
                        const count = availabilityByDifficulty[difficulty] ?? 0;
                        const isSelected = selectedDifficulty === difficulty;
                        return (
                          <button
                            key={difficulty}
                            type="button"
                            onClick={() => setSelectedDifficulty(difficulty)}
                            className={`rounded-lg border p-4 text-left transition-all ${
                              isSelected ? "border-blue-500 bg-blue-50 shadow-sm" : "border-[#e5e5e5] bg-white hover:border-[#d4d4d4]"
                            }`}
                          >
                            <span className="text-[13px] font-semibold text-[#171717]">{DIFFICULTY_LABELS[difficulty]}</span>
                            <span className="mt-1 block text-[12px] leading-5 text-[#737373]">{DIFFICULTY_HELP[difficulty]}</span>
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  <div>
                    <div className="mb-2 flex items-center justify-between">
                      <label htmlFor="question-count" className="text-[13px] font-semibold text-[#171717]">
                        Cantidad de preguntas
                      </label>
                    </div>
                    <input
                      id="question-count"
                      type="number"
                      min={minimumQuestionCount}
                      max={15}
                      value={questionCount}
                      onChange={(event) => setQuestionCount(Number(event.target.value))}
                      className="w-full rounded-lg border border-[#d4d4d4] bg-white px-3 py-2.5 text-[13px] text-[#171717] outline-none transition-colors focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                    />
                    {questionCount === minimumQuestionCount ? (
                      <p className="mt-2 text-[12px] leading-5 text-[#737373]">
                        Mínimo {minimumQuestionCount} {minimumQuestionCount === 1 ? "pregunta" : "preguntas"} para incluir al menos una por tema seleccionado.
                      </p>
                    ) : null}
                  </div>
                </>
              ) : null}
            </div>
          </section>

          <aside className="rounded-xl border border-[#e5e5e5] bg-white p-6">
            <p className="text-[12px] font-semibold uppercase tracking-[0.14em] text-[#a3a3a3]">Resumen</p>
            <div className="mt-5 space-y-4">
              <div>
                <p className="text-[12px] text-[#737373]">Materia</p>
                <p className="mt-1 text-[14px] font-semibold text-[#171717]">{availability?.subject ? (SUBJECT_LABELS[availability.subject] ?? availability.subject) : "..."}</p>
              </div>
              <div>
                <p className="text-[12px] text-[#737373]">Tema</p>
                <p className="mt-1 text-[14px] font-semibold capitalize text-[#171717]">
                  {useAllTopics ? "Todos los temas" : activeTopics.length ? activeTopics.map(formatTopic).join(", ") : "Sin seleccionar"}
                </p>
              </div>
              <div>
                <p className="text-[12px] text-[#737373]">Dificultad</p>
                <p className="mt-1 text-[14px] font-semibold text-[#171717]">{DIFFICULTY_LABELS[selectedDifficulty]}</p>
              </div>
              <div className="rounded-lg border border-[#f0f0f0] bg-[#fafafa] p-4">
                <p className="text-[28px] font-bold text-[#171717]">{questionCount}</p>
                <p className="text-[12px] text-[#737373]">preguntas que tendrá el examen</p>
              </div>
              {unavailableTopics.length ? (
                <div className="rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-[12px] leading-5 text-amber-800">
                  Sin preguntas en {DIFFICULTY_LABELS[selectedDifficulty].toLowerCase()} para: {unavailableTopics.map(formatTopic).join(", ")}.
                </div>
              ) : null}
            </div>

            <button
              onClick={() => void handleStartExam()}
              disabled={!canStart || isStarting}
              className="mt-6 flex w-full items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 px-4 py-3 text-[14px] font-semibold text-white shadow-sm transition-all hover:from-blue-700 hover:to-indigo-700 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {isStarting ? "Iniciando..." : "Comenzar examen"}
              <ArrowRight className="h-4 w-4" />
            </button>

            {!canStart && hasBank ? (
              <p className="mt-3 text-[12px] leading-5 text-[#b45309]">
                Ajusta la cantidad, los temas o la dificultad para iniciar el examen. Debe haber al menos una pregunta por cada tema seleccionado.
              </p>
            ) : null}
          </aside>
        </div>

        <section className="mt-6 rounded-xl border border-[#e5e5e5] bg-white p-6">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div className="min-w-0">
              <div className="flex items-center gap-2">
                <History className="h-4 w-4 text-black-600" />
                <h2 className="text-[16px] font-semibold text-[#171717]">Último intento</h2>
              </div>
              {latestResult && !isLatestOpen ? (
                <div className="mt-2">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="text-[13px] font-semibold text-[#171717]">{Math.round(latestResult.result.scoreGlobal)}%</span>
                    {latestResult.difficulty ? (
                      <span className="rounded-full border border-blue-100 bg-blue-50 px-2 py-0.5 text-[11px] font-medium text-blue-700">
                        {DIFFICULTY_LABELS[latestResult.difficulty]}
                      </span>
                    ) : null}
                    {latestResult.topics.map((topic) => (
                      <span
                        key={topic}
                        className="rounded-full border border-[#e5e5e5] bg-[#fafafa] px-2 py-0.5 text-[11px] font-medium capitalize text-[#525252]"
                      >
                        {formatTopic(topic)}
                      </span>
                    ))}
                    <span className="text-[12px] text-[#737373]">
                      {latestResult.result.answersFeedback.length} preguntas
                    </span>
                  </div>
                </div>
              ) : !latestResult ? (
                <p className="mt-1 text-[13px] text-[#737373]">Completa un examen para mostrar el resultado</p>
              ) : null}
            </div>
            <button
              type="button"
              onClick={() => setIsLatestOpen((value) => !value)}
              disabled={!latestResult}
              className="inline-flex items-center justify-center gap-2 rounded-lg border border-[#d4d4d4] bg-white px-4 py-2.5 text-[13px] font-medium text-[#171717] transition-colors hover:bg-[#fafafa] disabled:cursor-not-allowed disabled:opacity-50"
            >
              {isLatestOpen ? "Ocultar resultado" : "Ver resultado"}
              {isLatestOpen ? <X className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
            </button>
          </div>

          {latestResult && isLatestOpen ? (
            <div className="mt-6 border-t border-[#f0f0f0] pt-6">
              <div className="mb-5 grid gap-4 md:grid-cols-3">
                <div className="rounded-lg border border-[#f0f0f0] bg-[#fafafa] p-4">
                  <p className="text-[11px] uppercase tracking-[0.14em] text-[#a3a3a3]">Puntaje</p>
                  <p className="mt-2 text-[28px] font-bold text-[#171717]">{Math.round(latestResult.result.scoreGlobal)}%</p>
                </div>
                <div className="rounded-lg border border-[#f0f0f0] bg-[#fafafa] p-4">
                  <p className="text-[11px] uppercase tracking-[0.14em] text-[#a3a3a3]">Temas</p>
                  <p className="mt-2 text-[13px] capitalize text-[#525252]">{latestResult.topics.map(formatTopic).join(", ")}</p>
                </div>
                <div className="rounded-lg border border-[#f0f0f0] bg-[#fafafa] p-4">
                  <p className="text-[11px] uppercase tracking-[0.14em] text-[#a3a3a3]">Preguntas</p>
                  <p className="mt-2 text-[28px] font-bold text-[#171717]">{latestResult.result.answersFeedback.length}</p>
                </div>
              </div>

              <div className="grid gap-4 lg:grid-cols-2">
                {sortByMastery(Object.entries(latestResult.result.topicBreakdown)).map(([topic, result]) => (
                  <div key={topic} className="rounded-lg border border-[#e5e5e5] bg-[#fafafa] p-4">
                    <div className="mb-2 flex items-center justify-between">
                      <p className="text-[13px] font-semibold capitalize text-[#171717]">{formatTopic(topic)}</p>
                      <div className="flex items-center gap-2">
                        <span className="text-[12px] text-[#737373]">{Math.round(result.scorePercentage)}%</span>
                        <span className={`rounded-full border px-2 py-0.5 text-[10px] font-medium ${MASTERY_BADGE[result.mastery]}`}>
                          {MASTERY_LABELS[result.mastery]}
                        </span>
                      </div>
                    </div>
                    <div className="h-2 overflow-hidden rounded-full bg-[#e5e5e5]">
                      <div className={`h-full rounded-full ${MASTERY_BAR[result.mastery]}`} style={{ width: `${result.scorePercentage}%` }} />
                    </div>
                    <p className="mt-2 text-[12px] text-[#737373]">
                      {result.correctAnswers}/{result.totalQuestions} correctas
                    </p>
                  </div>
                ))}
              </div>

              <ExamRecommendationPanels
                positiveRecommendations={latestResult.result.positiveRecommendations}
                improvementRecommendations={latestResult.result.improvementRecommendations}
                compact
              />

              {latestResult.result.answersFeedback.length ? (
                <div className="mt-5 space-y-3">
                  <p className="text-[13px] font-semibold text-[#171717]">Revisión de todas las preguntas</p>
                  {latestResult.result.answersFeedback.map((item, index) => (
                    <div
                      key={item.questionId}
                      className={`rounded-lg border p-4 ${
                        item.isCorrect ? "border-emerald-100 bg-emerald-50/30" : "border-red-100 bg-red-50/30"
                      }`}
                    >
                      <div className="mb-2 flex items-start justify-between gap-3">
                        <div className="flex flex-wrap gap-2">
                          <span className="rounded-full bg-white px-2 py-0.5 text-[11px] font-medium capitalize text-[#525252]">{formatTopic(item.topic)}</span>
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
                <p className="mt-5 rounded-lg border border-emerald-100 bg-emerald-50 px-4 py-3 text-[13px] text-emerald-700">
                  No hay preguntas para revisar en tu último intento.
                </p>
              )}
            </div>
          ) : null}
        </section>
      </div>
    </div>
  );
}
