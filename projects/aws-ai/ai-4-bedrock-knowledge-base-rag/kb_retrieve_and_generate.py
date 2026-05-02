import argparse
import json
import sys
import time
from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


DEFAULT_QUERY = "How does the S3 document pipeline work according to my notes?"
DEFAULT_MODEL_ID = "openai.gpt-oss-20b-1:0"
ORCHESTRATION_PROMPT = """You turn the user's latest question into a concise search query for a knowledge base.

Conversation history:
$conversation_history$

User question:
$query$

Return only the search query.
$output_format_instructions$"""

GENERATION_PROMPT = """You are answering questions for an engineer learning AWS AI.
Use only the retrieved search results below. If the answer is not in the search results, say that the notes do not contain enough information.

Search results:
$search_results$

Question:
$query$

Answer clearly and concisely."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Retrieve from an Amazon Bedrock Knowledge Base and generate an answer."
    )
    parser.add_argument("--profile", default="aws-learning", help="AWS CLI profile name.")
    parser.add_argument("--region", default="eu-central-1", help="AWS Region.")
    parser.add_argument(
        "--knowledge-base-id",
        default="BHDJUFWYDC",
        help="Amazon Bedrock Knowledge Base ID.",
    )
    parser.add_argument("--query", default=DEFAULT_QUERY, help="Question to answer.")
    parser.add_argument("--top-k", type=int, default=3, help="Number of chunks to retrieve.")
    parser.add_argument(
        "--model-id",
        default=DEFAULT_MODEL_ID,
        help="Foundation model ID used to generate the answer.",
    )
    parser.add_argument(
        "--model-arn",
        default=None,
        help="Optional full model ARN. If omitted, one is built from region and model ID.",
    )
    parser.add_argument("--max-tokens", type=int, default=500, help="Max output tokens.")
    parser.add_argument("--temperature", type=float, default=0.2, help="Sampling temperature.")
    parser.add_argument("--top-p", type=float, default=0.9, help="Nucleus sampling value.")
    return parser.parse_args()


def model_arn(region: str, model_id: str, explicit_arn: Optional[str]) -> str:
    if explicit_arn:
        return explicit_arn
    return f"arn:aws:bedrock:{region}::foundation-model/{model_id}"


def source_uri(reference: dict) -> str:
    location = reference.get("location", {})
    if location.get("type") == "S3":
        return location.get("s3Location", {}).get("uri", "unknown")
    return location.get("type", "unknown")


def reference_text(reference: dict) -> str:
    content = reference.get("content", {})
    return content.get("text", "").strip()


def retrieve_sources(client, args: argparse.Namespace) -> list:
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
    return response.get("retrievalResults", [])


def main() -> int:
    args = parse_args()
    generation_model_arn = model_arn(args.region, args.model_id, args.model_arn)

    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    client = session.client("bedrock-agent-runtime")

    try:
        retrieved_sources = retrieve_sources(client, args)
    except ClientError as exc:
        error = exc.response.get("Error", {})
        print(
            json.dumps(
                {
                    "ok": False,
                    "stage": "retrieve",
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
                    "stage": "retrieve",
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

    request = {
        "input": {
            "text": args.query,
        },
        "retrieveAndGenerateConfiguration": {
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": args.knowledge_base_id,
                "modelArn": generation_model_arn,
                "retrievalConfiguration": {
                    "vectorSearchConfiguration": {
                        "numberOfResults": args.top_k,
                    }
                },
                "orchestrationConfiguration": {
                    "promptTemplate": {
                        "textPromptTemplate": ORCHESTRATION_PROMPT,
                    }
                },
                "generationConfiguration": {
                    "promptTemplate": {
                        "textPromptTemplate": GENERATION_PROMPT,
                    },
                    "inferenceConfig": {
                        "textInferenceConfig": {
                            "maxTokens": args.max_tokens,
                            "temperature": args.temperature,
                            "topP": args.top_p,
                        }
                    }
                },
            },
        },
    }

    started = time.perf_counter()
    try:
        response = client.retrieve_and_generate(**request)
    except ClientError as exc:
        error = exc.response.get("Error", {})
        print(
            json.dumps(
                {
                    "ok": False,
                    "stage": "retrieve_and_generate",
                    "error_code": error.get("Code"),
                    "message": error.get("Message"),
                    "region": args.region,
                    "knowledge_base_id": args.knowledge_base_id,
                    "model_arn": generation_model_arn,
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
                    "stage": "retrieve_and_generate",
                    "error_code": exc.__class__.__name__,
                    "message": str(exc),
                    "region": args.region,
                    "knowledge_base_id": args.knowledge_base_id,
                    "model_arn": generation_model_arn,
                },
                indent=2,
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 1

    elapsed_ms = round((time.perf_counter() - started) * 1000)
    answer = response.get("output", {}).get("text", "").strip()
    citations = response.get("citations", [])

    print(f"query: {args.query}")
    print(f"knowledge_base_id: {args.knowledge_base_id}")
    print(f"model_arn: {generation_model_arn}")
    print(f"latency_ms: {elapsed_ms}")

    print()
    print(f"retrieved_sources: {len(retrieved_sources)}")
    for index, source in enumerate(retrieved_sources, start=1):
        text = " ".join(reference_text(source).split())
        print(f"[source {index}] score={source.get('score')}")
        print(f"uri={source_uri(source)}")
        print(f"text={text[:300]}")

    print()
    print("answer:")
    print(answer)

    print()
    print(f"citations: {len(citations)}")
    for citation_index, citation in enumerate(citations, start=1):
        generated_text = (
            citation.get("generatedResponsePart", {})
            .get("textResponsePart", {})
            .get("text", "")
            .strip()
        )
        if generated_text:
            print()
            print(f"[citation {citation_index}] generated_text={generated_text[:250]}")

        references = citation.get("retrievedReferences", [])
        if not references:
            print("  no retrievedReferences returned in this citation")

        for reference_index, reference in enumerate(references, start=1):
            text = " ".join(reference_text(reference).split())
            print(f"  source {reference_index}: {source_uri(reference)}")
            print(f"  text: {text[:500]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
