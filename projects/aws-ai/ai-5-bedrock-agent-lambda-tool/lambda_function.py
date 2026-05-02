import json
import sys
from typing import Any, Dict


LESSONS = {
    "AI-1": {
        "title": "Bedrock 调用与权限",
        "summary": (
            "You built the smallest useful Bedrock loop: verify model access, use "
            "an AWS profile, call a foundation model with boto3, and understand why "
            "Bedrock model access and IAM permission are separate controls."
        ),
        "key_services": ["Amazon Bedrock", "Bedrock Runtime", "IAM", "CloudWatch"],
        "completed_outputs": [
            "Local Python script that calls Bedrock",
            "Example IAM policy scoped to model invocation",
            "Notes about Region, model ID, request shape, errors, and cost",
        ],
        "concepts": [
            "bedrock vs bedrock-runtime clients",
            "Model access vs IAM authorization",
            "Region and model availability",
            "Token-based model cost",
        ],
        "next_step": "Wrap model invocation behind a backend boundary instead of calling Bedrock directly from a client.",
    },
    "AI-2": {
        "title": "Bedrock Serverless API",
        "summary": (
            "You moved Bedrock invocation behind an HTTP API. API Gateway receives "
            "the request, Lambda validates inputs and calls Bedrock Runtime, and "
            "CloudWatch Logs captures operational signals without exposing AWS "
            "credentials to the frontend."
        ),
        "key_services": ["API Gateway", "AWS Lambda", "Amazon Bedrock", "CloudWatch Logs", "IAM"],
        "completed_outputs": [
            "A serverless /summarize style API design",
            "Clear frontend vs backend responsibility boundary",
            "Input validation, timeout, logging, and least-privilege notes",
        ],
        "concepts": [
            "Why browsers should not hold AWS credentials",
            "API Gateway route and Lambda integration",
            "Lambda execution role",
            "Backend cost and input controls",
        ],
        "next_step": "Turn the synchronous API pattern into an event-driven document pipeline.",
    },
    "AI-3": {
        "title": "S3 AI 文档处理流水线",
        "summary": (
            "You used S3 events to make AI processing asynchronous. Uploading a "
            "document can trigger Lambda, Lambda can call Bedrock, and results can "
            "be written back to S3 with a traceable failure path."
        ),
        "key_services": ["Amazon S3", "AWS Lambda", "Amazon Bedrock", "SQS", "SNS", "CloudWatch Logs"],
        "completed_outputs": [
            "S3 ObjectCreated event processing design",
            "Sample document input and output result shape",
            "Failure, idempotency, and notification notes",
        ],
        "concepts": [
            "Event-driven processing",
            "S3 input/output prefixes",
            "DLQ and failure tracking",
            "When Lambda should become Step Functions",
        ],
        "next_step": "Use managed RAG when users need to ask questions over a document set.",
    },
    "AI-4": {
        "title": "Bedrock Knowledge Bases / 托管 RAG",
        "summary": (
            "You created a managed RAG path with S3 documents, a Knowledge Base, "
            "ingestion, Titan Embeddings, a vector store, Retrieve, and "
            "RetrieveAndGenerate. You also observed that retrieve quality and "
            "generation quality need to be debugged separately."
        ),
        "key_services": ["Bedrock Knowledge Bases", "Amazon S3", "Titan Embeddings", "S3 Vectors"],
        "completed_outputs": [
            "Knowledge Base resource record and cleanup record",
            "Retrieve script for source chunks",
            "RetrieveAndGenerate script with custom prompt handling",
        ],
        "concepts": [
            "Data source and ingestion job",
            "Chunking, embeddings, and vector store",
            "Retrieve vs RetrieveAndGenerate",
            "Citations and model-specific prompt behavior",
        ],
        "next_step": "Add a Bedrock Agent so a model can decide when to call an external tool.",
    },
    "AI-5": {
        "title": "Bedrock Agent 与 Lambda 工具调用",
        "summary": (
            "You are building an agent that can decide when to call a Lambda tool. "
            "The action schema tells the agent what the tool can do, Lambda runs "
            "the business logic, and an agent alias provides the stable runtime "
            "target for applications."
        ),
        "key_services": ["Bedrock Agents", "AWS Lambda", "IAM", "CloudWatch Logs"],
        "completed_outputs": [
            "Lambda tool handler with static lesson data",
            "OpenAPI action schema for get_lesson_summary",
            "Local event fixture and InvokeAgent boto3 client",
        ],
        "concepts": [
            "Agent instruction and orchestration",
            "Action group schema",
            "Lambda event and response contract",
            "Agent alias and Lambda resource-based policy",
        ],
        "next_step": "After this works with static data, move the lesson source to S3 or DynamoDB and tighten permissions to that resource.",
    },
}


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    print(
        json.dumps(
            {
                "actionGroup": event.get("actionGroup"),
                "apiPath": event.get("apiPath"),
                "httpMethod": event.get("httpMethod"),
                "parameters": event.get("parameters", []),
            },
            ensure_ascii=False,
        )
    )

    status_code = 200
    try:
        body = handle_get_lesson_summary(event)
    except ValueError as exc:
        status_code = 400
        body = {
            "error": str(exc),
            "valid_lesson_ids": sorted(LESSONS),
        }
    except Exception:
        status_code = 500
        body = {
            "error": "Internal tool error",
        }

    return build_bedrock_response(event, status_code, body)


