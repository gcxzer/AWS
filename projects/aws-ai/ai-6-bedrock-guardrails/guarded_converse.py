import argparse
import json
import sys
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


DEFAULT_PROMPT = "Explain the difference between IAM permissions and Bedrock Guardrails in two sentences."
DEFAULT_MODEL_ID = "amazon.nova-micro-v1:0"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Call a Bedrock model with Guardrail checks around it.")
    parser.add_argument("--profile", default="aws-learning", help="AWS CLI profile name.")
    parser.add_argument("--region", default="eu-central-1", help="AWS Region.")
    parser.add_argument("--guardrail-id", required=True, help="Guardrail ID or ARN.")
    parser.add_argument("--guardrail-version", default="1", help="Guardrail version, such as 1 or DRAFT.")
    parser.add_argument("--model-id", default=DEFAULT_MODEL_ID, help="Foundation model ID.")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="Prompt to send to the model.")
    parser.add_argument("--max-tokens", type=int, default=300, help="Max output tokens.")
    parser.add_argument("--temperature", type=float, default=0.2, help="Sampling temperature.")
    return parser.parse_args()


def apply_guardrail(
    client,
    guardrail_id: str,
    guardrail_version: str,
    source: str,
    text: str,
) -> Dict[str, Any]:
    return client.apply_guardrail(
        guardrailIdentifier=guardrail_id,
        guardrailVersion=guardrail_version,
        source=source,
        outputScope="FULL",
        content=[
            {
                "text": {
                    "text": text,
                }
            }
        ],
    )


def guardrail_action(response: Dict[str, Any]) -> Optional[str]:
    action = response.get("action")
    if action:
        return str(action)
    return None


def is_blocked(response: Dict[str, Any]) -> bool:
    action = guardrail_action(response)
    return action in {"GUARDRAIL_INTERVENED", "BLOCKED", "INTERVENED"}


def converse(client, model_id: str, prompt: str, max_tokens: int, temperature: float) -> str:
    response = client.converse(
        modelId=model_id,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt,
                    }
                ],
            }
        ],
        inferenceConfig={
            "maxTokens": max_tokens,
            "temperature": temperature,
        },
    )
    content = response.get("output", {}).get("message", {}).get("content", [])
    return "\n".join(part.get("text", "") for part in content if "text" in part).strip()


def compact_assessment(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "action": response.get("action"),
        "outputs": response.get("outputs", []),
        "assessments": response.get("assessments", []),
    }


def main() -> int:
    args = parse_args()
    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    client = session.client("bedrock-runtime")

    try:
        input_check = apply_guardrail(
            client,
            args.guardrail_id,
            args.guardrail_version,
            "INPUT",
            args.prompt,
        )
        print("input_guardrail:")
        print(json.dumps(compact_assessment(input_check), indent=2, ensure_ascii=False, default=str))

        if is_blocked(input_check):
            print()
            print("model_call_skipped: input guardrail intervened")
            return 0

        answer = converse(client, args.model_id, args.prompt, args.max_tokens, args.temperature)
        print()
        print("model_answer:")
        print(answer)

        output_check = apply_guardrail(
            client,
            args.guardrail_id,
            args.guardrail_version,
            "OUTPUT",
            answer,
        )
        print()
        print("output_guardrail:")
        print(json.dumps(compact_assessment(output_check), indent=2, ensure_ascii=False, default=str))
        return 0
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
                    "model_id": args.model_id,
                    "guardrail_id": args.guardrail_id,
                    "guardrail_version": args.guardrail_version,
                },
                indent=2,
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
