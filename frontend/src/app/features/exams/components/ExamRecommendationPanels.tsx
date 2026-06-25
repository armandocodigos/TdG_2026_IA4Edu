import { CheckCircle2, Lightbulb, TrendingUp } from "lucide-react";

import { MathText } from "@/app/components/ui/MathText";

function cleanRecommendationText(value: string) {
  let cleanValue = value.trim().replace(/^["'“”]+/, "").replace(/["'“”;,]+$/, "").trim();
  if ((cleanValue.startsWith('"') && cleanValue.endsWith('"')) || (cleanValue.startsWith("'") && cleanValue.endsWith("'"))) {
    cleanValue = cleanValue.slice(1, -1).trim();
  }
  return cleanValue.replace(/["'“”;,]+$/, "").trim();
}

export function ExamRecommendationPanels({
  positiveRecommendations,
  improvementRecommendations,
  compact = false,
}: {
  positiveRecommendations: string[];
  improvementRecommendations: string[];
  compact?: boolean;
}) {
  const wrapperClassName = compact ? "mt-5 rounded-lg border border-[#e5e5e5] bg-white p-4" : "mb-6 rounded-lg border border-[#e5e5e5] bg-white p-6";
  const headerClassName = compact ? "mb-3 flex items-center gap-2" : "mb-4 flex items-center gap-2";
  const titleClassName = compact ? "text-[13px] font-semibold text-[#171717]" : "text-[18px] font-semibold text-[#171717]";
  const gridClassName = compact ? "grid gap-3 lg:grid-cols-2" : "grid gap-4 lg:grid-cols-2";
  const panelClassName = compact ? "rounded-lg p-3" : "rounded-lg p-4";
  const cardGap = compact ? "space-y-2" : "space-y-3";
  const cardPadding = compact ? "px-3 py-2.5" : "px-3 py-3";
  const numberClassName = compact
    ? "mt-0.5 flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full text-[11px] font-semibold"
    : "mt-0.5 flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full text-[12px] font-semibold";
  const textClassName = compact ? "text-[12px] leading-5" : "text-[13px] leading-6";

  return (
    <div className={wrapperClassName}>
      <div className={headerClassName}>
        <Lightbulb className="h-4 w-4 text-blue-600" />
        {compact ? <p className={titleClassName}>Recomendaciones</p> : <h2 className={titleClassName}>Recomendaciones</h2>}
      </div>
      <div className={gridClassName}>
        <div className={`${panelClassName} border border-emerald-100 bg-emerald-50/40`}>
          <div className="mb-2 flex items-center gap-2">
            <CheckCircle2 className="h-4 w-4 text-emerald-600" />
            {compact ? (
              <p className="text-[13px] font-semibold text-emerald-900">Lo que ya dominas</p>
            ) : (
              <h3 className="text-[14px] font-semibold text-emerald-900">Lo que ya dominas</h3>
            )}
          </div>
          {positiveRecommendations.length ? (
            <div className={cardGap}>
              {positiveRecommendations.map((recommendation, index) => (
                <div key={recommendation} className={`flex gap-3 rounded-md border border-emerald-100 bg-white ${cardPadding}`}>
                  <span className={`${numberClassName} bg-emerald-100 text-emerald-700`}>{index + 1}</span>
                  <MathText content={cleanRecommendationText(recommendation)} className={`${textClassName} text-emerald-900`} />
                </div>
              ))}
            </div>
          ) : (
            <p className={`rounded-md border border-emerald-100 bg-white px-3 py-2 ${textClassName} text-emerald-700`}>
              Aún no hay suficientes aciertos para detectar fortalezas claras.
            </p>
          )}
        </div>

        <div className={`${panelClassName} border border-amber-100 bg-amber-50/50`}>
          <div className="mb-2 flex items-center gap-2">
            <TrendingUp className="h-4 w-4 text-amber-600" />
            {compact ? (
              <p className="text-[13px] font-semibold text-amber-900">Para reforzar</p>
            ) : (
              <h3 className="text-[14px] font-semibold text-amber-900">Para reforzar</h3>
            )}
          </div>
          {improvementRecommendations.length ? (
            <div className={cardGap}>
              {improvementRecommendations.map((recommendation, index) => (
                <div key={recommendation} className={`flex gap-3 rounded-md border border-amber-100 bg-white ${cardPadding}`}>
                  <span className={`${numberClassName} bg-amber-100 text-amber-700`}>{index + 1}</span>
                  <MathText content={cleanRecommendationText(recommendation)} className={`${textClassName} text-amber-900`} />
                </div>
              ))}
            </div>
          ) : (
            <p className={`rounded-md border border-amber-100 bg-white px-3 py-2 ${textClassName} text-amber-700`}>
              No se detectaron errores importantes en este intento.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
