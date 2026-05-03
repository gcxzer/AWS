# AI-16 Batch Transform Offline Inference

This lesson prepares a SageMaker Batch Transform flow without creating cloud resources.

Batch Transform is useful when inference can be done from files in S3 instead of a long-running real-time endpoint.

## Core Chain

```text
S3 batch input
  -> SageMaker Model
  -> Batch Transform Job
  -> S3 prediction output
  -> job finishes and instance stops
```

## Files

| File | Purpose |
| --- | --- |
| `config.json` | Account, role, model artifact placeholder, inference image, transform sizing |
| `batch_transform_plan.py` | Prints the SageMaker API request sequence without creating resources |
| `data/input/batch_input.jsonl` | Local sample batch inference input |

## Dry Run

```bash
uv run python projects/aws-ai/ai-16-batch-transform-offline-inference/batch_transform_plan.py
```

This only prints the plan. It does not call `create_model` or `create_transform_job`.

## Input Format

```json
{"text":"The support team answered quickly and solved my issue."}
```

Batch Transform can split the input file by line and send one JSON object per inference request.

## Cost Rule

Batch Transform creates temporary compute for the job and stops when the job completes.

It is safer for learning than a real-time endpoint, but it still charges while the transform job is running.
