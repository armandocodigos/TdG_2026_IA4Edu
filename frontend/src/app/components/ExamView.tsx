import { Check, ChevronLeft, ChevronRight, Clock, X } from "lucide-react";
import { useCallback, useEffect, useRef, useState } from "react";
import { MathText } from "@/app/components/ui/MathText";

interface Question {
  id: string;
  question: string;
  options: string[];
  meta?: string[];
}

interface ExamViewProps {
  title: string;
  subtitle?: string;
  contextTags?: string[];
  duration?: string;
  questions: Question[];
  answers: Record<string, string>;
  onAnswer: (questionId: string, answer: string) => Promise<void> | void;
  onComplete: () => Promise<void> | void;
  onExit: () => Promise<void> | void;
  submitLabel?: string;
  submittingTitle?: string;
  submittingDescription?: string;
  isSubmitting?: boolean;
  savingQuestionId?: string | null;
}

export function ExamView({
  title,
  subtitle,
  contextTags = [],
  duration,
  questions,
  answers,
  onAnswer,
  onComplete,
  onExit,
  submitLabel = "Enviar",
  submittingTitle = "Finalizando",
  submittingDescription = "Estamos procesando tus respuestas y preparando tu resultado.",
  isSubmitting = false,
  savingQuestionId = null,
}: ExamViewProps) {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const autoAdvanceTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const [submitProgress, setSubmitProgress] = useState(0);
  const [submitOverlayVisible, setSubmitOverlayVisible] = useState(false);

  useEffect(() => {
    if (isSubmitting) {
      setSubmitProgress(0);
      setSubmitOverlayVisible(true);
      const interval = setInterval(() => {
        setSubmitProgress((prev) => {
          if (prev < 45) return Math.min(prev + 3, 45);
          if (prev < 82) return prev + 0.28;
          return prev;
        });
      }, 200);
      return () => clearInterval(interval);
    } else {
      setSubmitProgress(100);
      const timeout = setTimeout(() => setSubmitOverlayVisible(false), 500);
      return () => clearTimeout(timeout);
    }
  }, [isSubmitting]);

  const totalQuestions = questions.length;
  const progress = totalQuestions ? ((currentQuestion + 1) / totalQuestions) * 100 : 0;
  const answeredCount = Object.keys(answers).length;
  const question = questions[currentQuestion];
  const currentAnswer = question ? answers[question.id] : undefined;

  const advanceToNext = useCallback(() => {
    if (currentQuestion < totalQuestions - 1) {
      setIsTransitioning(true);
      setTimeout(() => {
        setCurrentQuestion((v) => v + 1);
        setIsTransitioning(false);
      }, 250);
    }
  }, [currentQuestion, totalQuestions]);

  async function handleOptionClick(questionId: string, option: string) {
    if (autoAdvanceTimer.current) {
      clearTimeout(autoAdvanceTimer.current);
    }

    await onAnswer(questionId, option);

    if (currentQuestion < totalQuestions - 1) {
      autoAdvanceTimer.current = setTimeout(() => {
        advanceToNext();
      }, 600);
    }
  }

  if (!question) {
    return (
      <div className="flex h-full flex-col items-center justify-center bg-[#fafafa] p-8">
        <div className="w-full max-w-md rounded-xl border border-[#e5e5e5] bg-white p-8 text-center">
          <h2 className="mb-2 text-xl font-semibold text-[#171717]">No hay preguntas disponibles</h2>
          <p className="mb-6 text-[13px] text-[#737373]">
            Intenta iniciar un nuevo examen desde la página principal.
          </p>
          <button
            onClick={() => void onExit()}
            className="w-full rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 px-4 py-2.5 text-[13px] font-medium text-white transition-all hover:from-blue-700 hover:to-indigo-700"
          >
            Volver al inicio
          </button>
        </div>
      </div>
    );
  }

  async function handleSubmit() {
    await onComplete();
  }

  return (
    <div className="flex h-full flex-col bg-gray-50">
      {submitOverlayVisible ? (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-white/80 px-6 backdrop-blur-sm">
          <div className="w-full max-w-sm rounded-xl border border-blue-100 bg-white p-6 text-center shadow-xl shadow-blue-100/70">
            <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-blue-50">
              <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-100 border-t-blue-600" />
            </div>
            <p className="text-[15px] font-semibold text-[#171717]">{submittingTitle}</p>
            {submittingDescription ? (
              <p className="mt-2 text-[13px] leading-6 text-[#737373]">{submittingDescription}</p>
            ) : null}
            <div className="mt-5">
              <div className="mb-1.5 flex items-center justify-between text-[12px] text-[#737373]">
                <span>Procesando...</span>
                <span className="font-medium tabular-nums">{Math.round(submitProgress)}%</span>
              </div>
              <div className="h-2 w-full overflow-hidden rounded-full bg-blue-100">
                <div
                  className="h-full rounded-full bg-blue-600 transition-all duration-200 ease-out"
                  style={{ width: `${submitProgress}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      ) : null}

      <header className="sticky top-0 z-20 border-b border-gray-200 bg-white/90 backdrop-blur-md">
        <div className="absolute bottom-0 left-0 h-1 w-full bg-gray-100 translate-y-full">
          <div
            className="h-full bg-gradient-to-r from-blue-500 to-indigo-600 transition-all duration-500 ease-out"
            style={{ width: `${progress}%` }}
          />
        </div>

        <div className="mx-auto flex max-w-5xl items-center justify-between gap-6 px-6 py-4">
          <div className="flex min-w-0 items-center gap-5">
            <button
              onClick={() => void onExit()}
              className="group flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full border border-gray-200 bg-white shadow-sm transition-all hover:border-red-200 hover:bg-red-50"
              title="Salir del examen"
            >
              <X className="h-4 w-4 text-gray-500 transition-colors group-hover:text-red-600" />
            </button>

            <div className="hidden min-w-0 sm:block">
              <div className="flex items-center gap-2">
                <h1 className="truncate text-[17px] font-bold tracking-tight text-gray-900">{title}</h1>
              </div>
              {subtitle ? (
                <p className="mt-1 max-w-lg truncate text-[13px] font-medium text-gray-500">
                  {subtitle}
                </p>
              ) : null}
              {contextTags.length ? (
                <div className="mt-2 flex max-w-xl flex-wrap gap-1.5">
                  {contextTags.map((tag) => (
                    <span
                      key={tag}
                      className="rounded-full border border-blue-100 bg-blue-50 px-2.5 py-1 text-[11px] font-medium capitalize text-blue-700"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              ) : null}
            </div>
          </div>

          <div className="flex items-center gap-5">
            {duration ? (
              <div className="flex items-center gap-2 rounded-full border border-gray-200 bg-white px-3 py-1.5 text-[13px] font-medium text-gray-600 shadow-sm">
                <Clock className="h-4 w-4 text-gray-400" />
                <span>{duration}</span>
              </div>
            ) : null}

            <div className="flex items-center gap-3">
              <div className="flex flex-col items-end">
                <span className="text-[13px] font-bold text-gray-900">
                  Pregunta {currentQuestion + 1} de {totalQuestions}
                </span>
                <span className="text-[11px] font-bold uppercase tracking-wider text-gray-500">
                  {answeredCount} respondidas
                </span>
              </div>
              
              <div className="flex h-11 w-11 flex-shrink-0 items-center justify-center rounded-full bg-white ring-1 ring-gray-200 shadow-sm">
                <span className="text-[12px] font-bold text-blue-600">
                  {Math.round(progress)}%
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="flex-1 overflow-auto p-8">
        <div className="mx-auto max-w-4xl">
          <div
            className={`rounded-xl border border-[#e5e5e5] bg-white p-8 transition-opacity duration-250 ${
              isTransitioning ? "opacity-0" : "opacity-100"
            }`}
          >
            <MathText content={question.question} className="mb-3 text-[17px] font-medium leading-relaxed text-[#171717]" />

            {question.meta?.length ? (
              <div className="mb-8 flex flex-wrap gap-2">
                {question.meta.map((item) => (
                  <span
                    key={item}
                    className="rounded-full border border-blue-100 bg-blue-50 px-3 py-1 text-[11px] font-medium capitalize text-blue-700"
                  >
                    {item.replace(/_/g, ' ')}
                  </span>
                ))}
              </div>
            ) : null}

            <div className="space-y-3">
              {question.options.map((option, index) => {
                const letter = String.fromCharCode(65 + index); 
                return (
                  <button
                    key={option}
                    onClick={() => void handleOptionClick(question.id, option)}
                    disabled={isSubmitting || savingQuestionId === question.id}
                    className={`w-full rounded-xl border px-5 py-4 text-left transition-all duration-200 ${
                      currentAnswer === option
                        ? "border-blue-500 bg-blue-50 shadow-sm shadow-blue-100"
                        : "border-[#e5e5e5] bg-white hover:border-[#d4d4d4] hover:bg-[#fafafa] hover:shadow-sm"
                    } disabled:cursor-not-allowed disabled:opacity-70`}
                  >
                    <div className="flex items-center gap-3">
                      <div
                        className={`flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-full border-2 text-[12px] font-semibold transition-colors ${
                          currentAnswer === option
                            ? "border-blue-500 bg-blue-500 text-white"
                            : "border-[#d4d4d4] text-[#737373]"
                        }`}
                      >
                        {currentAnswer === option ? <Check className="h-3.5 w-3.5" /> : letter}
                      </div>
                      <MathText content={option} className="text-[14px] text-[#171717]" />
                    </div>
                  </button>
                );
              })}
            </div>

            {savingQuestionId === question.id ? (
              <p className="mt-4 text-[12px] text-[#737373]">Guardando respuesta...</p>
            ) : null}
          </div>
        </div>
      </div>

      <div className="border-t border-[#e5e5e5] bg-white">
        <div className="mx-auto max-w-4xl px-8 py-4">
          <div className="flex items-center justify-between gap-4">
            <button
              onClick={() => {
                if (autoAdvanceTimer.current) clearTimeout(autoAdvanceTimer.current);
                setCurrentQuestion((value) => value - 1);
              }}
              disabled={currentQuestion === 0}
              className="flex items-center gap-2 rounded-lg px-4 py-2 text-[13px] font-medium text-[#737373] transition-colors hover:bg-[#f5f5f5] hover:text-[#171717] disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:bg-transparent"
            >
              <ChevronLeft className="h-4 w-4" />
              Anterior
            </button>

            <div className="flex gap-1.5">
              {questions.map((item, index) => (
                <button
                  key={item.id}
                  onClick={() => {
                    if (autoAdvanceTimer.current) clearTimeout(autoAdvanceTimer.current);
                    setCurrentQuestion(index);
                  }}
                  className={`h-8 w-8 rounded-lg text-[12px] font-medium transition-all duration-200 ${
                    index === currentQuestion
                      ? "bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-sm"
                      : answers[item.id]
                        ? "border border-blue-200 bg-blue-50 text-blue-600"
                        : "bg-[#f5f5f5] text-[#737373] hover:bg-[#e5e5e5]"
                  }`}
                >
                  {index + 1}
                </button>
              ))}
            </div>

            {currentQuestion === totalQuestions - 1 ? (
              <div className="flex items-center gap-3">
                <button
                  onClick={() => void handleSubmit()}
                  disabled={isSubmitting || answeredCount < totalQuestions}
                  className="flex items-center gap-2 rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 px-5 py-2 text-[13px] font-medium text-white shadow-sm transition-all hover:from-blue-700 hover:to-indigo-700 hover:shadow-md disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {isSubmitting ? "Finalizando..." : submitLabel}
                  <Check className="h-4 w-4" />
                </button>
              </div>
            ) : (
              <button
                onClick={() => {
                  if (autoAdvanceTimer.current) clearTimeout(autoAdvanceTimer.current);
                  advanceToNext();
                }}
                className="flex items-center gap-2 rounded-lg bg-[#171717] px-5 py-2 text-[13px] font-medium text-white transition-colors hover:bg-[#404040]"
              >
                Siguiente
                <ChevronRight className="h-4 w-4" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
