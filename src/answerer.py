"""Answer generation using retrieved evidence."""

from __future__ import annotations

import re

from src.llm import generate_llm_answer
from src.models import ScoredChunk
from src.text_utils import split_sentences, tokenize


def build_answer(question: str, results: list[ScoredChunk], contradictions: list[dict]) -> str:
    if not results:
        return "I could not find enough SupportDesk information to answer this question."

    question_terms = set(tokenize(question))
    sentences: list[str] = []
    minimum_score = 1 if len(question_terms) <= 3 else 2
    top_score = results[0].rerank_score if results else 0.0
    answer_results = [result for result in results[:4] if result.rerank_score >= top_score * 0.45]
    for result in answer_results:
        candidates = _clean_sentences(result.chunk.text)
        ranked = sorted(
            candidates,
            key=lambda s: _sentence_score(f"{result.chunk.title} {s}", question_terms),
            reverse=True,
        )
        for sentence in ranked[:2]:
            score = _sentence_score(f"{result.chunk.title} {sentence}", question_terms)
            if score >= minimum_score and sentence not in sentences:
                sentences.append(sentence)

    evidence_answer = " ".join(sentences[:4])
    if not evidence_answer:
        return "I could not find enough SupportDesk information to answer this question."
    llm_answer = generate_llm_answer(question, evidence_answer)
    answer = _safe_llm_answer(llm_answer, evidence_answer)
    if contradictions:
        notes = []
        for item in contradictions:
            notes.append(
                f"For {item['claim']}, I used {item['chosen']['source_type']} value "
                f"{item['chosen']['value']} over {item['conflicting_values']}."
            )
        answer += " Contradiction note: " + " ".join(notes)
    return answer.strip()


def _safe_llm_answer(llm_answer: str, evidence_answer: str) -> str:
    """Use the LLM answer only when it stays close to retrieved evidence."""
    if len(llm_answer.split()) < 5:
        return evidence_answer
    evidence_terms = set(tokenize(evidence_answer))
    answer_terms = set(tokenize(llm_answer))
    if not evidence_terms or len(evidence_terms & answer_terms) / max(len(answer_terms), 1) < 0.45:
        return evidence_answer
    return llm_answer


def _clean_sentences(text: str) -> list[str]:
    cleaned = []
    for line in text.splitlines():
        role_match = re.match(r"^(customer|staff|community):\s*(.*)", line.strip(), flags=re.I)
        if role_match:
            role = role_match.group(1).lower()
            if role == "customer":
                continue
            line = role_match.group(2)
        else:
            line = line.strip()
        if line.endswith("?"):
            continue
        cleaned.extend(sentence for sentence in split_sentences(line) if not sentence.endswith("?"))
    return cleaned


def _sentence_score(sentence: str, question_terms: set[str]) -> int:
    return len(question_terms & set(tokenize(sentence)))
