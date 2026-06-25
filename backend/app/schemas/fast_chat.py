from pydantic import BaseModel, ConfigDict, Field
from app.schemas.common import RAGMetadataItem


class FastChatRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=4000)
    topic: str | None = Field(default=None, max_length=200)
    use_rag: bool = Field(default=False)


class FastChatSourceRead(BaseModel):
    id: str
    source: str
    topic: str
    chunk_index: int


class FastChatResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    answer: str
    model_used: str
    rag_enabled: bool
    context_count: int
    sources: list[FastChatSourceRead]
    rag_metadata: list[RAGMetadataItem]
    latency_ms: int
