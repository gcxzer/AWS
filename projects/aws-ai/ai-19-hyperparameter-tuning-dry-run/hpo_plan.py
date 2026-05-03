import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


PROJECT_DIR = Path(__file__).parent
CONFIG_PATH = PROJECT_DIR / "config.json"


def load_config() -> Dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


def build_tuning_job_name() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"ai-19-hpo-{timestamp}"


def build_training_command() -> str:
    return (
        "pip install --no-cache-dir -r /opt/ml/input/data/code/requirements.txt && "
        "python /opt/ml/input/data/code/train_text_classifier.py "
        "--model-id ${SM_HP_MODEL_ID} "
        "--num-labels ${SM_HP_NUM_LABELS} "
        "--epochs ${SM_HP_EPOCHS} "
        "--batch-size ${SM_HP_BATCH_SIZE} "
        "--learning-rate ${SM_HP_LEARNING_RATE}"
    )


def build_hpo_request(config: Dict[str, Any], tuning_job_name: str) -> Dict[str, Any]:
    bucket = config["bucket"]
    source_prefix = config["source_training_prefix"].strip("/")
    output_prefix = config["prefix"].strip("/")

    return {
        "HyperParameterTuningJobName": tuning_job_name,
        "HyperParameterTuningJobConfig": {
            "Strategy": "Bayesian",
            "HyperParameterTuningJobObjective": {
                "Type": config["objective_type"],
                "MetricName": config["objective_metric_name"],
            },
            "ResourceLimits": {
                "MaxNumberOfTrainingJobs": config["max_number_of_training_jobs"],
                "MaxParallelTrainingJobs": config["max_parallel_training_jobs"],
            },
            "ParameterRanges": {
                "ContinuousParameterRanges": [
                    {
                        "Name": "learning_rate",
                        "MinValue": "0.00001",
                        "MaxValue": "0.0001",
                        "ScalingType": "Logarithmic",
                    }
                ],
                "IntegerParameterRanges": [
                    {
                        "Name": "batch_size",
                        "MinValue": "2",
                        "MaxValue": "8",
                        "ScalingType": "Linear",
                    },
                    {
                        "Name": "epochs",
                        "MinValue": "1",
                        "MaxValue": "3",
                        "ScalingType": "Linear",
                    },
                ],
            },
        },
        "TrainingJobDefinition": {
            "StaticHyperParameters": {
                "model_id": config["hf_model_id"],
                "num_labels": str(config["num_labels"]),
            },
            "AlgorithmSpecification": {
                "TrainingImage": config["training_image_uri"],
                "TrainingInputMode": "File",
                "ContainerEntrypoint": ["bash", "-lc"],
                "ContainerArguments": [build_training_command()],
                "MetricDefinitions": [
                    {
                        "Name": "eval_loss",
                        "Regex": "eval_loss=([0-9\\.]+)",
                    },
                    {
                        "Name": "eval_accuracy",
                        "Regex": "eval_accuracy=([0-9\\.]+)",
                    },
                ],
            },
            "RoleArn": config["sagemaker_role_arn"],
            "InputDataConfig": [
                {
                    "ChannelName": "train",
                    "DataSource": {
                        "S3DataSource": {
                            "S3DataType": "S3Prefix",
                            "S3Uri": f"s3://{bucket}/{source_prefix}/train/",
                            "S3DataDistributionType": "FullyReplicated",
                        }
                    },
                },
                {
                    "ChannelName": "test",
                    "DataSource": {
                        "S3DataSource": {
                            "S3DataType": "S3Prefix",
                            "S3Uri": f"s3://{bucket}/{source_prefix}/test/",
                            "S3DataDistributionType": "FullyReplicated",
                        }
                    },
                },
                {
                    "ChannelName": "code",
                    "DataSource": {
                        "S3DataSource": {
                            "S3DataType": "S3Prefix",
                            "S3Uri": f"s3://{bucket}/{source_prefix}/scripts/",
                            "S3DataDistributionType": "FullyReplicated",
                        }
                    },
                },
            ],
            "OutputDataConfig": {
                "S3OutputPath": f"s3://{bucket}/{output_prefix}/models/{tuning_job_name}",
            },
            "ResourceConfig": {
                "InstanceType": config["training_instance_type"],
                "InstanceCount": 1,
                "VolumeSizeInGB": config["training_volume_size_gb"],
            },
            "StoppingCondition": {
                "MaxRuntimeInSeconds": config["training_max_runtime_seconds"],
            },
        },
        "Tags": [
            {"Key": "Project", "Value": "aws-ai"},
            {"Key": "Lesson", "Value": "ai-19-hyperparameter-tuning-dry-run"},
        ],
    }


def main() -> None:
    config = load_config()
    tuning_job_name = build_tuning_job_name()
    request = build_hpo_request(config, tuning_job_name)

    print("AI-19 SageMaker Hyperparameter Tuning dry run")
    print("Dry run only: this script does not create AWS resources.")
    print()
    print("HPO meaning:")
    print("  One tuning job can create many training jobs.")
    print()
    print("Cost guardrails:")
    print(f"  MaxNumberOfTrainingJobs: {config['max_number_of_training_jobs']}")
    print(f"  MaxParallelTrainingJobs: {config['max_parallel_training_jobs']}")
    print(f"  InstanceType per training job: {config['training_instance_type']}")
    print()
    print("Compatibility note:")
    print("  A real HPO run must ensure the training container reads SageMaker hyperparameters.")
    print("  This dry-run shows the request shape and cost boundary.")
    print()
    print("create_hyper_parameter_tuning_job request:")
    print(json.dumps(request, indent=2))


if __name__ == "__main__":
    main()
