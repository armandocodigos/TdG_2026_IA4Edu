import { useEffect, useState } from "react";
import { useNavigate } from "react-router";
import {
  ArrowRight,
  BookOpen,
  CheckCircle2,
  Eye,
  FileQuestion,
  History,
  Sparkles,
  Target,
  TrendingUp,
  X,
} from "lucide-react";

import { MathText } from "@/app/components/ui/MathText";
import { useAuth } from "@/app/features/auth/AuthProvider";
import { DiagnosticRecommendationPanels } from "@/app/features/diagnostic/components/DiagnosticRecommendationPanels";
import { fetchDiagnosticProfile, fetchLatestDiagnosticReview, startDiagnostic } from "@/app/features/diagnostic/api";
import { storeDiagnosticAttempt } from "@/app/features/diagnostic/storage";
import type { DiagnosticAttemptReview, DiagnosticBreakdown, DiagnosticProfile } from "@/app/features/diagnostic/types";
import { getErrorMessage } from "@/app/shared/api/errors";
import type { MasteryLevel } from "@/app/shared/types/domain";

const MASTERY_CONFIG: Record<MasteryLevel, { label: string; color: string; bg: string; border: string; bar: string }> = {
  high: { label: "Dominado", color: "text-emerald-700", bg: "bg-emerald-50", border: "border-emerald-200", bar: "bg-emerald-500" },
  medium: { label: "En progreso", color: "text-amber-700", bg: "bg-amber-50", border: "border-amber-200", bar: "bg-amber-400" },
  low: { label: "Por reforzar", color: "text-red-600", bg: "bg-red-50", border: "border-red-200", bar: "bg-red-400" },
};

