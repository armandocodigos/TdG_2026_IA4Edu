import re

from core.analysis.conversation_cleaner import (
    clean_conversational_text,
    extract_equation_from_text,
)

from sympy import (
    Eq,
    Function,
    Ge,
    Gt,
    Le,
    Lt,
    Symbol,
    sin,
    cos,
    tan,
    log,
    exp
)

from sympy.parsing.sympy_parser import (

    parse_expr,

    standard_transformations,

    implicit_multiplication,
)

from core.classification.classifier import (
    classify_math
)

from core.classification.structure_detector import (
    analyze_structure,
)

from core.logging.logger import (
    log_parse
)

from core.models.common import (
    MathParseResult
)


########################################################
# TRANSFORMATIONS
########################################################

transformations = (

    standard_transformations +

    (
        implicit_multiplication,
    )
)


########################################################
# LOCAL FUNCTIONS
########################################################

LOCAL_DICT = {

    "sin": sin,

    "cos": cos,

    "tan": tan,

    "log": log,

    "exp": exp,
}


EQUATION_PATTERN = (
    r'([0-9a-zA-Z\+\-\*/\^\(\)\s]+'
    r'='
    r'[0-9a-zA-Z\+\-\*/\^\(\)\s]+)'
)


RELATION_PATTERN = (
    r'([0-9a-zA-Z\+\-\*/\^\(\)\s]+'
    r'(?:<=|>=|<|>)'
    r'[0-9a-zA-Z\+\-\*/\^\(\)\s]+)'
)


IDENTIFIER_PATTERN = r'\b[A-Za-z][A-Za-z0-9_]*\b'


FUNCTION_NAMES = set(
    LOCAL_DICT.keys()
)


