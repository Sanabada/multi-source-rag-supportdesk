"""Run the required 10 example queries and save responses."""

from __future__ import annotations

import json
from pathlib import Path

from src.multi_source_rag import SupportDeskRAG, format_result


ROOT = Path(__file__).resolve().parent
QUERIES_PATH = ROOT / "examples" / "queries.json"
OUTPUT_PATH = ROOT / "examples" / "example_responses.md"


def main() -> None:
    queries = json.loads(QUERIES_PATH.read_text(encoding="utf-8"))
    rag = SupportDeskRAG()
    sections = ["# Example Queries and Responses", ""]
    for index, query in enumerate(queries, start=1):
        result = rag.ask(query)
        sections.append(f"## {index}. {query}")
        sections.append("")
        sections.append("```text")
        sections.append(format_result(result))
        sections.append("```")
        sections.append("")
    OUTPUT_PATH.write_text("\n".join(sections), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
