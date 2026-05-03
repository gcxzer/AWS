# AI-15 SageMaker Model Artifact and Deployment Plan

This lesson prepares the deployment side of the SageMaker flow without creating cloud resources.

AI-14 explained how a Hugging Face training job would produce a `model.tar.gz`. AI-15 explains how that artifact becomes an online inference endpoint.

## Core Chain

```text
AI-14 model.tar.gz
  -> SageMaker Model
  -> Endpoint Configuration
  -> Endpoint
  -> InvokeEndpoint
```

## Files

| File | Purpose |
| --- | --- |
| `config.json` | Account, role, S3 artifact placeholder, inference image, endpoint sizing |
| `deployment_plan.py` | Prints the SageMaker API request sequence without creating resources |
| `model_artifact_layout.md` | Explains what should be inside `model.tar.gz` |
| `inference_code/inference.py` | SageMaker inference entry point skeleton |
| `inference_code/requirements.txt` | Extra dependencies for the inference container |

## Dry Run

```bash
uv run python projects/aws-ai/ai-15-sagemaker-model-deployment/deployment_plan.py
```

This only prints the plan. It does not call `create_model`, `create_endpoint_config`, or `create_endpoint`.

## Important Cost Rule

Do not create an endpoint unless you are ready to delete it immediately after testing.

Delete order:

```text
Endpoint
Endpoint Configuration
Model
S3 artifact if no longer needed
CloudWatch logs if no longer needed
```
