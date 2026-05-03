import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


PROJECT_DIR = Path(__file__).parent
CONFIG_PATH = PROJECT_DIR / "config.json"


def load_config() -> Dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


def build_resource_names() -> Dict[str, str]:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    base_name = f"ai-16-batch-classifier-{timestamp}"
    return {
        "model_name": base_name,
        "transform_job_name": f"{base_name}-transform",
    }


def build_create_model_request(config: Dict[str, Any], model_name: str) -> Dict[str, Any]:
    return {
        "ModelName": model_name,
        "ExecutionRoleArn": config["sagemaker_role_arn"],
        "PrimaryContainer": {
            "Image": config["inference_image_uri"],
            "ModelDataUrl": config["source_model_artifact_s3_uri"],
            "Environment": {
                "SAGEMAKER_PROGRAM": "inference.py",
                "SAGEMAKER_SUBMIT_DIRECTORY": "/opt/ml/model/code",
                "SAGEMAKER_CONTAINER_LOG_LEVEL": "20",
                "SAGEMAKER_REGION": config["region"],
            },
        },
        "Tags": [
            {"Key": "Project", "Value": "aws-ai"},
            {"Key": "Lesson", "Value": "ai-16-batch-transform-offline-inference"},
        ],
    }


def build_create_transform_job_request(
    config: Dict[str, Any],
    model_name: str,
    transform_job_name: str,
) -> Dict[str, Any]:
    return {
        "TransformJobName": transform_job_name,
        "ModelName": model_name,
        "BatchStrategy": "SingleRecord",
        "TransformInput": {
            "DataSource": {
                "S3DataSource": {
                    "S3DataType": "S3Prefix",
                    "S3Uri": config["transform_input_s3_uri"],
                }
            },
            "ContentType": "application/jsonlines",
            "SplitType": "Line",
        },
        "TransformOutput": {
            "S3OutputPath": config["transform_output_s3_uri"],
            "Accept": "application/jsonlines",
            "AssembleWith": "Line",
        },
        "TransformResources": {
            "InstanceType": config["transform_instance_type"],
            "InstanceCount": config["transform_instance_count"],
        },
        "Tags": [
            {"Key": "Project", "Value": "aws-ai"},
            {"Key": "Lesson", "Value": "ai-16-batch-transform-offline-inference"},
        ],
    }


def print_json(title: str, payload: Dict[str, Any]) -> None:
    print(title)
    print(json.dumps(payload, indent=2))
    print()


def main() -> None:
    config = load_config()
    names = build_resource_names()

    print("AI-16 SageMaker Batch Transform plan")
    print("Dry run only: this script does not create AWS resources.")
    print()
    print("Resource order:")
    print("  1. SageMaker Model")
    print("  2. Batch Transform Job")
    print("  3. S3 prediction output")
    print("  4. Delete model and temporary S3 output when no longer needed")
    print()

    print_json(
        "create_model request:",
        build_create_model_request(config, names["model_name"]),
    )
    print_json(
        "create_transform_job request:",
        build_create_transform_job_request(
            config,
            names["model_name"],
            names["transform_job_name"],
        ),
    )

    print("Cost note:")
    print("  Batch Transform starts temporary instances and stops when the job completes.")
    print("  It avoids the long-running endpoint cost risk.")


if __name__ == "__main__":
    main()
