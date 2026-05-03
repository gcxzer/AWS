import json
from pathlib import Path
from typing import Any, Dict, List


PROJECT_DIR = Path(__file__).parent
CONFIG_PATH = PROJECT_DIR / "config.json"


def load_config() -> Dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


def artifact_arn(config: Dict[str, Any], name: str) -> str:
    return (
        f"arn:aws:sagemaker:{config['region']}:{config['account_id']}:"
        f"artifact/{name}"
    )


def action_arn(config: Dict[str, Any], name: str) -> str:
    return (
        f"arn:aws:sagemaker:{config['region']}:{config['account_id']}:"
        f"action/{name}"
    )


def context_arn(config: Dict[str, Any], name: str) -> str:
    return (
        f"arn:aws:sagemaker:{config['region']}:{config['account_id']}:"
        f"context/{name}"
    )


def build_experiment_plan(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    parameters = {
        key: {"NumberValue": value}
        for key, value in config["hyperparameters"].items()
    }
    metrics = [
        {
            "MetricName": metric_name,
            "Value": metric_value,
            "Source": "evaluation",
        }
        for metric_name, metric_value in config["example_metrics"].items()
    ]

    return [
        {
            "Operation": "CreateExperiment",
            "Request": {
                "ExperimentName": config["experiment_name"],
                "DisplayName": "AI-22 Hugging Face Review Classifier",
                "Description": "Compare training runs for the review classifier learning project.",
                "Tags": [
                    {"Key": "Project", "Value": "aws-ai"},
                    {"Key": "Lesson", "Value": "ai-22-experiments-lineage-debugging"},
                ],
            },
        },
        {
            "Operation": "CreateTrial",
            "Request": {
                "TrialName": config["trial_name"],
                "ExperimentName": config["experiment_name"],
                "DisplayName": "BERT tiny baseline",
                "MetadataProperties": {
                    "ProjectId": "aws-ai-learning",
                    "CommitId": "local-dry-run",
                    "Repository": "local-vscode-workspace",
                },
            },
        },
        {
            "Operation": "CreateTrialComponent",
            "Request": {
                "TrialComponentName": config["trial_component_name"],
                "DisplayName": config["training_job_name"],
                "Status": {
                    "PrimaryStatus": "Completed",
                    "Message": "Example completed training component for dry-run planning.",
                },
                "Parameters": parameters,
                "InputArtifacts": {
                    "train-data": {
                        "MediaType": "application/jsonl",
                        "Value": config["source_data_s3_uri"],
                    },
                    "test-data": {
                        "MediaType": "application/jsonl",
                        "Value": config["test_data_s3_uri"],
                    },
                    "training-code": {
                        "MediaType": "text/x-python",
                        "Value": config["training_script_s3_uri"],
                    },
                },
                "OutputArtifacts": {
                    "model-artifact": {
                        "MediaType": "application/x-tar",
                        "Value": config["model_artifact_s3_uri"],
                    }
                },
                "Metrics": metrics,
            },
        },
        {
            "Operation": "AssociateTrialComponent",
            "Request": {
                "TrialName": config["trial_name"],
                "TrialComponentName": config["trial_component_name"],
            },
        },
    ]


def build_lineage_plan(config: Dict[str, Any]) -> Dict[str, Any]:
    raw_data_artifact_name = "ai-22-raw-training-data"
    script_artifact_name = "ai-22-training-script"
    model_artifact_name = "ai-22-model-artifact"
    training_action_name = "ai-22-training-action"
    registry_context_name = config["model_package_group_name"]

    raw_data_arn = artifact_arn(config, raw_data_artifact_name)
    script_arn = artifact_arn(config, script_artifact_name)
    model_artifact_arn = artifact_arn(config, model_artifact_name)
    training_action_arn = action_arn(config, training_action_name)
    registry_context_arn = context_arn(config, registry_context_name)

    return {
        "Artifacts": [
            {
                "Operation": "CreateArtifact",
                "Request": {
                    "ArtifactName": raw_data_artifact_name,
                    "ArtifactType": "DataSet",
                    "Source": {"SourceUri": config["source_data_s3_uri"]},
                    "Properties": {"format": "jsonl", "purpose": "training"},
                },
                "ExampleArn": raw_data_arn,
            },
            {
                "Operation": "CreateArtifact",
                "Request": {
                    "ArtifactName": script_artifact_name,
                    "ArtifactType": "Code",
                    "Source": {"SourceUri": config["training_script_s3_uri"]},
                    "Properties": {"framework": "huggingface-transformers"},
                },
                "ExampleArn": script_arn,
            },
            {
                "Operation": "CreateArtifact",
                "Request": {
                    "ArtifactName": model_artifact_name,
                    "ArtifactType": "Model",
                    "Source": {"SourceUri": config["model_artifact_s3_uri"]},
                    "Properties": {"base_model": config["model_name"]},
                },
                "ExampleArn": model_artifact_arn,
            },
        ],
        "Actions": [
            {
                "Operation": "CreateAction",
                "Request": {
                    "ActionName": training_action_name,
                    "ActionType": "TrainingJob",
                    "Source": {
                        "SourceUri": (
                            f"arn:aws:sagemaker:{config['region']}:"
                            f"{config['account_id']}:training-job/"
                            f"{config['training_job_name']}"
                        )
                    },
                    "Properties": {
                        "image": "pytorch-training-cpu",
                        "role": config["sagemaker_role_arn"],
                    },
                },
                "ExampleArn": training_action_arn,
            }
        ],
        "Contexts": [
            {
                "Operation": "CreateContext",
                "Request": {
                    "ContextName": registry_context_name,
                    "ContextType": "ModelPackageGroup",
                    "Source": {"SourceUri": config["model_package_group_name"]},
                    "Properties": {"lesson": "ai-20-ai-22"},
                },
                "ExampleArn": registry_context_arn,
            }
        ],
        "Associations": [
            {
                "Operation": "AddAssociation",
                "Request": {
                    "SourceArn": raw_data_arn,
                    "DestinationArn": training_action_arn,
                    "AssociationType": "ContributedTo",
                },
            },
            {
                "Operation": "AddAssociation",
                "Request": {
                    "SourceArn": script_arn,
                    "DestinationArn": training_action_arn,
                    "AssociationType": "ContributedTo",
                },
            },
            {
                "Operation": "AddAssociation",
                "Request": {
                    "SourceArn": training_action_arn,
                    "DestinationArn": model_artifact_arn,
                    "AssociationType": "Produced",
                },
            },
            {
                "Operation": "AddAssociation",
                "Request": {
                    "SourceArn": model_artifact_arn,
                    "DestinationArn": registry_context_arn,
                    "AssociationType": "AssociatedWith",
                },
            },
        ],
    }


def build_debugger_profiler_plan(config: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "Note": "These fields belong on a real Training Job request. This lesson does not enable them.",
        "DebugHookConfig": {
            "S3OutputPath": config["debugger_output_s3_uri"],
            "CollectionConfigurations": [
                {"CollectionName": "losses"},
                {"CollectionName": "weights"},
            ],
        },
        "ProfilerConfig": {
            "S3OutputPath": config["profiler_output_s3_uri"],
            "ProfilingIntervalInMilliseconds": 500,
        },
        "WhatToWatch": [
            "loss curve",
            "evaluation metrics",
            "CPU/GPU utilization",
            "memory pressure",
            "data loading time",
        ],
    }


def main() -> None:
    config = load_config()

    print("AI-22 SageMaker Experiments, Lineage, and Debugging dry run")
    print("Dry run only: this script does not create AWS resources.")
    print()
    print("Concept flow:")
    print("  1. Create an experiment")
    print("  2. Create a trial for one training attempt")
    print("  3. Record a trial component with parameters, metrics, inputs, outputs")
    print("  4. Associate the trial component with the trial")
    print("  5. Connect lineage: data/code -> training action -> model artifact -> registry")
    print()
    print("Experiment request plan:")
    print(json.dumps(build_experiment_plan(config), indent=2))
    print()
    print("Lineage request plan:")
    print(json.dumps(build_lineage_plan(config), indent=2))
    print()
    print("Debugger and profiler configuration shape:")
    print(json.dumps(build_debugger_profiler_plan(config), indent=2))
    print()
    print("Cost note:")
    print("  Experiment and lineage metadata are not training compute.")
    print("  Training jobs, endpoint deployment, and extra S3/CloudWatch output can cost money.")


if __name__ == "__main__":
    main()
