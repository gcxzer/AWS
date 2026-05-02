# AI-12 VS Code SageMaker Setup

This project keeps the local VS Code based SageMaker setup.

Studio and JupyterLab are not the main development tools for this track. Local scripts use `aws-learning`, boto3, and later the SageMaker SDK to create SageMaker resources.

## Files

| File | Purpose |
| --- | --- |
| `config.json` | Shared local config for profile, region, role, bucket, and prefix |
| `check_environment.py` | Read-only environment check |
| `init_s3_layout.py` | Create `.keep` marker files for the AI-12 S3 layout |

## Commands

Check local AWS and SageMaker access:

```bash
uv run python projects/aws-ai/ai-12-vscode-sagemaker-setup/check_environment.py
```

Initialize S3 layout:

```bash
uv run python projects/aws-ai/ai-12-vscode-sagemaker-setup/init_s3_layout.py
```

List the S3 layout:

```bash
aws s3 ls s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-12/ \
  --recursive \
  --profile aws-learning
```

## Cost Notes

The scripts here do not create SageMaker jobs, endpoints, notebooks, or Studio spaces.

The created `.keep` files are only S3 objects. The resources to watch later are:

```text
Endpoint
Studio app / space
Notebook instance
GPU instance
Training / Processing / Transform job runtime
```
