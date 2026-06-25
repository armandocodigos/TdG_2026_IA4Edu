import { useState } from "react";
import { Check, ChevronLeft, ChevronRight, X } from "lucide-react";

import { Badge } from "@/app/components/ui/badge";
import { Button } from "@/app/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/app/components/ui/card";

export interface AssessmentQuestion {
  id: string;
  prompt: string;
  options: string[];
  tags: string[];
}

interface AssessmentRunnerProps {
  title: string;
  subtitle: string;
  questions: AssessmentQuestion[];
  answers: Record<string, string>;
  onAnswer: (questionId: string, answer: string) => Promise<void>;
  onSubmit: () => Promise<void>;
  onExit: () => void;
  submitLabel: string;
  isSubmitting: boolean;
  savingQuestionId: string | null;
}

export function AssessmentRunner({
  title,
  subtitle,
  questions,
  answers,
  onAnswer,
  onSubmit,
  onExit,
  submitLabel,
  isSubmitting,
  savingQuestionId,
}: AssessmentRunnerProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const question = questions[currentIndex];
  const totalQuestions = questions.length;
  const answeredCount = Object.keys(answers).length;
  const progress = ((currentIndex + 1) / totalQuestions) * 100;
  const selectedAnswer = answers[question.id];

  return (
    <div className="min-h-full bg-[#f7f4ec]">
      <div className="mx-auto flex max-w-5xl flex-col gap-6 px-6 py-8">
        <div className="flex items-start justify-between gap-4">
          <div>
            <Button variant="ghost" className="mb-3 px-0 text-[#6f6556] hover:bg-transparent" onClick={onExit}>
              <X className="h-4 w-4" />
              Exit
            </Button>
            <h1 className="text-3xl font-semibold text-[#1c180f]">{title}</h1>
            <p className="mt-2 max-w-2xl text-sm text-[#6f6556]">{subtitle}</p>
          </div>
          <Card className="min-w-56 border-[#ddd5c7] bg-white shadow-sm">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm text-[#1c180f]">Progress</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center justify-between text-sm text-[#6f6556]">
                <span>
                  Question {currentIndex + 1} of {totalQuestions}
                </span>
                <span>{answeredCount} answered</span>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-[#ede4d7]">
                <div className="h-full rounded-full bg-[#d26d31] transition-all" style={{ width: `${progress}%` }} />
              </div>
            </CardContent>
          </Card>
        </div>

        <Card className="border-[#ddd5c7] bg-white shadow-sm">
          <CardHeader className="gap-4">
            <div className="flex flex-wrap gap-2">
              {question.tags.map((tag) => (
                <Badge key={tag} variant="outline" className="border-[#d9cdbd] bg-[#fcf8f2] text-[#6f6556]">
                  {tag}
                </Badge>
              ))}
            </div>
            <CardTitle className="text-xl leading-relaxed text-[#1c180f]">{question.prompt}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {question.options.map((option) => {
              const isSelected = selectedAnswer === option;
              const isSaving = savingQuestionId === question.id && isSelected;
              return (
                <button
                  key={option}
                  type="button"
                  onClick={() => void onAnswer(question.id, option)}
                  disabled={isSubmitting || savingQuestionId === question.id}
                  className={`w-full rounded-2xl border px-5 py-4 text-left transition ${
                    isSelected
                      ? "border-[#d26d31] bg-[#fff4ec] text-[#1c180f]"
                      : "border-[#e4dbce] bg-[#fffdfa] text-[#3c3427] hover:border-[#d9cdbd] hover:bg-[#fcf8f2]"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`flex h-5 w-5 items-center justify-center rounded-full border ${
                        isSelected ? "border-[#d26d31] bg-[#d26d31]" : "border-[#c8bdaf] bg-white"
                      }`}
                    >
                      {isSelected ? <div className="h-2 w-2 rounded-full bg-white" /> : null}
                    </div>
                    <span className="flex-1 text-sm">{option}</span>
                    {isSaving ? <span className="text-xs text-[#a07a54]">Saving...</span> : null}
                  </div>
                </button>
              );
            })}
          </CardContent>
          <CardFooter className="flex items-center justify-between gap-4 border-t border-[#efe7db] pt-6">
            <Button
              variant="outline"
              onClick={() => setCurrentIndex((index) => Math.max(index - 1, 0))}
              disabled={currentIndex === 0 || isSubmitting}
            >
              <ChevronLeft className="h-4 w-4" />
              Previous
            </Button>

            <div className="flex flex-wrap justify-center gap-2">
              {questions.map((item, index) => (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => setCurrentIndex(index)}
                  className={`h-9 w-9 rounded-full border text-xs font-semibold transition ${
                    index === currentIndex
                      ? "border-[#1c180f] bg-[#1c180f] text-white"
                      : answers[item.id]
                        ? "border-[#d26d31] bg-[#fff4ec] text-[#d26d31]"
                        : "border-[#ddd5c7] bg-white text-[#6f6556] hover:border-[#cdbca6]"
                  }`}
                >
                  {index + 1}
                </button>
              ))}
            </div>

            {currentIndex === totalQuestions - 1 ? (
              <Button onClick={() => void onSubmit()} disabled={isSubmitting}>
                {submitLabel}
                <Check className="h-4 w-4" />
              </Button>
            ) : (
              <Button onClick={() => setCurrentIndex((index) => Math.min(index + 1, totalQuestions - 1))} disabled={isSubmitting}>
                Next
                <ChevronRight className="h-4 w-4" />
              </Button>
            )}
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}
