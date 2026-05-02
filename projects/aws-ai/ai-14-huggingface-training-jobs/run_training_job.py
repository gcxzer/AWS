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
    return f"ai-14-hf-train-{timestamp}"


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
    output_s3_uri = f"s3://{bucket}/{prefix}/models/{job_name}"

    train_command = (
        "pip install --no-cache-dir -r /opt/ml/input/data/code/requirements.txt && "
        "python /opt/ml/input/data/code/train_text_classifier.py "
        f"--model-id {config['hf_model_id']} "
        f"--num-labels {config['num_labels']} "
        f"--epochs {config['epochs']} "
        f"--batch-size {config['batch_size']} "
        f"--learning-rate {config['learning_rate']}"
    )

    sagemaker.create_training_job(
        TrainingJobName=job_name,
        RoleArn=config["sagemaker_role_arn"],
        AlgorithmSpecification={
            "TrainingImage": config["training_image_uri"],
            "TrainingInputMode": "File",
            "ContainerEntrypoint": ["bash", "-lc"],
            "ContainerArguments": [train_command],
        },
        InputDataConfig=[
            {
                "ChannelName": "train",
                "DataSource": {
                    "S3DataSource": {
                        "S3DataType": "S3Prefix",
                        "S3Uri": f"s3://{bucket}/{prefix}/train/",
                        "S3DataDistributionType": "FullyReplicated",
                    }
                },
            },
            {
                "ChannelName": "test",
                "DataSource": {
                    "S3DataSource": {
                        "S3DataType": "S3Prefix",
                        "S3Uri": f"s3://{bucket}/{prefix}/test/",
                        "S3DataDistributionType": "FullyReplicated",
                    }
                },
            },
            {
                "ChannelName": "code",
                "DataSource": {
                    "S3DataSource": {
                        "S3DataType": "S3Prefix",
                        "S3Uri": f"s3://{bucket}/{prefix}/scripts/",
                        "S3DataDistributionType": "FullyReplicated",
                    }
                },
            },
        ],
        OutputDataConfig={
            "S3OutputPath": output_s3_uri,
        },
        ResourceConfig={
            "InstanceType": config["training_instance_type"],
            "InstanceCount": 1,
            "VolumeSizeInGB": config["training_volume_size_gb"],
        },
        StoppingCondition={
            "MaxRuntimeInSeconds": config["training_max_runtime_seconds"],
        },
        Tags=[
            {"Key": "Project", "Value": "aws-ai"},
            {"Key": "Lesson", "Value": "ai-14-huggingface-training-jobs"},
        ],
    )

    print("Created SageMaker Training job:")
    print(f"  Job name: {job_name}")
    print(f"  Instance: {config['training_instance_type']}")
    print(f"  Image: {config['training_image_uri']}")
    print(f"  HF model: {config['hf_model_id']}")
    print(f"  Output: {output_s3_uri}")


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
        print("SageMaker Training job creation failed.")
        print(f"Original error: {error}")
        raise SystemExit(1)
