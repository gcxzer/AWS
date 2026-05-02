# AI-11 SageMaker Overview And Selection

This project is the entry point for the SageMaker AI learning track.

AI-11 does not create SageMaker resources yet. It focuses on concepts, selection boundaries, cost risks, and cleanup order.

The learning track uses local VS Code as the main development environment. SageMaker Studio and JupyterLab are optional console tools and cost-risk resources, not the default place to write code.

The SageMaker model track is modern Hugging Face first:

```text
Local VS Code
  -> SageMaker SDK / boto3
  -> Hugging Face or PyTorch container
  -> Batch Transform or short-lived Endpoint
```

## Core Question

When should you use each AWS AI path?

| Need | Service |
| --- | --- |
| Managed foundation model generation, RAG, agents, flows | Bedrock |
| OCR, translation, speech, PII detection, image recognition | Specialized AI APIs |
| Train, tune, deploy, monitor, and govern your own Hugging Face models | SageMaker AI |

## Files

| File | Purpose |
| --- | --- |
| `templates/sagemaker-cleanup-checklist.md` | Cleanup order for SageMaker resources |
| `templates/sagemaker-selection-table.md` | Service selection table |

## Cost Warning

The most dangerous beginner mistake in SageMaker is leaving realtime endpoints or Studio apps running.

Prioritize job-style resources first:

```text
Processing Job
Training Job
Batch Transform
```

Treat realtime endpoints carefully:

```text
Endpoint -> delete immediately after learning test
```
