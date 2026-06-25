import json
import logging
import re
import time

from app.core.config import get_settings
from app.services.ollama_client import OllamaClient

logger = logging.getLogger(__name__)

MAX_RECOMMENDATIONS = 4

LATEX_JSON_COMMANDS = (
    "alpha", "beta", "cdot", "circ", "cos", "cot", "csc", "delta", "Delta",
    "div", "frac", "geq", "infty", "in", "int", "left", "le", "leq", "lim",
    "ln", "log", "mathbb", "mathcal", "neq", "notin", "over", "overline",
    "partial", "pi", "pm", "right", "sec", "sin", "sqrt", "sum", "tan",
    "theta", "to", "times", "vec",
)
LATEX_JSON_COMMAND_PATTERN = re.compile(rf"(?<!\\)\\(?=({'|'.join(LATEX_JSON_COMMANDS)})\b)")

MASTERY_LABELS = {
    "high": "Dominado",
    "medium": "En progreso",
    "low": "Por reforzar",
}

FORBIDDEN_STYLE_FRAGMENTS = (
    "tu acierto en",
    "la pregunta de",
    "en la pregunta",
    "practic",
    "repas",
)

# Patrón que detecta referencias numéricas a ejercicios/preguntas ("en el ejercicio 3", "la pregunta 2", etc.)
EXERCISE_NUMBER_PATTERN = re.compile(r"\b(el ejercicio|en el ejercicio|la pregunta)\s+\d+\b", re.IGNORECASE)

INCORRECT_MARKERS = (
    "respondiste",
    "en lugar de",
    "el error",
    "fallaste",
    "tu error",
    "incorrect",
    "equivocaste",
    "no acertaste",
)

