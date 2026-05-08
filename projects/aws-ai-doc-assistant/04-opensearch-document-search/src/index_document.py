"""Index a local text document into a local OpenSearch-shaped JSON index."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from local_search_index import index_document


DEFAULT_INDEX_PATH = Path("data/local-search-index.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Index a document into the local search index.")
    parser.add_argument("file", help="Local text file to index.")
    parser.add_argument("--index-path", default=str(DEFAULT_INDEX_PATH))
    parser.add_argument("--user-id", default="user_001")
    parser.add_argument("--document-id", default="doc_004")
    parser.add_argument("--source")
    parser.add_argument("--s3-uri")
    parser.add_argument("--max-chars", type=int, default=450)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    records = index_document(
        file_path=args.file,
        index_path=args.index_path,
        user_id=args.user_id,
        document_id=args.document_id,
        source=args.source,
        s3_uri=args.s3_uri,
        max_chars=args.max_chars,
    )
    print(json.dumps(records, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
