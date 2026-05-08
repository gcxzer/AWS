"""Save one chat message to DynamoDB."""

from __future__ import annotations

import argparse
import json

from config import AWS_PROFILE, AWS_REGION, CHAT_MESSAGES_TABLE, DEFAULT_USER_ID
from dynamodb_client import save_chat_message


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Save a chat message to DynamoDB.")
    parser.add_argument("--session-id", default="session_002")
    parser.add_argument("--user-id", default=DEFAULT_USER_ID)
    parser.add_argument("--document-id", default="doc_003")
    parser.add_argument("--role", choices=["user", "assistant", "system"], default="user")
    parser.add_argument("--content", default="Summarize this document.")
    parser.add_argument("--created-at")
    parser.add_argument("--table", default=CHAT_MESSAGES_TABLE)
    parser.add_argument("--profile", default=AWS_PROFILE)
    parser.add_argument("--region", default=AWS_REGION)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    item = save_chat_message(
        session_id=args.session_id,
        user_id=args.user_id,
        document_id=args.document_id,
        role=args.role,
        content=args.content,
        created_at=args.created_at,
        table_name=args.table,
        profile_name=args.profile,
        region_name=args.region,
    )
    print(json.dumps(item, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
