# ============================================================
# HYBRID VALIDATOR
# ============================================================
# Estrategia por tema:
#   - Álgebra (lineal, cuadrática, sistemas, polinomios,
#     inecuaciones): validación determinista con SymPy.
#   - Trigonometría y funciones: validación asistida por LLM,
#     porque solveset genera soluciones infinitas y
#     la notación f(x) no se reduce algebraicamente.
# ============================================================

import requests
import json
import re

from sympy import Symbol, simplify
from sympy.parsing.sympy_parser import (
    implicit_multiplication,
    parse_expr,
    standard_transformations,
)

from core.config import (
    OLLAMA_URL,
    MODEL,
)

# ============================================================
# TEMAS QUE USAN SYMPY
# ============================================================

ALGEBRAIC_TOPICS = {
    "single_linear_equation",
    "single_nonlinear_equation",
    "linear_system",
    "nonlinear_system",
    "polynomials",
    "inequalities",
    "quadratic_equations",
    "equations",
}

# ============================================================
# TEMAS QUE DELEGAN AL LLM
# ============================================================

LLM_TOPICS = {
    "trigonometry_basics",
    "functions",
}


FUNCTION_PATTERN = (
    r'f\s*\(\s*x\s*\)\s*=?\s*'
    r'([0-9xX\+\-\*/\^\(\)\. \t]+)'
)


EVALUATION_PATTERN = (
    r'f\s*\(\s*([-+]?\d+(?:\.\d+)?)\s*\)'
    r'\s*=\s*([-+]?\d+(?:\.\d+)?)(?!\s*[\*/\+\-])'
)


UNSUBSTITUTED_EVALUATION_PATTERN = (
    r'f\s*\(\s*[-+]?\d+(?:\.\d+)?\s*\)'
    r'\s*=\s*[^,\n]*[a-zA-Z]'
)


INPUT_PATTERNS = (
    r'f\s*\(\s*([-+]?\d+(?:\.\d+)?)\s*\)',
    r'evaluar(?:la|lo)?\s*(?:con|en)\s*([-+]?\d+(?:\.\d+)?)',
    r'evaluand(?:o|ola|olo)\s*(?:con|en)\s*([-+]?\d+(?:\.\d+)?)',
    r'x\s*(?:vale|=|es)\s*([-+]?\d+(?:\.\d+)?)',
)


OUTPUT_PATTERNS = (
    r'(?:resultado|respuesta).{0,80}?\b(?:es|da|dio)\s*'
    r'([-+]?\d+(?:\.\d+)?)',
    r'(?:resultado|respuesta|obtuve|dio|da)\s*(?:de|es|como)?\s*'
    r'([-+]?\d+(?:\.\d+)?)',
    r'=\s*([-+]?\d+(?:\.\d+)?)',
)


function_transformations = (
    standard_transformations
    +
    (
        implicit_multiplication,
    )
)

# ============================================================
# RESULTADO DE VALIDACIÓN
# ============================================================

class ValidationResult:

    def __init__(
        self,
        is_correct: bool,
        error_type: str | None,
        method: str,
        detail: str | None = None,
    ):

        self.is_correct = is_correct
        self.error_type = error_type
        self.method = method
        self.detail = detail

    def __repr__(self):
        return (
            f"ValidationResult("
            f"is_correct={self.is_correct}, "
            f"error_type={self.error_type!r}, "
            f"method={self.method!r})"
        )


# ============================================================
# PROMPT PARA VALIDACIÓN POR LLM
# ============================================================

VALIDATION_PROMPT = """\
Eres un validador matemático estricto para un tutor de álgebra \
y precálculo.

TEMA: {topic}
PASO ANTERIOR DEL ESTUDIANTE: {previous_step}
PASO ACTUAL DEL ESTUDIANTE: {current_step}

Tu única tarea es determinar si el paso actual es \
matemáticamente correcto dado el paso anterior.

Responde ÚNICAMENTE con un objeto JSON con este formato exacto:
{{
  "is_correct": true,
  "error_type": null,
  "detail": "breve razón"
}}

o si hay error:
{{
  "is_correct": false,
  "error_type": "tipo_de_error",
  "detail": "qué está mal específicamente"
}}

Tipos de error posibles:
- "error_signo": el estudiante cambió un signo incorrectamente
- "error_operacion": operación aritmética incorrecta
- "error_identidad": usó una identidad trigonométrica mal
- "error_dominio": valor fuera del dominio
- "error_sustitucion": sustituyó incorrectamente
- "paso_no_equivalente": el paso no es equivalente al anterior

SOLO responde el JSON. Sin explicaciones adicionales.
"""

