"""Upload a local document to the learning project's S3 bucket."""

from __future__ import annotations

import argparse
import json

from config import AWS_PROFILE, AWS_REGION, DEFAULT_USER_ID, S3_BUCKET
from s3_client import build_document_key, upload_document


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload a document to S3.")
    parser.add_argument("file", help="Local file path to upload.")
    parser.add_argument("--key", help="S3 object key. Defaults to raw/<user-id>/<filename>.")
    parser.add_argument("--user-id", default=DEFAULT_USER_ID)
    parser.add_argument("--document-type", default="sample")
    parser.add_argument("--source", default="python-upload")
    parser.add_argument("--bucket", default=S3_BUCKET)
    parser.add_argument("--profile", default=AWS_PROFILE)
    parser.add_argument("--region", default=AWS_REGION)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    key = args.key or build_document_key(args.file, args.user_id)
    result = upload_document(
        args.file,
        bucket=args.bucket,
        key=key,
        user_id=args.user_id,
        document_type=args.document_type,
        source=args.source,
        profile_name=args.profile,
        region_name=args.region,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
