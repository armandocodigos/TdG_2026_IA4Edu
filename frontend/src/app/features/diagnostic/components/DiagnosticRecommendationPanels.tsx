import { CheckCircle2, Lightbulb, TrendingUp } from "lucide-react";

import { MathText } from "@/app/components/ui/MathText";

function cleanRecommendationText(value: string) {
  let cleanValue = value.trim().replace(/^["'“”]+/, "").replace(/["'“”;,]+$/, "").trim();
  if ((cleanValue.startsWith('"') && cleanValue.endsWith('"')) || (cleanValue.startsWith("'") && cleanValue.endsWith("'"))) {
    cleanValue = cleanValue.slice(1, -1).trim();
  }
  return cleanValue.replace(/["'“”;,]+$/, "").trim();
}

export function DiagnosticRecommendationPanels({
  positiveRecommendations,
  improvementRecommendations,
  compact = false,
}: {
  positiveRecommendations: string[];
  improvementRecommendations: string[];
  compact?: boolean;
}) {
  const textClassName = compact ? "text-[12px] leading-5" : "text-[13px] leading-6";

  return (
    <div className={compact ? "" : "mb-6 rounded-xl border border-[#e5e5e5] bg-white p-6"}>
      {!compact ? (
        <div className="mb-4 flex items-center gap-2">
          <Lightbulb className="h-4 w-4 text-blue-600" />
          <h2 className="text-[16px] font-semibold text-[#171717]">Recomendaciones</h2>
        </div>
      ) : null}
      <div className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-lg border border-emerald-100 bg-emerald-50/40 p-4">
          <div className="mb-3 flex items-center gap-2">
            <CheckCircle2 className="h-4 w-4 text-emerald-600" />
            <h3 className="text-[14px] font-semibold text-emerald-900">Lo que ya dominas</h3>
          </div>
          {positiveRecommendations.length ? (
            <div className="space-y-3">
              {positiveRecommendations.map((recommendation, index) => (
                <div key={recommendation} className="flex gap-3 rounded-md border border-emerald-100 bg-white px-3 py-3">
                  <span className="mt-0.5 flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full bg-emerald-100 text-[12px] font-semibold text-emerald-700">
                    {index + 1}
                  </span>
                  <MathText content={cleanRecommendationText(recommendation)} className={`${textClassName} text-emerald-900`} />
                </div>
              ))}
            </div>
          ) : (
            <p className={`${textClassName} rounded-md border border-emerald-100 bg-white px-3 py-2 text-emerald-700`}>
              Aún no hay suficientes aciertos para detectar fortalezas claras.
            </p>
          )}
        </div>

        <div className="rounded-lg border border-amber-100 bg-amber-50/50 p-4">
          <div className="mb-3 flex items-center gap-2">
            <TrendingUp className="h-4 w-4 text-amber-600" />
            <h3 className="text-[14px] font-semibold text-amber-900">Para reforzar</h3>
          </div>
          {improvementRecommendations.length ? (
            <div className="space-y-3">
              {improvementRecommendations.map((recommendation, index) => (
                <div key={recommendation} className="flex gap-3 rounded-md border border-amber-100 bg-white px-3 py-3">
                  <span className="mt-0.5 flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full bg-amber-100 text-[12px] font-semibold text-amber-700">
                    {index + 1}
                  </span>
                  <MathText content={cleanRecommendationText(recommendation)} className={`${textClassName} text-amber-900`} />
                </div>
              ))}
            </div>
          ) : (
            <p className={`${textClassName} rounded-md border border-amber-100 bg-white px-3 py-2 text-amber-700`}>
              No se detectaron errores importantes en este diagnóstico.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
