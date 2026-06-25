from sympy import Equality, Poly

from sympy.core.add import Add
from sympy.core.mul import Mul
from sympy.core.power import Pow

from core.classification.structure_detector import (
    classify_structure,
)


LEGACY_MATH_TYPES = {
    "single_linear_equation": "ecuacion_lineal",
    "single_nonlinear_equation": "ecuacion_cuadratica",
    "linear_system": "sistema",
    "nonlinear_system": "sistema",
    "factoring_expression": "expresion_algebraica",
    "function_expression": "funcion",
    "inequality_expression": "inecuacion",
    "trigonometric_expression": "trigonometria",
}


def classify_math(expr):

    structure = classify_structure(
        expr
    )

    if structure == "single_nonlinear_equation":

        try:

            equation = expr[0] if isinstance(expr, list) else expr

            symbols = list(
                (equation.lhs - equation.rhs).free_symbols
            )

            poly = Poly(
                equation.lhs - equation.rhs,
                *symbols
            )

            if poly.total_degree() == 2:
                return "ecuacion_cuadratica"

        except Exception:
            pass

        return "ecuacion"

    if structure:

        return LEGACY_MATH_TYPES.get(
            structure,
            structure
        )

    if isinstance(expr, Equality):

        lhs = expr.lhs
        rhs = expr.rhs

        poly_expr = lhs - rhs

        symbols = list(poly_expr.free_symbols)

        if len(symbols) == 1:

            try:

                poly = Poly(
                    poly_expr,
                    symbols[0]
                )

                degree = poly.degree()

                if degree == 1:
                    return "ecuacion_lineal"

                if degree == 2:
                    return "ecuacion_cuadratica"

            except Exception:
                pass

        return "ecuacion"

    if isinstance(expr, Pow):
        return "potencia"

    if isinstance(expr, Mul):
        return "multiplicacion"

    if isinstance(expr, Add):
        return "expresion_algebraica"

    return "desconocido"
