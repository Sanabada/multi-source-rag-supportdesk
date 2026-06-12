"""First-stage retrieval and source weighting."""

from __future__ import annotations

import math
from collections import Counter

from src.models import Chunk, ScoredChunk
from src.text_utils import tokenize


SOURCE_WEIGHTS = {
    "docs": 1.30,
    "blog": 1.10,
    "forum": 0.95,
}


class Retriever:
    """A small local retriever that follows the same idea as vector search.

    It uses TF-IDF cosine similarity so the project works without paid APIs,
    external vector databases, or model downloads.
    """

    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        self.chunk_tokens = [tokenize(f"{c.title} {c.text}") for c in chunks]
        self.idf = self._build_idf()
        self.vectors = [self._tfidf(tokens) for tokens in self.chunk_tokens]

    def search(self, question: str, top_k: int = 8) -> list[ScoredChunk]:
        query_vector = self._tfidf(tokenize(question))
        scored: list[ScoredChunk] = []
        for chunk, vector in zip(self.chunks, self.vectors):
            base = self._cosine(query_vector, vector)
            if base <= 0:
                continue
            source_weight = SOURCE_WEIGHTS[chunk.source_type]
            quality_boost = 0.10 if chunk.metadata.get("accepted_answer") else 0.0
            weighted = (base * source_weight) + quality_boost
            scored.append(
                ScoredChunk(
                    chunk=chunk,
                    retrieval_score=base,
                    weighted_score=weighted,
                    reasons=[
                        f"tfidf={base:.3f}",
                        f"source_weight={source_weight}",
                    ],
                )
            )
        return sorted(scored, key=lambda item: item.weighted_score, reverse=True)[:top_k]

    def _build_idf(self) -> dict[str, float]:
        doc_count = len(self.chunk_tokens)
        df: Counter[str] = Counter()
        for tokens in self.chunk_tokens:
            df.update(set(tokens))
        return {term: math.log((doc_count + 1) / (count + 1)) + 1 for term, count in df.items()}

    def _tfidf(self, tokens: list[str]) -> dict[str, float]:
        counts = Counter(tokens)
        total = sum(counts.values()) or 1
        return {term: (count / total) * self.idf.get(term, 1.0) for term, count in counts.items()}

    @staticmethod
    def _cosine(left: dict[str, float], right: dict[str, float]) -> float:
        shared = set(left) & set(right)
        numerator = sum(left[t] * right[t] for t in shared)
        left_norm = math.sqrt(sum(v * v for v in left.values()))
        right_norm = math.sqrt(sum(v * v for v in right.values()))
        if left_norm == 0 or right_norm == 0:
            return 0.0
        return numerator / (left_norm * right_norm)
