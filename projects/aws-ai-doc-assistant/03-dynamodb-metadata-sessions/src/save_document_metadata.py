"""Save one document metadata item to DynamoDB."""

from __future__ import annotations

import argparse
import json

from config import AWS_PROFILE, AWS_REGION, DEFAULT_USER_ID, DOCUMENTS_TABLE, S3_BUCKET
from dynamodb_client import save_document_metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Save document metadata to DynamoDB.")
    parser.add_argument("--user-id", default=DEFAULT_USER_ID)
    parser.add_argument("--document-id", default="doc_003")
    parser.add_argument("--title", default="sample-python-2.txt")
    parser.add_argument("--s3-bucket", default=S3_BUCKET)
    parser.add_argument("--s3-key", default="raw/user_001/sample-python-2.txt")
    parser.add_argument("--status", default="uploaded")
    parser.add_argument("--table", default=DOCUMENTS_TABLE)
    parser.add_argument("--profile", default=AWS_PROFILE)
    parser.add_argument("--region", default=AWS_REGION)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    item = save_document_metadata(
        user_id=args.user_id,
        document_id=args.document_id,
        title=args.title,
        s3_bucket=args.s3_bucket,
        s3_key=args.s3_key,
        status=args.status,
        table_name=args.table,
        profile_name=args.profile,
        region_name=args.region,
    )
    print(json.dumps(item, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
