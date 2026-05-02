import argparse
import json
import sys

import boto3
from botocore.exceptions import BotoCoreError, ClientError


DEFAULT_QUERY = "How does the S3 document pipeline work according to my notes?"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Retrieve source chunks from an Amazon Bedrock Knowledge Base."
    )
    parser.add_argument("--profile", default="aws-learning", help="AWS CLI profile name.")
    parser.add_argument("--region", default="eu-central-1", help="AWS Region.")
    parser.add_argument(
        "--knowledge-base-id",
        default="BHDJUFWYDC",
        help="Amazon Bedrock Knowledge Base ID.",
    )
    parser.add_argument("--query", default=DEFAULT_QUERY, help="Question to retrieve for.")
    parser.add_argument("--top-k", type=int, default=3, help="Number of chunks to return.")
    return parser.parse_args()


def source_uri(result: dict) -> str:
    location = result.get("location", {})
    if location.get("type") == "S3":
        return location.get("s3Location", {}).get("uri", "unknown")
    return location.get("type", "unknown")


def chunk_text(result: dict) -> str:
    return result.get("content", {}).get("text", "").strip()


def main() -> int:
    args = parse_args()
    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    client = session.client("bedrock-agent-runtime")

    try:
        response = client.retrieve(
            knowledgeBaseId=args.knowledge_base_id,
            retrievalQuery={
                "text": args.query,
                "type": "TEXT",
            },
            retrievalConfiguration={
                "vectorSearchConfiguration": {
                    "numberOfResults": args.top_k,
                }
            },
        )
    except ClientError as exc:
        error = exc.response.get("Error", {})
        print(
            json.dumps(
                {
                    "ok": False,
                    "error_code": error.get("Code"),
                    "message": error.get("Message"),
                    "region": args.region,
                    "knowledge_base_id": args.knowledge_base_id,
                },
                indent=2,
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 1
    except BotoCoreError as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error_code": exc.__class__.__name__,
                    "message": str(exc),
                    "region": args.region,
                    "knowledge_base_id": args.knowledge_base_id,
                },
                indent=2,
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 1

    results = response.get("retrievalResults", [])
    print(f"query: {args.query}")
    print(f"knowledge_base_id: {args.knowledge_base_id}")
    print(f"results: {len(results)}")

    for index, result in enumerate(results, start=1):
        text = " ".join(chunk_text(result).split())
        print()
        print(f"[{index}] score={result.get('score')}")
        print(f"source={source_uri(result)}")
        print(text[:700])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
