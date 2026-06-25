from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class SemanticStateResult:

    previous_step: str

    current_step: str

    canonical_state: str

    semantic_repeat: bool

    semantic_loop: bool

    semantic_progress: bool

    success: bool

    error: Optional[str]

    def to_dict(self):

        return asdict(self)