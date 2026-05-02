# AI-5: Bedrock Agent 与 Lambda 工具调用

目标：构建一个能调用 Lambda tool 的 Bedrock Agent。

推荐架构：

```text
User
  -> Bedrock Agent alias
  -> Agent orchestration model
  -> Action group schema
  -> Lambda tool
  -> static lesson data
  -> Agent final answer
```

## 文件

| 文件 | 作用 |
| --- | --- |
| `lambda_function.py` | Bedrock Agent action group 的 Lambda tool handler |
| `action-schema.json` | OpenAPI 3.0 action schema，告诉 Agent 什么时候调用 `get_lesson_summary` |
| `events/get-lesson-summary-ai-2.json` | 本地 Lambda event 样例 |
| `invoke_agent.py` | 用 boto3 调 `InvokeAgent` 的本地脚本 |

## 本地测试 Lambda tool

```bash
uv run python projects/aws-ai/ai-5-bedrock-agent-lambda-tool/lambda_function.py \
  projects/aws-ai/ai-5-bedrock-agent-lambda-tool/events/get-lesson-summary-ai-2.json
```

预期看到 Bedrock Agent Lambda response envelope：

```text
messageVersion: 1.0
response.actionGroup: LessonSummaryActionGroup
response.apiPath: /lesson-summary
response.httpStatusCode: 200
response.responseBody.application/json.body: JSON string
```

## Bedrock Console 配置

推荐资源名：

| 资源 | 建议名称 |
| --- | --- |
| Lambda function | `ai-5-lesson-summary-tool` |
| Bedrock Agent | `ai-5-lesson-helper-agent` |
| Action group | `LessonSummaryActionGroup` |
| Agent alias | `ai5-dev` |

Agent instruction 建议：

```text
You are an AWS AI learning helper. When the user asks what they learned in a specific AI lesson, asks for a recap, or asks which services and outputs belonged to a lesson, call the get_lesson_summary tool. Do not invent lesson facts that are not returned by the tool. If the lesson ID is ambiguous, ask a short clarification question.
```

Action group 选择：

```text
Define with API schema
Executor: Lambda function
Schema: paste action-schema.json into the console editor, or upload it to S3
```

## Lambda resource policy

Bedrock Agent 调 Lambda 需要 Lambda resource-based policy。拿到 Agent ID 后添加：

```bash
ACCOUNT_ID=$(aws sts get-caller-identity \
  --profile aws-learning \
  --query Account \
  --output text)

aws lambda add-permission \
  --profile aws-learning \
  --region eu-central-1 \
  --function-name ai-5-lesson-summary-tool \
  --statement-id AllowBedrockAgentInvokeAI5 \
  --action lambda:InvokeFunction \
  --principal bedrock.amazonaws.com \
  --source-account "$ACCOUNT_ID" \
  --source-arn "arn:aws:bedrock:eu-central-1:${ACCOUNT_ID}:agent/AGENT_ID"
```

把 `AGENT_ID` 替换成真实 Bedrock Agent ID。

## InvokeAgent 本地调用

创建 alias 后运行：

```bash
uv run python projects/aws-ai/ai-5-bedrock-agent-lambda-tool/invoke_agent.py \
  --agent-id AGENT_ID \
  --agent-alias-id AGENT_ALIAS_ID \
  --prompt "Give me a brief summary of what I learned in AI-2."
```

当前 profile 需要有 `bedrock:InvokeAgent` 权限，并且 `--region`、Agent ID、alias ID 要和 Console 里的资源一致。

学习阶段建议保留 trace：

```text
enableTrace=True
```

这样可以观察 Agent 什么时候选择 action group、传了什么参数，以及 Lambda 返回后如何生成最终回答。

把 `AGENT_ID` 和 `AGENT_ALIAS_ID` 替换成 Console 里的真实值。

如果在 Bedrock Console 的 Test 面板测试，Console 可能使用内置测试 alias：

```text
TSTALIASID
```

这表示你正在测试 draft agent，不一定是你自己创建的 `ai5-dev` alias。

## 清理

1. 删除 Agent alias。
2. 删除 Action group 或 Agent。
3. 删除 Lambda function `ai-5-lesson-summary-tool`。
4. 删除 Lambda execution role。
5. 删除 CloudWatch Log Group。

本地代码和笔记保留。
