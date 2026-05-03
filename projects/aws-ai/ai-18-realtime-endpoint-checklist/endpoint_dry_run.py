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
    base_name = f"ai-18-realtime-classifier-{timestamp}"
    return {
        "model_name": base_name,
        "endpoint_config_name": f"{base_name}-config",
        "endpoint_name": f"{base_name}-endpoint",
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
            {"Key": "Lesson", "Value": "ai-18-realtime-endpoint-checklist"},
        ],
    }


def build_create_endpoint_config_request(
    config: Dict[str, Any],
    model_name: str,
    endpoint_config_name: str,
) -> Dict[str, Any]:
    return {
        "EndpointConfigName": endpoint_config_name,
        "ProductionVariants": [
            {
                "VariantName": "AllTraffic",
                "ModelName": model_name,
                "InitialInstanceCount": config["endpoint_initial_instance_count"],
                "InstanceType": config["endpoint_instance_type"],
                "InitialVariantWeight": 1.0,
            }
        ],
        "Tags": [
            {"Key": "Project", "Value": "aws-ai"},
            {"Key": "Lesson", "Value": "ai-18-realtime-endpoint-checklist"},
        ],
    }


def build_create_endpoint_request(endpoint_name: str, endpoint_config_name: str) -> Dict[str, Any]:
    return {
        "EndpointName": endpoint_name,
        "EndpointConfigName": endpoint_config_name,
        "Tags": [
            {"Key": "Project", "Value": "aws-ai"},
            {"Key": "Lesson", "Value": "ai-18-realtime-endpoint-checklist"},
        ],
    }


def build_invoke_endpoint_example(endpoint_name: str) -> Dict[str, Any]:
    return {
        "EndpointName": endpoint_name,
        "ContentType": "application/json",
        "Accept": "application/json",
        "Body": {
            "text": "The support team answered quickly and solved my issue."
        },
    }


def print_json(title: str, payload: Dict[str, Any]) -> None:
    print(title)
    print(json.dumps(payload, indent=2))
    print()


def main() -> None:
    config = load_config()
    names = build_resource_names()

    print("AI-18 SageMaker real-time endpoint dry run")
    print("Dry run only: this script does not create AWS resources.")
    print()
    print("Create order:")
    print("  1. CreateModel")
    print("  2. CreateEndpointConfig")
    print("  3. CreateEndpoint")
    print("  4. Wait for endpoint status InService")
    print("  5. InvokeEndpoint")
    print()

    print_json(
        "create_model request:",
        build_create_model_request(config, names["model_name"]),
    )
    print_json(
        "create_endpoint_config request:",
        build_create_endpoint_config_request(
            config,
            names["model_name"],
            names["endpoint_config_name"],
        ),
    )
    print_json(
        "create_endpoint request:",
        build_create_endpoint_request(
            names["endpoint_name"],
            names["endpoint_config_name"],
        ),
    )
    print_json(
        "invoke_endpoint example:",
        build_invoke_endpoint_example(names["endpoint_name"]),
    )

    print("Delete order:")
    print(f"  1. DeleteEndpoint: {names['endpoint_name']}")
    print(f"  2. DeleteEndpointConfig: {names['endpoint_config_name']}")
    print(f"  3. DeleteModel: {names['model_name']}")
    print("  4. Remove temporary S3 artifacts and CloudWatch logs if no longer needed")
    print()
    print("Cost warning:")
    print("  Endpoint billing starts when endpoint instances are created.")
    print("  Do not create an endpoint unless you are ready to delete it immediately after testing.")


if __name__ == "__main__":
    main()
