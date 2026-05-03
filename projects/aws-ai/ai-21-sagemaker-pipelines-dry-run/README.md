# AI-21 SageMaker Pipelines Dry Run

This lesson prepares a local-only SageMaker Pipeline definition plan.

No AWS resources are created.

## Pipeline Shape

```text
Processing
  -> Training
  -> Evaluation
  -> Condition
  -> Register Model
```

## Dry Run

```bash
uv run python projects/aws-ai/ai-21-sagemaker-pipelines-dry-run/pipeline_plan.py
```

This prints a `CreatePipeline` request shape and a readable pipeline definition.

## Main Idea

SageMaker Pipelines make ML workflows repeatable. A pipeline definition is metadata; a pipeline execution can launch processing jobs, training jobs, and model registry actions.
