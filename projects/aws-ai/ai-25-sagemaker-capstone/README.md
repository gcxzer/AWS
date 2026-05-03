# AI-25 SageMaker Capstone

This project is a local-only capstone plan for the SageMaker learning track.

No AWS resources are created by default.

## Theme

```text
Hugging Face text classification productionization flow
```

## Target Flow

```text
S3 raw data
  -> Processing
  -> Training / packaging
  -> Evaluation
  -> Model Registry
  -> Batch Transform
  -> optional short-lived Endpoint
  -> Monitor / Clarify checklist
  -> Cleanup report
```

## Dry Run

```bash
uv run python projects/aws-ai/ai-25-sagemaker-capstone/capstone_plan.py
```

The script prints the planned stages, resource boundaries, cost points, and cleanup order.

It does not import boto3 and does not call AWS.

## Low-Cost Rule

Use Batch Transform as the default inference validation path.

Only use a realtime endpoint for a short manual verification, then delete:

```text
DeleteEndpoint
DeleteEndpointConfig
DeleteModel
```
