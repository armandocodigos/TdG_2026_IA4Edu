from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class TransformationResult:

    original_expr: str

    student_expr: str

    equivalent: bool

    transformation: Optional[str]

    details: Optional[str]

    success: bool

    error: Optional[str]

    def to_dict(self):

        return asdict(self)