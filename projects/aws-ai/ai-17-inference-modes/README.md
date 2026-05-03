# AI-17 Inference Modes

This lesson is a local-only study note for SageMaker inference mode selection.

No AWS resources are created.

## Modes

| Mode | Best for |
| --- | --- |
| Real-time Endpoint | Low-latency synchronous APIs |
| Serverless Inference | Low or spiky traffic with acceptable cold starts |
| Asynchronous Inference | Slow or large requests where results can be stored in S3 |
| Batch Transform | Offline batch inference from S3 files |
| Multi-model Endpoint | Many small, low-traffic models sharing instances |

## Main Note

```text
notes/aws-ai/17-inference-modes.md
```

## Cost Rule

Real-time endpoints are the biggest learning-stage cost risk because they keep instances running until deleted.

Batch Transform and job-style workloads are safer for learning because compute stops when the job finishes.
