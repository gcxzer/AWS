"""Query all chat messages for one session."""

from __future__ import annotations

import argparse
import json

from config import AWS_PROFILE, AWS_REGION, CHAT_MESSAGES_TABLE
from dynamodb_client import get_chat_history


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Query chat history by session_id.")
    parser.add_argument("session_id", nargs="?", default="session_002")
    parser.add_argument("--table", default=CHAT_MESSAGES_TABLE)
    parser.add_argument("--profile", default=AWS_PROFILE)
    parser.add_argument("--region", default=AWS_REGION)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    items = get_chat_history(
        args.session_id,
        table_name=args.table,
        profile_name=args.profile,
        region_name=args.region,
    )
    print(json.dumps(items, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
