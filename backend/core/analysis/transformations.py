from sympy import simplify
from sympy import expand

from core.parsing.parser import MathParser

from core.analysis.equivalence import (
    AlgebraEquivalence
)

from core.models.transformation import (
    TransformationResult
)

from core.logging.transformation_logger import (
    log_transformation
)


class TransformationAnalyzer:

    def __init__(self):

        self.parser = MathParser()

        self.equivalence = (
            AlgebraEquivalence()
        )

    def analyze(
        self,
        original_text: str,
        student_text: str
    ):

        try:

            equivalence_result = (
                self.equivalence.compare(
                    original_text,
                    student_text
                )
            )

            if not equivalence_result.success:

                result = TransformationResult(
                    original_expr=original_text,
                    student_expr=student_text,
                    equivalent=False,
                    transformation=None,
                    details=None,
                    success=False,
                    error="equivalence_failed"
                )

                log_transformation(
                    result.to_dict()
                )

                return result

            original = self.parser.parse(
                original_text
            )

            student = self.parser.parse(
                student_text
            )

            original_eq = (
                original.sympy_expr
            )

            student_eq = (
                student.sympy_expr
            )

            transformation = None

            if (
                not hasattr(
                    original_eq,
                    "lhs"
                )
                or
                not hasattr(
                    student_eq,
                    "lhs"
                )
            ):

                transformation = (
                    "equivalente_general"
                    if equivalence_result.equivalent
                    else "paso_incorrecto"
                )

                result = TransformationResult(
                    original_expr=original_text,
                    student_expr=student_text,
                    equivalent=(
                        equivalence_result.equivalent
                    ),
                    transformation=transformation,
                    details=None,
                    success=True,
                    error=None
                )

                log_transformation(
                    result.to_dict()
                )

                return result

            # ====================================================
            # EXPANSION
            # ====================================================

            if transformation is None:

                if expand(
                    original_eq.lhs
                ) == expand(
                    student_eq.lhs
                ):

                    transformation = (
                        "expansion"
                    )

            # ====================================================
            # RESTA AMBOS LADOS
            # ====================================================

            if (
                simplify(
                    original_eq.lhs -
                    student_eq.lhs
                ).is_number

                and

                simplify(
                    original_eq.rhs -
                    student_eq.rhs
                ).is_number
            ):

                lhs_diff = simplify(
                    original_eq.lhs -
                    student_eq.lhs
                )

                rhs_diff = simplify(
                    original_eq.rhs -
                    student_eq.rhs
                )

                if (

                    lhs_diff == rhs_diff

                    and

                    lhs_diff != 0

                    and

                    rhs_diff != 0
                ):

                    transformation = (
                        "suma_resta_ambos_lados"
                    )

            # ====================================================
            # DIVISION AMBOS LADOS
            # ====================================================

            if transformation is None:

                try:

                    lhs_ratio = simplify(
                        original_eq.lhs /
                        student_eq.lhs
                    )

                    rhs_ratio = simplify(
                        original_eq.rhs /
                        student_eq.rhs
                    )

                    if lhs_ratio == rhs_ratio:

                        transformation = (
                            "division_ambos_lados"
                        )

                except Exception:
                    pass

            # ====================================================
            # DEFAULT
            # ====================================================

            if transformation is None:

                if equivalence_result.equivalent:

                    transformation = (
                        "equivalente_general"
                    )

                else:

                    transformation = (
                        "paso_incorrecto"
                    )

            result = TransformationResult(
                original_expr=original_text,
                student_expr=student_text,
                equivalent=(
                    equivalence_result.equivalent
                ),
                transformation=transformation,
                details=None,
                success=True,
                error=None
            )

            log_transformation(
                result.to_dict()
            )

            return result

        except Exception as e:

            result = TransformationResult(
                original_expr=original_text,
                student_expr=student_text,
                equivalent=False,
                transformation=None,
                details=None,
                success=False,
                error=str(e)
            )

            log_transformation(
                result.to_dict()
            )

            return result
