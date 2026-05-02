import argparse
import json
import sys
from typing import Any, Dict

import boto3
from botocore.exceptions import BotoCoreError, ClientError


DEFAULT_TEXT = "My email is test@example.com. Please summarize this safely."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply an Amazon Bedrock Guardrail to text.")
    parser.add_argument("--profile", default="aws-learning", help="AWS CLI profile name.")
    parser.add_argument("--region", default="eu-central-1", help="AWS Region.")
    parser.add_argument("--guardrail-id", required=True, help="Guardrail ID or ARN.")
    parser.add_argument("--guardrail-version", default="DRAFT", help="Guardrail version, such as DRAFT or 1.")
    parser.add_argument("--text", default=DEFAULT_TEXT, help="Text to evaluate.")
    parser.add_argument(
        "--source",
        choices=["INPUT", "OUTPUT"],
        default="INPUT",
        help="Whether the text is user input or model output.",
    )
    parser.add_argument(
        "--output-scope",
        choices=["INTERVENTIONS", "FULL"],
        default="FULL",
        help="How much assessment detail to return.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    client = session.client("bedrock-runtime")

    request: Dict[str, Any] = {
        "guardrailIdentifier": args.guardrail_id,
        "guardrailVersion": args.guardrail_version,
        "source": args.source,
        "outputScope": args.output_scope,
        "content": [
            {
                "text": {
                    "text": args.text,
                }
            }
        ],
    }

    try:
        response = client.apply_guardrail(**request)
    except ClientError as exc:
        error = exc.response.get("Error", {})
        print(
            json.dumps(
                {
                    "ok": False,
                    "error_code": error.get("Code"),
                    "message": error.get("Message"),
                    "region": args.region,
                    "guardrail_id": args.guardrail_id,
                    "guardrail_version": args.guardrail_version,
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
                    "guardrail_id": args.guardrail_id,
                    "guardrail_version": args.guardrail_version,
                },
                indent=2,
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 1

    print(json.dumps(response, indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
