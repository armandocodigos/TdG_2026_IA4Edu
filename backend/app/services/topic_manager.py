from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from app.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)


class TopicManager:
    """Service that scans the datasets folder for topic files and precomputes
    representative embeddings for fast topic classification.

    Use ``get_topic_manager()`` to obtain the singleton instance.
    """

    def __init__(self, base_dir: Optional[Path] = None, embedding_service: Optional[EmbeddingService] = None) -> None:
        self.base_dir = base_dir or Path(__file__).resolve().parents[2]
        self.datasets_dir = self.base_dir / "datasets"
        self.embedding_service = embedding_service or EmbeddingService()

        # mapping: normalized topic name -> absolute file path (first found)
        self.topics: Dict[str, str] = {}
        # mapping: normalized topic name -> embedding vector
        self.topic_embeddings: Dict[str, List[float]] = {}

        self.initialized = False

        # threshold can be tuned via env var TOPIC_SIMILARITY_THRESHOLD (default 0.6)
        try:
            self.threshold = float(os.getenv("TOPIC_SIMILARITY_THRESHOLD", "0.6"))
        except Exception:
            self.threshold = 0.6

    def initialize(self) -> None:
        if self.initialized:
            logger.debug("TopicManager: already initialized")
            return

        logger.info("TopicManager: scanning datasets to collect topics: %s", self.datasets_dir)
        self._scan_datasets()
        if self.topics:
            self._build_topic_embeddings()
        self.initialized = True
        logger.info("TopicManager: initialized with %d topics", len(self.topics))

    def _scan_datasets(self) -> None:
        SUPPORTED = {".md", ".txt"}
        IGNORED = {"readme.md", "readme.txt"}

        targets = [self.datasets_dir / "precalculo", self.datasets_dir / "preuniversitario"]
        for directory in targets:
            if not directory.exists():
                logger.debug("TopicManager: dataset dir not found: %s", directory)
                continue

            for path in directory.rglob("*"):
                if not path.is_file():
                    continue
                if path.suffix.lower() not in SUPPORTED:
                    continue
                if path.name.lower() in IGNORED:
                    continue

                # Normalize topic name from filename
                topic = path.stem.replace("_", " ").replace("-", " ").strip().lower() or "general"

                # Keep the first occurrence to build a simple name->file map
                if topic in self.topics:
                    continue
                try:
                    self.topics[topic] = str(path.resolve())
                except Exception:
                    self.topics[topic] = str(path)

    def _build_topic_embeddings(self) -> None:
        logger.info("TopicManager: computing embeddings for %d topics", len(self.topics))
        for topic in list(self.topics.keys()):
            try:
                emb = self.embedding_service.embed_text(topic)
            except Exception as exc:  # pragma: no cover - runtime failure of remote embed
                logger.exception("TopicManager: failed to embed topic '%s': %s", topic, exc)
                continue
            self.topic_embeddings[topic] = emb

    def get_topics(self) -> Dict[str, str]:
        return dict(self.topics)

    def get_topic_embeddings(self) -> Dict[str, List[float]]:
        return dict(self.topic_embeddings)

    def find_best_match(self, query_embedding: List[float]) -> Tuple[Optional[str], float]:
        """Return (best_topic_name, similarity) or (None, 0.0) if nothing suitable."""
        import math

        best_topic: Optional[str] = None
        best_score = -1.0
        for topic, emb in self.topic_embeddings.items():
            if not emb or len(emb) != len(query_embedding):
                continue
            numerator = sum(a * b for a, b in zip(query_embedding, emb))
            left_norm = math.sqrt(sum(a * a for a in query_embedding))
            right_norm = math.sqrt(sum(b * b for b in emb))
            if left_norm == 0 or right_norm == 0:
                continue
            sim = numerator / (left_norm * right_norm)
            if sim > best_score:
                best_score = sim
                best_topic = topic

        if best_topic is None:
            return None, 0.0
        return best_topic, float(best_score)


# Module-level singleton
_TOPIC_MANAGER: Optional[TopicManager] = None


def get_topic_manager() -> TopicManager:
    global _TOPIC_MANAGER
    if _TOPIC_MANAGER is None:
        _TOPIC_MANAGER = TopicManager()
    return _TOPIC_MANAGER
