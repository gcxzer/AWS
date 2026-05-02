import argparse
import json
import os
from pathlib import Path
from typing import Dict, Iterable, List

import torch
from torch.optim import AdamW
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def read_jsonl(path: Path) -> List[Dict[str, object]]:
    records: List[Dict[str, object]] = []
    with path.open("r", encoding="utf-8") as input_file:
        for line_number, line in enumerate(input_file, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValueError(f"Invalid JSON on line {line_number}: {error}") from error
    return records


def batch_records(records: List[Dict[str, object]], batch_size: int) -> Iterable[List[Dict[str, object]]]:
    for index in range(0, len(records), batch_size):
        yield records[index : index + batch_size]


def encode_batch(tokenizer, records: List[Dict[str, object]]) -> Dict[str, torch.Tensor]:
    texts = [str(record["text"]) for record in records]
    labels = torch.tensor([int(record["label"]) for record in records], dtype=torch.long)
    encoded = tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=128,
        return_tensors="pt",
    )
    encoded["labels"] = labels
    return encoded


def evaluate(model, tokenizer, records: List[Dict[str, object]], batch_size: int) -> Dict[str, float]:
    model.eval()
    total = 0
    correct = 0
    total_loss = 0.0

    with torch.no_grad():
        for batch in batch_records(records, batch_size):
            encoded = encode_batch(tokenizer, batch)
            outputs = model(**encoded)
            predictions = torch.argmax(outputs.logits, dim=-1)
            correct += int((predictions == encoded["labels"]).sum().item())
            total += len(batch)
            total_loss += float(outputs.loss.item()) * len(batch)

    return {
        "eval_accuracy": correct / total if total else 0.0,
        "eval_loss": total_loss / total if total else 0.0,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a tiny Hugging Face text classifier.")
    parser.add_argument("--model-id", required=True)
    parser.add_argument("--num-labels", type=int, default=3)
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--learning-rate", type=float, default=5e-5)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    train_dir = Path(os.environ.get("SM_CHANNEL_TRAIN", "/opt/ml/input/data/train"))
    test_dir = Path(os.environ.get("SM_CHANNEL_TEST", "/opt/ml/input/data/test"))
    model_dir = Path(os.environ.get("SM_MODEL_DIR", "/opt/ml/model"))

    train_records = read_jsonl(train_dir / "train.jsonl")
    test_records = read_jsonl(test_dir / "test.jsonl")

    tokenizer = AutoTokenizer.from_pretrained(args.model_id)
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model_id,
        num_labels=args.num_labels,
    )
    optimizer = AdamW(model.parameters(), lr=args.learning_rate)

    model.train()
    for epoch in range(args.epochs):
        total_loss = 0.0
        total = 0
        for batch in batch_records(train_records, args.batch_size):
            encoded = encode_batch(tokenizer, batch)
            outputs = model(**encoded)
            outputs.loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            total_loss += float(outputs.loss.item()) * len(batch)
            total += len(batch)

        average_loss = total_loss / total if total else 0.0
        print(f"epoch={epoch + 1} train_loss={average_loss:.6f}")

    metrics = evaluate(model, tokenizer, test_records, args.batch_size)
    print(f"eval_accuracy={metrics['eval_accuracy']:.6f}")
    print(f"eval_loss={metrics['eval_loss']:.6f}")

    model_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(model_dir)
    tokenizer.save_pretrained(model_dir)
    with (model_dir / "metrics.json").open("w", encoding="utf-8") as metrics_file:
        json.dump(metrics, metrics_file, indent=2)

    print(f"Saved model artifact contents to {model_dir}")


if __name__ == "__main__":
    main()
