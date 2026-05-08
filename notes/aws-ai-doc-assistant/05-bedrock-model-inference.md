# 阶段 5：Bedrock 模型调用

## 目标

理解 Amazon Bedrock 是什么、如何在 Console 里测试模型、如何通过 API 调用模型，以及它如何接收阶段 4 的 OpenSearch 检索结果并生成回答。

本阶段要学会回答：

- Bedrock 是什么？
- Foundation model 是什么？
- Model access / Marketplace subscription 是什么？
- Console playground 和 API 调用有什么区别？
- Converse API、InvokeModel、ConverseStream 分别适合什么？
- prompt、system prompt、messages、inference config 是什么？
- tokens、latency、cost 怎么理解？
- Bedrock 如何接在 OpenSearch retrieval 后面形成 RAG？

## 一句话理解 Bedrock

Amazon Bedrock 是 AWS 上的托管生成式 AI 平台。

它让你通过 AWS 的权限、网络、计费和 API 调用不同提供商的大模型，例如：

- Amazon Nova
- Anthropic Claude
- Meta Llama
- Mistral
- Cohere
- Stability AI
- 其他 Bedrock 支持的 foundation models

你不需要自己部署 GPU，不需要自己托管模型服务器。你调用 API，AWS 帮你运行模型并按用量计费。

## Bedrock 在本项目里的位置

前面几个阶段分工：

```text
S3
保存原始文档

DynamoDB
保存文档 metadata 和聊天记录

OpenSearch
从文档 chunks 里找相关上下文

Bedrock
根据用户问题 + 检索上下文生成回答
```

RAG 中的 Bedrock 不应该直接凭空回答，而应该接收 OpenSearch 找到的上下文：

```text
用户问题:
"OpenSearch 在这个系统里干什么？"

OpenSearch retrieval:
"Amazon OpenSearch Service is used for retrieval..."

Bedrock prompt:
请根据下面上下文回答用户问题。
上下文: ...
问题: ...

Bedrock answer:
OpenSearch 在这个系统里负责检索相关文档片段...
```

## 核心概念

### Foundation Model

foundation model 是基础模型。

例如：

```text
Claude
Llama
Nova
Mistral
Titan Embeddings
```

不同模型适合不同任务：

- 文本生成
- 对话
- 总结
- 代码
- embedding
- 图片
- 多模态

### Model ID

API 调用时需要指定模型 ID 或 inference profile。

例子可能类似：

```text
anthropic.claude-3-5-sonnet-...
amazon.nova-pro-...
meta.llama...
```

具体可用 ID 会随 Region 和时间变化，应以 Bedrock Console / 官方模型列表为准。

### Model Access

Bedrock 模型需要访问权限。

现在 AWS 对许多模型支持自动访问或自动订阅流程，但实际能否调用取决于：

- 当前 Region 是否支持该模型
- 账号是否有 Marketplace / Bedrock 相关权限
- IAM policy 是否允许 `bedrock:InvokeModel`
- 该模型是否支持你选的 API

Console 路径：

```text
Amazon Bedrock
-> Model catalog
-> 选择模型
-> 在 Playground 测试
```

如果需要启用模型访问，Console 会提示相应步骤。

### Prompt

prompt 是给模型的输入。

最简单：

```text
Explain Amazon S3 in one paragraph.
```

RAG prompt 通常包含：

```text
system instruction
retrieved context
user question
answer constraints
```

例如：

```text
你是一个 AWS 文档助手。
只根据给定上下文回答。
如果上下文没有答案，就说不知道。

上下文:
...

问题:
OpenSearch 在这个系统里干什么？
```

### System Prompt

system prompt 是更高优先级的行为指令。

例如：

```text
你是一个准确、简洁的 AWS 学习助手。
如果上下文不足，不要编造答案。
回答时指出使用了哪些文档片段。
```

### Messages

对话模型通常使用 messages：

```json
[
  {
    "role": "user",
    "content": "Explain S3."
  }
]
```

多轮对话会包括历史：

```json
[
  { "role": "user", "content": "What is S3?" },
  { "role": "assistant", "content": "S3 is object storage..." },
  { "role": "user", "content": "How is it used in this project?" }
]
```

本项目里，历史消息可以来自阶段 3 的 DynamoDB 表：

```text
DocAssistantChatMessages
```

### Inference Config

控制生成行为。

常见参数：

```text
maxTokens
temperature
topP
stopSequences
```

常用理解：

```text
temperature 越低，回答越稳定
temperature 越高，回答越发散
maxTokens 控制最长输出
```

学习和 RAG 问答建议：

```text
temperature: 0 或 0.2
maxTokens: 300-1000
```

## Bedrock API 选择

