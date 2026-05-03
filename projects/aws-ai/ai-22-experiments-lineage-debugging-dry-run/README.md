# AI-22 SageMaker Experiments, Lineage, and Debugging Dry Run

This lesson prepares a local-only request plan for SageMaker experiment tracking and lineage.

No AWS resources are created.

## Main Shape

```text
Experiment
  -> Trial
    -> Trial Component
      -> parameters, metrics, input artifacts, output artifacts
```

Lineage shape:

```text
raw data + training code + hyperparameters
  -> training action
  -> model.tar.gz
  -> model registry / deployment
```

## Dry Run

```bash
uv run python projects/aws-ai/ai-22-experiments-lineage-debugging-dry-run/experiment_plan.py
```

This prints readable request shapes for:

- `CreateExperiment`
- `CreateTrial`
- `CreateTrialComponent`
- `AssociateTrialComponent`
- lineage artifacts, actions, contexts, and associations
- Debugger / Profiler configuration

## Main Idea

Experiments compare runs. Lineage explains where a model came from. Debugger and Profiler explain what happened during training.