function getMasteryStyle(mastery: MasteryLevel) {
  return MASTERY_CONFIG[mastery];
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

export function DiagnosticOverviewPage() {
  const [profile, setProfile] = useState<DiagnosticProfile | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [latestReview, setLatestReview] = useState<DiagnosticAttemptReview | null>(null);
  const [isReviewOpen, setIsReviewOpen] = useState(false);
  const [isStarting, setIsStarting] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const navigate = useNavigate();
  const { user } = useAuth();
  const currentSubject = user?.subject;
  const topicEntries = sortByMastery(Object.entries(profile?.topicResults ?? {}) as Array<[string, DiagnosticBreakdown]>);
  const topicValues = topicEntries.map(([, value]) => value);
  const averageScore = topicValues.length
    ? topicValues.reduce((sum, result) => sum + result.scorePercentage, 0) / topicValues.length
    : 0;
  const globalScore = latestReview?.scoreGlobal ?? averageScore;
  const circumference = 2 * Math.PI * 54;
  const dashOffset = circumference - (globalScore / 100) * circumference;
  const scoreStrokeColor = globalScore >= 75 ? "#10b981" : globalScore >= 40 ? "#f59e0b" : "#ef4444";

  function getScoreLabel(score: number) {
    if (score >= 90) return "¡Excelente!";
    if (score >= 75) return "¡Muy bien!";
    if (score >= 60) return "Buen trabajo";
    if (score >= 40) return "Puedes mejorar";
    return "Sigue practicando";
  }

  useEffect(() => {
    if (!currentSubject) return;
    let isActive = true;

    setIsLoading(true);
    setProfile(null);
    setLatestReview(null);
    setIsReviewOpen(false);
    setError(null);

    Promise.allSettled([fetchDiagnosticProfile(), fetchLatestDiagnosticReview()])
      .then((payload) => {
        if (!isActive) return;

        const [profileResult, reviewResult] = payload;
        if (profileResult.status === "fulfilled") {
          setProfile(profileResult.value);
        } else {
          setError(getErrorMessage(profileResult.reason));
        }

        if (reviewResult.status === "fulfilled") {
          setLatestReview(reviewResult.value);
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

  async function handleStartDiagnostic() {
    setError(null);
    setIsStarting(true);

    try {
      const attempt = await startDiagnostic();
      storeDiagnosticAttempt(attempt);
      navigate(`/diagnostic/${attempt.id}`, {
        state: { attempt },
      });
    } catch (startError) {
      setError(getErrorMessage(startError, "No se pudo iniciar el diagnóstico."));
    } finally {
      setIsStarting(false);
    }
  }

  return (
    <div className="px-8 py-8">
      <div className="mx-auto max-w-7xl">
        {/* ── Hero section ── */}
        <div className="relative mb-8 overflow-hidden rounded-2xl border border-blue-100 bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
          {/* Decorative circles */}
          <div className="pointer-events-none absolute -right-8 -top-8 h-40 w-40 rounded-full bg-blue-200/20" />
          <div className="pointer-events-none absolute -bottom-6 right-24 h-28 w-28 rounded-full bg-indigo-200/20" />

          <div className="relative flex items-center justify-between px-8 py-8">
            <div className="max-w-xl">
              <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-blue-200 bg-white/70 px-3 py-1 text-[12px] font-medium text-blue-700 backdrop-blur-sm">
                <FileQuestion className="h-3.5 w-3.5" />
                10 preguntas
              </div>
              <h1 className="mb-2 text-[28px] font-bold tracking-tight text-[#171717]">Examen de Diagnóstico</h1>
              <p className="mb-6 max-w-lg text-[14px] leading-relaxed text-[#525252]">
                Evalúa tu nivel de conocimiento antes de comenzar a estudiar. El resultado te ayudará a crear un plan de aprendizaje personalizado.
              </p>
              <button
                onClick={() => void handleStartDiagnostic()}
                disabled={isStarting}
                className="group flex items-center gap-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-3 text-[14px] font-semibold text-white shadow-lg shadow-blue-500/25 transition-all hover:from-blue-700 hover:to-indigo-700 hover:shadow-xl hover:shadow-blue-500/30 disabled:cursor-not-allowed disabled:opacity-70"
              >
                {isStarting ? "Iniciando..." : "Comenzar diagnóstico"}
                <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
              </button>
            </div>

            {/* Decorative illustration */}
            <div className="hidden lg:flex lg:items-center lg:gap-4">
              <div className="grid grid-cols-2 gap-3">
                <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-white/80 shadow-sm backdrop-blur-sm">
                  <Target className="h-8 w-8 text-blue-500" />
                </div>
                <div className="mt-4 flex h-20 w-20 items-center justify-center rounded-2xl bg-white/80 shadow-sm backdrop-blur-sm">
                  <TrendingUp className="h-8 w-8 text-purple-500" />
                </div>
                <div className="-mt-4 flex h-20 w-20 items-center justify-center rounded-2xl bg-white/80 shadow-sm backdrop-blur-sm">
                  <Sparkles className="h-8 w-8 text-amber-500" />
                </div>
                <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-white/80 shadow-sm backdrop-blur-sm">
                  <CheckCircle2 className="h-8 w-8 text-emerald-500" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {error ? (
          <div className="mb-6 rounded-lg border border-[#fecaca] bg-[#fef2f2] px-4 py-3 text-[13px] text-[#b91c1c]">
            {error}
          </div>
        ) : null}

        {/* ── Results section (full width, horizontal) ── */}
        <div className="rounded-xl border border-[#e5e5e5] bg-white">
          <div className="border-b border-[#f0f0f0] px-6 py-4">
            <div className="flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-blue-600" />
              <h3 className="text-[16px] font-semibold text-[#171717]">Tu último resultado</h3>
            </div>
          </div>

          <div className="p-6">
            {isLoading ? <p className="text-[13px] text-[#737373]">Cargando perfil...</p> : null}

            {!isLoading && !profile ? (
              <div className="flex flex-col items-center rounded-xl border border-dashed border-[#e5e5e5] bg-[#fafafa] px-6 py-12 text-center">
                <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-[#f0f0f0]">
                  <BookOpen className="h-7 w-7 text-[#a3a3a3]" />
                </div>
                <p className="text-[14px] font-medium text-[#525252]">Aún no has realizado un diagnóstico</p>
                <p className="mt-1.5 max-w-sm text-[13px] leading-relaxed text-[#a3a3a3]">
                  Completa tu primer examen para ver un análisis detallado de tus fortalezas y áreas de mejora.
                </p>
              </div>
            ) : null}

            {profile ? (
              <>
                <div className="grid gap-8 lg:grid-cols-[auto_minmax(0,1fr)]">
                  <div className="flex flex-col items-center justify-center lg:border-r lg:border-[#f0f0f0] lg:pr-8">
                    <div className="relative flex h-32 w-32 items-center justify-center">
                      <svg className="h-32 w-32 -rotate-90" viewBox="0 0 128 128">
                        <circle cx="64" cy="64" r="54" fill="none" stroke="#f0f0f0" strokeWidth="8" />
                        <circle
                          cx="64"
                          cy="64"
                          r="54"
                          fill="none"
                          stroke={scoreStrokeColor}
                          strokeWidth="8"
                          strokeDasharray={`${circumference}`}
                          strokeDashoffset={dashOffset}
                          strokeLinecap="round"
                          className="transition-all duration-1000 ease-out"
                        />
                      </svg>
                      <div className="absolute text-center">
                        <span className="block text-[28px] font-bold text-[#171717]">{Math.round(globalScore)}%</span>
                      </div>
                    </div>
                    <p className="mt-2 text-[14px] font-medium text-[#171717]">{getScoreLabel(globalScore)}</p>
                    <p className="mt-0.5 text-[12px] text-[#737373]">Puntaje global</p>
                  </div>

                  <div>
                    <p className="mb-3 text-[13px] font-semibold text-[#171717]">Resultados por tema</p>
                    <div className="grid gap-3 md:grid-cols-2">
                      {topicEntries.map(([topic, result]) => {
                        const style = getMasteryStyle(result.mastery);
                        return (
                          <div key={topic} className="rounded-lg border border-[#f0f0f0] bg-[#fafafa] p-3">
                            <div className="mb-2 flex min-h-6 items-start justify-between gap-2">
                              <span className="min-w-0 text-[13px] font-medium capitalize leading-5 text-[#171717]">{topic.replace(/_/g, " ")}</span>
                              <span className={`flex-shrink-0 rounded-full border px-2 py-0.5 text-[10px] font-medium ${style.color} ${style.bg} ${style.border}`}>
                                {style.label}
                              </span>
                            </div>
                            <div className="h-2 w-full overflow-hidden rounded-full bg-[#e5e5e5]">
                              <div
                                className={`h-full rounded-full transition-all duration-700 ${style.bar}`}
                                style={{ width: `${result.scorePercentage}%` }}
                              />
                            </div>
                            <p className="mt-1.5 text-[11px] text-[#737373]">
                              {result.correctAnswers}/{result.totalQuestions} correctas · {Math.round(result.scorePercentage)}%
                            </p>
                          </div>
                        );
                      })}
                    </div>
                  </div>

                </div>

                <div className="mt-6 grid gap-4 border-t border-[#f0f0f0] pt-5 md:grid-cols-2">
                  <div className="rounded-lg border border-emerald-100 bg-emerald-50/50 p-4">
                      <div className="mb-2 flex items-center gap-1.5">
                        <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600" />
                        <p className="text-[12px] font-semibold text-emerald-800">Fortalezas</p>
                      </div>
                      <div className="flex flex-wrap gap-1">
                        {profile.strengths.length > 0 ? (
                          profile.strengths.map((s) => (
                            <span key={s} className="rounded-md bg-emerald-100 px-2 py-0.5 text-[11px] font-medium capitalize text-emerald-700">
                              {s.replace(/_/g, " ")}
                            </span>
                          ))
                        ) : (
                          <p className="text-[11px] text-emerald-600/60">—</p>
                        )}
                      </div>
                  </div>

                  <div className="rounded-lg border border-amber-100 bg-amber-50/50 p-4">
                      <div className="mb-2 flex items-center gap-1.5">
                        <TrendingUp className="h-3.5 w-3.5 text-amber-600" />
                        <p className="text-[12px] font-semibold text-amber-800">Por mejorar</p>
                      </div>
                      <div className="flex flex-wrap gap-1">
                        {(profile.weaknesses?.length ?? 0) > 0 ? (
                          (profile.weaknesses ?? []).map((w) => (
                            <span key={w} className="rounded-md bg-amber-100 px-2 py-0.5 text-[11px] font-medium capitalize text-amber-700">
                              {w.replace(/_/g, " ")}
                            </span>
                          ))
                        ) : (
                          <p className="text-[11px] text-amber-600/60">¡Sin áreas débiles!</p>
                        )}
                      </div>
                  </div>
                </div>

                <div className="mt-6 border-t border-[#f0f0f0] pt-5">
                  <DiagnosticRecommendationPanels
                    positiveRecommendations={profile.positiveRecommendations}
                    improvementRecommendations={profile.improvementRecommendations}
                    compact
                  />
                </div>
              </>
            ) : null}

          </div>
        </div>

        {latestReview ? (
          <section className="mt-6 rounded-xl border border-[#e5e5e5] bg-white p-6">
            <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
              <div className="min-w-0">
                <div className="flex items-center gap-2">
                  <History className="h-4 w-4 text-black-600" />
                  <h2 className="text-[16px] font-semibold text-[#171717]">Último intento</h2>
                </div>
                {!isReviewOpen ? (
                  <div className="mt-2">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="text-[13px] font-semibold text-[#171717]">{Math.round(latestReview.scoreGlobal)}%</span>
                      <span className="rounded-full border border-blue-100 bg-blue-50 px-2 py-0.5 text-[11px] font-medium capitalize text-blue-700">
                        {latestReview.subject.replace(/_/g, " ")}
                      </span>
                      <span className="text-[12px] text-[#737373]">
                        {latestReview.answersFeedback.length} preguntas
                      </span>
                    </div>
                  </div>
                ) : null}
              </div>
              <button
                type="button"
                onClick={() => setIsReviewOpen((value) => !value)}
                className="inline-flex items-center justify-center gap-2 rounded-lg border border-[#d4d4d4] bg-white px-4 py-2.5 text-[13px] font-medium text-[#171717] transition-colors hover:bg-[#fafafa]"
              >
                {isReviewOpen ? "Ocultar resultado" : "Ver resultado"}
                {isReviewOpen ? <X className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>

            {isReviewOpen ? (
              <div className="mt-6 border-t border-[#f0f0f0] pt-6">
                {latestReview.answersFeedback.length ? (
                  <div className="space-y-3">
                    <p className="text-[13px] font-semibold text-[#171717]">Revisión de todas las preguntas</p>
                    {latestReview.answersFeedback.map((item, index) => (
                      <div
                        key={item.questionId}
                        className={`rounded-lg border p-4 ${
                          item.isCorrect ? "border-emerald-100 bg-emerald-50/30" : "border-red-100 bg-red-50/30"
                        }`}
                      >
                        <div className="mb-2 flex items-start justify-between gap-3">
                          <span className="rounded-full bg-white px-2 py-0.5 text-[11px] font-medium capitalize text-[#525252]">
                            {item.topic.replace(/_/g, " ")}
                          </span>
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
                    No hay preguntas para revisar en tu último intento.
                  </p>
                )}
              </div>
            ) : null}
          </section>
        ) : null}
      </div>
    </div>
  );
}
