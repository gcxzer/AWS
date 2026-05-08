"""Search the local OpenSearch-shaped JSON index."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from local_search_index import search_documents


DEFAULT_INDEX_PATH = Path("data/local-search-index.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search the local document index.")
    parser.add_argument("query", help="Keyword query.")
    parser.add_argument("--index-path", default=str(DEFAULT_INDEX_PATH))
    parser.add_argument("--user-id", default="user_001")
    parser.add_argument("--limit", type=int, default=5)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = search_documents(
        query=args.query,
        index_path=args.index_path,
        user_id=args.user_id,
        limit=args.limit,
    )
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
