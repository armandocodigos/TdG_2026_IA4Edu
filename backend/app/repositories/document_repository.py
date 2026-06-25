from math import sqrt

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.enums import Subject
from app.services.embedding_service import EmbeddingService


class DocumentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_many(self, documents: list[Document]) -> list[Document]:
        self.db.add_all(documents)
        self.db.flush()
        return documents

    def delete_all(self) -> None:
        self.db.query(Document).delete()
        self.db.flush()

    def retrieve_similar(
        self,
        query_embedding: list[float],
        *,
        subject: Subject | None = None,
        topic: str | None = None,
        limit: int = 3,
    ) -> list[tuple[Document, float]]:
        dialect = self.db.bind.dialect.name if self.db.bind else ""
        if dialect == "postgresql":
            return self._retrieve_postgres(query_embedding, subject=subject, topic=topic, limit=limit)
        return self._retrieve_python(query_embedding, subject=subject, topic=topic, limit=limit)

    def _retrieve_postgres(
        self,
        query_embedding: list[float],
        *,
        subject: Subject | None,
        topic: str | None,
        limit: int,
    ) -> list[tuple[Document, float]]:
        vector_literal = "[" + ",".join(str(value) for value in query_embedding) + "]"
        conditions = ["embedding IS NOT NULL"]
        params: dict[str, object] = {
            "vector": vector_literal,
            "limit": limit,
        }

        if subject is not None:
            conditions.append("subject = :subject")
            params["subject"] = subject.value

        if topic:
            conditions.append("topic = :topic")
            params["topic"] = topic

        sql = f"""
            SELECT id, 1 - (embedding <=> CAST(:vector AS vector)) AS similarity_score
            FROM documents
            WHERE {' AND '.join(conditions)}
            ORDER BY embedding <=> CAST(:vector AS vector)
            LIMIT :limit
        """
        rows = self.db.execute(text(sql), params).fetchall()
        id_to_score = {row[0]: float(row[1]) for row in rows}
        if not id_to_score:
            return []
        documents = self.db.execute(select(Document).where(Document.id.in_(id_to_score.keys()))).scalars().all()
        return [(document, id_to_score[document.id]) for document in documents]

    def _retrieve_python(
        self,
        query_embedding: list[float],
        *,
        subject: Subject | None,
        topic: str | None,
        limit: int,
    ) -> list[tuple[Document, float]]:
        stmt = select(Document)
        if subject:
            stmt = stmt.where(Document.subject == subject)
        if topic:
            stmt = stmt.where(Document.topic == topic)

        documents = self.db.execute(stmt).scalars().all()
        scored = [
            (document, self._cosine_similarity(query_embedding, document.embedding or []))
            for document in documents
            if document.embedding
        ]
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:limit]

    @staticmethod
    def _cosine_similarity(left: list[float], right: list[float]) -> float:
        if not left or not right or len(left) != len(right):
            return -1.0
        numerator = sum(a * b for a, b in zip(left, right, strict=True))
        left_norm = sqrt(sum(value * value for value in left))
        right_norm = sqrt(sum(value * value for value in right))
        if left_norm == 0 or right_norm == 0:
            return -1.0
        return numerator / (left_norm * right_norm)

    def generate_topic_embeddings(self, topics: list[str], embedding_service: EmbeddingService) -> dict[str, list[float]]:
        """Optional helper: compute embeddings for a list of topic names.

        Returns a mapping topic_name -> embedding vector. This is a convenience
        method that can be used at startup if topic embeddings are desired
        to be produced from repository-level code.
        """
        results: dict[str, list[float]] = {}
        for topic in topics:
            try:
                results[topic] = embedding_service.embed_text(topic)
            except Exception:
                # don't fail hard from here; caller may handle missing vectors
                continue
        return results
