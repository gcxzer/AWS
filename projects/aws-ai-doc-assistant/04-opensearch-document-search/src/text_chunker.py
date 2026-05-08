"""Text chunking helpers for the OpenSearch learning stage."""

from __future__ import annotations

from pathlib import Path


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def split_paragraphs(text: str) -> list[str]:
    paragraphs = [part.strip() for part in text.split("\n\n")]
    return [paragraph for paragraph in paragraphs if paragraph]


def chunk_text(text: str, max_chars: int = 450) -> list[str]:
    """Split text into small paragraph-aware chunks.

    This deliberately stays simple for the first pass. OpenSearch stores chunks as
    documents, so the important idea here is one source file -> many searchable
    chunk records.
    """
    chunks: list[str] = []
    current = ""

    for paragraph in split_paragraphs(text):
        if not current:
            current = paragraph
            continue

        next_value = f"{current}\n\n{paragraph}"
        if len(next_value) <= max_chars:
            current = next_value
        else:
            chunks.append(current)
            current = paragraph

    if current:
        chunks.append(current)

    return chunks
