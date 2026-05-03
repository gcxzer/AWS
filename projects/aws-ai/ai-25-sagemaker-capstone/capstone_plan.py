import json
from pathlib import Path
from typing import Any, Dict, List


PROJECT_DIR = Path(__file__).parent
CONFIG_PATH = PROJECT_DIR / "config.json"


def load_config() -> Dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


def build_stage_plan(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        {
            "Stage": "01-data-layout",
            "Purpose": "Keep raw data, scripts, model artifacts, evaluation files, and batch outputs in predictable S3 prefixes.",
            "Inputs": ["local files"],
            "Outputs": [
                config["raw_data_s3_uri"],
                config["scripts_s3_uri"],
            ],
            "AWSResources": ["S3"],
            "CostBehavior": "S3 storage only unless data is moved or processed.",
        },
        {
            "Stage": "02-processing",
            "Purpose": "Convert raw JSONL reviews into train/test data for the classifier.",
            "Inputs": [config["raw_data_s3_uri"], config["scripts_s3_uri"]],
            "Outputs": [config["processed_data_s3_uri"]],
            "AWSResources": ["SageMaker Processing Job"],
            "InstanceType": config["processing_instance_type"],
            "CostBehavior": "Job style cost. Charges stop when the job completes.",
        },
        {
            "Stage": "03-training-or-packaging",
            "Purpose": "Train or package a Hugging Face text classifier and produce model.tar.gz.",
            "Inputs": [config["processed_data_s3_uri"], config["scripts_s3_uri"]],
            "Outputs": [config["model_artifact_s3_uri"]],
            "AWSResources": ["SageMaker Training Job"],
            "InstanceType": config["training_instance_type"],
            "CostBehavior": "Job style cost. Quotas may block the chosen instance type.",
        },
        {
            "Stage": "04-evaluation",
            "Purpose": "Write metrics.json so the model can be judged before registration.",
            "Inputs": [config["model_artifact_s3_uri"], config["processed_data_s3_uri"]],
            "Outputs": [config["evaluation_s3_uri"]],
            "AWSResources": ["SageMaker Processing Job or training-script evaluation output"],
            "CostBehavior": "No extra job if metrics are emitted by training; otherwise processing cost.",
        },
        {
            "Stage": "05-model-registry",
            "Purpose": "Register the model artifact and supported inference metadata.",
            "Inputs": [config["model_artifact_s3_uri"], config["evaluation_s3_uri"]],
            "Outputs": [config["model_package_group_name"]],
            "AWSResources": ["Model Package Group", "Model Package"],
            "CostBehavior": "Control-plane metadata. Deployment costs come later.",
        },
        {
            "Stage": "06-batch-transform",
            "Purpose": "Run offline inference without keeping an endpoint alive.",
            "Inputs": [config["batch_input_s3_uri"], config["model_artifact_s3_uri"]],
            "Outputs": [config["batch_output_s3_uri"]],
            "AWSResources": ["SageMaker Model", "Batch Transform Job"],
            "InstanceType": config["batch_transform_instance_type"],
            "CostBehavior": "Job style cost. Charges stop when the transform job completes.",
        },
        {
            "Stage": "07-optional-realtime-endpoint",
            "Purpose": "Optionally verify realtime inference, then delete immediately.",
            "EnabledByDefault": config["enable_realtime_endpoint"],
            "Inputs": [config["model_artifact_s3_uri"]],
            "Outputs": [config["endpoint_name"]],
            "AWSResources": ["SageMaker Model", "Endpoint Config", "Endpoint"],
            "InstanceType": config["optional_endpoint_instance_type"],
            "CostBehavior": "Service style cost. Charges continue until the endpoint is deleted.",
        },
        {
            "Stage": "08-monitor-clarify-checklist",
            "Purpose": "Design production monitoring and explainability before enabling paid jobs.",
            "EnabledByDefault": config["enable_model_monitor"] or config["enable_clarify"],
            "Inputs": [
                config["data_capture_s3_uri"],
                config["baseline_s3_uri"],
            ],
            "Outputs": ["monitoring checklist", "clarify checklist"],
            "AWSResources": ["Data Capture", "Monitoring Schedule", "Clarify Processing Job"],
            "CostBehavior": "Potential S3, processing, and CloudWatch costs if enabled.",
        },
        {
            "Stage": "09-cleanup-report",
            "Purpose": "Prove every paid or persistent resource has a deletion path.",
            "Inputs": ["all stages above"],
            "Outputs": ["cleanup_checklist.md"],
            "AWSResources": ["SageMaker", "S3", "CloudWatch", "ECR"],
            "CostBehavior": "Cleanup prevents accidental ongoing cost.",
        },
    ]


