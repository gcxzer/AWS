#!/usr/bin/env python3
"""Translate text with Amazon Translate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import boto3


DEFAULT_INPUT = Path("events/sample-texts.json")
DEFAULT_OUTPUT = Path("outputs/translate-output.json")


def load_sample(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)["translate"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Translate text with Amazon Translate.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--region", default="eu-central-1")
    args = parser.parse_args()

    sample = load_sample(args.input)
    client = boto3.client("translate", region_name=args.region)
    response = client.translate_text(
        Text=sample["text"],
        SourceLanguageCode=sample.get("source_language_code", "en"),
        TargetLanguageCode=sample.get("target_language_code", "zh"),
    )

    result = {
        "service": "translate",
        "operation": "TranslateText",
        "region": args.region,
        "source_language_code": response["SourceLanguageCode"],
        "target_language_code": response["TargetLanguageCode"],
        "input_chars": len(sample["text"]),
        "translated_text": response["TranslatedText"],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
