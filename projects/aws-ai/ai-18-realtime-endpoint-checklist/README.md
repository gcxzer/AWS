# AI-18 Real-time Endpoint Checklist

This lesson is a local-only checklist and dry-run plan for SageMaker real-time endpoints.

No AWS resources are created.

## Core Chain

```text
model.tar.gz
  -> SageMaker Model
  -> Endpoint Configuration
  -> Endpoint
  -> InvokeEndpoint
  -> DeleteEndpoint first
```

## Dry Run

```bash
uv run python projects/aws-ai/ai-18-realtime-endpoint-checklist/endpoint_dry_run.py
```

This prints the API request shape for:

```text
CreateModel
CreateEndpointConfig
CreateEndpoint
InvokeEndpoint
DeleteEndpoint
DeleteEndpointConfig
DeleteModel
```

## Cost Rule

The endpoint is the running resource.

Delete order:

```text
1. Delete endpoint
2. Delete endpoint configuration
3. Delete model
4. Clean temporary S3 artifacts and CloudWatch logs if no longer needed
```
