from sympy import simplify
from sympy import solve
from sympy import solveset
from sympy.core.relational import Equality

from core.parsing.parser import MathParser

from core.models.equivalence import (
    EquivalenceResult
)

from core.logging.equivalence_logger import (
    log_equivalence
)


class AlgebraEquivalence:

    def __init__(self):

        self.parser = MathParser()

    def solution_signature(
        self,
        expr
    ):

        if isinstance(
            expr,
            list
        ):

            variables = sorted(
                {
                    symbol
                    for equation in expr
                    for symbol in equation.free_symbols
                },
                key=lambda symbol: symbol.name
            )

            return solve(
                expr,
                variables,
                dict=True
            )

        if isinstance(
            expr,
            Equality
        ):

            return solveset(
                expr
            )

        return simplify(
            expr
        )

    def compare(
        self,
        original_text: str,
        student_text: str
    ):

        try:

            original = self.parser.parse(
                original_text
            )

            student = self.parser.parse(
                student_text
            )

            if not original.success:

                result = EquivalenceResult(
                    original_expr=original_text,
                    student_expr=student_text,
                    equivalent=False,
                    error_type="parse_error_original",
                    details=original.error,
                    success=False
                )

                log_equivalence(
                    result.to_dict()
                )

                return result

            if not student.success:

                result = EquivalenceResult(
                    original_expr=original_text,
                    student_expr=student_text,
                    equivalent=False,
                    error_type="parse_error_student",
                    details=student.error,
                    success=False
                )

                log_equivalence(
                    result.to_dict()
                )

                return result

            original_eq = original.sympy_expr

            student_eq = student.sympy_expr

            original_solution = self.solution_signature(
                original_eq
            )

            student_solution = self.solution_signature(
                student_eq
            )

            equivalent = (
                original_solution ==
                student_solution
            )

            error_type = None

            if not equivalent:

                # ========================================================
                # detección simple de error de signo
                # ========================================================

                try:

                    original_sol = list(
                        original_solution
                    )[0]

                    student_sol = list(
                        student_solution
                    )[0]

                    if simplify(
                        original_sol + student_sol
                    ) == 0:

                        error_type = "error_signo"

                    else:

                        error_type = (
                            "paso_no_equivalente"
                        )

                except Exception:

                    error_type = (
                        "paso_no_equivalente"
                    )

            result = EquivalenceResult(
                original_expr=original_text,
                student_expr=student_text,
                equivalent=equivalent,
                error_type=error_type,
                details=None,
                success=True
            )

            log_equivalence(
                result.to_dict()
            )

            return result

        except Exception as e:

            result = EquivalenceResult(
                original_expr=original_text,
                student_expr=student_text,
                equivalent=False,
                error_type="system_error",
                details=str(e),
                success=False
            )

            log_equivalence(
                result.to_dict()
            )

            return result
