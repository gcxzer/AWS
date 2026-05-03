# AI-19 Hyperparameter Tuning Dry Run

This lesson prepares a local-only SageMaker HPO request plan.

No AWS resources are created.

## What HPO Does

```text
Hyperparameter tuning job
  -> training job 1 with one parameter set
  -> training job 2 with another parameter set
  -> ...
  -> best training job
```

## Dry Run

```bash
uv run python projects/aws-ai/ai-19-hyperparameter-tuning-dry-run/hpo_plan.py
```

This prints a `CreateHyperParameterTuningJob` request shape without calling AWS.

## Cost Rule

HPO multiplies cost because it launches multiple training jobs.

Keep these small:

```text
MaxNumberOfTrainingJobs
MaxParallelTrainingJobs
InstanceType
MaxRuntimeInSeconds
```
