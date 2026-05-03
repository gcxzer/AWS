import json
from pathlib import Path
from typing import Any, Dict


PROJECT_DIR = Path(__file__).parent
CONFIG_PATH = PROJECT_DIR / "config.json"


def load_config() -> Dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


def build_create_model_package_group_request(config: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "ModelPackageGroupName": config["model_package_group_name"],
        "ModelPackageGroupDescription": config["model_package_group_description"],
        "Tags": [
            {"Key": "Project", "Value": "aws-ai"},
            {"Key": "Lesson", "Value": "ai-20-model-registry-dry-run"},
        ],
    }


def build_create_model_package_request(config: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "ModelPackageGroupName": config["model_package_group_name"],
        "ModelPackageDescription": config["model_package_description"],
        "ModelApprovalStatus": config["approval_status"],
        "InferenceSpecification": {
            "Containers": [
                {
                    "Image": config["inference_image_uri"],
                    "ModelDataUrl": config["source_model_artifact_s3_uri"],
                }
            ],
            "SupportedContentTypes": ["application/json"],
            "SupportedResponseMIMETypes": ["application/json"],
            "SupportedRealtimeInferenceInstanceTypes": ["ml.m5.large"],
            "SupportedTransformInstanceTypes": ["ml.m5.large"],
        },
        "ModelMetrics": {
            "ModelQuality": {
                "Statistics": {
                    "ContentType": "application/json",
                    "S3Uri": "s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-20/metrics/model-quality.json",
                }
            }
        },
        "CustomerMetadataProperties": {
            "eval_accuracy": str(config["eval_accuracy"]),
            "eval_loss": str(config["eval_loss"]),
            "source": "ai-14-huggingface-training-jobs",
        },
        "Tags": [
            {"Key": "Project", "Value": "aws-ai"},
            {"Key": "Lesson", "Value": "ai-20-model-registry-dry-run"},
        ],
    }


def build_update_approval_request(config: Dict[str, Any], model_package_arn: str) -> Dict[str, Any]:
    return {
        "ModelPackageArn": model_package_arn,
        "ModelApprovalStatus": "Approved",
        "ApprovalDescription": "Approved after reviewing evaluation metrics and deployment readiness.",
    }


def print_json(title: str, payload: Dict[str, Any]) -> None:
    print(title)
    print(json.dumps(payload, indent=2))
    print()


def main() -> None:
    config = load_config()
    placeholder_package_arn = (
        "arn:aws:sagemaker:eu-central-1:089781651608:model-package/"
        f"{config['model_package_group_name']}/1"
    )

    print("AI-20 SageMaker Model Registry dry run")
    print("Dry run only: this script does not create AWS resources.")
    print()
    print("Registry flow:")
    print("  1. CreateModelPackageGroup")
    print("  2. CreateModelPackage")
    print("  3. Review metrics")
    print("  4. UpdateModelPackage approval status")
    print()

    print_json(
        "create_model_package_group request:",
        build_create_model_package_group_request(config),
    )
    print_json(
        "create_model_package request:",
        build_create_model_package_request(config),
    )
    print_json(
        "update_model_package approval request:",
        build_update_approval_request(config, placeholder_package_arn),
    )

    print("Cost note:")
    print("  Model Registry resources are control-plane metadata.")
    print("  Main costs still come from training jobs, endpoints, batch jobs, S3, and logs.")


if __name__ == "__main__":
    main()
