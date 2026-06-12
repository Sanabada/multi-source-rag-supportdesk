"""Load and chunk documentation, forum, and blog sources."""

from __future__ import annotations

import json
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.models import Chunk


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def load_docs(path: Path) -> list[Chunk]:
    """Documentation is chunked by heading because each heading is one product topic."""
    return _load_markdown_sections(path, source_type="docs", prefix="doc")


def load_blogs(paths: list[Path]) -> list[Chunk]:
    """Blogs are chunked by section because each section describes one update or tip."""
    chunks: list[Chunk] = []
    for path in paths:
        chunks.extend(_load_markdown_sections(path, source_type="blog", prefix="blog"))
    return chunks


def load_forums(path: Path) -> list[Chunk]:
    """Forums are chunked by full thread so the question and answer stay together."""
    chunks: list[Chunk] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        thread = json.loads(line)
        text = "\n".join(f"{post['author']}: {post['text']}" for post in thread["posts"])
        chunks.append(
            Chunk(
                id=f"forum:{thread['thread_id']}",
                source_type="forum",
                title=thread["title"],
                text=text,
                metadata={
                    "thread_id": thread["thread_id"],
                    "date": thread["date"],
                    "accepted_answer": thread["accepted_answer"],
                    "file": str(path.relative_to(ROOT)),
                },
            )
        )
    return chunks


def load_all_chunks(data_dir: Path = DATA_DIR) -> list[Chunk]:
    """Load all sources, represent them as LangChain Documents, then return chunks."""
    chunks = []
    for chunk in [
        *load_docs(data_dir / "docs" / "supportdesk_docs.md"),
        *load_forums(data_dir / "forums" / "forum_threads.jsonl"),
        *load_blogs(sorted((data_dir / "blogs").glob("*.md"))),
    ]:
        chunks.extend(_split_with_langchain(chunk))
    return chunks


def _load_markdown_sections(path: Path, source_type: str, prefix: str) -> list[Chunk]:
    text = path.read_text(encoding="utf-8")
    chunks: list[Chunk] = []
    title = "Overview"
    lines: list[str] = []

    def flush() -> None:
        body = "\n".join(lines).strip()
        if body:
            chunks.append(
                Chunk(
                    id=f"{prefix}:{path.stem}:{len(chunks) + 1}",
                    source_type=source_type,
                    title=title,
                    text=body,
                    metadata={"file": str(path.relative_to(ROOT)), "section": title},
                )
            )

    for line in text.splitlines():
        if line.startswith("## "):
            flush()
            title = line.removeprefix("## ").strip()
            lines = []
        elif not line.startswith("#") and not line.startswith("Date:"):
            lines.append(line)
    flush()
    return chunks


def _split_with_langchain(chunk: Chunk) -> list[Chunk]:
    """Use LangChain text splitting while preserving stable chunk ids."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=80)
    document = Document(
        page_content=chunk.text,
        metadata={
            **chunk.metadata,
            "id": chunk.id,
            "source_type": chunk.source_type,
            "title": chunk.title,
        },
    )
    documents = splitter.split_documents([document])
    output = []
    for index, doc in enumerate(documents, start=1):
        split_id = chunk.id if len(documents) == 1 else f"{chunk.id}:{index}"
        output.append(
            Chunk(
                id=split_id,
                source_type=chunk.source_type,
                title=chunk.title,
                text=doc.page_content,
                metadata={k: v for k, v in doc.metadata.items() if k not in {"id", "source_type", "title"}},
            )
        )
    return output
