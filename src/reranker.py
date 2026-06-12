"""Simple reranking layer used after retrieval."""

from __future__ import annotations

from src.models import ScoredChunk
from src.text_utils import tokenize


AUTHORITY = {
    "docs": 3,
    "blog": 2,
    "forum": 1,
}


def rerank(question: str, results: list[ScoredChunk], top_k: int = 5) -> list[ScoredChunk]:
    question_terms = set(tokenize(question))
    for result in results:
        chunk_terms = set(tokenize(f"{result.chunk.title} {result.chunk.text}"))
        overlap = len(question_terms & chunk_terms) / max(len(question_terms), 1)
        authority_boost = AUTHORITY[result.chunk.source_type] * 0.03
        title_boost = 0.05 * len(question_terms & set(tokenize(result.chunk.title)))
        result.rerank_score = result.weighted_score + overlap + authority_boost + title_boost
        result.reasons.extend(
            [
                f"overlap={overlap:.3f}",
                f"authority={AUTHORITY[result.chunk.source_type]}",
            ]
        )
    return sorted(results, key=lambda item: item.rerank_score, reverse=True)[:top_k]
