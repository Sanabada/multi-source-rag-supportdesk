"""Rule-based contradiction handling for simple support facts."""

from __future__ import annotations

import re

from src.models import ScoredChunk


SOURCE_PRIORITY = {
    "docs": 3,
    "blog": 2,
    "forum": 1,
}

CLAIM_PATTERNS = {
    "refund_period_days": re.compile(r"\b(14|30)\s+days?\b", re.I),
}


def detect_contradictions(question: str, results: list[ScoredChunk]) -> list[dict]:
    active_claims = _active_claims(question)
    contradictions: list[dict] = []

    for claim, pattern in CLAIM_PATTERNS.items():
        if claim not in active_claims:
            continue
        evidence = []
        for result in results:
            combined = f"{result.chunk.title} {result.chunk.text}"
            for match in pattern.finditer(combined):
                evidence.append(
                    {
                        "value": match.group(1),
                        "source_id": result.chunk.id,
                        "source_type": result.chunk.source_type,
                        "title": result.chunk.title,
                        "priority": SOURCE_PRIORITY[result.chunk.source_type],
                    }
                )
        values = {item["value"] for item in evidence}
        if len(values) > 1:
            chosen = sorted(evidence, key=lambda item: item["priority"], reverse=True)[0]
            contradictions.append(
                {
                    "claim": claim,
                    "chosen": chosen,
                    "conflicting_values": sorted(values - {chosen["value"]}),
                    "evidence": evidence,
                }
            )
    return contradictions


def _active_claims(question: str) -> set[str]:
    text = question.lower()
    claims = set()
    if "refund" in text:
        claims.add("refund_period_days")
    return claims
