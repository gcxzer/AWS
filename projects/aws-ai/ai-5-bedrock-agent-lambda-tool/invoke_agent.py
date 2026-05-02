import argparse
import json
import sys
import uuid
from typing import Any, Dict

import boto3
from botocore.exceptions import BotoCoreError, ClientError


DEFAULT_PROMPT = "Summarize what I learned in AI-2. Use the lesson tool when useful."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Invoke an Amazon Bedrock Agent with boto3.")
    parser.add_argument("--profile", default="aws-learning", help="AWS CLI profile name.")
    parser.add_argument("--region", default="eu-central-1", help="AWS Region.")
    parser.add_argument("--agent-id", required=True, help="Bedrock Agent ID.")
    parser.add_argument("--agent-alias-id", required=True, help="Bedrock Agent alias ID.")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="Prompt to send to the agent.")
    parser.add_argument(
        "--session-id",
        default=None,
        help="Conversation session ID. Reuse the same value to continue a session.",
    )
    parser.add_argument(
        "--disable-trace",
        action="store_true",
        help="Disable trace events. Trace is useful while learning how the agent chose tools.",
    )
    parser.add_argument(
        "--stream-final-response",
        action="store_true",
        help="Stream the final response in smaller chunks.",
    )
    parser.add_argument(
        "--apply-guardrail-interval",
        type=int,
        default=50,
        help="Character interval for guardrail application when a guardrail is configured.",
    )
    parser.add_argument(
        "--raw-trace",
        action="store_true",
        help="Print raw trace events as JSON. This can be verbose.",
    )
    return parser.parse_args()


def trace_summary(trace_event: Dict[str, Any]) -> Dict[str, Any]:
    trace = trace_event.get("trace", {})
    summary = {}
    for key, value in trace.items():
        if isinstance(value, dict):
            summary[key] = sorted(value.keys())
        else:
            summary[key] = type(value).__name__
    return summary


def main() -> int:
    args = parse_args()
    session_id = args.session_id or f"ai5-{uuid.uuid4().hex[:12]}"
    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    client = session.client("bedrock-agent-runtime")

    try:
        response = client.invoke_agent(
            agentId=args.agent_id,
            agentAliasId=args.agent_alias_id,
            sessionId=session_id,
            inputText=args.prompt,
            enableTrace=not args.disable_trace,
            streamingConfigurations={
                "applyGuardrailInterval": args.apply_guardrail_interval,
                "streamFinalResponse": args.stream_final_response,
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
                    "agent_id": args.agent_id,
                    "agent_alias_id": args.agent_alias_id,
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
                    "agent_id": args.agent_id,
                    "agent_alias_id": args.agent_alias_id,
                },
                indent=2,
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 1

    completion = ""
    print(f"session_id: {session_id}")
    print()

    for event in response.get("completion", []):
        if "chunk" in event:
            completion += event["chunk"]["bytes"].decode("utf-8")
        elif "trace" in event and not args.disable_trace:
            if args.raw_trace:
                print(json.dumps(event["trace"], indent=2, ensure_ascii=False, default=str))
            else:
                print(f"trace: {json.dumps(trace_summary(event['trace']), ensure_ascii=False)}")
        elif "returnControl" in event:
            print(json.dumps({"returnControl": event["returnControl"]}, indent=2, ensure_ascii=False))

    print()
    print("agent_response:")
    print(completion.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