class MathParser:

    def extract_ordered_pair_solution(
        self,
        text: str
    ):

        match = re.search(
            r'\(\s*([a-zA-Z])\s*,\s*([a-zA-Z])\s*\)'
            r'\s*=\s*'
            r'\(\s*([-+]?\d+(?:\.\d+)?)\s*,\s*'
            r'([-+]?\d+(?:\.\d+)?)\s*\)',
            text
        )

        if not match:
            return None

        return "\n".join([
            f"{match.group(1)} = {match.group(3)}",
            f"{match.group(2)} = {match.group(4)}",
        ])

    def extract_verbal_assignment(
        self,
        text: str
    ):

        match = re.search(
            r'\b([a-zA-Z])\s+'
            r'(?:debe\s+de\s+ser|debe\s+ser|es|sea|'
            r'debe\s+de\s+ser\s+igual\s+a|'
            r'debe\s+ser\s+igual\s+a|'
            r'es\s+igual\s+a|sea\s+igual\s+a)\s+'
            r'([-+]?\d+(?:\.\d+)?)\b',
            text,
            re.IGNORECASE
        )

        if not match:
            return None

        return (
            f"{match.group(1)} = {match.group(2)}"
        )

    ####################################################
    # EXTRACT MATH
    ####################################################

    def extract_math(
        self,
        text: str
    ):

        ################################################
        # NORMALIZE
        ################################################

        cleaned = clean_conversational_text(
            text
        )

        ordered_pair = self.extract_ordered_pair_solution(
            cleaned
        )

        if ordered_pair:
            return ordered_pair

        verbal_assignment = self.extract_verbal_assignment(
            cleaned
        )

        if verbal_assignment:
            return verbal_assignment

        equations = self.extract_equations(
            cleaned
        )

        if equations:

            return "\n".join(
                equations
            )

        ################################################
        # PATTERNS
        ################################################

        patterns = [

            ############################################
            # INECUACIONES
            ############################################

            RELATION_PATTERN,

            ############################################
            # ECUACIONES
            ############################################

            EQUATION_PATTERN,

            ############################################
            # TRIGONOMETRIA
            ############################################

            r'(sin\([^\)]+\))',

            r'(cos\([^\)]+\))',

            r'(tan\([^\)]+\))',

            ############################################
            # LOGARITMOS
            ############################################

            r'(log\([^\)]+\))',

            ############################################
            # EXPONENCIALES
            ############################################

            r'(exp\([^\)]+\))',

            ############################################
            # POTENCIAS
            ############################################

            r'([0-9a-zA-Z\+\-\*/\^\(\)\s]*[a-zA-Z0-9]\^[0-9]+[0-9a-zA-Z\+\-\*/\^\(\)\s]*)',
        ]

        ################################################
        # SEARCH
        ################################################

        for pattern in patterns:

            match = re.search(
                pattern,
                cleaned
            )

            if not match:
                continue

            expr = (

                match
                .group(1)
                .strip()
            )

            ############################################
            # VALIDACION
            ############################################

            if (

                any(
                    char.isdigit()
                    for char in expr
                )

                or

                "sin" in expr

                or

                "cos" in expr

                or

                "tan" in expr

                or

                "log" in expr

                or

                "exp" in expr
            ):

                return expr

        return None

    def extract_equations(
        self,
        text: str
    ):

        equations = []

        normalized = re.sub(
            r'\s+y\s+(?=[A-Za-z]\s*=)',
            '\n',
            text,
            flags=re.IGNORECASE
        )

        parts = []

        for line in normalized.splitlines():
            parts.extend(
                re.split(
                    (
                        r'[,;]'
                        r'|\ba resolverla\b'
                        r'|\bobtenemos(?:\s+que)?\b'
                        r'|\blo cual\b'
                        r'|\bpor lo que\b'
                    ),
                    line
                )
            )

        for line in parts:

            line = line.strip()

            if not line:
                continue

            equation = extract_equation_from_text(
                line
            )

            if not equation:
                match = re.search(
                    EQUATION_PATTERN,
                    line
                )

                if not match:
                    continue

                equation = (
                    match
                    .group(1)
                    .strip()
                )

            if any(
                char.isdigit()
                for char in equation
            ):

                equations.append(
                    equation
                )

        if len(equations) > 1:
            return equations

        return equations

    def build_local_dict(
        self,
        expr: str
    ):

        local_dict = LOCAL_DICT.copy()

        identifiers = re.findall(
            IDENTIFIER_PATTERN,
            expr
        )

        for identifier in identifiers:

            if identifier in FUNCTION_NAMES:
                continue

            if re.search(
                rf'\b{re.escape(identifier)}\s*\(',
                expr
            ):

                local_dict[identifier] = Function(
                    identifier
                )

            else:

                local_dict[identifier] = Symbol(
                    identifier
                )

        return local_dict

    ####################################################
    # NORMALIZATION
    ####################################################

    def normalize(
        self,
        expr: str
    ):

        expr = expr.replace(
            "^",
            "**"
        )

        lines = [
            " ".join(
                line.split()
            )
            for line in expr.splitlines()
            if line.strip()
        ]

        expr = "\n".join(
            lines
        )

        return expr

    ####################################################
    # TO SYMPY
    ####################################################

    def to_sympy(
        self,
        expr: str
    ):

        ############################################
        # INECUACIONES
        ############################################

        for operator, relation in (
            ("<=", Le),
            (">=", Ge),
            ("<", Lt),
            (">", Gt),
        ):

            if operator not in expr:
                continue

            lhs, rhs = expr.split(
                operator,
                1
            )

            lhs_expr = parse_expr(

                lhs,

                transformations=transformations,

                local_dict=self.build_local_dict(
                    lhs
                )
            )

            rhs_expr = parse_expr(

                rhs,

                transformations=transformations,

                local_dict=self.build_local_dict(
                    rhs
                )
            )

            return relation(
                lhs_expr,
                rhs_expr
            )

        ############################################
        # ECUACIONES
        ############################################

        if "=" in expr:

            equations = []

            for equation in expr.splitlines():

                if not equation.strip():
                    continue

                lhs, rhs = equation.split(
                    "=",
                    1
                )

                lhs_expr = parse_expr(

                    lhs,

                    transformations=transformations,

                    local_dict=self.build_local_dict(
                        lhs
                    )
                )

                rhs_expr = parse_expr(

                    rhs,

                    transformations=transformations,

                    local_dict=self.build_local_dict(
                        rhs
                    )
                )

                equations.append(
                    Eq(
                        lhs_expr,
                        rhs_expr
                    )
                )

            if len(equations) == 1:

                return equations[0]

            return equations

        ############################################
        # EXPRESIONES
        ############################################

        return parse_expr(

            expr,

            transformations=transformations,

            local_dict=self.build_local_dict(
                expr
            )
        )

    ####################################################
    # PARSE
    ####################################################

    def parse(
        self,
        text: str
    ):

        try:

            ############################################
            # EXTRACTION
            ############################################

            extracted = self.extract_math(
                text
            )

            ############################################
            # NO CONTENT
            ############################################

            if not extracted:

                result = MathParseResult(

                    original_text=text,

                    extracted_math=None,

                    normalized_latex=None,

                    sympy_repr=None,

                    sympy_expr=None,

                    math_type=None,

                    variables=[],

                    success=False,

                    error=(
                        "No mathematical "
                        "content detected."
                    )
                )

                log_parse(
                    result.to_dict()
                )

                return result

            ############################################
            # NORMALIZATION
            ############################################

            normalized = self.normalize(
                extracted
            )

            ############################################
            # SYMPY
            ############################################

            expr = self.to_sympy(
                normalized
            )

            ############################################
            # CLASSIFICATION
            ############################################

            math_type = classify_math(
                expr
            )

            structure_result = analyze_structure(
                expr
            )

            ############################################
            # VARIABLES
            ############################################

            variables = sorted(

                [
                    str(v)
                    for equation in (
                        expr
                        if isinstance(expr, list)
                        else [expr]
                    )
                    for v in equation.free_symbols
                ]
            )

            variables = sorted(
                set(variables)
            )

            ############################################
            # SUCCESS RESULT
            ############################################

            result = MathParseResult(

                original_text=text,

                extracted_math=extracted,

                normalized_latex=normalized,

                sympy_repr=str(expr),

                sympy_expr=expr,

                math_type=math_type,

                variables=variables,

                success=True,

                error=None,

                structure=structure_result.structure,

                domain=structure_result.domain,

                concept=structure_result.concept,

                difficulty=structure_result.difficulty,
            )

            log_parse(
                result.to_dict()
            )

            return result

        except Exception as e:

            ############################################
            # ERROR RESULT
            ############################################

            result = MathParseResult(

                original_text=text,

                extracted_math=None,

                normalized_latex=None,

                sympy_repr=None,

                sympy_expr=None,

                math_type=None,

                variables=[],

                success=False,

                error=str(e)
            )

            log_parse(
                result.to_dict()
            )

            return result
