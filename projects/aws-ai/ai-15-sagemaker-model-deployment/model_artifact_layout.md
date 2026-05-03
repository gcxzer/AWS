# AI-15 Model Artifact Layout

SageMaker deployment starts from a model artifact in S3, usually named `model.tar.gz`.

For this Hugging Face text classifier path, the artifact should look like this after unpacking:

```text
model.tar.gz
  config.json
  model.safetensors or pytorch_model.bin
  tokenizer.json
  tokenizer_config.json
  vocab.txt
  special_tokens_map.json
  metrics.json
  code/
    inference.py
    requirements.txt
```

## What Each Part Means

| Path | Meaning |
| --- | --- |
| `config.json` | Hugging Face model architecture/config saved by `save_pretrained` |
| `model.safetensors` or `pytorch_model.bin` | Learned model weights |
| tokenizer files | Text-to-token conversion assets |
| `metrics.json` | Training/evaluation output for humans and later governance |
| `code/inference.py` | SageMaker inference entry point |
| `code/requirements.txt` | Extra Python dependencies installed by the inference container |

## Deployment Chain

```text
model.tar.gz in S3
  -> SageMaker Model
  -> Endpoint Configuration
  -> Endpoint
  -> InvokeEndpoint request
```

## Cost Boundary

`model.tar.gz`, `SageMaker Model`, and `Endpoint Configuration` are not the main cost risk.

The `Endpoint` is the cost risk because it keeps at least one instance running until deleted.
