# AI-10 AWS Specialized AI APIs

This project contains small learning scripts for AWS specialized AI APIs.

The goal is service selection:

```text
Use specialized AI APIs for stable recognition or conversion tasks.
Use Bedrock for open-ended generation, Q&A, reasoning, RAG, agents, and flows.
```

## Local Files

| File | Purpose |
| --- | --- |
| `events/sample-texts.json` | Sample inputs for Comprehend and Translate |
| `comprehend_pii_entities.py` | Detect PII entities in text |
| `translate_text.py` | Translate text |
| `textract_detect_text.py` | Extract text from a local image |
| `outputs/` | Suggested output directory |

## Region

Use the same learning region where possible:

```text
eu-central-1
```

Check service availability in the console before running each demo.

## Demo Order

1. Comprehend PII detection.
2. Translate text.
3. Textract OCR from a small PNG/JPEG image.

## Cost Notes

- Comprehend and Translate are charged by text volume.
- Textract is charged by page or document processing type.
- Transcribe is charged by audio duration.
- Polly is charged by characters synthesized.
- Rekognition is charged by image/video requests and feature type.

Keep inputs small for learning.

## Cleanup

These first scripts do not create persistent AWS resources.

If later demos use S3 or async jobs, delete temporary S3 inputs/outputs and IAM policies after testing.
