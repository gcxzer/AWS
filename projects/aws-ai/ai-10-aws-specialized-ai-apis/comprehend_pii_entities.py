#!/usr/bin/env python3
"""Detect PII entities with Amazon Comprehend."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import boto3


DEFAULT_INPUT = Path("events/sample-texts.json")
DEFAULT_OUTPUT = Path("outputs/comprehend-pii-output.json")


def load_sample(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)["comprehend"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect PII entities with Amazon Comprehend.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--region", default="eu-central-1")
    args = parser.parse_args()

    sample = load_sample(args.input)
    client = boto3.client("comprehend", region_name=args.region)
    response = client.detect_pii_entities(
        Text=sample["text"],
        LanguageCode=sample.get("language_code", "en"),
    )

    result = {
        "service": "comprehend",
        "operation": "DetectPiiEntities",
        "region": args.region,
        "input_chars": len(sample["text"]),
        "entities": response.get("Entities", []),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
