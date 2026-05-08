"""Small DynamoDB helper functions for the learning project."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import boto3
from boto3.dynamodb.conditions import Key

from config import AWS_PROFILE, AWS_REGION, CHAT_MESSAGES_TABLE, DOCUMENTS_TABLE, S3_BUCKET


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def make_dynamodb_resource(profile_name: str = AWS_PROFILE, region_name: str = AWS_REGION):
    session = boto3.Session(profile_name=profile_name, region_name=region_name)
    return session.resource("dynamodb")


def documents_table(
    table_name: str = DOCUMENTS_TABLE,
    *,
    profile_name: str = AWS_PROFILE,
    region_name: str = AWS_REGION,
):
    dynamodb = make_dynamodb_resource(profile_name=profile_name, region_name=region_name)
    return dynamodb.Table(table_name)


def chat_messages_table(
    table_name: str = CHAT_MESSAGES_TABLE,
    *,
    profile_name: str = AWS_PROFILE,
    region_name: str = AWS_REGION,
):
    dynamodb = make_dynamodb_resource(profile_name=profile_name, region_name=region_name)
    return dynamodb.Table(table_name)


def build_s3_uri(bucket: str, key: str) -> str:
    return f"s3://{bucket}/{key}"


def save_document_metadata(
    *,
    user_id: str,
    document_id: str,
    title: str,
    s3_key: str,
    status: str = "uploaded",
    s3_bucket: str = S3_BUCKET,
    uploaded_at: str | None = None,
    table_name: str = DOCUMENTS_TABLE,
    profile_name: str = AWS_PROFILE,
    region_name: str = AWS_REGION,
) -> dict[str, Any]:
    item = {
        "user_id": user_id,
        "document_id": document_id,
        "title": title,
        "s3_bucket": s3_bucket,
        "s3_key": s3_key,
        "s3_uri": build_s3_uri(s3_bucket, s3_key),
        "status": status,
        "uploaded_at": uploaded_at or now_iso(),
    }

    table = documents_table(table_name, profile_name=profile_name, region_name=region_name)
    table.put_item(Item=item)
    return item


def get_user_documents(
    user_id: str,
    *,
    table_name: str = DOCUMENTS_TABLE,
    profile_name: str = AWS_PROFILE,
    region_name: str = AWS_REGION,
) -> list[dict[str, Any]]:
    table = documents_table(table_name, profile_name=profile_name, region_name=region_name)
    response = table.query(KeyConditionExpression=Key("user_id").eq(user_id))
    return response.get("Items", [])


def get_document(
    user_id: str,
    document_id: str,
    *,
    table_name: str = DOCUMENTS_TABLE,
    profile_name: str = AWS_PROFILE,
    region_name: str = AWS_REGION,
) -> dict[str, Any] | None:
    table = documents_table(table_name, profile_name=profile_name, region_name=region_name)
    response = table.get_item(Key={"user_id": user_id, "document_id": document_id})
    return response.get("Item")


def save_chat_message(
    *,
    session_id: str,
    user_id: str,
    role: str,
    content: str,
    document_id: str | None = None,
    created_at: str | None = None,
    table_name: str = CHAT_MESSAGES_TABLE,
    profile_name: str = AWS_PROFILE,
    region_name: str = AWS_REGION,
) -> dict[str, Any]:
    item = {
        "session_id": session_id,
        "created_at": created_at or now_iso(),
        "user_id": user_id,
        "role": role,
        "content": content,
    }
    if document_id:
        item["document_id"] = document_id

    table = chat_messages_table(table_name, profile_name=profile_name, region_name=region_name)
    table.put_item(Item=item)
    return item


def get_chat_history(
    session_id: str,
    *,
    table_name: str = CHAT_MESSAGES_TABLE,
    profile_name: str = AWS_PROFILE,
    region_name: str = AWS_REGION,
) -> list[dict[str, Any]]:
    table = chat_messages_table(table_name, profile_name=profile_name, region_name=region_name)
    response = table.query(KeyConditionExpression=Key("session_id").eq(session_id))
    return response.get("Items", [])
