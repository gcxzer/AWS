# SageMaker Cleanup Checklist

Use this after every SageMaker learning session.

## Realtime Inference

- [ ] Delete realtime endpoints.
- [ ] Delete endpoint configurations.
- [ ] Delete SageMaker models that are no longer needed.

## Development Environments

- [ ] Stop or delete Studio apps.
- [ ] Stop or delete notebook instances.
- [ ] Delete temporary spaces if created only for learning.

## Jobs

- [ ] Confirm processing jobs are completed or stopped.
- [ ] Confirm training jobs are completed or stopped.
- [ ] Confirm transform jobs are completed or stopped.
- [ ] Confirm tuning jobs are completed or stopped.

## Artifacts

- [ ] Delete temporary S3 processing outputs.
- [ ] Delete temporary S3 training outputs.
- [ ] Delete temporary S3 batch transform outputs.
- [ ] Delete model artifacts that are not needed.

## MLOps Resources

- [ ] Delete temporary model packages.
- [ ] Delete temporary model package groups.
- [ ] Delete temporary pipelines.
- [ ] Delete temporary experiments or keep only the learning record.

## IAM And Logs

- [ ] Delete temporary IAM policies or roles.
- [ ] Delete no-longer-needed CloudWatch Log Groups or set retention.
- [ ] Confirm no unexpected SageMaker costs in Cost Explorer.
