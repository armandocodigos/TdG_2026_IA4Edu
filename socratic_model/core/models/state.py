from dataclasses import (
    dataclass,
    asdict
)

from typing import Optional


@dataclass
class StateResult:

    previous_step: str

    current_step: str

    # ====================================================
    # TRANSFORMACIÓN
    # ====================================================

    transformation: Optional[str]

    # ====================================================
    # MATEMÁTICA
    # ====================================================

    mathematically_equivalent: bool

    mathematically_valid: bool

    # ====================================================
    # ESTRUCTURA
    # ====================================================

    structural_state: str

    # ====================================================
    # PEDAGOGÍA
    # ====================================================

    pedagogical_state: str

    progress: bool

    regression: bool

    # ====================================================
    # CONVERSACIONAL
    # ====================================================

    repetition: bool

    # ====================================================
    # SEMÁNTICO
    # ====================================================

    semantic_loop: bool

    # ====================================================
    # SISTEMA
    # ====================================================

    success: bool

    error: Optional[str]

    domain: Optional[str] = None

    concept: Optional[str] = None

    structure: Optional[str] = None

    difficulty: Optional[str] = None

    variables: Optional[list] = None

    validation_error_type: Optional[str] = None

    validation_detail: Optional[str] = None

    def to_dict(self):

        return asdict(self)
