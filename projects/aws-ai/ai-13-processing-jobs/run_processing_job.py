import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import boto3
from botocore.exceptions import BotoCoreError, ClientError, TokenRetrievalError


PROJECT_DIR = Path(__file__).parent
CONFIG_PATH = PROJECT_DIR / "config.json"


def load_config() -> Dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


def build_job_name() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"ai-13-preprocess-{timestamp}"


def main() -> None:
    config = load_config()
    session = boto3.Session(
        profile_name=config["profile"],
        region_name=config["region"],
    )
    sagemaker = session.client("sagemaker")

    bucket = config["bucket"]
    prefix = config["prefix"].strip("/")
    job_name = build_job_name()
    output_s3_uri = f"s3://{bucket}/{prefix}/processed/{job_name}"

    sagemaker.create_processing_job(
        ProcessingJobName=job_name,
        RoleArn=config["sagemaker_role_arn"],
        AppSpecification={
            "ImageUri": config["processing_image_uri"],
            "ContainerEntrypoint": [
                "python",
                "/opt/ml/processing/code/preprocess_reviews.py",
            ],
            "ContainerArguments": [
                "--input",
                "/opt/ml/processing/input/sample_reviews.jsonl",
                "--output-dir",
                "/opt/ml/processing/output",
            ],
        },
        ProcessingInputs=[
            {
                "InputName": "raw-reviews",
                "S3Input": {
                    "S3Uri": f"s3://{bucket}/{prefix}/raw/",
                    "LocalPath": "/opt/ml/processing/input",
                    "S3DataType": "S3Prefix",
                    "S3InputMode": "File",
                    "S3DataDistributionType": "FullyReplicated",
                    "S3CompressionType": "None",
                },
            },
            {
                "InputName": "preprocess-script",
                "S3Input": {
                    "S3Uri": f"s3://{bucket}/{prefix}/scripts/",
                    "LocalPath": "/opt/ml/processing/code",
                    "S3DataType": "S3Prefix",
                    "S3InputMode": "File",
                    "S3DataDistributionType": "FullyReplicated",
                    "S3CompressionType": "None",
                },
            },
        ],
        ProcessingOutputConfig={
            "Outputs": [
                {
                    "OutputName": "processed-data",
                    "S3Output": {
                        "S3Uri": output_s3_uri,
                        "LocalPath": "/opt/ml/processing/output",
                        "S3UploadMode": "EndOfJob",
                    },
                }
            ]
        },
        ProcessingResources={
            "ClusterConfig": {
                "InstanceCount": 1,
                "InstanceType": config["processing_instance_type"],
                "VolumeSizeInGB": config["processing_volume_size_gb"],
            }
        },
        StoppingCondition={
            "MaxRuntimeInSeconds": config["processing_max_runtime_seconds"],
        },
        Tags=[
            {"Key": "Project", "Value": "aws-ai"},
            {"Key": "Lesson", "Value": "ai-13-processing-jobs"},
        ],
    )

    print("Created SageMaker Processing job:")
    print(f"  Job name: {job_name}")
    print(f"  Instance: {config['processing_instance_type']}")
    print(f"  Image: {config['processing_image_uri']}")
    print(f"  Output: {output_s3_uri}")
    print()
    print("Check status:")
    print(
        "  aws sagemaker describe-processing-job "
        f"--processing-job-name {job_name} "
        f"--region {config['region']} "
        f"--profile {config['profile']} "
        "--query 'ProcessingJobStatus'"
    )


if __name__ == "__main__":
    try:
        main()
    except TokenRetrievalError as error:
        print("AWS SSO token is expired or cannot be refreshed.")
        print()
        print("Run this first:")
        print("  aws sso login --profile aws-learning")
        print()
        print(f"Original error: {error}")
        raise SystemExit(1)
    except (BotoCoreError, ClientError, OSError) as error:
        print("SageMaker Processing job creation failed.")
        print(f"Original error: {error}")
        raise SystemExit(1)
