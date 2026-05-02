# AI-14 Hugging Face Training Jobs

This project prepares a SageMaker Training Job that uses the AI-13 processed JSONL data and trains a tiny Hugging Face transformer text classifier.

The training job is not started during preparation.

## Model

```text
HF_MODEL_ID = prajjwal1/bert-tiny
```

This is intentionally small so the SageMaker mechanics are cheap to learn. The same flow applies to larger Hugging Face models after quota and cost planning.

## S3 Layout

```text
s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-14/train/train.jsonl
s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-14/test/test.jsonl
s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-14/scripts/train_text_classifier.py
s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-14/scripts/requirements.txt
s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-14/models/<training-job-name>/model.tar.gz
```

## Prepare Inputs

```bash
uv run python projects/aws-ai/ai-14-huggingface-training-jobs/upload_training_inputs.py
```

This copies AI-13 output into AI-14 input folders and uploads the training script.

Preparation status:

```text
train/train.jsonl uploaded
test/test.jsonl uploaded
scripts/train_text_classifier.py uploaded
scripts/requirements.txt uploaded
```

## Run Training

Do not run this until training instance quota is available.

```bash
uv run python projects/aws-ai/ai-14-huggingface-training-jobs/run_training_job.py
```

## Quota Note

Current `eu-central-1` training job quotas checked during preparation showed common training instance quotas as `0`, including:

```text
ml.m5.large for training job usage: 0
ml.t3.large for training job usage: 0
ml.g5.xlarge for training job usage: 0
```

Before running AI-14, request quota for a small CPU training instance such as `ml.m5.large`, or choose another region with available training quota.
