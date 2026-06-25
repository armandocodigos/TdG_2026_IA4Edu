import logging
import re
from time import perf_counter

logger = logging.getLogger(__name__)

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.document import Document
from app.models.user import User
from app.repositories.document_repository import DocumentRepository
from app.schemas.common import RAGMetadataItem
from app.schemas.fast_chat import FastChatRequest, FastChatResponse, FastChatSourceRead
from app.services.embedding_service import EmbeddingService
from app.services.ollama_client import OllamaClient


class FastChatService:
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

    def answer(self, *, user: User, payload: FastChatRequest, extracted_content: str | None = None) -> FastChatResponse:
        print(f"[FastChat Service] Received payload from user {user.id}: {payload}, extracted_content_length={len(extracted_content) if extracted_content else 0}")
        started_at = perf_counter()
        model_used = self.settings.fast_chat_model
        rag_enabled = payload.use_rag
        retrieved_documents: list[tuple[Document, float]] = []

        if rag_enabled:
            query_embedding = self.embedding_service.embed_text(payload.query)
            retrieved_documents = self.document_repository.retrieve_similar(
                query_embedding,
                subject=user.subject,
                topic=payload.topic,
                limit=self.settings.rag_top_k,
            )

        print(f"[FastChat Service] Retrieved {len(retrieved_documents)} documents")

        prompt = self._build_prompt(
            user=user,
            query=payload.query,
            topic=payload.topic,
            rag_enabled=rag_enabled,
            retrieved_documents=retrieved_documents,
            extracted_content=extracted_content,
        )

        logger.info("Enriched prompt sent to Ollama: \n%s", prompt)

        answer = self.ollama_client.generate(model=model_used, prompt=prompt)

        answer = self._clean_math_formatting(answer)

        return FastChatResponse(
            answer=answer,
            model_used=model_used,
            rag_enabled=rag_enabled,
            context_count=len(retrieved_documents),
            sources=[
                FastChatSourceRead(
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
            latency_ms=int((perf_counter() - started_at) * 1000),
        )

    def _build_prompt(
        self,
        *,
        user: User,
        query: str,
        topic: str | None,
        rag_enabled: bool,
        retrieved_documents: list[tuple[Document, float]],
        extracted_content: str | None = None,
    ) -> str:
        sections = [
            "You are a highly precise and efficient math tutor specialized in pre-calculus and calculus.",

            "Your goal is to produce correct, minimal, and well-justified solutions.",

            "Reasoning protocol (follow strictly):",
            "1. Identify the type of problem (algebra, derivative, integral, limits, etc.).",
            "2. Extract key data and rewrite the problem in mathematical form if needed.",
            "3. Solve step-by-step, showing only essential transformations.",
            "4. Perform a quick validation of the result (substitution, derivative check, simplification, etc.).",
            "5. Present the final answer clearly.",

            "Style rules:",
            "- Be direct and concise.",
            "- Show only necessary steps, but never skip critical transformations.",
            "- Use clear and correct mathematical notation.",
            "- Format all math using Markdown LaTeX strictly compatible with KaTeX:",
            "  * Inline: $expression$ (must open and close with single $)",
            "  * Block: $$expression$$ (must open and close with double $$)",
            "- CRITICAL: Always close LaTeX delimiters. If you open with $$, you MUST close with $$. If you open with $, you MUST close with $.",
            "- Every mathematical expression must be wrapped in either $ $ or $$ $$.",
            "- Prohibition: Do NOT use macros not supported by KaTeX or raw amsmath environments like \\begin{align*}.",
            "- Requirement: Breakdown multiline equations using the safe environment \\begin{aligned} ... \\end{aligned}.",
            "- Requirement: For systems of equations, strictly use \\begin{cases} ... \\end{cases}.",
            "- Do NOT use square brackets [ ] for math expressions.",
            "- Do NOT use backslash-parenthesis \\( \\) or backslash-bracket \\[ \\] delimiters.",
            "- Do NOT add explanations outside math unless strictly needed.",
            "- Do NOT include conversational filler text.",

            "Answer structure:",
            "- If the solution is short, give a compact explanation + final result.",
            "- If multi-step, use a clean progression of steps.",
            "- Always include the final answer in a separate line or block.",

            "Robustness rules:",
            "- If the question is not related to mathematics (pre-calculus or calculus), respond with: 'Solo puedo responder preguntas relacionadas a matemáticas.' and nothing else.",
            "- If the problem is ambiguous or missing data, ask ONE concise clarification question.",
            "- If multiple interpretations exist, choose the most standard one and state the assumption briefly.",
            "- If the result is undefined or does not exist, explicitly state it.",

            f"Student subject: {user.subject.value}.",
        ]
        if topic:
            sections.append(f"Requested topic: {topic}.")
        if rag_enabled and retrieved_documents:
            context = "\n\n".join(
                f"[Source: {document.source} | Topic: {document.topic} | Chunk: {document.chunk_index} | Score: {score:.4f}]\n{document.content}"
                for document, score in retrieved_documents
            )
            sections.append(
                "Use the provided context ONLY if the user's question is related to mathematics. Otherwise, ignore it."
            )
            sections.append("=== CONTEXTO ACADÉMICO UCA INYECTADO ===")
            sections.append(context)
            sections.append("========================================")
        elif rag_enabled:
            sections.append("No relevant context was found. Answer with your base knowledge only.")
            
        if extracted_content:
            sections.append("CONTEXTO ADJUNTO POR EL ESTUDIANTE:")
            sections.append(extracted_content)
            sections.append("PREGUNTA DEL ESTUDIANTE:")
            sections.append(query)
        else:
            sections.append(f"Student question: {query}")
            
        return "\n\n".join(sections)

    def _clean_math_formatting(self, response: str) -> str:
        """
        Post-processes the response to ensure proper LaTeX formatting.
        This function corrects common formatting issues from the language model.
        """
        response = response.replace("\\[", "$$").replace("\\]", "$$")
        response = response.replace("\\(", "$").replace("\\)", "$")
        response = re.sub(r"([^\n])\$\$", r"\1\n$$", response)
        response = re.sub(r"\$\$([^\n])", r"$$\n\1", response)

        if len(response.split("$$")) % 2 == 0:
            response = f"{response}\n$$"

        cleaned = response.strip()
        if self._has_unbalanced_math_delimiters(cleaned):
            return self._escape_unbalanced_math(cleaned)
        return cleaned

    def _has_unbalanced_math_delimiters(self, text: str) -> bool:
        block_count = len(re.findall(r"(?<!\\)\$\$", text))
        if block_count % 2 == 1:
            return True

        without_blocks = re.sub(r"(?s)(?<!\\)\$\$.*?(?<!\\)\$\$", "", text)
        inline_count = len(re.findall(r"(?<!\\)\$(?!\$)", without_blocks))
        return inline_count % 2 == 1

    def _escape_unbalanced_math(self, text: str) -> str:
        lines = text.split("\n")
        escaped_lines: list[str] = []

        for line in lines:
            without_blocks = re.sub(r"\$\$[^$]*\$\$", "", line)
            single_dollar_count = len(re.findall(r"(?<!\\)\$(?!\$)", without_blocks))
            if single_dollar_count % 2 == 1:
                last_index = line.rfind("$")
                while last_index > 0 and line[last_index - 1] == "\\":
                    last_index = line.rfind("$", 0, last_index)
                if last_index >= 0:
                    line = f"{line[:last_index]}\\{line[last_index:]}"
            escaped_lines.append(line)

        return "\n".join(escaped_lines)

