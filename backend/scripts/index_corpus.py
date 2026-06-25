from pathlib import Path
import re

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import SessionLocal
from app.models.document import Document
from app.models.enums import Subject
from app.repositories.document_repository import DocumentRepository
from app.services.embedding_service import EmbeddingService
from app.utils.text_chunker import chunk_text


SUPPORTED_EXTENSIONS = {".md", ".txt"}
IGNORED_FILENAMES = {"readme.md", "readme.txt"}


def should_index_file(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return False
    if path.name.lower() in IGNORED_FILENAMES:
        return False
    return True


def infer_subject_from_path(path: Path) -> Subject:
    lowered = str(path).lower()
    if "preuniversitario" in lowered:
        return Subject.PREUNIVERSITARIO
    return Subject.PRECALCULO


def infer_topic_from_path(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ").strip().lower() or "general"


def parse_front_matter(content: str) -> tuple[dict, str]:
    if content.startswith("---"):
        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if match:
            fm_text = match.group(1)
            clean_content = content[match.end():]
            
            metadata = {}
            for line in fm_text.splitlines():
                if ":" in line:
                    key, val = line.split(":", 1)
                    metadata[key.strip().lower()] = val.strip()
            return metadata, clean_content
    return {}, content


def map_subject(subject_str: str, default: Subject) -> Subject:
    if not subject_str:
        return default
    subject_str_lower = subject_str.lower()
    for name, member in Subject.__members__.items():
        if name.lower() == subject_str_lower or str(member.value).lower() == subject_str_lower:
            return member
    return default


def index_directory(directory: Path, db: Session) -> int:
    settings = get_settings()
    embedding_service = EmbeddingService()
    repository = DocumentRepository(db)

    files = [path for path in directory.rglob("*") if should_index_file(path)]
    total_chunks = 0
    all_documents = []

    for file_path in files:
        raw_content = file_path.read_text(encoding="utf-8")
        fm_metadata, clean_content = parse_front_matter(raw_content)

        # Mecanismo de Contingencia Absoluta (Fallback)
        fallback_subject = infer_subject_from_path(file_path)
        fallback_topic = infer_topic_from_path(file_path)

        subject_str = fm_metadata.pop("subject", None)
        subject = map_subject(subject_str, fallback_subject) if subject_str else fallback_subject
        topic = fm_metadata.pop("topic", fallback_topic)

        metadata_json = {"source_path": str(file_path)}
        # Agregar los metadatos restantes de Front Matter al JSON (ej. content_type)
        metadata_json.update(fm_metadata)

        chunks = chunk_text(clean_content, settings.rag_chunk_size, settings.rag_chunk_overlap)
        
        for index, chunk in enumerate(chunks):
            all_documents.append(
                Document(
                    source=str(file_path.relative_to(directory)),
                    topic=topic,
                    subject=subject,
                    content=chunk,
                    embedding=embedding_service.embed_text(chunk),
                    chunk_index=index,
                    metadata_json=metadata_json,
                )
            )
            total_chunks += 1

    # Inserción masiva optimizada en una sola llamada a DB (Batching)
    if all_documents:
        repository.create_many(all_documents)
        
    db.commit()
    return total_chunks


def main() -> None:
    settings = get_settings()
    base_dir = Path(__file__).resolve().parents[2]
    dataset_dir = base_dir / "datasets"

    if not dataset_dir.exists():
        raise SystemExit(f"Dataset directory not found: {dataset_dir}")

    db = SessionLocal()
    try:
        repository = DocumentRepository(db)
        repository.delete_all()
        indexed = index_directory(dataset_dir, db)
    finally:
        db.close()

    print(f"Indexed {indexed} chunks from {dataset_dir} using {settings.embedding_model}.")


if __name__ == "__main__":
    main()
