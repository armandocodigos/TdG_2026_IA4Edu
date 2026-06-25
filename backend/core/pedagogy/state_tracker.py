import re

from sympy import simplify, solve
from sympy.parsing.sympy_parser import parse_expr
from types import SimpleNamespace

from core.parsing.parser import MathParser

from core.analysis.transformations import (
    TransformationAnalyzer
)

from core.models.state import (
    StateResult
)

from core.logging.state_logger import (
    log_state
)

from core.classification.structure_detector import (
    analyze_structure,
)

from core.analysis.hybrid_validator import (
    HybridValidator,
)


class AlgebraStateTracker:

    def __init__(self):

        self.parser = MathParser()

        self.transformer = (
            TransformationAnalyzer()
        )

        self.validator = HybridValidator(
            algebraic_checker=self.transformer
        )

        self.history = []

    def compute_depth(
        self,
        expr
    ):

        try:

            if (
                expr is not None
                and
                hasattr(expr, "lhs")
            ):

                lhs = expr.lhs

                if len(lhs.free_symbols) == 1:

                    symbol = list(
                        lhs.free_symbols
                    )[0]

                    # variable aislada
                    if lhs == symbol:

                        return 3

                    # forma lineal
                    return 2

            return 1

        except Exception:

            return 0

    def _solution_claim_result(
        self,
        previous_step,
        current_step,
    ):

        try:

            previous_parsed = self.parser.parse(
                previous_step
            )

            previous_expr = previous_parsed.sympy_expr

            if previous_expr is None:

                return None

            current_parsed = self.parser.parse(
                current_step
            )

            current_expr = current_parsed.sympy_expr

            current_expressions = (
                current_expr
                if isinstance(current_expr, list)
                else [current_expr]
            )

            if not all(
                hasattr(expression, "lhs")
                and
                len(expression.lhs.free_symbols) == 1
                and
                expression.lhs
                ==
                list(expression.lhs.free_symbols)[0]
                for expression in current_expressions
                if expression is not None
            ):

                return None

            expressions = (
                previous_expr
                if isinstance(previous_expr, list)
                else [previous_expr]
            )

            if not all(
                hasattr(expression, "lhs")
                for expression in expressions
            ):

                return None

            symbols = sorted(
                {
                    symbol
                    for expression in expressions
                    for symbol in (
                        expression.lhs - expression.rhs
                    ).free_symbols
                },
                key=lambda symbol: symbol.name
            )

            if not symbols:
                return None

            claims_by_symbol = {}

            for symbol in symbols:

                matches = re.findall(
                    rf'\b{re.escape(str(symbol))}\s*=\s*'
                    r'([-+]?\d+(?:\.\d+)?(?:/\d+(?:\.\d+)?)?)'
                    r'(?![ \t]*[\+\-\*/A-Za-z])',
                    current_step
                )

                if matches:
                    claims_by_symbol[str(symbol)] = set([
                        str(simplify(parse_expr(match)))
                        for match in matches
                    ])

            if not claims_by_symbol:
                return None

            if len(symbols) == 1:

                symbol = symbols[0]

                expected = set([
                    str(simplify(solution))
                    for solution in solve(
                        previous_expr,
                        symbol
                    )
                ])

                claimed = claims_by_symbol.get(
                    str(symbol),
                    set()
                )

                variables = [str(symbol)]

            else:

                solutions = solve(
                    expressions,
                    symbols,
                    dict=True
                )

                if len(solutions) != 1:
                    return None

                expected = {
                    str(symbol): str(
                        simplify(
                            solutions[0][symbol]
                        )
                    )
                    for symbol in symbols
                    if symbol in solutions[0]
                }

                claimed = {
                    symbol: next(iter(values))
                    for symbol, values in claims_by_symbol.items()
                    if values
                }

                variables = [
                    str(symbol)
                    for symbol in symbols
                ]

            if not expected:
                return None

            if claimed == expected:
                state = "solucion_final"
                valid = True
                progress = True
                error = None

            elif (
                isinstance(claimed, set)
                and
                claimed < expected
            ):
                state = "solucion_parcial"
                valid = False
                progress = True
                error = None

            elif (
                isinstance(claimed, dict)
                and
                claimed
                and
                all(
                    expected.get(symbol) == value
                    for symbol, value in claimed.items()
                )
            ):

                state = "solucion_parcial_sistema"
                valid = True
                progress = True
                error = None

            else:
                state = "paso_incorrecto"
                valid = False
                progress = False
                error = "solution_claim_mismatch"

            result = StateResult(

                previous_step=previous_step,
                current_step=current_step,
                transformation="solucion_por_conjunto",
                mathematically_equivalent=valid,
                mathematically_valid=valid,
                structural_state="variable_aislada",
                pedagogical_state=state,
                progress=progress,
                regression=False,
                repetition=False,
                semantic_loop=False,
                success=True,
                error=error,
                variables=variables,
            )

            log_state(
                result.to_dict()
            )

            return result

        except Exception:
            return None

    def _system_equation_step_result(
        self,
        previous_step,
        current_step,
        topic,
    ):

        if topic not in (
            "linear_system",
            "nonlinear_system",
        ):

            return None

        try:

            previous_parsed = self.parser.parse(
                previous_step
            )

            current_parsed = self.parser.parse(
                current_step
            )

            previous_expr = previous_parsed.sympy_expr
            current_expr = current_parsed.sympy_expr

            if (
                not isinstance(previous_expr, list)
                or
                isinstance(current_expr, list)
                or
                not hasattr(current_expr, "lhs")
            ):

                return None

            current_delta = simplify(
                current_expr.lhs - current_expr.rhs
            )

            system_symbols = sorted(
                {
                    symbol
                    for equation in previous_expr
                    for symbol in equation.free_symbols
                },
                key=lambda symbol: symbol.name
            )

            system_solution = solve(
                previous_expr,
                system_symbols,
                dict=True
            )

            expected_solution = (
                system_solution[0]
                if len(system_solution) == 1
                else {}
            )

            for equation in previous_expr:

                if not hasattr(equation, "lhs"):
                    continue

                previous_delta = simplify(
                    equation.lhs - equation.rhs
                )

                equivalent = (
                    simplify(
                        previous_delta - current_delta
                    )
                    == 0
                    or
                    simplify(
                        previous_delta + current_delta
                    )
                    == 0
                )

                if not equivalent and current_delta != 0:

                    ratio = simplify(
                        previous_delta / current_delta
                    )

                    equivalent = (
                        not ratio.free_symbols
                    )

                if equivalent:

                    result = StateResult(
                        previous_step=previous_step,
                        current_step=current_step,
                        transformation="reordenamiento_sistema",
                        mathematically_equivalent=True,
                        mathematically_valid=True,
                        structural_state="ecuacion_del_sistema",
                        pedagogical_state="avance_valido",
                        progress=True,
                        regression=False,
                        repetition=False,
                        semantic_loop=False,
                        success=True,
                        error=None,
                        variables=current_parsed.variables,
                    )

                    log_state(
                        result.to_dict()
                    )

                    return result

            current_symbols = sorted(
                current_delta.free_symbols,
                key=lambda symbol: symbol.name
            )

            if (
                len(current_symbols) == 1
                and
                current_symbols[0] in expected_solution
            ):

                symbol = current_symbols[0]

                current_solutions = solve(
                    current_expr,
                    symbol
                )

                if (
                    len(current_solutions) == 1
                    and
                    simplify(
                        current_solutions[0]
                        -
                        expected_solution[symbol]
                    )
                    == 0
                ):

                    result = StateResult(
                        previous_step=previous_step,
                        current_step=current_step,
                        transformation="sustitucion_sistema",
                        mathematically_equivalent=True,
                        mathematically_valid=True,
                        structural_state="ecuacion_del_sistema",
                        pedagogical_state="avance_valido",
                        progress=True,
                        regression=False,
                        repetition=False,
                        semantic_loop=False,
                        success=True,
                        error=None,
                        variables=current_parsed.variables,
                    )

                    log_state(
                        result.to_dict()
                    )

                    return result

            for equation in previous_expr:

                for symbol, value in expected_solution.items():

                    substituted = equation.subs(
                        symbol,
                        value
                    )

                    substituted_delta = simplify(
                        substituted.lhs - substituted.rhs
                    )

                    equivalent = (
                        simplify(
                            substituted_delta - current_delta
                        )
                        == 0
                        or
                        simplify(
                            substituted_delta + current_delta
                        )
                        == 0
                    )

                    if equivalent:

                        result = StateResult(
                            previous_step=previous_step,
                            current_step=current_step,
                            transformation="sustitucion_sistema",
                            mathematically_equivalent=True,
                            mathematically_valid=True,
                            structural_state="ecuacion_del_sistema",
                            pedagogical_state="avance_valido",
                            progress=True,
                            regression=False,
                            repetition=False,
                            semantic_loop=False,
                            success=True,
                            error=None,
                            variables=current_parsed.variables,
                        )

                        log_state(
                            result.to_dict()
                        )

                        return result

            return None

        except Exception:
            return None

    def _system_invalid_equation_result(
        self,
        previous_step,
        current_step,
        topic,
    ):

        if topic not in (
            "linear_system",
            "nonlinear_system",
        ):

            return None

        try:

            previous_parsed = self.parser.parse(
                previous_step
            )

            current_parsed = self.parser.parse(
                current_step
            )

            previous_expr = previous_parsed.sympy_expr
            current_expr = current_parsed.sympy_expr

            if not isinstance(previous_expr, list):
                return None

            current_expressions = (
                current_expr
                if isinstance(current_expr, list)
                else [current_expr]
            )

            if not all(
                hasattr(expression, "lhs")
                for expression in current_expressions
                if expression is not None
            ):

                return None

            system_variables = {
                str(symbol)
                for equation in previous_expr
                for symbol in equation.free_symbols
            }

            current_variables = {
                str(symbol)
                for expression in current_expressions
                for symbol in expression.free_symbols
            }

            if (
                not current_variables
                or
                not current_variables <= system_variables
            ):

                return None

            result = StateResult(
                previous_step=previous_step,
                current_step=current_step,
                transformation="paso_incorrecto",
                mathematically_equivalent=False,
                mathematically_valid=False,
                structural_state="ecuacion_del_sistema",
                pedagogical_state="paso_incorrecto",
                progress=False,
                regression=False,
                repetition=False,
                semantic_loop=False,
                success=True,
                error="system_step_not_equivalent",
                variables=current_parsed.variables,
            )

            log_state(
                result.to_dict()
            )

            return result

        except Exception:
            return None
        
    def analyze_step(
        self,
        previous_step: str,
        current_step: str,
        topic: str = None,
    ):

        try:

            solution_claim_result = (
                self._solution_claim_result(
                    previous_step,
                    current_step
                )
            )

            if solution_claim_result is not None:
                return solution_claim_result

            system_step_result = (
                self._system_equation_step_result(
                    previous_step,
                    current_step,
                    topic,
                )
            )

            if system_step_result is not None:
                return system_step_result

            system_invalid_result = (
                self._system_invalid_equation_result(
                    previous_step,
                    current_step,
                    topic,
                )
            )

            if system_invalid_result is not None:
                return system_invalid_result

            # ====================================================
            # REPETICIÓN EXACTA
            # ====================================================

            exact_repetition = (

                previous_step.strip()
                ==
                current_step.strip()

            )

            transform_result = (
                self.transformer.analyze(
                    previous_step,
                    current_step
                )
            )

            if not transform_result.success:

                if topic in (
                    "trigonometry_basics",
                    "functions",
                ):

                    transform_result = SimpleNamespace(
                        success=True,
                        equivalent=False,
                        transformation="llm_validation",
                        error=None,
                    )

                else:

                    result = StateResult(

                        previous_step=
                        previous_step,

                        current_step=
                        current_step,

                        transformation=None,

                        mathematically_equivalent=
                        False,

                        mathematically_valid=
                        False,

                        structural_state=
                        "error",

                        pedagogical_state=
                        "transform_error",

                        progress=False,

                        regression=False,

                        repetition=False,

                        semantic_loop=False,

                        success=False,

                        error="transform_failed"
                    )

                    log_state(
                        result.to_dict()
                    )

                    return result

            # ====================================================
            # PARSE
            # ====================================================

            current_parsed = (
                self.parser.parse(
                    current_step
                )
            )

            previous_parsed = (
                self.parser.parse(
                    previous_step
                )
            )

            expr = (
                current_parsed.sympy_expr
            )

            previous_expr = (
                previous_parsed.sympy_expr
            )

            structure_result = analyze_structure(
                current_parsed
            )

            # ====================================================
            # REPETICIÓN
            # ====================================================

            repetition = (
                exact_repetition
            )

            # ====================================================
            # LOOP
            # ====================================================

            loop_detected = (
                repetition
            )

            # ====================================================
            # VALIDEZ MATEMÁTICA
            # ====================================================

            # ====================================================
            # VALIDACIÓN HÍBRIDA
            # ====================================================

            validation = self.validator.validate(
                previous_step,
                current_step,
                topic=topic,
            )

            mathematically_equivalent = (
                validation.is_correct
            )

            mathematically_valid = (
                validation.is_correct
            )

            # ====================================================
            # ESTRUCTURA
            # ====================================================

            structural_state = (
                structure_result.structure
                or
                "expresion_general"
            )

            if (
                expr is not None
                and
                hasattr(expr, "lhs")
            ):

                lhs = expr.lhs

                if len(lhs.free_symbols) == 1:

                    symbol = list(
                        lhs.free_symbols
                    )[0]

                    if lhs == symbol:

                        structural_state = (
                            "variable_aislada"
                        )

            # ====================================================
            # DEPTH ALGEBRAICO
            # ====================================================

            previous_depth = (
                self.compute_depth(
                    previous_expr
                )
            )

            current_depth = (
                self.compute_depth(
                    expr
                )
            )

            # ====================================================
            # SOLUCIONES PARCIALES
            # ====================================================

            partial_solution = False

            try:

                if topic in (
                    "linear_system",
                    "nonlinear_system",
                ):

                    raise ValueError(
                        "system partials are handled separately"
                    )

                previous_solutions = solve(
                    previous_expr
                )

                current_solutions = solve(
                    expr
                )

                if (

                    previous_solutions
                    and
                    current_solutions

                ):

                    previous_set = set([
                        str(s)
                        for s in previous_solutions
                    ])

                    current_set = set([
                        str(s)
                        for s in current_solutions
                    ])

                    if (

                        current_set
                        <
                        previous_set

                    ):

                        partial_solution = True

            except Exception:
                pass

            # ====================================================
            # PEDAGOGÍA
            # ====================================================

            pedagogical_state = (
                "sin_clasificar"
            )

            progress = False

            regression = False

            if repetition:

                pedagogical_state = (
                    "repeticion"
                )

            elif partial_solution:

                pedagogical_state = (
                    "solucion_parcial"
                )

            elif not mathematically_valid:

                if (
                    topic == "functions"
                    and
                    validation.error_type
                    in (
                        "error_sustitucion",
                        "error_operacion",
                    )
                ):

                    pedagogical_state = (
                        f"{validation.error_type}_funcion"
                    )

                else:

                    pedagogical_state = (
                        "paso_incorrecto"
                    )

            elif mathematically_valid:

                # ====================================================
                # RETROCESO
                # ====================================================

                if current_depth < previous_depth:

                    pedagogical_state = (
                        "retroceso"
                    )

                    regression = True

                # ====================================================
                # EXPANSIONES LATERALES
                # ====================================================

                elif transform_result.transformation in (

                    "expansion",
                    "factorizacion"

                ):

                    pedagogical_state = (
                        "equivalencia_lateral"
                    )

                # ====================================================
                # AVANCE REAL
                # ====================================================

                else:

                    pedagogical_state = (
                        "avance_valido"
                    )

                    progress = True

            # ====================================================
            # SOLUCIÓN FINAL
            # ====================================================

            if (

                structural_state ==
                "variable_aislada"

                and

                mathematically_valid

                and

                not partial_solution

            ):

                pedagogical_state = (
                    "solucion_final"
                )

            if (
                topic == "functions"
                and
                validation.detail == "resultado_validado"
                and
                mathematically_valid
            ):

                pedagogical_state = (
                    "solucion_final"
                )

            if (
                topic == "functions"
                and
                validation.detail == "sustitucion_validada"
                and
                mathematically_valid
            ):

                pedagogical_state = (
                    "sustitucion_funcion_validada"
                )

            self.history.append(
                current_step.strip()
            )

            result = StateResult(

                previous_step=
                previous_step,

                current_step=
                current_step,

                transformation=
                transform_result.transformation,

                mathematically_equivalent=
                mathematically_equivalent,

                mathematically_valid=
                mathematically_valid,

                structural_state=
                structural_state,

                pedagogical_state=
                pedagogical_state,

                progress=
                progress,

                regression=
                regression,

                repetition=
                repetition,

                semantic_loop=
                loop_detected,

                success=True,

                error=None,

                domain=structure_result.domain,

                concept=structure_result.concept,

                structure=structure_result.structure,

                difficulty=structure_result.difficulty,

                variables=structure_result.variables,

                validation_error_type=validation.error_type,

                validation_detail=validation.detail,
            )

            log_state(
                result.to_dict()
            )

            return result

        except Exception as e:

            result = StateResult(

                previous_step=
                previous_step,

                current_step=
                current_step,

                transformation=None,

                mathematically_equivalent=
                False,

                mathematically_valid=
                False,

                structural_state=
                "error",

                pedagogical_state=
                "system_error",

                progress=False,

                regression=False,

                repetition=False,

                semantic_loop=False,

                success=False,

                error=str(e)
            )

            log_state(
                result.to_dict()
            )

            return result
