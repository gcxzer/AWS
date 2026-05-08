"""Read one document metadata item by user_id and document_id."""

from __future__ import annotations

import argparse
import json

from config import AWS_PROFILE, AWS_REGION, DEFAULT_USER_ID, DOCUMENTS_TABLE
from dynamodb_client import get_document


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Get one document metadata item.")
    parser.add_argument("document_id")
    parser.add_argument("--user-id", default=DEFAULT_USER_ID)
    parser.add_argument("--table", default=DOCUMENTS_TABLE)
    parser.add_argument("--profile", default=AWS_PROFILE)
    parser.add_argument("--region", default=AWS_REGION)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    item = get_document(
        args.user_id,
        args.document_id,
        table_name=args.table,
        profile_name=args.profile,
        region_name=args.region,
    )
    print(json.dumps(item, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
