import json
from pathlib import Path
from typing import Any, Dict

import boto3
from botocore.exceptions import BotoCoreError, ClientError, TokenRetrievalError


PROJECT_DIR = Path(__file__).parent
CONFIG_PATH = PROJECT_DIR / "config.json"
LOCAL_UPLOADS = {
    PROJECT_DIR / "scripts/train_text_classifier.py": "scripts/train_text_classifier.py",
    PROJECT_DIR / "requirements.txt": "scripts/requirements.txt",
}


def load_config() -> Dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


def parse_s3_uri(uri: str) -> tuple[str, str]:
    if not uri.startswith("s3://"):
        raise ValueError(f"Expected S3 URI, got: {uri}")
    bucket, _, key = uri.removeprefix("s3://").partition("/")
    return bucket, key.rstrip("/")


def copy_processed_data(s3, source_uri: str, bucket: str, prefix: str) -> None:
    source_bucket, source_prefix = parse_s3_uri(source_uri)
    copies = {
        f"{source_prefix}/train.jsonl": f"{prefix}/train/train.jsonl",
        f"{source_prefix}/test.jsonl": f"{prefix}/test/test.jsonl",
    }

    for source_key, target_key in copies.items():
        s3.copy_object(
            Bucket=bucket,
            Key=target_key,
            CopySource={"Bucket": source_bucket, "Key": source_key},
        )
        print(f"Copied s3://{source_bucket}/{source_key} -> s3://{bucket}/{target_key}")


def upload_local_files(s3, bucket: str, prefix: str) -> None:
    for local_path, relative_key in LOCAL_UPLOADS.items():
        if not local_path.exists():
            raise FileNotFoundError(f"Missing local file: {local_path}")
        key = f"{prefix}/{relative_key}"
        s3.upload_file(str(local_path), bucket, key)
        print(f"Uploaded {local_path} -> s3://{bucket}/{key}")


def main() -> None:
    config = load_config()
    session = boto3.Session(
        profile_name=config["profile"],
        region_name=config["region"],
    )
    s3 = session.client("s3")

    bucket = config["bucket"]
    prefix = config["prefix"].strip("/")

    copy_processed_data(
        s3,
        source_uri=config["source_processed_s3_uri"],
        bucket=bucket,
        prefix=prefix,
    )
    upload_local_files(s3, bucket=bucket, prefix=prefix)


if __name__ == "__main__":
    try:
        main()
    except TokenRetrievalError as error:
        print("AWS SSO token is expired or cannot be refreshed.")
        print()
        print("Run this first:")
        print("  aws sso login --profile aws-learning")
        print()
        print(f"Original error: {error}")
        raise SystemExit(1)
    except (BotoCoreError, ClientError, OSError) as error:
        print("AI-14 training input upload failed.")
        print(f"Original error: {error}")
        raise SystemExit(1)