Bedrock 有几类推理 API。官方当前文档把它们按用途区分。

### Converse API

推荐用于跨模型的对话调用。

特点：

- 统一消息格式
- 适合多轮对话
- 支持 system prompt
- 支持 tool use 的模型也可通过相关配置扩展
- 需要 `bedrock:InvokeModel` 权限

适合本项目：

```text
RAG 问答
文档总结
聊天助手
后续接 Agent/tool calling
```

### ConverseStream

Converse 的流式版本。

适合：

```text
前端逐字显示回答
聊天体验更好
长回答不必等全部生成完
```

需要权限：

```text
bedrock:InvokeModelWithResponseStream
```

### InvokeModel

更底层的模型调用方式。

特点：

- 请求体通常和具体模型有关
- 灵活，但跨模型时要写不同格式
- 适合你需要直接控制某个模型特定接口

### OpenAI-compatible APIs

Bedrock 也支持 OpenAI-compatible API 形态，用于迁移已有 OpenAI 风格应用。

如果已有代码用 Chat Completions / Responses 风格，可以考虑。

本项目从 AWS 原生学习角度，优先记：

```text
Converse API
InvokeModel
ConverseStream
```

## Console 学习流程

入口：

```text
AWS Console
-> Amazon Bedrock
```

建议按这个顺序看：

### 1. Model Catalog

看有哪些模型。

重点观察：

- provider
- model name
- model capabilities
- supported modality
- supported Region
- pricing link

### 2. Playground

在 Console 里直接输入 prompt 测试。

示例 prompt：

```text
Explain Amazon S3 in one paragraph for a beginner.
```

再测试 RAG 风格 prompt：

```text
You are an AWS document assistant.
Answer only from the context.

Context:
Amazon OpenSearch Service is used for retrieval. The application splits each document into smaller chunks, stores every chunk as a searchable document, and returns chunks that match a user's question.

Question:
What does OpenSearch do in this project?
```

观察模型是否基于 context 回答。

### 3. 查看调用示例

很多 Bedrock Console 页面会提供 SDK 示例。

重点看：

```text
boto3 client: bedrock-runtime
operation: converse 或 invoke_model
modelId
messages
inferenceConfig
```

## Python Converse API 示例

推荐结构：

```python
import boto3

client = boto3.Session(
    profile_name="aws-learning",
    region_name="eu-central-1",
).client("bedrock-runtime")

response = client.converse(
    modelId="MODEL_ID_HERE",
    messages=[
        {
            "role": "user",
            "content": [
                {"text": "Explain S3 in one paragraph."}
            ],
        }
    ],
    inferenceConfig={
        "maxTokens": 300,
        "temperature": 0.2,
    },
)

text = response["output"]["message"]["content"][0]["text"]
print(text)
```

`MODEL_ID_HERE` 要换成当前 Region 可用且账号有权限的模型 ID。

## RAG Prompt 示例

把 OpenSearch 返回的 chunks 拼成 context：

```text
[chunk 1]
Amazon OpenSearch Service is used for retrieval...

[chunk 2]
Amazon Bedrock generates answers from retrieved context...
```

再组织 prompt：

```text
你是一个 AWS 文档助手。
只根据上下文回答问题。
如果上下文没有答案，就说“我在当前文档中没有找到答案”。

上下文:
[chunk 1]
Amazon OpenSearch Service is used for retrieval...

[chunk 2]
Amazon Bedrock generates answers from retrieved context...

问题:
OpenSearch 在这个项目里负责什么？
```

模型输出：

```text
OpenSearch 在这个项目里负责 retrieval，也就是从文档 chunks 中检索和用户问题最相关的片段，再把这些片段交给 Bedrock 生成回答。
```

## 和 DynamoDB 聊天历史结合

阶段 3 的聊天表：

```text
DocAssistantChatMessages
```

可以存：

```text
user question
assistant answer
document_id
session_id
created_at
```

调用流程：

```text
1. 用户提问
2. 从 DynamoDB 读取 session 历史
3. 从 OpenSearch 检索相关 chunk
4. 把历史 + chunk + 当前问题传给 Bedrock
5. 把模型回答写回 DynamoDB
```

## 错误和排查

### AccessDeniedException

常见原因：

- IAM policy 没有 `bedrock:InvokeModel`
- 模型访问没有启用
- 当前模型不允许当前账号调用
- 使用了错误 Region

排查：

```text
确认当前 profile
确认 Region
确认 Console 里模型可用
确认 IAM 权限
```

### ValidationException

常见原因：

- modelId 错误
- 请求格式不符合该 API
- 该模型不支持 Converse 或指定参数

### ThrottlingException

请求过快或达到限制。

处理：

- retry with backoff
- 降低并发
- 检查 service quotas

