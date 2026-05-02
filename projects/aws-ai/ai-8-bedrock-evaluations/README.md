# AI-8: Bedrock Evaluations / RAG 评估

目标：从“问几题感觉还行”升级到“有评估集、有期望答案、有指标和报告”。

本目录先放本地评估材料，不创建 AWS Evaluation job：

| 文件 | 作用 |
| --- | --- |
| `datasets/aws-ai-rag-eval.jsonl` | 小型 RAG 评估集，每行一个 JSON object |
| `validate_eval_dataset.py` | 校验 JSONL 格式和必填字段 |
| `manual-scorecard.md` | 不创建 AWS Evaluation job 时使用的人工评分表 |

## 本地校验

```bash
uv run python projects/aws-ai/ai-8-bedrock-evaluations/validate_eval_dataset.py \
  projects/aws-ai/ai-8-bedrock-evaluations/datasets/aws-ai-rag-eval.jsonl
```

## 评估集字段

| 字段 | 说明 |
| --- | --- |
| `id` | 本地样本 ID |
| `question` | 用户问题 |
| `expected_answer` | 期望答案要点 |
| `expected_source` | 期望命中的资料 |
| `evaluation_type` | `retrieve_only` 或 `retrieve_and_generate` |
| `notes` | 本地备注 |

这个文件是学习模板，不是直接提交给 AWS Evaluation job 的最终格式。真正创建 Bedrock Evaluation job 前，需要按 Console 当前要求转换成对应 JSONL schema 并上传到 S3。

## 下一步

1. 先人工阅读评估集，确认问题是否覆盖 AI-1 到 AI-5 的关键概念。
2. 用 `manual-scorecard.md` 对模型或 RAG 回答做人工评分。
3. 后续如果重新创建 Knowledge Base，再用这些问题做 retrieve-only / retrieve-and-generate 评估。
4. 如果不创建 KB，也可以把它作为人工回归测试集。
