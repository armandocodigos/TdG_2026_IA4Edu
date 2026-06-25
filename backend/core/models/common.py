from dataclasses import dataclass, asdict
from typing import Optional, List, Any


@dataclass
class MathParseResult:

    original_text: str

    extracted_math: Optional[str]

    normalized_latex: Optional[str]

    sympy_repr: Optional[str]

    sympy_expr: Optional[Any]

    math_type: Optional[str]

    variables: List[str]

    success: bool

    error: Optional[str]

    structure: Optional[str] = None

    domain: Optional[str] = None

    concept: Optional[str] = None

    difficulty: Optional[str] = None

    def to_dict(self):

        data = asdict(self)

        # evitar serializar objeto sympy
        data["sympy_expr"] = str(
            self.sympy_expr
        )

        return data