### ModelTimeoutException

模型响应超时。

处理：

- 减少输入 context
- 降低 maxTokens
- 使用流式输出
- 换更快模型

## IAM 权限

最小推理权限大致包括：

```json
{
  "Effect": "Allow",
  "Action": [
    "bedrock:InvokeModel",
    "bedrock:InvokeModelWithResponseStream"
  ],
  "Resource": "*"
}
```

生产环境不建议长期用 `Resource: "*"`.

更好做法是限制到具体模型 ARN 或 inference profile ARN。

本学习项目当前使用：

```text
profile: aws-learning
region: eu-central-1
```

之前验证过该 profile 是 SSO assumed role，并且有管理员权限。学习阶段可用，生产项目要改成最小权限。

## Tokens、Latency、Cost

### Tokens

模型按 token 处理文本。

大致理解：

```text
input tokens = prompt + context + chat history
output tokens = 模型生成的回答
```

RAG 的成本往往取决于：

- 检索回来多少 chunk
- 每个 chunk 多长
- 是否带聊天历史
- 输出回答多长

### Latency

影响延迟的因素：

- 模型大小
- 输入 token 数
- 输出 token 数
- 是否跨 Region / inference profile
- 是否流式返回

### Cost

Bedrock 费用通常和模型、输入 token、输出 token、调用方式有关。

不同模型价格不同。

学习建议：

```text
先用小模型
限制 maxTokens
不要把整篇文档塞进 prompt
只放 top 3-5 chunks
设置 Budget alert
```

## 代码目录规划

阶段 5 代码目录：

```text
projects/aws-ai-doc-assistant/05-bedrock-model-inference/
```

建议结构：

```text
05-bedrock-model-inference/
  README.md
  src/
    config.py
    bedrock_client.py
    ask_bedrock.py
    answer_with_context.py
  data/
    sample_context.txt
```

### ask_bedrock.py

最小模型调用：

```bash
uv run python src/ask_bedrock.py "Explain S3 in one paragraph."
```

### answer_with_context.py

RAG 风格调用：

```bash
uv run python src/answer_with_context.py \
  --question "What does OpenSearch do in this project?" \
  --context-file data/sample_context.txt
```

## 本项目的阶段 5 输出

阶段 5 完成后，应该能做到：

```text
输入用户问题
输入检索上下文
调用 Bedrock
得到回答
把回答保存到 DynamoDB 聊天表
```

它连接阶段 4 和阶段 6：

```text
阶段 4:
OpenSearch 找 chunk

阶段 5:
Bedrock 根据 chunk 回答

阶段 6:
把 S3 + DynamoDB + OpenSearch + Bedrock 串成 RAG pipeline
```

## 清理和安全

Bedrock 本身不需要删除固定资源。

但要注意：

- 不要把 API 输出、敏感 prompt、用户文档内容随便写进公开日志
- 不要在代码里硬编码 AWS credentials
- 不要把模型调用脚本做成无限循环
- 保持 Budget alert
- 生产环境使用最小 IAM 权限

## 实现记录

### 2026-05-06

- 已整理 Bedrock 模型调用阶段的完整学习笔记
- 已确认官方 Bedrock 推理 API 包括 Converse、ConverseStream、InvokeModel、OpenAI-compatible APIs 等
- 阶段 5 推荐以 Converse API 作为跨模型对话调用入口
- 已记录 Console Playground 学习流程
- 已记录 RAG prompt 结构
- 已记录 IAM、错误排查、token、latency、cost 基础

## 完成标准

- [x] 能说明 Bedrock 是 AWS 上调用 foundation model 的托管平台
- [x] 能说明 Console Playground 和 API 调用的区别
- [x] 能解释 Converse API 和 InvokeModel 的区别
- [x] 能解释 prompt、system prompt、messages、inferenceConfig
- [x] 能解释 Bedrock 如何接 OpenSearch retrieval 结果
- [x] 能解释常见错误：AccessDenied、ValidationException、Throttling、Timeout
- [x] 能说明 token、latency、cost 的基本影响因素
- [x] 能规划阶段 5 的代码结构

## 下一步

进入 [阶段 6：RAG 流程整合](06-rag-pipeline-integration.md)。

阶段 6 会把前面内容串起来：

```text
S3 原始文件
-> DynamoDB 文档 metadata
-> OpenSearch 检索 chunk
-> Bedrock 生成回答
-> DynamoDB 保存聊天记录
```

## 参考资料

- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html)
- [Submit prompts and generate responses using the API](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-api.html)
- [Using the Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-call.html)
- [Converse API reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html)
- [InvokeModel API reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html)
- [Access Amazon Bedrock foundation models](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html)
- [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/)
