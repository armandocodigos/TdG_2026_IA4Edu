from pydantic import BaseModel, ConfigDict, Field
from app.schemas.common import RAGMetadataItem


class SolveRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=4000)
    topic: str | None = Field(default=None, max_length=200)


class SolveSourceRead(BaseModel):
    id: str
    source: str
    topic: str
    chunk_index: int


class SolveResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    answer: str
    model_used: str
    rag_enabled: bool
    context_count: int
    sources: list[SolveSourceRead]
    rag_metadata: list[RAGMetadataItem]
