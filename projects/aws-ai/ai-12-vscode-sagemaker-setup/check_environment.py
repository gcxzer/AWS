import json
from pathlib import Path
from typing import Any, Dict

import boto3
from botocore.exceptions import BotoCoreError, ClientError, TokenRetrievalError


CONFIG_PATH = Path(__file__).with_name("config.json")


def load_config() -> Dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


def main() -> None:
    config = load_config()
    session = boto3.Session(
        profile_name=config["profile"],
        region_name=config["region"],
    )

    sts = session.client("sts")
    iam = session.client("iam")
    s3 = session.client("s3")
    sagemaker = session.client("sagemaker")

    identity = sts.get_caller_identity()
    role_name = config["sagemaker_role_arn"].split("/")[-1]
    role = iam.get_role(RoleName=role_name)["Role"]

    s3.head_bucket(Bucket=config["bucket"])
    domains = sagemaker.list_domains()["Domains"]

    matching_domains = [
        domain
        for domain in domains
        if domain["Status"] in {"InService", "Ready"}
    ]

    print("Local AWS identity:")
    print(f"  Account: {identity['Account']}")
    print(f"  Arn: {identity['Arn']}")
    print()
    print("SageMaker execution role:")
    print(f"  RoleName: {role['RoleName']}")
    print(f"  Arn: {role['Arn']}")
    print()
    print("S3 artifact location:")
    print(f"  s3://{config['bucket']}/{config['prefix']}/")
    print()
    print("SageMaker domains:")
    for domain in matching_domains:
        print(f"  {domain['DomainId']}  {domain['DomainName']}  {domain['Status']}")

    if not matching_domains:
        raise RuntimeError("No active SageMaker domain found in the configured region.")


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
    except (BotoCoreError, ClientError) as error:
        print("AWS environment check failed.")
        print(f"Original error: {error}")
        raise SystemExit(1)
