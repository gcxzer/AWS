# Project 4: File Upload and Data Processing

Status:

```text
Started locally on 2026-05-01.
First AWS milestone completed on 2026-05-01.
AWS resources deleted on 2026-05-01.
```

This project builds a small event-driven file pipeline. Uploading a text or CSV file to an input S3 bucket triggers Lambda. Lambda reads the file, generates a JSON summary, writes the result to an output S3 bucket, and records progress in CloudWatch Logs. SNS and SQS are added after the first path works.

Architecture:

```text
Uploader
  -> S3 input bucket
  -> S3 ObjectCreated event
  -> Lambda function
  -> S3 output bucket
  -> CloudWatch Logs

Optional later:
  -> SNS notification
  -> SQS dead-letter queue
  -> EventBridge comparison path
```

Architecture diagram:

```text
../../../assets/project-4-file-processing-flow.svg
```

## Files

```text
projects/aws-main/project-4-file-processing/
  lambda_function.py
  events/
    s3-object-created.json
  sample-data/
    sample.csv
```

## First Learning Milestone

Build this in three small passes:

1. Direct path: `S3 input -> Lambda -> S3 output -> CloudWatch Logs`. Completed on 2026-05-01.
2. Failure tracking: add an SQS dead-letter queue to the Lambda asynchronous invocation config. Completed on 2026-05-01.
3. Notification and routing: add SNS notification, then compare direct S3 notifications with EventBridge. SNS notification completed on 2026-05-01.

## Deleted AWS Resources

Use `eu-central-1` unless there is a clear reason to change region.

```text
Input bucket:  xzhu-aws-learning-file-input-20260501
Output bucket: xzhu-aws-learning-file-output-20260501
Lambda:        learning-file-processor
IAM role:      learning-file-processor-role
Log group:     /aws/lambda/learning-file-processor
SQS DLQ:       learning-file-processing-dlq
SNS topic:     learning-file-processing-results
```

Cleanup completed on 2026-05-01:

```text
S3 event notification: deleted
Lambda function: deleted
SQS queue: deleted
SNS topic: deleted
S3 input/output buckets: emptied and deleted
IAM role: deleted
CloudWatch log group: deleted
```

Current verification:

```text
Uploaded object: s3://xzhu-aws-learning-file-input-20260501/uploads/sample.csv
Generated output: s3://xzhu-aws-learning-file-output-20260501/processed/uploads/sample.csv.summary.json
CloudWatch log group exists: /aws/lambda/learning-file-processor
```

SQS failure tracking verification:

```text
Queue: learning-file-processing-dlq
Failure condition tested: MAX_BYTES=10 with uploads/sample.csv
Lambda condition: RetriesExhausted
Approximate invoke count: 3
Captured error: uploads/sample.csv is 140 bytes, larger than MAX_BYTES=10
```

SNS notification verification:

```text
Topic: learning-file-processing-results
Lambda environment variable: SNS_TOPIC_ARN points to the topic ARN
Lambda permission: sns:Publish on the topic ARN
Result: successful processing notification received after uploading a new file
```

## Lambda Environment Variables

Required:

```text
OUTPUT_BUCKET=xzhu-aws-learning-file-output-20260501
```

Optional:

```text
OUTPUT_PREFIX=processed
MAX_BYTES=1048576
SNS_TOPIC_ARN=
```

## Local Smoke Test

This does not call AWS. It only checks the text/CSV summary logic with the local sample file.

```bash
cd projects/aws-main/project-4-file-processing
python lambda_function.py sample-data/sample.csv
```

Expected shape:

```json
{
  "source_bucket": "local-input-bucket",
  "source_key": "sample.csv",
  "line_count": 4,
  "word_count": 9,
  "csv": {
    "column_count": 4,
    "data_row_count": 3
  }
}
```

## Deployment Outline

Set the profile and region:

```bash
export AWS_PROFILE=aws-learning
export AWS_REGION=eu-central-1
```

Create buckets:

```bash
aws s3 mb s3://xzhu-aws-learning-file-input-20260501 --region eu-central-1
aws s3 mb s3://xzhu-aws-learning-file-output-20260501 --region eu-central-1
```

Create a Lambda execution role with permissions for:

```text
CloudWatch Logs:
  logs:CreateLogGroup
  logs:CreateLogStream
  logs:PutLogEvents

S3 input bucket:
  s3:GetObject on arn:aws:s3:::xzhu-aws-learning-file-input-20260501/uploads/*

S3 output bucket:
  s3:PutObject on arn:aws:s3:::xzhu-aws-learning-file-output-20260501/processed/*

SNS later:
  sns:Publish on the learning-file-processing-results topic
```

Package and deploy Lambda:

```bash
zip function.zip lambda_function.py
aws lambda create-function \
  --function-name learning-file-processor \
  --runtime python3.12 \
  --handler lambda_function.lambda_handler \
  --role ROLE_ARN_FROM_IAM \
  --zip-file fileb://function.zip \
  --environment Variables="{OUTPUT_BUCKET=xzhu-aws-learning-file-output-20260501,OUTPUT_PREFIX=processed,MAX_BYTES=1048576}"
```

Allow S3 to invoke Lambda:

```bash
aws lambda add-permission \
  --function-name learning-file-processor \
  --statement-id allow-s3-input-bucket \
  --action lambda:InvokeFunction \
  --principal s3.amazonaws.com \
  --source-arn arn:aws:s3:::xzhu-aws-learning-file-input-20260501
```

Configure the input bucket notification for `ObjectCreated` events under the `uploads/` prefix. This can be done in the S3 console first because it is easier to see the relationship while learning.

Upload a sample:

```bash
aws s3 cp sample-data/sample.csv s3://xzhu-aws-learning-file-input-20260501/uploads/sample.csv
```

Check the generated summary:

```bash
aws s3 ls s3://xzhu-aws-learning-file-output-20260501/processed/ --recursive
aws s3 cp s3://xzhu-aws-learning-file-output-20260501/processed/uploads/sample.csv.summary.json -
```

## Cleanup

Cleanup was completed on 2026-05-01. The deletion order was:

```text
1. Delete S3 bucket notification.
2. Delete Lambda function.
3. Delete SQS queue and SNS topic if created.
4. Empty and delete both S3 buckets.
5. Delete the IAM role and inline policies created for this project.
6. Delete the CloudWatch log group: /aws/lambda/learning-file-processor.
```

## Related Notes

See the Chinese learning note:

```text
../../../notes/aws-main/06-project-4-file-processing.md
```