class FeedbackService:
    """Genera recomendaciones positivas y de mejora para diagnóstico y exámenes.

    Estrategia:
    - Dos llamadas Ollama independientes: una solo con respuestas correctas,
      otra solo con respuestas incorrectas. El modelo no puede mezclar categorías.
    - JSON mode forzado en Ollama para evitar parse failures por typos.
    - Validación semántica: descarta items con estilo prohibido, marcadores
      de error en positivos o longitud insuficiente.
    """

    def __init__(self, ollama_client: OllamaClient | None = None) -> None:
        self.settings = get_settings()
        self.ollama_client = ollama_client or OllamaClient()

    def generate_split_recommendations(
        self,
        *,
        subject: str,
        score_global: float,
        topic_breakdown: dict[str, dict[str, float | int | str]],
        answers_feedback: list[dict[str, str | bool | None]],
        max_positive: int = MAX_RECOMMENDATIONS,
        max_improvement: int = MAX_RECOMMENDATIONS,
        log_label: str = "FEEDBACK_SOURCE",
    ) -> tuple[list[str], list[str]]:
        correct = [item for item in answers_feedback if item["is_correct"]]
        incorrect = [item for item in answers_feedback if not item["is_correct"]]
        expected_positive = min(len(correct), max_positive)
        expected_improvement = min(len(incorrect), max_improvement)

        positive = self._generate_for_category(
            category="positive",
            answers=correct,
            expected_count=expected_positive,
            subject=subject,
            score_global=score_global,
            topic_breakdown=topic_breakdown,
            log_label=log_label,
        )
        improvement = self._generate_for_category(
            category="improvement",
            answers=incorrect,
            expected_count=expected_improvement,
            subject=subject,
            score_global=score_global,
            topic_breakdown=topic_breakdown,
            log_label=log_label,
        )

        return positive[:expected_positive], improvement[:expected_improvement]

    def _generate_for_category(
        self,
        *,
        category: str,
        answers: list[dict],
        expected_count: int,
        subject: str,
        score_global: float,
        topic_breakdown: dict,
        log_label: str,
    ) -> list[str]:
        if expected_count == 0 or not answers:
            return []

        best: list[str] = []
        for attempt_number in range(1, 3):
            prompt = self._build_category_prompt(
                category=category,
                answers=answers,
                expected_count=expected_count,
                subject=subject,
                score_global=score_global,
                topic_breakdown=topic_breakdown,
                strict=attempt_number > 1,
            )
            started_at = time.monotonic()
            try:
                raw_response = self.ollama_client.generate(
                    model=self.settings.fast_llm_model,
                    prompt=prompt,
                    json_mode=True,
                )
            except Exception:
                logger.exception(
                    "%s status=ollama_error category=%s attempt=%d", log_label, category, attempt_number
                )
                break

            duration = time.monotonic() - started_at
            parsed = self.parse_category(category=category, raw_response=raw_response)
            validated = self._validate_items(category=category, items=parsed)
            logger.warning(
                "%s status=attempt category=%s attempt=%d duration=%.2fs raw=%d parsed=%d valid=%d expected=%d",
                log_label, category, attempt_number, duration, len(raw_response), len(parsed), len(validated), expected_count,
            )
            if len(parsed) == 0:
                logger.warning(
                    "%s parse_failed category=%s raw_preview=%r",
                    log_label, category, raw_response[:300],
                )

            if len(validated) >= expected_count:
                return validated[:expected_count]

            if len(validated) > len(best):
                best = validated

        return list(best)[:expected_count]

    def _build_category_prompt(
        self,
        *,
        category: str,
        answers: list[dict],
        expected_count: int,
        subject: str,
        score_global: float,
        topic_breakdown: dict,
        strict: bool,
    ) -> str:
        subject_label = subject.replace("_", " ").title()
        topic_lines = []
        for topic, result in topic_breakdown.items():
            label = MASTERY_LABELS.get(str(result.get("mastery", "")), str(result.get("mastery", "")))
            topic_lines.append(
                f"- {str(topic).replace('_', ' ').title()}: "
                f"{result.get('correct_answers', '?')}/{result.get('total_questions', '?')} correctas, "
                f"{result.get('score_percentage', '?')}% - {label}"
            )

        answer_lines = self._build_answer_prompt_lines(answers)

        shared_rules = [
            "- Escribe en lenguaje simple y directo, pensado para estudiantes de nivel básico-intermedio.",
            "- NUNCA uses comandos LaTeX como \\frac, \\sin, \\cos, \\pi, \\sqrt, etc. Escribe las expresiones en texto plano:",
            "  por ejemplo escribe 'sen(x)' en lugar de \\sin(x), '1/2' en lugar de \\frac{1}{2}, 'π' en lugar de \\pi.",
            "- Si necesitas una fórmula corta, escríbela entre signos de dólar: $sen(x)$, $x^2$, $1/2$.",
            "- Explica los pasos de forma concreta y sin jerga técnica avanzada.",
        ]

        if category == "positive":
            header = (
                f"Eres tutor académico de {subject_label}. Un estudiante respondió CORRECTAMENTE "
                f"{len(answers)} ejercicio(s). Genera un consejo breve que refuerce lo que hizo bien."
            )
            section_header = "## Respuestas correctas del estudiante"
            instructions = [
                f"- Genera exactamente {expected_count} recomendaciones.",
                "- Cada recomendación corresponde a UNA respuesta correcta de la lista.",
                "- Nombra el concepto o habilidad que el estudiante aplicó bien.",
                "- Sugiere cómo generalizar ese mismo criterio para ejercicios similares (sin revelar respuestas concretas).",
                "- Tono positivo y profesional, NUNCA efusivo. NO uses signos de exclamación: nada de '¡', nada de '!'. Escribe en afirmaciones tranquilas (ej.: 'Buen manejo de…', 'Tu resolución muestra…').",
                "- NUNCA escribas 'respondiste X en lugar de', 'el error', 'fallaste', 'incorrecta', 'equivocaste'.",
                "- No digas 'practica', 'repasa', 'recuerda'.",
                "- 2 frases por recomendación, directas y concretas.",
                *shared_rules,
            ]
        else:
            header = (
                f"Eres tutor académico de {subject_label}. Un estudiante respondió INCORRECTAMENTE "
                f"{len(answers)} ejercicio(s). Genera pistas y consejos para que comprenda cómo resolverlo."
            )
            section_header = "## Respuestas incorrectas del estudiante"
            instructions = [
                f"- Genera exactamente {expected_count} recomendaciones.",
                "- Cada recomendación corresponde a UNA respuesta incorrecta de la lista.",
                "- NUNCA menciones 'el ejercicio N', 'la pregunta N', etc. Habla del tema o concepto directamente.",
                "- NUNCA reveles la respuesta correcta. En lugar de decir 'la respuesta es X', guía al estudiante:",
                "  * Señala el concepto o propiedad clave que aplica en ese tipo de ejercicio.",
                "  * Describe el procedimiento o los pasos que llevan a la solución, sin decir cuál es.",
                "  * Indica qué debe verificar o en qué debe fijarse al resolver ese tipo de ejercicio.",
                "- Escribe en frases afirmativas. NUNCA termines con una pregunta ('¿Cómo...?', '¿Qué...?', etc.).",
                "- Escribe como un tutor que da una pista concreta, no como alguien que corrige un examen.",
                "- No digas 'practica', 'repasa', 'recuerda'.",
                "- 2 a 3 frases por recomendación.",
                *shared_rules,
            ]

        if strict:
            instructions.append(
                "- Reintento estricto: respeta exactamente las reglas anteriores, sin texto fuera del JSON."
            )

        return (
            f"{header}\n\n"
            f"## Resultado global\n"
            f"- Materia: {subject_label}\n"
            f"- Puntaje global: {score_global}%\n\n"
            f"## Resultados por tema\n"
            f"{chr(10).join(topic_lines) if topic_lines else 'Sin resultados por tema.'}\n\n"
            f"{section_header}\n"
            f"{chr(10).join(answer_lines) if answer_lines else 'Sin entradas.'}\n\n"
            f"## Formato de salida\n"
            f"Devuelve SOLO JSON válido con esta forma exacta:\n"
            f'{{"recommendations":["..."]}}\n\n'
            f"## Reglas\n"
            + "\n".join(instructions)
            + "\n- Responde en español."
        )

    def _build_answer_prompt_lines(self, answers: list[dict]) -> list[str]:
        lines: list[str] = []
        for index, item in enumerate(answers, start=1):
            explanation = item.get("explanation") or "Sin explicación registrada."
            result_label = "correcta" if item.get("is_correct") else "incorrecta"
            difficulty = item.get("difficulty")
            difficulty_part = f"Dificultad: {difficulty} | " if difficulty else ""
            lines.append(
                f"{index}. Tema: {str(item.get('topic', '')).replace('_', ' ')} | "
                f"{difficulty_part}"
                f"Habilidad: {str(item.get('skill', '')).replace('_', ' ')} | "
                f"Pregunta: {item.get('question_text', '')} | "
                f"Respuesta del estudiante: {item.get('student_answer', '')} | "
                f"Respuesta correcta: {item.get('correct_answer', '')} | "
                f"Resultado: {result_label} | "
                f"Explicación base: {explanation}"
            )
        return lines

    def parse_category(self, *, category: str, raw_response: str) -> list[str]:
        cleaned = self._strip_code_fence(raw_response)
        payload = self._load_json_payload(cleaned)
        if payload is None:
            return self._parse_sectioned_category(cleaned, category=category)
        return self._extract_items_from_payload(payload, category=category)

    def parse_legacy_combined(self, raw_response: str) -> tuple[list[str], list[str]]:
        """Parse the legacy combined format ``{positive_recommendations, improvement_recommendations}``.

        Retained so prior parser tests and any combined-output mocks keep working.
        """
        cleaned = self._strip_code_fence(raw_response)
        payload = self._load_json_payload(cleaned)
        if payload is None:
            return self._parse_sectioned_combined(cleaned)
        positive = self._extract_items_from_payload(payload, category="positive")
        improvement = self._extract_items_from_payload(payload, category="improvement")
        return positive, improvement

    def _load_json_payload(self, text: str):
        for candidate in self._json_candidates(text):
            for variant in self._json_variants(candidate):
                try:
                    return json.loads(variant)
                except json.JSONDecodeError:
                    continue
        return None

    def _extract_items_from_payload(self, payload, *, category: str) -> list[str]:
        if isinstance(payload, list):
            return self._clean_recommendations(payload)

        if not isinstance(payload, dict):
            return []

        for wrapper_key in ("feedback", "data", "result"):
            nested = payload.get(wrapper_key)
            if isinstance(nested, dict):
                items = self._extract_items_from_payload(nested, category=category)
                if items:
                    return items

        if category == "positive":
            candidate_keys = (
                "recommendations",
                "recomendaciones",
                "positive_recommendations",
                "positive_recommendactions",
                "positive_recommendaions",
                "positive_recommends",
                "positive_recommend",
                "positiveRecommendations",
                "lo_que_ya_dominas",
                "fortalezas",
                "sugerencias",
                "retroalimentacion",
                "retroalimentación",
                "items",
                "list",
            )
        else:
            candidate_keys = (
                "recommendations",
                "recomendaciones",
                "improvement_recommendations",
                "improvement_recommendactions",
                "improvement_recommendaions",
                "improvement_recommends",
                "improvement_recommend",
                "improvementRecommendations",
                "para_reforzar",
                "mejoras",
                "sugerencias",
                "retroalimentacion",
                "retroalimentación",
                "items",
                "list",
            )

        raw_value = self._first_present(payload, *candidate_keys)
        if raw_value:
            return self._clean_recommendations(raw_value)

        # catch-all: return the first list value found in the payload
        for value in payload.values():
            if isinstance(value, list) and value:
                return self._clean_recommendations(value)

        return []

    def _validate_items(self, *, category: str, items: list[str]) -> list[str]:
        valid: list[str] = []
        for item in items:
            lower = item.lower()
            if len(item) < 25:
                continue
            if any(fragment in lower for fragment in FORBIDDEN_STYLE_FRAGMENTS):
                logger.warning("FEEDBACK_VALIDATION dropped category=%s reason=style preview=%r", category, item[:80])
                continue
            if EXERCISE_NUMBER_PATTERN.search(item):
                logger.warning("FEEDBACK_VALIDATION dropped category=%s reason=exercise_ref preview=%r", category, item[:80])
                continue
            if item.rstrip().endswith("?"):
                logger.warning("FEEDBACK_VALIDATION dropped category=%s reason=ends_with_question preview=%r", category, item[:80])
                continue
            if category == "positive" and any(marker in lower for marker in INCORRECT_MARKERS):
                logger.warning("FEEDBACK_VALIDATION dropped category=positive reason=error_marker preview=%r", item[:80])
                continue
            if category == "positive":
                item = self._neutralize_exclamations(item)
            if item in valid:
                continue
            valid.append(item)
        return valid

    def _neutralize_exclamations(self, item: str) -> str:
        """Quita signos de exclamación para evitar tono efusivo en recomendaciones positivas."""
        cleaned = item.replace("¡", "")
        cleaned = re.sub(r"!+", ".", cleaned)
        cleaned = re.sub(r"\s+\.", ".", cleaned)
        cleaned = re.sub(r"\.{2,}", ".", cleaned)
        return cleaned.strip()

    def _json_candidates(self, text: str) -> list[str]:
        candidates = [text.strip()]
        candidates.extend(self._balanced_json_objects(text))
        seen: list[str] = []
        for candidate in candidates:
            if candidate and candidate not in seen:
                seen.append(candidate)
        return seen

    def _json_variants(self, candidate: str) -> list[str]:
        # Try the original string first — if json_mode produced valid JSON,
        # escaping LaTeX would double-escape already-valid sequences (\\log → \\\\log).
        without_trailing = re.sub(r",\s*([}\]])", r"\1", candidate)
        escaped = self._escape_latex_json_commands(candidate)
        escaped_no_trailing = re.sub(r",\s*([}\]])", r"\1", escaped)
        variants = [candidate, without_trailing, escaped, escaped_no_trailing]
        seen: list[str] = []
        for variant in variants:
            if variant not in seen:
                seen.append(variant)
        return seen

    def _balanced_json_objects(self, text: str) -> list[str]:
        candidates: list[str] = []
        start: int | None = None
        depth = 0
        in_string = False
        escaped = False
        for index, char in enumerate(text):
            if in_string:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    in_string = False
                continue
            if char == '"':
                in_string = True
                continue
            if char == "{":
                if depth == 0:
                    start = index
                depth += 1
                continue
            if char == "}" and depth:
                depth -= 1
                if depth == 0 and start is not None:
                    candidates.append(text[start : index + 1])
                    start = None
        return candidates

    def _escape_latex_json_commands(self, raw_response: str) -> str:
        return LATEX_JSON_COMMAND_PATTERN.sub(r"\\\\", raw_response)

    def _strip_code_fence(self, raw_response: str) -> str:
        cleaned = raw_response.strip()
        if not cleaned.startswith("```"):
            return cleaned
        lines = cleaned.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines).strip()

    def _first_present(self, payload: dict, *keys: str):
        for key in keys:
            if key in payload:
                return payload[key]
        return []

    def _parse_sectioned_category(self, raw_response: str, *, category: str) -> list[str]:
        positive, improvement = self._parse_sectioned_combined(raw_response)
        return positive if category == "positive" else improvement

    def _parse_sectioned_combined(self, raw_response: str) -> tuple[list[str], list[str]]:
        positive: list[str] = []
        improvement: list[str] = []
        current: list[str] | None = None
        for raw_line in raw_response.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            lower_line = line.lower()
            heading = lower_line.strip("#*:- ")
            if heading in {
                "positive", "positive recommendations", "positive_recommendations",
                "lo que ya dominas", "dominas", "fortalezas",
            }:
                current = positive
                continue
            if heading in {
                "improvement", "improvement recommendations", "improvement_recommendations",
                "para reforzar", "mejoras", "areas de mejora", "áreas de mejora",
            }:
                current = improvement
                continue
            if current is None:
                continue
            cleaned = line.lstrip("0123456789.-*•) ").strip()
            if cleaned:
                current.append(cleaned)
        return self._clean_recommendations(positive), self._clean_recommendations(improvement)

    def _clean_recommendations(self, values) -> list[str]:
        if not isinstance(values, list):
            return []
        recommendations: list[str] = []
        for value in values:
            if isinstance(value, dict):
                value = self._first_present(value, "text", "recommendation", "feedback", "message")
            if not isinstance(value, str):
                continue
            clean_value = value.strip().lstrip("0123456789.-*•) ").strip()
            clean_value = clean_value.strip().strip('",;').strip()
            if (clean_value.startswith('"') and clean_value.endswith('"')) or (
                clean_value.startswith("'") and clean_value.endswith("'")
            ):
                clean_value = clean_value[1:-1].strip()
            clean_value = clean_value.strip('",;').strip()
            if len(clean_value) > 15 and clean_value not in recommendations:
                recommendations.append(clean_value)
        return recommendations
