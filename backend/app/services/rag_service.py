import logging
from time import perf_counter

logger = logging.getLogger(__name__)

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.document import Document
from app.models.user import User
from app.repositories.document_repository import DocumentRepository
from app.schemas.common import RAGMetadataItem
from app.schemas.solve import SolveRequest, SolveResponse, SolveSourceRead
from app.services.embedding_service import EmbeddingService
from app.services.ollama_client import OllamaClient
from app.services.topic_manager import get_topic_manager


class RAGService:
    def __init__(
        self,
        db: Session,
        ollama_client: OllamaClient | None = None,
        embedding_service: EmbeddingService | None = None,
    ) -> None:
        self.db = db
        self.settings = get_settings()
        self.ollama_client = ollama_client or OllamaClient()
        self.embedding_service = embedding_service or EmbeddingService(self.ollama_client)
        self.document_repository = DocumentRepository(db)

    def classify_query(self, query: str) -> str | None:
        """Classify the user query into one of the known topics using embeddings.

        Returns the normalized topic name if a confident match is found, otherwise None.
        """
        topic_manager = get_topic_manager()
        # Ensure topic manager has scanned and prepared embeddings
        if not topic_manager.initialized:
            try:
                topic_manager.initialize()
            except Exception:
                logger.exception("RAGService: topic manager initialization failed")
                return None

        topic_embeddings = topic_manager.get_topic_embeddings()
        if not topic_embeddings:
            return None

        # embed query
        query_embedding = self.embedding_service.embed_text(query)

        best_topic, best_score = topic_manager.find_best_match(query_embedding)
        if best_topic and best_score >= getattr(topic_manager, "threshold", 0.6):
            return best_topic
        return None

    def solve(self, *, user: User, payload: SolveRequest) -> SolveResponse:
        started_at = perf_counter()
        rag_enabled = True
        model_used = self.settings.fast_llm_model
        retrieved_documents: list[tuple[Document, float]] = []

        # If frontend didn't provide a topic, try to classify it automatically
        topic_to_use = payload.topic if payload.topic else None
        if not topic_to_use:
            try:
                classified = self.classify_query(payload.query)
                if classified:
                    topic_to_use = classified
                    logger.info("RAGService: query classified as topic '%s'", topic_to_use)
                else:
                    logger.debug("RAGService: no topic classified for query; falling back to subject/global search")
            except Exception:
                logger.exception("RAGService: topic classification failed; proceeding without topic filter")

        query_embedding = self.embedding_service.embed_text(payload.query)
        retrieved_documents = self.document_repository.retrieve_similar(
            query_embedding,
            subject=user.subject,
            topic=topic_to_use,
            limit=self.settings.rag_top_k,
        )

        prompt = self._build_prompt(
            user=user,
            query=payload.query,
            topic=topic_to_use,
            rag_enabled=rag_enabled,
            retrieved_documents=retrieved_documents,
        )
        logger.info("Enriched prompt sent to Ollama: \n%s", prompt)
        answer = self.ollama_client.generate(model=model_used, prompt=prompt)

        latency_ms = int((perf_counter() - started_at) * 1000)

        return SolveResponse(
            answer=answer,
            model_used=model_used,
            rag_enabled=rag_enabled,
            context_count=len(retrieved_documents),
            sources=[
                SolveSourceRead(
                    id=document.id,
                    source=document.source,
                    topic=document.topic,
                    chunk_index=document.chunk_index,
                )
                for document, _ in retrieved_documents
            ],
            rag_metadata=[
                RAGMetadataItem(
                    source_file=document.source,
                    chunk_index=document.chunk_index,
                    topic=document.topic,
                    similarity_score=score,
                )
                for document, score in retrieved_documents
            ],
        )

    def _build_prompt(
        self,
        *,
        user: User,
        query: str,
        topic: str | None,
        rag_enabled: bool,
        retrieved_documents: list[tuple[Document, float]],
    ) -> str:
        sections = [
            "You are a Socratic math tutor. You must follow the Zero-Reveal strategy: NEVER give the final direct answer or simplified solution.",
            "Instead, formulate guiding questions or progressive hints to help the student think and arrive at the answer themselves.",
            f"Student subject: {user.subject.value}.",
            "Explain clearly and avoid unnecessary words.",
            "Always answer in the same language as the student's question.",
            "If the retrieved context is in another language, use it only as reference and still answer in the student's language.",
            "",
            "Format all math using Markdown LaTeX strictly compatible with KaTeX:",
            "  * Inline: $expression$ (must open and close with single $)",
            "  * Block: $$expression$$ (must open and close with double $$)",
            "- CRITICAL: Always close LaTeX delimiters. If you open with $$, you MUST close with $$. If you open with $, you MUST close with $.",
            "- Prohibition: Do NOT use macros not supported by KaTeX or raw amsmath environments like \\begin{align*}.",
            "- Requirement: Breakdown multiline equations using the safe environment \\begin{aligned} ... \\end{aligned}.",
            "- Requirement: For systems of equations, strictly use \\begin{cases} ... \\end{cases}.",
        ]
        if topic:
            sections.append(f"Topic: {topic}.")
        if rag_enabled and retrieved_documents:
            context = "\n\n".join(
                f"[Source: {document.source} | Topic: {document.topic} | Chunk: {document.chunk_index} | Score: {score:.4f}]\n{document.content}"
                for document, score in retrieved_documents
            )
            sections.append("Use the provided context when it is relevant.")
            sections.append("=== CONTEXTO ACADÉMICO UCA INYECTADO ===")
            sections.append(context)
            sections.append("========================================")
        elif rag_enabled:
            sections.append("No relevant context was found. Answer with your base knowledge only.")
        sections.append(f"Student question: {query}")
        return "\n\n".join(sections)
