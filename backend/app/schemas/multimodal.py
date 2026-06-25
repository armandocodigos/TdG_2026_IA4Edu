from pydantic import BaseModel
from typing import Optional, Dict, Any


class MultimodalResponse(BaseModel):
    status: str
    file_type: str
    latex_content: str
    raw_transcription: str
    metadata: Dict[str, Any]
