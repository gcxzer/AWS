# AI Resource Cleanup Runbook

Use this after each learning experiment.

## General Order

1. Stop or delete public entry points first.
2. Delete aliases / deployments / versions.
3. Delete compute or AI resources.
4. Delete storage after exporting anything worth keeping.
5. Delete service roles and custom policies that are no longer used.
6. Delete CloudWatch log groups or set retention.
7. Verify with Console search or read-only CLI.

## Common Resources

| Resource | Cleanup |
| --- | --- |
| API Gateway | Delete API / routes / stages |
| Lambda | Delete function, log group, execution role |
| S3 | Empty bucket, delete bucket |
| SQS / SNS | Delete queue / topic |
| Knowledge Base | Delete KB, data source, vector store, S3 docs |
| Agent | Delete aliases, agent, Lambda tools if temporary, roles |
| Guardrail | Delete versions, delete guardrail |
| Flow | Delete aliases, versions, flow, service role |
| Evaluation | Stop job if running, delete S3 outputs if not needed, delete role |

## Verification

Record:

```text
Resource:
Region:
Deleted at:
Verification:
Residual risk:
```
