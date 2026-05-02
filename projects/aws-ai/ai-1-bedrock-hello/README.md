# AI-1: Bedrock 调用与权限

目标：跑通本地 Python 调用 Amazon Bedrock 的最小闭环，并理解 AWS 侧的身份、权限、Region、model access、SDK、错误和成本。

## 当前学习重点

这节课不讲 prompt 工程，也不讲 LLM 原理。你已经有 AI 基础，所以这里重点看 AWS 平台层：

- `aws-learning` SSO profile 是否能拿到临时凭证。
- Bedrock 控制面和运行时 API 的区别。
- 当前 Region 支持哪些 foundation models。
- IAM 权限和 Bedrock model access 的区别。
- boto3 如何调用 `bedrock-runtime`。
- CloudWatch / CLI 错误如何帮助排查问题。
- 一次模型调用的大致成本由什么决定。

## 当前状态

```text
开始日期：2026-05-02
Region: eu-central-1
已验证模型：openai.gpt-oss-20b-1:0
状态：本地 Python -> boto3 -> bedrock-runtime -> Converse API 已跑通
```

首次成功调用记录：

```text
latency_ms: 1621
input_tokens: 123
output_tokens: 199
stop_reason: end_turn
```

已完成的 smoke tests：

- 文本总结：成功。
- 服务分类：成功，invoice PDF 抽取场景分类到 `Amazon Textract`。
- JSON 结构化抽取：成功；第一次因 `max_tokens` 过小被截断，调高后完成。
- 错误处理：无效 model id 返回 `ValidationException`。

## 推荐流程

1. 重新登录 AWS SSO：

```bash
aws sso login --profile aws-learning
```

2. 验证身份：

```bash
aws sts get-caller-identity --profile aws-learning
```

3. 查看当前 Region 可见模型：

```bash
aws bedrock list-foundation-models \
  --profile aws-learning \
  --region eu-central-1 \
  --query "modelSummaries[?contains(outputModalities, 'TEXT')].[providerName,modelName,modelId,inferenceTypesSupported]" \
  --output table
```

4. 运行本地 Bedrock 调用：

```bash
uv run python projects/aws-ai/ai-1-bedrock-hello/bedrock_hello.py \
  --profile aws-learning \
  --region eu-central-1 \
  --model-id <model-id>
```

如果 Frankfurt 当前没有你想用的模型，可以把 `--region` 换成 Bedrock 控制台里支持该模型的 Region，例如 `us-east-1`。

## 常见错误

| 错误 | 常见原因 | 处理方式 |
| --- | --- | --- |
| `Token has expired` | SSO 临时凭证过期 | 重新运行 `aws sso login --profile aws-learning` |
| `AccessDeniedException` | IAM 权限不足，或没有模型访问权限 | 检查 IAM policy 和 Bedrock model access |
| `ValidationException` | model id、请求格式或参数不符合模型要求 | 先用 `list-foundation-models` 确认 model id |
| `ThrottlingException` | 请求太快或 quota 太低 | 降低频率，查看 Bedrock quota |
| `ModelNotReadyException` | 模型暂时不可用 | 等待后重试或换模型 |

## 验收标准

- [x] `aws sts get-caller-identity --profile aws-learning` 成功。
- [x] 能列出 Bedrock text models。
- [x] `bedrock_hello.py` 能返回一段模型输出。
- [x] 能解释 `bedrock` 和 `bedrock-runtime` 的区别。
- [x] 能解释 model access 和 IAM permission 的区别。
- [x] 能说清本次调用使用的 Region、model id、输入/输出规模。

## 清理

本项目默认只保留本地脚本，不创建长期 AWS 资源。若后续为了最小权限创建了临时 IAM policy 或 role，实验结束后删除。
