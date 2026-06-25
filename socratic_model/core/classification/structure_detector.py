from collections import Counter
from dataclasses import dataclass
from typing import Any, List, Optional

from sympy import Poly, cos, exp, factor, log, simplify, sin, srepr, tan
from sympy.core.function import AppliedUndef
from sympy.core.relational import Equality, Relational


STRUCTURE_TO_CONCEPT = {
    "single_linear_equation": "equations",
    "single_nonlinear_equation": "equations",
    "linear_system": "systems",
    "nonlinear_system": "systems",
    "factoring_expression": "factoring",
    "function_expression": "functions",
    "inequality_expression": "inequalities",
    "trigonometric_expression": "trigonometry",
}


@dataclass
class StructureResult:

    domain: str
    concept: Optional[str]
    structure: Optional[str]
    difficulty: str
    variables: List[str]


def unwrap_expr(value: Any):

    if hasattr(value, "sympy_expr"):
        return value.sympy_expr

    return value


def as_expressions(value: Any):

    expr = unwrap_expr(value)

    if expr is None:
        return []

    if isinstance(expr, list):
        return expr

    return [expr]


def get_equations(value: Any):

    return [
        expression
        for expression in as_expressions(value)
        if isinstance(expression, Equality)
    ]


def equation_expression(equation):

    return simplify(
        equation.lhs - equation.rhs
    )


def equation_key(equation):

    expr = equation_expression(
        equation
    )

    symbols = sorted(
        expr.free_symbols,
        key=lambda symbol: symbol.name
    )

    try:

        poly = Poly(
            expr,
            *symbols
        )

        terms = poly.terms()

        first_coeff = next(
            coeff
            for _, coeff in terms
            if coeff != 0
        )

        return tuple(
            (
                monom,
                simplify(
                    coeff / first_coeff
                )
            )
            for monom, coeff in terms
        )

    except Exception:

        simplified = simplify(
            expr
        )

        negated = simplify(
            -expr
        )

        return min(
            srepr(simplified),
            srepr(negated)
        )


def unique_equations(value: Any):

    seen = set()

    unique = []

    for equation in get_equations(
        value
    ):

        key = equation_key(
            equation
        )

        if key in seen:
            continue

        seen.add(
            key
        )

        unique.append(
            equation
        )

    return unique


def count_equations(value: Any):

    return len(
        unique_equations(
            value
        )
    )


def extract_variables(value: Any):

    variables = set()

    for expression in as_expressions(
        value
    ):

        variables.update(
            expression.free_symbols
        )

    return sorted(
        variables,
        key=lambda symbol: symbol.name
    )


def count_variables(value: Any):

    return len(
        extract_variables(
            value
        )
    )


def is_linear(value: Any):

    try:

        expr = value

        if isinstance(
            value,
            Equality
        ):

            expr = equation_expression(
                value
            )

        symbols = sorted(
            expr.free_symbols,
            key=lambda symbol: symbol.name
        )

        if not symbols:
            return True

        poly = Poly(
            expr,
            *symbols
        )

        return poly.total_degree() <= 1

    except Exception:

        return False


def has_shared_variables(equations):

    occurrences = Counter()

    for equation in equations:

        for symbol in equation.free_symbols:

            occurrences[symbol] += 1

    return any(
        count > 1
        for count in occurrences.values()
    )


def is_system(value: Any):

    equations = get_equations(
        value
    )

    return (
        len(equations) > 1
        and
        has_shared_variables(
            equations
        )
    )


def classify_equation_type(value: Any):

    equations = get_equations(
        value
    )

    if not equations:
        return None

    linear = all(
        is_linear(
            equation
        )
        for equation in equations
    )

    if len(equations) == 1:

        if linear:
            return "single_linear_equation"

        return "single_nonlinear_equation"

    if not has_shared_variables(
        equations
    ):

        return None

    if linear:
        return "linear_system"

    return "nonlinear_system"


def has_any_function(expressions, functions):

    return any(
        expression.has(
            *functions
        )
        for expression in expressions
    )


def has_undefined_function(expressions):

    return any(
        expression.has(
            AppliedUndef
        )
        for expression in expressions
    )


def has_inequality(expressions):

    return any(
        isinstance(expression, Relational)
        and
        not isinstance(expression, Equality)
        for expression in expressions
    )

def is_polynomial_expression(expression):
    """Detecta expresiones polinomiales de grado >= 2 (aunque no sean factorizables)."""

    if isinstance(expression, Relational):
        return False

    try:

        symbols = sorted(
            expression.free_symbols,
            key=lambda symbol: symbol.name
        )

        if not symbols:
            return False

        poly = Poly(expression, *symbols)

        return poly.total_degree() >= 2

    except Exception:

        return False
    
def is_factorable_expression(expression):

    if isinstance(
        expression,
        Relational
    ):

        return False

    try:

        symbols = sorted(
            expression.free_symbols,
            key=lambda symbol: symbol.name
        )

        if not symbols:
            return False

        factored = factor(
            expression
        )

        return factored != expression

    except Exception:

        return False


def classify_structure(value: Any):

    expressions = as_expressions(
        value
    )

    if not expressions:
        return None

    if has_any_function(
        expressions,
        (
            sin,
            cos,
            tan
        )
    ):

        return "trigonometric_expression"

    if has_inequality(
        expressions
    ):

        return "inequality_expression"

    if has_undefined_function(
        expressions
    ):

        return "function_expression"

    if has_any_function(
        expressions,
        (
            log,
            exp
        )
    ):

        return "function_expression"

    equation_type = classify_equation_type(
        value
    )

    if equation_type:
        return equation_type

    if any(
        is_factorable_expression(
            expression
        )
        for expression in expressions
    ):

        return "factoring_expression"

    if any(
        is_polynomial_expression(
            expression
        )
        for expression in expressions
    ):

        return "factoring_expression"
    
    return None


def detect_equation_type(value: Any):

    return classify_equation_type(
        value
    )


def analyze_structure(value: Any):

    structure = classify_structure(
        value
    )

    variables = [
        str(symbol)
        for symbol in extract_variables(
            value
        )
    ]

    return StructureResult(
        domain="precalculus"
        if structure == "trigonometric_expression"
        else "algebra",
        concept=STRUCTURE_TO_CONCEPT.get(
            structure
        ),
        structure=structure,
        difficulty="basic",
        variables=variables,
    )
