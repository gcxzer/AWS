import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote_plus

try:
    import boto3
except ImportError:
    boto3 = None


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

_CLIENTS = {}


def lambda_handler(event, context):
    records = event.get("Records", [])
    if not records:
        return {"processed": 0, "results": []}

    results = []
    for record in records:
        results.append(process_s3_record(record))

    return {"processed": len(results), "results": results}


def process_s3_record(record):
    source_bucket = record["s3"]["bucket"]["name"]
    source_key = unquote_plus(record["s3"]["object"]["key"])
    object_size = int(record["s3"]["object"].get("size", 0))
    max_bytes = get_max_bytes()

    if object_size and object_size > max_bytes:
        raise ValueError(f"{source_key} is {object_size} bytes, larger than MAX_BYTES={max_bytes}")

    text = read_s3_text(source_bucket, source_key, max_bytes)
    summary = build_text_summary(
        text=text,
        source_bucket=source_bucket,
        source_key=source_key,
        object_size=object_size,
    )

    output_bucket = get_required_env("OUTPUT_BUCKET")
    output_key = build_output_key(source_key)
    body = json.dumps(summary, ensure_ascii=False, indent=2).encode("utf-8")

    client("s3").put_object(
        Bucket=output_bucket,
        Key=output_key,
        Body=body,
        ContentType="application/json; charset=utf-8",
    )

    publish_notification(summary, output_bucket, output_key)
    LOGGER.info("Processed s3://%s/%s -> s3://%s/%s", source_bucket, source_key, output_bucket, output_key)

    return {
        "source": f"s3://{source_bucket}/{source_key}",
        "output": f"s3://{output_bucket}/{output_key}",
        "line_count": summary["line_count"],
        "word_count": summary["word_count"],
    }


def read_s3_text(bucket, key, max_bytes):
    response = client("s3").get_object(Bucket=bucket, Key=key)
    body = response["Body"].read(max_bytes + 1)
    if len(body) > max_bytes:
        raise ValueError(f"{key} is larger than MAX_BYTES={max_bytes}")
    return body.decode("utf-8")


def build_text_summary(text, source_bucket="", source_key="", object_size=0):
    lines = text.splitlines()
    non_empty_lines = [line for line in lines if line.strip()]
    words = text.split()
    headers = parse_csv_headers(source_key, lines)

    summary = {
        "source_bucket": source_bucket,
        "source_key": source_key,
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "object_size_bytes": object_size or len(text.encode("utf-8")),
        "line_count": len(lines),
        "non_empty_line_count": len(non_empty_lines),
        "word_count": len(words),
        "character_count": len(text),
        "preview": [line[:160] for line in non_empty_lines[:5]],
    }

    if headers:
        summary["csv"] = {
            "columns": headers,
            "column_count": len(headers),
            "data_row_count": max(len(non_empty_lines) - 1, 0),
        }

    return summary


def parse_csv_headers(source_key, lines):
    if not source_key.lower().endswith(".csv") or not lines:
        return []
    return [column.strip() for column in lines[0].split(",") if column.strip()]


def build_output_key(source_key):
    prefix = os.environ.get("OUTPUT_PREFIX", "processed").strip("/")
    normalized_key = source_key.strip("/")
    if prefix:
        return f"{prefix}/{normalized_key}.summary.json"
    return f"{normalized_key}.summary.json"


def publish_notification(summary, output_bucket, output_key):
    topic_arn = os.environ.get("SNS_TOPIC_ARN", "").strip()
    if not topic_arn:
        return

    message = {
        "source": f"s3://{summary['source_bucket']}/{summary['source_key']}",
        "output": f"s3://{output_bucket}/{output_key}",
        "line_count": summary["line_count"],
        "word_count": summary["word_count"],
        "processed_at": summary["processed_at"],
    }
    client("sns").publish(
        TopicArn=topic_arn,
        Subject="AWS learning file processed",
        Message=json.dumps(message, ensure_ascii=False, indent=2),
    )


def get_max_bytes():
    return int(os.environ.get("MAX_BYTES", "1048576"))


def get_required_env(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"{name} environment variable is required")
    return value


def client(service_name):
    if boto3 is None:
        raise RuntimeError("boto3 is required when running against AWS")

    if service_name not in _CLIENTS:
        _CLIENTS[service_name] = boto3.client(service_name)
    return _CLIENTS[service_name]


def main(argv):
    sample_path = Path(argv[1]) if len(argv) > 1 else Path("sample-data/sample.csv")
    text = sample_path.read_text(encoding="utf-8")
    summary = build_text_summary(
        text=text,
        source_bucket="local-input-bucket",
        source_key=sample_path.name,
        object_size=sample_path.stat().st_size,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv)
