# AI-20 Model Registry Dry Run

This lesson prepares a local-only SageMaker Model Registry request plan.

No AWS resources are created.

## What Model Registry Does

```text
model.tar.gz
  -> Model Package
  -> Model Package Group
  -> Approval Status
  -> Deploy selected version
```

## Dry Run

```bash
uv run python projects/aws-ai/ai-20-model-registry-dry-run/model_registry_plan.py
```

This prints request shapes for:

```text
CreateModelPackageGroup
CreateModelPackage
UpdateModelPackage
```

## Main Idea

Model Registry is model version control plus approval metadata. It does not train or serve models.
