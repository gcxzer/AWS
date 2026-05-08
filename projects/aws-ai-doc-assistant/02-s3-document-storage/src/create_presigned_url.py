"""Create a short-lived presigned URL for a private S3 object."""

from __future__ import annotations

import argparse

from config import AWS_PROFILE, AWS_REGION, S3_BUCKET
from s3_client import create_presigned_download_url


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a presigned S3 download URL.")
    parser.add_argument("key", help="S3 object key, for example raw/user_001/sample.txt.")
    parser.add_argument("--expires-in", type=int, default=300, help="URL lifetime in seconds.")
    parser.add_argument("--bucket", default=S3_BUCKET)
    parser.add_argument("--profile", default=AWS_PROFILE)
    parser.add_argument("--region", default=AWS_REGION)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    url = create_presigned_download_url(
        bucket=args.bucket,
        key=args.key,
        expires_in=args.expires_in,
        profile_name=args.profile,
        region_name=args.region,
    )
    print(url)


if __name__ == "__main__":
    main()
