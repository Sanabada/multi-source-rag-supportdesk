"""End-to-end SupportDesk multi-source RAG pipeline."""

from __future__ import annotations

import argparse
import json
import warnings
from typing import TypedDict

warnings.filterwarnings("ignore")

from langgraph.graph import END, StateGraph

from src.answerer import build_answer
from src.contradictions import detect_contradictions
from src.loaders import load_all_chunks
from src.models import ScoredChunk
from src import rag_logger
from src.reranker import rerank
from src.retriever import Retriever


class RAGState(TypedDict, total=False):
    question: str
    retrieved: list[ScoredChunk]
    ranked: list[ScoredChunk]
    contradictions: list[dict]
    answer: str
    sources: list[dict]
    result: dict
    top_k: int


class SupportDeskRAG:
    """Small RAG application used by the CLI, examples, and tests."""

    def __init__(self) -> None:
        self.chunks = load_all_chunks()
        self.retriever = Retriever(self.chunks)
        self.graph = self._build_graph()

    def ask(self, question: str, top_k: int = 5) -> dict:
        state = self.graph.invoke({"question": question, "top_k": top_k})
        return state["result"]

    def _build_graph(self):
        graph = StateGraph(RAGState)
        graph.add_node("retrieve", self._retrieve)
        graph.add_node("rerank", self._rerank)
        graph.add_node("check_contradictions", self._check_contradictions)
        graph.add_node("generate_answer", self._generate_answer)
        graph.add_node("log_response", self._log_response)
        graph.set_entry_point("retrieve")
        graph.add_edge("retrieve", "rerank")
        graph.add_edge("rerank", "check_contradictions")
        graph.add_edge("check_contradictions", "generate_answer")
        graph.add_edge("generate_answer", "log_response")
        graph.add_edge("log_response", END)
        return graph.compile()

    def _retrieve(self, state: RAGState) -> RAGState:
        return {"retrieved": self.retriever.search(state["question"], top_k=8)}

    def _rerank(self, state: RAGState) -> RAGState:
        top_k = int(state.get("top_k", 5))
        return {"ranked": rerank(state["question"], state["retrieved"], top_k=top_k)}

    def _check_contradictions(self, state: RAGState) -> RAGState:
        return {"contradictions": detect_contradictions(state["question"], state["ranked"])}

    def _generate_answer(self, state: RAGState) -> RAGState:
        ranked = state["ranked"]
        contradictions = state["contradictions"]
        answer = build_answer(state["question"], ranked, contradictions)
        sources = [
            {
                "id": item.chunk.id,
                "type": item.chunk.source_type,
                "title": item.chunk.title,
                "score": round(item.rerank_score, 4),
                "file": item.chunk.metadata.get("file"),
                "reasons": item.reasons,
            }
            for item in ranked
        ]
        result = {
            "question": state["question"],
            "answer": answer,
            "sources": sources,
            "contradictions": contradictions,
        }
        return {"answer": answer, "sources": sources, "result": result}

    def _log_response(self, state: RAGState) -> RAGState:
        rag_logger.log_response(
            state["question"],
            state["answer"],
            state["sources"],
            state["contradictions"],
        )
        return state


def format_result(result: dict) -> str:
    lines = [f"Question: {result['question']}", f"Answer: {result['answer']}", "Sources used:"]
    for source in result["sources"]:
        lines.append(f"- {source['id']} [{source['type']}] {source['title']} score={source['score']}")
    if result["contradictions"]:
        lines.append("Contradictions:")
        for item in result["contradictions"]:
            lines.append(f"- {item['claim']}: chose {item['chosen']['value']} over {item['conflicting_values']}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask the SupportDesk RAG system a support question.")
    parser.add_argument("question", nargs="+")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    app = SupportDeskRAG()
    result = app.ask(" ".join(args.question))
    print(json.dumps(result, indent=2) if args.json else format_result(result))


if __name__ == "__main__":
    main()
