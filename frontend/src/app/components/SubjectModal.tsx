import { useState } from "react";
import { BookOpen, Calculator, Check, X } from "lucide-react";

import { updateSubject } from "@/app/features/auth/api";
import { useAuth } from "@/app/features/auth/AuthProvider";
import type { Subject } from "@/app/shared/types/domain";

interface SubjectModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const SUBJECT_OPTIONS: {
  value: Subject;
  label: string;
  description: string;
  icon: typeof BookOpen;
  gradient: string;
  border: string;
}[] = [
  {
    value: "precalculo",
    label: "Precálculo",
    description: "Funciones, álgebra, trigonometría y preparación para cálculo.",
    icon: Calculator,
    gradient: "from-blue-500 to-indigo-600",
    border: "border-blue-400 bg-blue-50/60 ring-2 ring-blue-200",
  },
  {
    value: "preuniversitario",
    label: "Curso Preuniversitario",
    description: "Matemáticas fundamentales para ingreso universitario.",
    icon: BookOpen,
    gradient: "from-purple-500 to-pink-600",
    border: "border-purple-400 bg-purple-50/60 ring-2 ring-purple-200",
  },
];

export function SubjectModal({ isOpen, onClose }: SubjectModalProps) {
  const { user, refreshUser } = useAuth();
  const [selected, setSelected] = useState<Subject | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Reset selection when modal opens
  const effectiveSelected = selected ?? user?.subject ?? null;
  const hasChanged = effectiveSelected !== user?.subject;

  if (!isOpen) return null;

  function handleClose() {
    setSelected(null);
    setError(null);
    onClose();
  }

  async function handleConfirm() {
    if (!effectiveSelected || !hasChanged) {
      handleClose();
      return;
    }

    setError(null);
    setIsSaving(true);
    try {
      await updateSubject(effectiveSelected);
      await refreshUser();
      setSelected(null);
      onClose();
    } catch {
      setError("No se pudo cambiar la materia. Intenta de nuevo.");
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" onClick={handleClose} />

      {/* Modal */}
      <div className="relative w-full max-w-md rounded-2xl border border-[#e5e5e5] bg-white p-6 shadow-xl">
        <div className="mb-5 flex items-center justify-between">
          <div>
            <h2 className="text-[18px] font-semibold text-[#171717]">Cambiar materia</h2>
            <p className="mt-1 text-[13px] text-[#737373]">
              Selecciona la materia en la que deseas trabajar.
            </p>
          </div>
          <button
            onClick={handleClose}
            className="flex h-8 w-8 items-center justify-center rounded-lg text-[#737373] transition-colors hover:bg-[#f5f5f5] hover:text-[#171717]"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        {error ? (
          <div className="mb-4 rounded-lg border border-[#fecaca] bg-[#fef2f2] px-4 py-2.5 text-[13px] text-[#b91c1c]">
            {error}
          </div>
        ) : null}

        <div className="space-y-3">
          {SUBJECT_OPTIONS.map((option) => {
            const Icon = option.icon;
            const isSelected = effectiveSelected === option.value;
            const isCurrent = user?.subject === option.value;
            return (
              <button
                key={option.value}
                onClick={() => setSelected(option.value)}
                disabled={isSaving}
                className={`w-full rounded-xl border-2 p-4 text-left transition-all duration-200 ${
                  isSelected
                    ? option.border
                    : "border-[#e5e5e5] bg-white hover:border-[#d4d4d4] hover:shadow-sm"
                } disabled:cursor-not-allowed disabled:opacity-60`}
              >
                <div className="flex items-start gap-3">
                  <div
                    className={`flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg bg-gradient-to-br ${option.gradient}`}
                  >
                    <Icon className="h-5 w-5 text-white" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <p className="text-[14px] font-medium text-[#171717]">{option.label}</p>
                      {isCurrent ? (
                        <span className="rounded-full bg-blue-100 px-2 py-0.5 text-[10px] font-medium text-blue-700">
                          Actual
                        </span>
                      ) : null}
                    </div>
                    <p className="mt-1 text-[12px] leading-5 text-[#737373]">{option.description}</p>
                  </div>
                  {isSelected ? (
                    <div className="flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full bg-blue-600">
                      <Check className="h-3.5 w-3.5 text-white" />
                    </div>
                  ) : (
                    <div className="h-6 w-6 flex-shrink-0 rounded-full border-2 border-[#d4d4d4]" />
                  )}
                </div>
              </button>
            );
          })}
        </div>

        {/* Action buttons */}
        <div className="mt-6 flex items-center justify-end gap-3">
          <button
            onClick={handleClose}
            disabled={isSaving}
            className="rounded-lg px-4 py-2 text-[13px] font-medium text-[#737373] transition-colors hover:bg-[#f5f5f5] hover:text-[#171717] disabled:opacity-60"
          >
            Cancelar
          </button>
          <button
            onClick={() => void handleConfirm()}
            disabled={isSaving || !hasChanged}
            className="flex items-center gap-2 rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 px-5 py-2 text-[13px] font-medium text-white shadow-sm transition-all hover:from-blue-700 hover:to-indigo-700 hover:shadow-md disabled:cursor-not-allowed disabled:opacity-50"
          >
            {isSaving ? "Guardando..." : "Confirmar cambio"}
          </button>
        </div>
      </div>
    </div>
  );
}
