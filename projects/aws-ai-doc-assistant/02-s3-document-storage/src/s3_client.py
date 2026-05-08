"""Small S3 helper functions used by the learning project."""

from __future__ import annotations

import mimetypes
from pathlib import Path
from typing import Any

import boto3

from config import AWS_PROFILE, AWS_REGION, PROJECT_NAME, S3_BUCKET, STAGE


def make_s3_client(profile_name: str = AWS_PROFILE, region_name: str = AWS_REGION):
    session = boto3.Session(profile_name=profile_name, region_name=region_name)
    return session.client("s3")


def build_document_key(file_path: str | Path, user_id: str) -> str:
    path = Path(file_path)
    return f"raw/{user_id}/{path.name}"


def upload_document(
    file_path: str | Path,
    *,
    bucket: str = S3_BUCKET,
    key: str,
    user_id: str,
    document_type: str,
    source: str,
    profile_name: str = AWS_PROFILE,
    region_name: str = AWS_REGION,
) -> dict[str, Any]:
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    metadata = {
        "user-id": user_id,
        "document-type": document_type,
        "source": source,
    }
    tags = {
        "project": PROJECT_NAME,
        "stage": STAGE,
        "owner": user_id,
    }

    s3 = make_s3_client(profile_name=profile_name, region_name=region_name)
    s3.upload_file(
        str(path),
        bucket,
        key,
        ExtraArgs={
            "ContentType": content_type,
            "Metadata": metadata,
            "ServerSideEncryption": "AES256",
        },
    )
    s3.put_object_tagging(
        Bucket=bucket,
        Key=key,
        Tagging={"TagSet": [{"Key": k, "Value": v} for k, v in tags.items()]},
    )

    head = s3.head_object(Bucket=bucket, Key=key)
    return {
        "bucket": bucket,
        "key": key,
        "s3_uri": f"s3://{bucket}/{key}",
        "content_type": head.get("ContentType"),
        "content_length": head.get("ContentLength"),
        "encryption": head.get("ServerSideEncryption"),
        "metadata": head.get("Metadata", {}),
        "tags": tags,
    }


def create_presigned_download_url(
    *,
    bucket: str = S3_BUCKET,
    key: str,
    expires_in: int = 300,
    profile_name: str = AWS_PROFILE,
    region_name: str = AWS_REGION,
) -> str:
    s3 = make_s3_client(profile_name=profile_name, region_name=region_name)
    return s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": bucket,
            "Key": key,
            "ResponseContentDisposition": "inline",
        },
        ExpiresIn=expires_in,
    )
