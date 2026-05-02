import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


REQUIRED_FIELDS = {
    "id",
    "question",
    "expected_answer",
    "expected_source",
    "evaluation_type",
}
VALID_EVALUATION_TYPES = {"retrieve_only", "retrieve_and_generate"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a local AI-8 evaluation JSONL dataset.")
    parser.add_argument("dataset", type=Path, help="Path to the JSONL dataset.")
    return parser.parse_args()


def validate_record(record: Dict[str, Any], line_number: int) -> List[str]:
    errors: List[str] = []
    missing = sorted(REQUIRED_FIELDS - set(record))
    if missing:
        errors.append(f"line {line_number}: missing fields: {', '.join(missing)}")

    for field in REQUIRED_FIELDS:
        value = record.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"line {line_number}: {field} must be a non-empty string")

    evaluation_type = record.get("evaluation_type")
    if evaluation_type not in VALID_EVALUATION_TYPES:
        errors.append(
            f"line {line_number}: evaluation_type must be one of {sorted(VALID_EVALUATION_TYPES)}"
        )

    return errors


def main() -> int:
    args = parse_args()
    if not args.dataset.exists():
        print(f"dataset not found: {args.dataset}", file=sys.stderr)
        return 1

    errors: List[str] = []
    ids = set()
    count = 0

    with args.dataset.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            count += 1
            try:
                record = json.loads(stripped)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_number}: invalid JSON: {exc}")
                continue

            if not isinstance(record, dict):
                errors.append(f"line {line_number}: record must be a JSON object")
                continue

            record_id = record.get("id")
            if record_id in ids:
                errors.append(f"line {line_number}: duplicate id: {record_id}")
            ids.add(record_id)
            errors.extend(validate_record(record, line_number))

    if count == 0:
        errors.append("dataset is empty")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(json.dumps({"ok": True, "records": count}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
