"""Performance analysis for retrieval and reranking."""

from __future__ import annotations

import json
import statistics
import time
from pathlib import Path

from src.loaders import load_all_chunks
from src.reranker import rerank
from src.retriever import Retriever


ROOT = Path(__file__).resolve().parent
REPORT_PATH = ROOT / "reports" / "performance_metrics.json"


GOLDEN = [
    {"question": "How long is a password reset link valid?", "relevant": {"doc:supportdesk_docs:2", "forum:F-1001", "blog:supportdesk_release_blog:4"}},
    {"question": "Why is my account locked after failed login attempts?", "relevant": {"doc:supportdesk_docs:1", "blog:supportdesk_release_blog:4"}},
    {"question": "What is the refund policy for paid subscriptions?", "relevant": {"doc:supportdesk_docs:4", "forum:F-1002", "blog:supportdesk_admin_tips:1"}},
    {"question": "Why is my mobile app not syncing ticket comments?", "relevant": {"doc:supportdesk_docs:5", "forum:F-1003", "blog:supportdesk_release_blog:1", "blog:supportdesk_admin_tips:4"}},
    {"question": "What is the maximum attachment size on the Team plan?", "relevant": {"doc:supportdesk_docs:6", "forum:F-1004", "blog:supportdesk_release_blog:2"}},
    {"question": "What should I do if the web app keeps crashing?", "relevant": {"doc:supportdesk_docs:7", "forum:F-1005", "blog:supportdesk_admin_tips:2"}},
    {"question": "How many agents and tickets are included in the Free plan?", "relevant": {"doc:supportdesk_docs:3", "forum:F-1006", "blog:supportdesk_admin_tips:3"}},
    {"question": "Can admins schedule ticket exports?", "relevant": {"doc:supportdesk_docs:8", "blog:supportdesk_release_blog:3"}},
]


def precision_at_k(ids: list[str], relevant: set[str], k: int) -> float:
    return len(set(ids[:k]) & relevant) / k


def recall_at_k(ids: list[str], relevant: set[str], k: int) -> float:
    return len(set(ids[:k]) & relevant) / len(relevant)


def reciprocal_rank(ids: list[str], relevant: set[str]) -> float:
    for index, chunk_id in enumerate(ids, start=1):
        if chunk_id in relevant:
            return 1 / index
    return 0.0


def main() -> None:
    chunks = load_all_chunks()
    retriever = Retriever(chunks)
    raw_rows = []
    reranked_rows = []
    latencies = []

    for item in GOLDEN:
        start = time.perf_counter()
        retrieved = retriever.search(item["question"], top_k=8)
        ranked = rerank(item["question"], retrieved, top_k=5)
        latencies.append((time.perf_counter() - start) * 1000)

        raw_ids = [result.chunk.id for result in retrieved[:5]]
        reranked_ids = [result.chunk.id for result in ranked]
        relevant = item["relevant"]
        raw_rows.append(_metrics(raw_ids, relevant))
        reranked_rows.append(_metrics(reranked_ids, relevant))

    output = {
        "dataset_size": {"queries": len(GOLDEN), "chunks": len(chunks)},
        "raw_retrieval": _average(raw_rows),
        "reranked": _average(reranked_rows),
        "latency_ms": {
            "mean": round(statistics.mean(latencies), 3),
            "max": round(max(latencies), 3),
        },
    }
    REPORT_PATH.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


def _metrics(ids: list[str], relevant: set[str]) -> dict:
    return {
        "precision_at_3": precision_at_k(ids, relevant, 3),
        "recall_at_5": recall_at_k(ids, relevant, 5),
        "mrr": reciprocal_rank(ids, relevant),
    }


def _average(rows: list[dict]) -> dict:
    return {key: round(statistics.mean(row[key] for row in rows), 3) for key in rows[0]}


if __name__ == "__main__":
    main()
