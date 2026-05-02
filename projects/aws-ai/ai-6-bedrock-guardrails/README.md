# AI-6: Bedrock Guardrails / 安全与边界

目标：学习 Bedrock Guardrails 如何在输入和输出阶段提供安全控制，并理解它和 IAM、应用层校验的边界。

推荐链路：

```text
User input
  -> Guardrail checks input
  -> Bedrock model / Agent / Knowledge Base
  -> Guardrail checks output
  -> Application response
```

本目录先放本地学习材料，不创建云上资源：

| 文件 | 作用 |
| --- | --- |
| `apply_guardrail.py` | 用 `bedrock-runtime.apply_guardrail` 测试已创建的 Guardrail |
| `guarded_converse.py` | 先检查 input，再调用模型，最后检查 output |
| `events/sample-inputs.json` | safe / unsafe / PII 风格测试输入 |

## 本地脚本

创建 Guardrail 后运行：

```bash
uv run python projects/aws-ai/ai-6-bedrock-guardrails/apply_guardrail.py \
  --guardrail-id GUARDRAIL_ID \
  --guardrail-version DRAFT \
  --text "My email is test@example.com. Please summarize this."
```

默认配置：

```text
profile: aws-learning
region: eu-central-1
source: INPUT
```

## Guarded model call

用 Guardrail 包住一次真实模型调用：

```bash
uv run python projects/aws-ai/ai-6-bedrock-guardrails/guarded_converse.py \
  --guardrail-id ewiyys4k9ven \
  --guardrail-version 1 \
  --prompt "Explain IAM permissions vs Bedrock Guardrails in two sentences."
```

链路：

```text
prompt
  -> ApplyGuardrail(source=INPUT)
  -> Bedrock Converse
  -> ApplyGuardrail(source=OUTPUT)
  -> final output
```

## Console 实验资源建议

| 资源 | 建议名称 |
| --- | --- |
| Guardrail | `ai-6-learning-guardrail` |
| Guardrail version | 先用 `DRAFT` 测试，稳定后再 create version |

当前实操资源：

```text
Guardrail name: ai-6-learning-guardrail
Guardrail ID: ewiyys4k9ven
Guardrail ARN: arn:aws:bedrock:eu-central-1:089781651608:guardrail/ewiyys4k9ven
Guardrail version: 1
Region: eu-central-1
```

学习阶段先配置最少内容：

```text
1. Sensitive information filter: email / phone / AWS key style text
2. Denied topic: credential exfiltration or internal secrets
3. Content filters: prompt attack / misconduct 低强度起步
```

## 清理

1. 删除 Guardrail version。
2. 删除 Guardrail `ai-6-learning-guardrail`。
3. 删除测试输出文件，如果有。

本地代码和笔记保留。
