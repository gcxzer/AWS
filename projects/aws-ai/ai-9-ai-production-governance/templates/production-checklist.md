# AI Production Checklist

Use this before exposing an AWS AI application beyond a local learning environment.

## Access And Auth

- [ ] End users do not hold AWS credentials in browsers or mobile clients.
- [ ] Backend authenticates users before AI requests.
- [ ] Backend enforces business authorization before accessing data.
- [ ] IAM roles use least privilege.
- [ ] Bedrock model access is enabled only for intended Regions and models.

## Input And Cost Controls

- [ ] Input length is bounded.
- [ ] Output token budget is bounded.
- [ ] Model ID is controlled server-side.
- [ ] Request rate limit exists per user / API key / tenant.
- [ ] Long-running jobs are asynchronous or use Step Functions.

## Safety

- [ ] Application validates schema and required fields before model calls.
- [ ] Guardrails are applied where content safety is required.
- [ ] Prompt injection risks are considered for RAG and tool calls.
- [ ] Tool calls require deterministic backend authorization.
- [ ] Sensitive output handling is defined.

## Observability

- [ ] Logs include request id, user or tenant id hash, model id, operation, latency, and error type.
- [ ] Logs do not include secrets, raw credentials, or full sensitive prompts.
- [ ] CloudWatch alarms exist for error rate and throttling.
- [ ] Cost and usage dashboards are reviewed.
- [ ] CloudTrail is enabled for audit.

## Reliability

- [ ] Timeouts are explicit.
- [ ] Retries use backoff and do not amplify cost.
- [ ] Failure paths are traceable.
- [ ] DLQ or durable failure records exist for async jobs.
- [ ] Idempotency is defined for event-driven pipelines.

## Data Protection

- [ ] Data retention is documented.
- [ ] S3 buckets block public access.
- [ ] Encryption requirements are documented.
- [ ] Secrets use Secrets Manager or SSM Parameter Store.
- [ ] PII handling is documented.

## Cleanup

- [ ] Temporary resources have owner and purpose tags.
- [ ] Cleanup runbook exists.
- [ ] CloudWatch log retention is set.
- [ ] Evaluation and test S3 outputs are reviewed and removed when no longer needed.
