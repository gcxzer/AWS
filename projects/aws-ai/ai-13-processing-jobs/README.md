# AI-13 Processing Jobs

This project starts with local preprocessing, then moves the same script into a SageMaker Processing job.

The track still uses local VS Code as the development entry point.

## Goal

Prepare Hugging Face style JSONL data:

```text
raw/sample_reviews.jsonl
  -> scripts/preprocess_reviews.py
  -> data/processed/train.jsonl
  -> data/processed/test.jsonl
```

## Local Run

```bash
uv run python projects/aws-ai/ai-13-processing-jobs/scripts/preprocess_reviews.py \
  --input projects/aws-ai/ai-13-processing-jobs/data/raw/sample_reviews.jsonl \
  --output-dir projects/aws-ai/ai-13-processing-jobs/data/processed
```

`data/processed/` is a generated output directory. Keep the directory, but do not treat `train.jsonl` and `test.jsonl` as source files.

## Upload Inputs To S3

```bash
uv run python projects/aws-ai/ai-13-processing-jobs/upload_inputs.py
```

Expected S3 objects:

```text
s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-13/raw/sample_reviews.jsonl
s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-13/scripts/preprocess_reviews.py
```

## Run SageMaker Processing

Create the Processing job:

```bash
uv run python projects/aws-ai/ai-13-processing-jobs/run_processing_job.py
```

This uses a SageMaker PyTorch CPU container only as a managed Python runtime. It is not training a model yet.

The job maps S3 into the container like this:

```text
s3://.../sagemaker/ai-13/raw/
  -> /opt/ml/processing/input

s3://.../sagemaker/ai-13/scripts/
  -> /opt/ml/processing/code

/opt/ml/processing/output
  -> s3://.../sagemaker/ai-13/processed/<job-name>/
```

Check status:

```bash
aws sagemaker describe-processing-job \
  --processing-job-name <job-name> \
  --region eu-central-1 \
  --profile aws-learning \
  --query 'ProcessingJobStatus'
```

`ml.m5.large` is not available in the current `eu-central-1` processing quota for this account. Use `ml.t3.medium`, which has available quota and is enough for this tiny preprocessing job.

## Completed Run

```text
Job name: ai-13-preprocess-20260502-191348
Status: Completed
Instance: ml.t3.medium
Output: s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-13/processed/ai-13-preprocess-20260502-191348/
```

## Output Schema

```json
{
  "id": "r001",
  "text": "The model answered quickly and the response was clear.",
  "label": 2,
  "label_name": "positive"
}
```

## Next Step

After the local script is verified, upload:

```text
data/raw/
scripts/preprocess_reviews.py
```

to S3 and run the script with SageMaker Processing.
