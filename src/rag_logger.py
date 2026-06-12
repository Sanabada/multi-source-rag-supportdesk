"""JSONL logging for source traceability."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "logs" / "retrieval_log.jsonl"


def log_response(question: str, answer: str, sources: list[dict], contradictions: list[dict]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "question": question,
        "answer": answer,
        "sources_used": sources,
        "contradictions": contradictions,
    }
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
