from sympy import solve
from sympy import simplify

from core.parsing.parser import MathParser

from core.models.semantic import (
    SemanticStateResult
)

from core.logging.semantic_logger import (
    log_semantic
)


class SemanticStateTracker:

    def __init__(self):

        self.parser = MathParser()

        self.semantic_history = []

    def build_canonical_state(
        self,
        expr
    ):

        try:

            if (
                expr is not None
                and
                hasattr(expr, "lhs")
            ):

                solutions = solve(expr)

                if solutions:

                    normalized = sorted([
                        str(
                            simplify(sol)
                        )
                        for sol in solutions
                    ])

                    return (
                        "|".join(normalized)
                    )

            return str(
                simplify(expr)
            )

        except Exception:

            return str(expr)

    def analyze(
        self,
        previous_step: str,
        current_step: str
    ):

        try:

            parsed = self.parser.parse(
                current_step
            )

            if not parsed.success:

                result = (
                    SemanticStateResult(
                        previous_step=
                        previous_step,

                        current_step=
                        current_step,

                        canonical_state=
                        "invalid",

                        semantic_repeat=
                        False,

                        semantic_loop=
                        False,

                        semantic_progress=
                        False,

                        success=False,

                        error=
                        "parse_failed"
                    )
                )

                log_semantic(
                    result.to_dict()
                )

                return result

            expr = parsed.sympy_expr

            canonical = (
                self.build_canonical_state(
                    expr
                )
            )

            semantic_repeat = (
                canonical
                in self.semantic_history
            )

            semantic_loop = (
                semantic_repeat
            )

            semantic_progress = (
                not semantic_repeat
            )

            self.semantic_history.append(
                canonical
            )

            result = (
                SemanticStateResult(
                    previous_step=
                    previous_step,

                    current_step=
                    current_step,

                    canonical_state=
                    canonical,

                    semantic_repeat=
                    semantic_repeat,

                    semantic_loop=
                    semantic_loop,

                    semantic_progress=
                    semantic_progress,

                    success=True,

                    error=None
                )
            )

            log_semantic(
                result.to_dict()
            )

            return result

        except Exception as e:

            result = (
                SemanticStateResult(
                    previous_step=
                    previous_step,

                    current_step=
                    current_step,

                    canonical_state=
                    "error",

                    semantic_repeat=
                    False,

                    semantic_loop=
                    False,

                    semantic_progress=
                    False,

                    success=False,

                    error=str(e)
                )
            )

            log_semantic(
                result.to_dict()
            )

            return result
