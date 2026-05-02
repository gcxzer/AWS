import json
from pathlib import Path
from typing import Any, Dict

import boto3
from botocore.exceptions import BotoCoreError, ClientError, TokenRetrievalError


PROJECT_DIR = Path(__file__).parent
CONFIG_PATH = PROJECT_DIR / "config.json"
UPLOADS = {
    PROJECT_DIR / "data/raw/sample_reviews.jsonl": "raw/sample_reviews.jsonl",
    PROJECT_DIR / "scripts/preprocess_reviews.py": "scripts/preprocess_reviews.py",
}


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

    for local_path, relative_key in UPLOADS.items():
        if not local_path.exists():
            raise FileNotFoundError(f"Missing local input: {local_path}")

        key = f"{prefix}/{relative_key}"
        s3.upload_file(str(local_path), bucket, key)
        print(f"Uploaded {local_path} -> s3://{bucket}/{key}")


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
        print("AI-13 input upload failed.")
        print(f"Original error: {error}")
        raise SystemExit(1)
