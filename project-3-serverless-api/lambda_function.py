import json
import os
from datetime import datetime, timezone
from uuid import uuid4

import boto3


TABLE_NAME = os.environ.get("TABLE_NAME", "learning-notes")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "")
    path = event.get("rawPath", "")

    if method == "GET" and path == "/notes":
        return list_notes()

    if method == "POST" and path == "/notes":
        return create_note(event)

    note_id = get_note_id(event, path)

    if method == "GET" and note_id:
        return get_note(note_id)

    if method == "DELETE" and note_id:
        return delete_note(note_id)

    return response(404, {"message": "Not found"})


def list_notes():
    result = table.scan()
    items = sorted(result.get("Items", []), key=lambda item: item.get("created_at", ""))
    return response(200, {"items": items})


def create_note(event):
    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return response(400, {"message": "Request body must be valid JSON"})

    title = str(body.get("title", "")).strip()
    content = str(body.get("content", "")).strip()

    if not title:
        return response(400, {"message": "title is required"})

    now = datetime.now(timezone.utc).isoformat()
    note = {
        "id": str(uuid4()),
        "title": title,
        "content": content,
        "created_at": now,
        "updated_at": now,
    }
    table.put_item(Item=note)

    return response(201, note)


def get_note(note_id):
    result = table.get_item(Key={"id": note_id})
    item = result.get("Item")

    if not item:
        return response(404, {"message": "Note not found"})

    return response(200, item)


def delete_note(note_id):
    table.delete_item(Key={"id": note_id})
    return response(200, {"deleted": True, "id": note_id})


def get_note_id(event, path):
    path_parameters = event.get("pathParameters") or {}
    note_id = path_parameters.get("id")
    if note_id:
        return note_id

    prefix = "/notes/"
    if path.startswith(prefix) and len(path) > len(prefix):
        return path[len(prefix) :]

    return ""


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "content-type": "application/json",
        },
        "body": json.dumps(body, ensure_ascii=False),
    }
