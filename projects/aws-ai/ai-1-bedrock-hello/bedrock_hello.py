import argparse
import json
import sys
import time

import boto3
from botocore.exceptions import BotoCoreError, ClientError


DEFAULT_PROMPT = (
    "Summarize this in three concise bullet points for an engineer learning AWS AI: "
    "Amazon Bedrock is a managed AWS service for building generative AI applications "
    "with foundation models, IAM-based access control, SDK integration, and AWS-native "
    "operations such as monitoring, quotas, and cost management."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Minimal Amazon Bedrock Converse API smoke test."
    )
    parser.add_argument("--profile", default="aws-learning", help="AWS CLI profile name.")
    parser.add_argument("--region", default="eu-central-1", help="AWS Region.")
    parser.add_argument("--model-id",required=True,help="Bedrock foundation model ID or inference profile ID.",)
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="Prompt text.")
    parser.add_argument("--max-tokens", type=int, default=300, help="Max output tokens.")
    parser.add_argument("--temperature", type=float, default=0.2, help="Sampling temperature.")
    return parser.parse_args()


def extract_text(response: dict) -> str:
    message = response.get("output", {}).get("message", {})
    parts = []
    for block in message.get("content", []):
        text = block.get("text")
        if text:
            parts.append(text)
    return "\n".join(parts).strip()


def main() -> int:
    args = parse_args()
    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    client = session.client("bedrock-runtime")

    request = {
        "modelId": args.model_id,
        "messages": [
            {
                "role": "user",
                "content": [{"text": args.prompt}],
            }
        ],
        "inferenceConfig": {
            "maxTokens": args.max_tokens,
            "temperature": args.temperature,
        },
    }

    started = time.perf_counter()
    try:
        response = client.converse(**request)
    except ClientError as exc:
        error = exc.response.get("Error", {})
        print(
            json.dumps(
                {
                    "ok": False,
                    "error_code": error.get("Code"),
                    "message": error.get("Message"),
                    "region": args.region,
                    "model_id": args.model_id,
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
                    "model_id": args.model_id,
                },
                indent=2,
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 1

    elapsed_ms = round((time.perf_counter() - started) * 1000)
    usage = response.get("usage", {})
    output = {
        "ok": True,
        "region": args.region,
        "model_id": args.model_id,
        "latency_ms": elapsed_ms,
        "input_tokens": usage.get("inputTokens"),
        "output_tokens": usage.get("outputTokens"),
        "stop_reason": response.get("stopReason"),
        "text": extract_text(response),
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
