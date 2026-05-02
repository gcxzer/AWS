import json
from pathlib import Path
from typing import Any, Dict

import boto3
from botocore.exceptions import BotoCoreError, ClientError, TokenRetrievalError


CONFIG_PATH = Path(__file__).with_name("config.json")
S3_FOLDERS = ("raw", "processed", "scripts", "models", "output")


def load_config() -> Dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


def main() -> None:
    config = load_config()
    session = boto3.Session(
        profile_name=config["profile"],
        region_name=config["region"],
    )
    s3 = session.client("s3")

    bucket = config["bucket"]
    prefix = config["prefix"].strip("/")

    for folder in S3_FOLDERS:
        key = f"{prefix}/{folder}/.keep"
        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=b"",
            ContentType="text/plain",
        )
        print(f"Created s3://{bucket}/{key}")


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
    except (BotoCoreError, ClientError) as error:
        print("S3 layout initialization failed.")
        print(f"Original error: {error}")
        raise SystemExit(1)