def build_registry_plan(config: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "CreateModelPackageGroup": {
            "ModelPackageGroupName": config["model_package_group_name"],
            "ModelPackageGroupDescription": "AI-25 capstone review classifier model package group",
        },
        "CreateModelPackage": {
            "ModelPackageGroupName": config["model_package_group_name"],
            "ModelApprovalStatus": "PendingManualApproval",
            "InferenceSpecification": {
                "Containers": [
                    {
                        "Image": "pytorch-inference-cpu-image-placeholder",
                        "ModelDataUrl": config["model_artifact_s3_uri"],
                    }
                ],
                "SupportedContentTypes": ["application/json"],
                "SupportedResponseMIMETypes": ["application/json"],
                "SupportedRealtimeInferenceInstanceTypes": [
                    config["optional_endpoint_instance_type"]
                ],
                "SupportedTransformInstanceTypes": [
                    config["batch_transform_instance_type"]
                ],
            },
            "CustomerMetadataProperties": {
                "base_model": config["base_model"],
                "project": config["project_name"],
                "evaluation": config["evaluation_s3_uri"],
            },
        },
    }


def build_optional_endpoint_plan(config: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "EnabledByDefault": config["enable_realtime_endpoint"],
        "CreateModel": {
            "ModelName": config["model_name"],
            "ExecutionRoleArn": config["sagemaker_role_arn"],
            "PrimaryContainer": {
                "Image": "pytorch-inference-cpu-image-placeholder",
                "ModelDataUrl": config["model_artifact_s3_uri"],
            },
        },
        "CreateEndpointConfig": {
            "EndpointConfigName": config["endpoint_config_name"],
            "ProductionVariants": [
                {
                    "VariantName": "AllTraffic",
                    "ModelName": config["model_name"],
                    "InitialInstanceCount": 1,
                    "InstanceType": config["optional_endpoint_instance_type"],
                }
            ],
            "DataCaptureConfig": {
                "EnableCapture": False,
                "DestinationS3Uri": config["data_capture_s3_uri"],
                "InitialSamplingPercentage": 100,
            },
        },
        "CreateEndpoint": {
            "EndpointName": config["endpoint_name"],
            "EndpointConfigName": config["endpoint_config_name"],
        },
    }


def build_cleanup_order(config: Dict[str, Any]) -> List[str]:
    return [
        f"Delete endpoint if created: {config['endpoint_name']}",
        f"Delete endpoint config if created: {config['endpoint_config_name']}",
        f"Delete SageMaker model if created: {config['model_name']}",
        "Confirm no running Studio apps, notebooks, or spaces",
        "Confirm no running processing, training, transform, HPO, or pipeline executions",
        f"Delete temporary S3 outputs under s3://{config['bucket']}/{config['prefix']}/ if no longer needed",
        f"Delete or archive model artifacts under {config['model_artifact_s3_uri']}",
        f"Delete temporary model packages/package group if created: {config['model_package_group_name']}",
        "Delete temporary pipeline if created",
        "Delete temporary ECR images if a custom container was built",
        "Delete or set retention on temporary CloudWatch log groups",
    ]


def main() -> None:
    config = load_config()

    print("AI-25 SageMaker Capstone dry run")
    print("Dry run only: this script does not create AWS resources.")
    print()
    print("Theme:")
    print(f"  {config['model_family']} using {config['base_model']}")
    print()
    print("Stage plan:")
    print(json.dumps(build_stage_plan(config), indent=2))
    print()
    print("Model Registry request shape:")
    print(json.dumps(build_registry_plan(config), indent=2))
    print()
    print("Optional realtime endpoint request shape:")
    print(json.dumps(build_optional_endpoint_plan(config), indent=2))
    print()
    print("Cleanup order:")
    for index, item in enumerate(build_cleanup_order(config), start=1):
        print(f"  {index}. {item}")
    print()
    print("Cost note:")
    print("  Batch Transform is the default validation path because it is job based.")
    print("  Realtime endpoints are optional and keep charging until deleted.")


if __name__ == "__main__":
    main()
