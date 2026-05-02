#!/usr/bin/env python3
"""Extract text from a local PNG/JPEG image with Amazon Textract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import boto3


DEFAULT_OUTPUT = Path("outputs/textract-detect-text-output.json")


def extract_lines(blocks: list[dict]) -> list[dict]:
    lines = []
    for block in blocks:
        if block.get("BlockType") == "LINE":
            lines.append(
                {
                    "text": block.get("Text", ""),
                    "confidence": block.get("Confidence"),
                }
            )
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract text from a local image with Textract.")
    parser.add_argument("image", type=Path, help="Local PNG or JPEG image path.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--region", default="eu-central-1")
    args = parser.parse_args()

    image_bytes = args.image.read_bytes()
    client = boto3.client("textract", region_name=args.region)
    response = client.detect_document_text(Document={"Bytes": image_bytes})
    lines = extract_lines(response.get("Blocks", []))

    result = {
        "service": "textract",
        "operation": "DetectDocumentText",
        "region": args.region,
        "source_image": str(args.image),
        "line_count": len(lines),
        "lines": lines,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
