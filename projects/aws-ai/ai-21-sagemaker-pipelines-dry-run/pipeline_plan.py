import json
from pathlib import Path
from typing import Any, Dict


PROJECT_DIR = Path(__file__).parent
CONFIG_PATH = PROJECT_DIR / "config.json"


def load_config() -> Dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


def build_pipeline_definition(config: Dict[str, Any]) -> Dict[str, Any]:
    bucket = config["bucket"]
    prefix = config["prefix"].strip("/")

    return {
        "Version": "2020-12-01",
        "Metadata": {
            "Purpose": "Local dry-run pipeline definition for AI-21",
            "Note": "This is a readable request plan. A real pipeline should be generated with the SageMaker SDK so property references are valid.",
        },
        "Parameters": [
            {
                "Name": "InputDataUri",
                "Type": "String",
                "DefaultValue": config["source_raw_data_s3_uri"],
            },
            {
                "Name": "ModelApprovalStatus",
                "Type": "String",
                "DefaultValue": config["default_approval_status"],
            },
            {
                "Name": "AccuracyThreshold",
                "Type": "Float",
                "DefaultValue": config["accuracy_threshold"],
            },
        ],
        "Steps": [
            {
                "Name": "ProcessReviews",
                "Type": "Processing",
                "Purpose": "Run preprocessing and write train/test JSONL to S3.",
                "Inputs": [
                    {
                        "Name": "raw-reviews",
                        "S3Uri": "${InputDataUri}",
                    }
                ],
                "Outputs": [
                    {
                        "Name": "processed-data",
                        "S3Uri": f"s3://{bucket}/{prefix}/processed/",
                    }
                ],
                "ImageUri": config["processing_image_uri"],
            },
            {
                "Name": "TrainClassifier",
                "Type": "Training",
                "DependsOn": ["ProcessReviews"],
                "Purpose": "Train Hugging Face text classifier from processed data.",
                "Inputs": [
                    {
                        "Name": "train",
                        "S3Uri": f"s3://{bucket}/{prefix}/processed/train/",
                    },
                    {
                        "Name": "test",
                        "S3Uri": f"s3://{bucket}/{prefix}/processed/test/",
                    },
                ],
                "OutputModelArtifact": f"s3://{bucket}/{prefix}/models/",
                "ImageUri": config["training_image_uri"],
            },
            {
                "Name": "EvaluateModel",
                "Type": "Processing",
                "DependsOn": ["TrainClassifier"],
                "Purpose": "Evaluate model artifact and write metrics JSON to S3.",
                "Inputs": [
                    {
                        "Name": "model-artifact",
                        "S3Uri": "${Steps.TrainClassifier.ModelArtifacts.S3ModelArtifacts}",
                    },
                    {
                        "Name": "test-data",
                        "S3Uri": f"s3://{bucket}/{prefix}/processed/test/",
                    },
                ],
                "Outputs": [
                    {
                        "Name": "evaluation",
                        "S3Uri": f"s3://{bucket}/{prefix}/evaluation/",
                    }
                ],
                "ImageUri": config["processing_image_uri"],
            },
            {
                "Name": "CheckAccuracy",
                "Type": "Condition",
                "DependsOn": ["EvaluateModel"],
                "Purpose": "Only register the model if evaluation accuracy meets the threshold.",
                "Condition": {
                    "Metric": "eval_accuracy",
                    "Operator": "GreaterThanOrEqualTo",
                    "Threshold": "${AccuracyThreshold}",
                    "Source": "${Steps.EvaluateModel.ProcessingOutputConfig.Outputs['evaluation']}",
                },
                "IfSteps": [
                    {
                        "Name": "RegisterModel",
                        "Type": "RegisterModel",
                        "Purpose": "Register approved candidate in SageMaker Model Registry.",
                        "ModelPackageGroupName": config["model_package_group_name"],
                        "ModelApprovalStatus": "${ModelApprovalStatus}",
                        "ModelDataUrl": "${Steps.TrainClassifier.ModelArtifacts.S3ModelArtifacts}",
                        "InferenceImage": config["inference_image_uri"],
                    }
                ],
                "ElseSteps": [
                    {
                        "Name": "SkipRegistration",
                        "Type": "Fail",
                        "Purpose": "Stop pipeline because model quality is below threshold.",
                    }
                ],
            },
        ],
    }


def build_create_pipeline_request(config: Dict[str, Any]) -> Dict[str, Any]:
    pipeline_definition = build_pipeline_definition(config)
    return {
        "PipelineName": config["pipeline_name"],
        "PipelineDisplayName": "AI-21 Review Classifier Pipeline",
        "PipelineDescription": config["pipeline_description"],
        "RoleArn": config["sagemaker_role_arn"],
        "PipelineDefinition": json.dumps(pipeline_definition, indent=2),
        "Tags": [
            {"Key": "Project", "Value": "aws-ai"},
            {"Key": "Lesson", "Value": "ai-21-sagemaker-pipelines-dry-run"},
        ],
    }


def main() -> None:
    config = load_config()
    request = build_create_pipeline_request(config)
    definition = json.loads(request["PipelineDefinition"])

    print("AI-21 SageMaker Pipeline dry run")
    print("Dry run only: this script does not create AWS resources.")
    print()
    print("Pipeline flow:")
    print("  1. Processing step")
    print("  2. Training step")
    print("  3. Evaluation step")
    print("  4. Condition step")
    print("  5. Register model if metrics pass")
    print()
    print("CreatePipeline request:")
    print(json.dumps(request, indent=2))
    print()
    print("Readable pipeline definition:")
    print(json.dumps(definition, indent=2))
    print()
    print("Cost note:")
    print("  A pipeline definition is metadata.")
    print("  Pipeline execution can create processing, training, and registry resources.")


if __name__ == "__main__":
    main()
