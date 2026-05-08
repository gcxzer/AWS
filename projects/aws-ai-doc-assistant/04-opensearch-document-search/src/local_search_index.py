"""A small local search index that mirrors the OpenSearch data shape."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from text_chunker import chunk_text, read_text


TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")


def tokenize(text: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_RE.finditer(text)]


def load_index(index_path: str | Path) -> list[dict[str, Any]]:
    path = Path(index_path)
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save_index(index_path: str | Path, records: list[dict[str, Any]]) -> None:
    path = Path(index_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")


def index_document(
    *,
    file_path: str | Path,
    index_path: str | Path,
    user_id: str,
    document_id: str,
    source: str | None = None,
    s3_uri: str | None = None,
    max_chars: int = 450,
) -> list[dict[str, Any]]:
    records = load_index(index_path)
    records = [
        record
        for record in records
        if not (record["user_id"] == user_id and record["document_id"] == document_id)
    ]

    text = read_text(file_path)
    chunks = chunk_text(text, max_chars=max_chars)
    source_name = source or Path(file_path).name

    new_records = []
    for index, chunk in enumerate(chunks, start=1):
        chunk_id = f"{document_id}#chunk_{index:04d}"
        new_records.append(
            {
                "user_id": user_id,
                "document_id": document_id,
                "chunk_id": chunk_id,
                "text": chunk,
                "source": source_name,
                "s3_uri": s3_uri,
                "token_count": len(tokenize(chunk)),
            }
        )

    records.extend(new_records)
    save_index(index_path, records)
    return new_records


def score_record(query_terms: list[str], record: dict[str, Any]) -> int:
    counts = Counter(tokenize(record["text"]))
    return sum(counts[term] for term in query_terms)


def search_documents(
    *,
    query: str,
    index_path: str | Path,
    user_id: str | None = None,
    limit: int = 5,
) -> list[dict[str, Any]]:
    query_terms = tokenize(query)
    records = load_index(index_path)
    results = []

    for record in records:
        if user_id and record["user_id"] != user_id:
            continue
        score = score_record(query_terms, record)
        if score <= 0:
            continue
        results.append({**record, "score": score})

    results.sort(key=lambda item: (-item["score"], item["document_id"], item["chunk_id"]))
    return results[:limit]
