from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RAGMetadataItem(BaseModel):
    source_file: str
    chunk_index: int
    topic: str
    similarity_score: float
