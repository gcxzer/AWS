# AI-25 Cleanup Checklist

Use this checklist after any real SageMaker capstone run.

## Realtime Endpoint

- [ ] Delete endpoint: `ai-25-review-classifier-endpoint`
- [ ] Delete endpoint config: `ai-25-review-classifier-endpoint-config`
- [ ] Delete SageMaker model: `ai-25-review-classifier-model`

## Job Resources

- [ ] Confirm no processing jobs are running.
- [ ] Confirm no training jobs are running.
- [ ] Confirm no transform jobs are running.
- [ ] Confirm no HPO jobs are running.
- [ ] Confirm no pipeline executions are running.

## Studio / Domain

- [ ] Confirm no running Studio apps.
- [ ] Confirm no running JupyterLab spaces.
- [ ] Confirm no running Code Editor spaces.
- [ ] Confirm no notebook instances are running.

## S3

- [ ] Review `s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-25/raw/`.
- [ ] Review `s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-25/processed/`.
- [ ] Review `s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-25/models/`.
- [ ] Review `s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-25/evaluation/`.
- [ ] Review `s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-25/batch/`.
- [ ] Review `s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-25/monitor/`.
- [ ] Delete temporary outputs that are no longer needed.
- [ ] Keep only artifacts needed for notes or later review.

## Model Registry

- [ ] Review model package group: `ai-25-review-classifier`.
- [ ] Delete temporary model packages if created only for learning.
- [ ] Delete model package group if no longer needed.

## Pipelines / Experiments / Lineage

- [ ] Delete temporary pipeline if created.
- [ ] Delete temporary experiment / trial records if they were only for practice.
- [ ] Review lineage artifacts/actions/contexts if manually created.

## Monitoring

- [ ] Delete monitoring schedules if created.
- [ ] Confirm data capture S3 prefixes are not growing.
- [ ] Delete temporary baseline and violation report outputs if not needed.
- [ ] Delete temporary Clarify outputs if not needed.
- [ ] Review CloudWatch alarms and SNS subscriptions.

## Containers / Logs

- [ ] Delete temporary ECR images if a custom container was built.
- [ ] Review CloudWatch log groups.
- [ ] Set log retention or delete temporary logs.

## Final Cost Check

- [ ] SageMaker dashboard shows no active endpoints.
- [ ] SageMaker Studio running instances page shows no running instances.
- [ ] No active notebook instances.
- [ ] No unexpected CloudWatch alarms.
- [ ] S3 prefixes have only intentional retained files.
