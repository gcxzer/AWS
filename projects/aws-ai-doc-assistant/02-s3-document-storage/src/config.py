"""Shared configuration for the AWS AI document assistant."""

from __future__ import annotations

import os


AWS_PROFILE = os.getenv("AWS_PROFILE", "aws-learning")
AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")

S3_BUCKET = os.getenv(
    "S3_BUCKET",
    "aws-ai-doc-assistant-xzhu-089781651608-eu-central-1-an",
)

DEFAULT_USER_ID = os.getenv("DEFAULT_USER_ID", "user_001")
PROJECT_NAME = "aws-ai-doc-assistant"
STAGE = os.getenv("STAGE", "learning")