def handle_get_lesson_summary(event: Dict[str, Any]) -> Dict[str, Any]:
    api_path = event.get("apiPath")
    http_method = str(event.get("httpMethod", "")).upper()
    if api_path != "/lesson-summary" or http_method != "GET":
        raise ValueError(f"Unsupported operation: {http_method} {api_path}")

    params = collect_parameters(event)
    lesson_id = normalize_lesson_id(params.get("lesson_id", ""))
    detail_level = str(params.get("detail_level") or "brief").lower()
    if detail_level not in {"brief", "detailed"}:
        raise ValueError("detail_level must be brief or detailed")

    lesson = LESSONS[lesson_id]
    response = {
        "lesson_id": lesson_id,
        "title": lesson["title"],
        "summary": lesson["summary"],
        "key_services": lesson["key_services"],
        "completed_outputs": lesson["completed_outputs"],
        "next_step": lesson["next_step"],
    }

    if detail_level == "detailed":
        response["concepts"] = lesson["concepts"]

    return response


def collect_parameters(event: Dict[str, Any]) -> Dict[str, str]:
    params: Dict[str, str] = {}

    for parameter in event.get("parameters") or []:
        name = parameter.get("name")
        value = parameter.get("value")
        if name and value is not None:
            params[name] = str(value)

    content = (event.get("requestBody") or {}).get("content") or {}
    for media_value in content.values():
        for property_value in media_value.get("properties") or []:
            name = property_value.get("name")
            value = property_value.get("value")
            if name and value is not None:
                params[name] = str(value)

    return params


def normalize_lesson_id(value: str) -> str:
    cleaned = str(value).strip().upper().replace(" ", "")
    if cleaned.isdigit():
        cleaned = f"AI-{cleaned}"
    elif cleaned.startswith("AI") and not cleaned.startswith("AI-"):
        cleaned = f"AI-{cleaned[2:]}"

    if cleaned not in LESSONS:
        raise ValueError(f"Unknown lesson_id: {value}")
    return cleaned


def build_bedrock_response(event: Dict[str, Any], status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    response_body = {
        "application/json": {
            "body": json.dumps(body, ensure_ascii=False),
        }
    }
    action_response = {
        "actionGroup": event.get("actionGroup", "LessonSummaryActionGroup"),
        "apiPath": event.get("apiPath", "/lesson-summary"),
        "httpMethod": event.get("httpMethod", "GET"),
        "httpStatusCode": status_code,
        "responseBody": response_body,
    }
    return {
        "messageVersion": "1.0",
        "response": action_response,
        "sessionAttributes": event.get("sessionAttributes", {}),
        "promptSessionAttributes": event.get("promptSessionAttributes", {}),
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python lambda_function.py path/to/bedrock-agent-event.json", file=sys.stderr)
        return 2

    with open(sys.argv[1], "r", encoding="utf-8") as file:
        event = json.load(file)

    print(json.dumps(lambda_handler(event, None), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
