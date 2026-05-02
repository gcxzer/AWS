import argparse
import json
import random
import re
from pathlib import Path
from typing import Dict, Iterable, List


LABELS = {
    "negative": 0,
    "neutral": 1,
    "positive": 2,
}


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def read_jsonl(path: Path) -> Iterable[Dict[str, str]]:
    with path.open("r", encoding="utf-8") as input_file:
        for line_number, line in enumerate(input_file, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"Invalid JSON on line {line_number}: {error}") from error


def transform_record(record: Dict[str, str], max_chars: int) -> Dict[str, object]:
    sentiment = str(record.get("sentiment", "")).lower()
    if sentiment not in LABELS:
        raise ValueError(f"Unsupported sentiment label: {sentiment}")

    text = normalize_text(str(record.get("text", "")))
    if not text:
        raise ValueError(f"Empty text for record id={record.get('id')}")

    return {
        "id": record.get("id"),
        "text": text[:max_chars],
        "label": LABELS[sentiment],
        "label_name": sentiment,
    }


def write_jsonl(path: Path, records: Iterable[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as output_file:
        for record in records:
            output_file.write(json.dumps(record, ensure_ascii=False) + "\n")


def split_records(
    records: List[Dict[str, object]],
    test_ratio: float,
    seed: int,
) -> tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    shuffled = records[:]
    random.Random(seed).shuffle(shuffled)
    test_size = max(1, round(len(shuffled) * test_ratio))
    test_records = shuffled[:test_size]
    train_records = shuffled[test_size:]
    return train_records, test_records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preprocess review JSONL data.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--test-ratio", type=float, default=0.3)
    parser.add_argument("--seed", type=int, default=13)
    parser.add_argument("--max-chars", type=int, default=512)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not 0 < args.test_ratio < 1:
        raise ValueError("--test-ratio must be between 0 and 1")

    records = [
        transform_record(record, max_chars=args.max_chars)
        for record in read_jsonl(args.input)
    ]
    if len(records) < 2:
        raise ValueError("At least two records are required for train/test split")

    train_records, test_records = split_records(
        records,
        test_ratio=args.test_ratio,
        seed=args.seed,
    )

    write_jsonl(args.output_dir / "train.jsonl", train_records)
    write_jsonl(args.output_dir / "test.jsonl", test_records)

    print(f"Input records: {len(records)}")
    print(f"Train records: {len(train_records)}")
    print(f"Test records: {len(test_records)}")
    print(f"Output directory: {args.output_dir}")


if __name__ == "__main__":
    main()
