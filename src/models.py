"""Shared data models for the SupportDesk RAG project."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Chunk:
    """One searchable piece of content."""

    id: str
    source_type: str
    title: str
    text: str
    metadata: dict


@dataclass
class ScoredChunk:
    """A chunk with retrieval and reranking scores."""

    chunk: Chunk
    retrieval_score: float
    weighted_score: float
    rerank_score: float = 0.0
    reasons: list[str] = field(default_factory=list)