# ============================================================
# VALIDADOR HÍBRIDO
# ============================================================

class HybridValidator:

    def __init__(self, algebraic_checker):

        # algebraic_checker es la instancia de
        # TransformationAnalyzer ya existente en el tracker
        self.algebraic = algebraic_checker

    def validate(
        self,
        previous_step: str,
        current_step: str,
        topic: str | None,
    ) -> ValidationResult:

        if topic in LLM_TOPICS:

            if topic == "functions":

                function_result = (
                    self._validate_function_evaluation(
                        previous_step,
                        current_step,
                    )
                )

                if function_result is not None:
                    return function_result

            return self._validate_with_llm(
                previous_step,
                current_step,
                topic,
            )

        return self._validate_with_sympy(
            previous_step,
            current_step,
        )

    # --------------------------------------------------------
    # VALIDACIÓN SYMPY
    # --------------------------------------------------------

    def _validate_with_sympy(
        self,
        previous_step: str,
        current_step: str,
    ) -> ValidationResult:

        try:

            result = self.algebraic.analyze(
                previous_step,
                current_step,
            )

            if not result.success:

                return ValidationResult(
                    is_correct=False,
                    error_type="parse_error",
                    method="sympy",
                    detail="No se pudo analizar el paso",
                )

            if result.equivalent:

                return ValidationResult(
                    is_correct=True,
                    error_type=None,
                    method="sympy",
                    detail=result.transformation,
                )

            # detectar error de signo
            error_type = "paso_no_equivalente"

            try:

                from core.analysis.equivalence import (
                    AlgebraEquivalence,
                )

                eq = AlgebraEquivalence()
                eq_result = eq.compare(
                    previous_step,
                    current_step,
                )

                if eq_result.error_type == "error_signo":
                    error_type = "error_signo"

            except Exception:
                pass

            return ValidationResult(
                is_correct=False,
                error_type=error_type,
                method="sympy",
            )

        except Exception as e:

            return ValidationResult(
                is_correct=False,
                error_type="system_error",
                method="sympy",
                detail=str(e),
            )

    # --------------------------------------------------------
    # VALIDACIÓN LLM
    # --------------------------------------------------------

    def _find_first_number(
        self,
        patterns,
        text
    ):

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                return match.group(1)

        return None

    def _find_function_evaluation_claim(
        self,
        text
    ):

        matches = list(
            re.finditer(
                EVALUATION_PATTERN,
                text,
                re.IGNORECASE
            )
        )

        if not matches:
            return None

        match = matches[-1]

        return (
            match.group(1),
            match.group(2),
        )

    def _has_unsubstituted_function_variable(
        self,
        text
    ):

        match = re.search(
            r'f\s*\(\s*[-+]?\d+(?:\.\d+)?\s*\)\s*=\s*'
            r'([^,\n]+)',
            text,
            re.IGNORECASE
        )

        if not match:
            return False

        expression_part = re.split(
            r'\s+y\s+|\s+lo\s+|\s+me\s+|\s+el\s+',
            match.group(1),
            maxsplit=1,
            flags=re.IGNORECASE
        )[0]

        return (
            re.search(
                r'[a-zA-Z]',
                expression_part
            )
            is not None
        )

    def _find_function_substitution_expression(
        self,
        text
    ):

        match = re.search(
            r'f\s*\(\s*[-+]?\d+(?:\.\d+)?\s*\)\s*=\s*'
            r'([^,\n]+)',
            text,
            re.IGNORECASE
        )

        if not match:
            return None

        expression_part = re.split(
            r'\s+y\s+|\s+lo\s+|\s+me\s+|\s+el\s+',
            match.group(1),
            maxsplit=1,
            flags=re.IGNORECASE
        )[0]

        expression_part = (
            expression_part
            .replace("^", "**")
            .strip()
        )

        if not re.search(
            r'[\*/\+\-]',
            expression_part
        ):
            return None

        return expression_part

    def _validate_function_evaluation(
        self,
        previous_step: str,
        current_step: str,
    ):

        combined = (
            f"{previous_step}\n{current_step}"
        )

        function_match = re.search(
            FUNCTION_PATTERN,
            combined,
            re.IGNORECASE
        )

        if not function_match:
            return None

        if self._has_unsubstituted_function_variable(
            current_step
        ):

            return ValidationResult(
                is_correct=False,
                error_type="error_sustitucion",
                method="function_evaluation",
                detail=(
                    "La evaluacion conserva x "
                    "despues de sustituir."
                ),
            )

        rhs = (
            function_match
            .group(1)
            .replace("^", "**")
            .strip()
        )

        evaluation_claim = (
            self._find_function_evaluation_claim(
                current_step
            )
            or
            self._find_function_evaluation_claim(
                combined
            )
        )

        if evaluation_claim:

            input_value = evaluation_claim[0]
            claimed_value = evaluation_claim[1]

        else:

            input_value = self._find_first_number(
                INPUT_PATTERNS,
                combined
            )

            claimed_value = None

        if input_value is None:

            return None

        try:

            x = Symbol("x")

            expr = parse_expr(
                rhs,
                transformations=function_transformations,
                local_dict={
                    "x": x
                }
            )

            expected = simplify(
                expr.subs(
                    x,
                    parse_expr(
                        input_value
                    )
                )
            )

            if claimed_value is None:

                substitution_expression = (
                    self._find_function_substitution_expression(
                        current_step
                    )
                )

                if substitution_expression:

                    substitution_value = simplify(
                        parse_expr(
                            substitution_expression,
                            transformations=function_transformations,
                        )
                    )

                    if simplify(
                        expected - substitution_value
                    ) == 0:

                        return ValidationResult(
                            is_correct=True,
                            error_type=None,
                            method="function_evaluation",
                            detail="sustitucion_validada",
                        )

                    return ValidationResult(
                        is_correct=False,
                        error_type="error_operacion",
                        method="function_evaluation",
                        detail=(
                            "La sustitucion escrita no coincide "
                            "con el valor esperado."
                        ),
                    )

                claimed_value = self._find_first_number(
                    OUTPUT_PATTERNS,
                    current_step
                )

                if claimed_value is None:
                    return None

            claimed = simplify(
                parse_expr(
                    claimed_value
                )
            )

            if simplify(
                expected - claimed
            ) == 0:

                return ValidationResult(
                    is_correct=True,
                    error_type=None,
                    method="function_evaluation",
                    detail="resultado_validado",
                )

            return ValidationResult(
                is_correct=False,
                error_type="error_operacion",
                method="function_evaluation",
                detail=(
                    "El valor evaluado no coincide "
                    "con la funcion."
                ),
            )

        except Exception:

            return None

    def _validate_with_llm(
        self,
        previous_step: str,
        current_step: str,
        topic: str,
    ) -> ValidationResult:

        prompt = VALIDATION_PROMPT.format(
            topic=topic,
            previous_step=previous_step,
            current_step=current_step,
        )

        try:

            response = requests.post(

                OLLAMA_URL,

                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.0,
                        "num_predict": 120,
                    },
                },

                timeout=30,
            )

            response.raise_for_status()

            raw = (
                response.json()
                .get("response", "")
                .strip()
            )

            # limpiar posibles backticks
            clean = raw.replace(
                "```json", ""
            ).replace(
                "```", ""
            ).strip()

            parsed = json.loads(clean)

            return ValidationResult(
                is_correct=bool(
                    parsed.get("is_correct", False)
                ),
                error_type=parsed.get("error_type"),
                method="llm",
                detail=parsed.get("detail"),
            )

        except Exception as e:

            # Si el LLM falla, marcar como no validado
            # pero no bloquear al estudiante
            return ValidationResult(
                is_correct=True,
                error_type=None,
                method="llm_fallback",
                detail=f"LLM no disponible: {str(e)}",
            )
