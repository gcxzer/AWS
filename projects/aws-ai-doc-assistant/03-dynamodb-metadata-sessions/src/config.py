"""Configuration for the DynamoDB learning stage."""

from __future__ import annotations

import os


AWS_PROFILE = os.getenv("AWS_PROFILE", "aws-learning")
AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")

DOCUMENTS_TABLE = os.getenv("DOCUMENTS_TABLE", "DocAssistantDocuments")
CHAT_MESSAGES_TABLE = os.getenv("CHAT_MESSAGES_TABLE", "DocAssistantChatMessages")
DEFAULT_USER_ID = os.getenv("DEFAULT_USER_ID", "user_001")

S3_BUCKET = os.getenv(
    "S3_BUCKET",
    "aws-ai-doc-assistant-xzhu-089781651608-eu-central-1-an",
)
