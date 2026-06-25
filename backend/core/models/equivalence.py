from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class EquivalenceResult:

    original_expr: str
    student_expr: str

    equivalent: bool

    error_type: Optional[str]

    details: Optional[str]

    success: bool

    def to_dict(self):
        return asdict(self)