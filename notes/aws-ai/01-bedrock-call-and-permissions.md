# AI-1：Bedrock 调用与权限

开始日期：2026-05-02

## 目标

本节目标不是学习 AI 原理，而是掌握 AWS 上调用模型的最小链路：

```text
AWS CLI profile
  -> SSO 临时凭证
  -> boto3 Session
  -> bedrock-runtime client
  -> Converse API
  -> foundation model response
```

完成后应能回答：

- 当前终端用哪个 AWS 身份在操作？
- 当前 Region 有哪些 Bedrock 模型？
- 哪些模型可以直接 `ON_DEMAND` 调用？
- Python 代码如何用 `boto3` 调 Bedrock Runtime？
- 响应里的 `latency_ms`、`input_tokens`、`output_tokens`、`stop_reason` 怎么读？
- Bedrock 调用失败时优先看哪些字段？

## 关键概念

### `profile`

`profile` 是本机 AWS CLI/SDK 的身份配置名。它不是 AWS 云上的资源，也不是权限本身。

它的作用是告诉 CLI 或 SDK：

```text
用哪套登录配置
进入哪个 AWS account
扮演哪个 permission set / role
默认操作哪个 region
默认用什么输出格式
```

当前学习使用：

```text
aws-learning
```

命令里的：

```bash
--profile aws-learning
```

意思是：这条命令使用 `aws-learning` 这套本地 AWS 身份配置。

### `boto3`

`boto3` 是 AWS 的 Python SDK。

对比：

```text
AWS CLI = 人在终端里敲命令调用 AWS
boto3 = Python 程序里写代码调用 AWS
```

它们可以使用同一个 profile：

```text
aws sts get-caller-identity --profile aws-learning
boto3.Session(profile_name="aws-learning")
```

### `bedrock` 和 `bedrock-runtime`

`bedrock` 是控制面 API，常用于查询和管理：

```text
列出 foundation models
查看模型信息
管理 Knowledge Bases
管理 Agents
管理 Guardrails
```

`bedrock-runtime` 是运行时 API，用于真正调用模型：

```text
发送 prompt / messages
执行模型推理
接收模型输出
```

本节对应关系：

```text
aws bedrock list-foundation-models = 查有哪些模型
boto3 client("bedrock-runtime").converse(...) = 调模型生成结果
```

### model access 和 IAM permission

Bedrock 调用通常要满足两层权限：

```text
model access = 账号是否被允许使用这个模型
IAM permission = 当前身份是否被允许调用这个模型
```

也就是说：

1. Bedrock 控制台里该模型对账号可用。
2. 当前 profile 对应的 role 有权限调用该模型。

如果其中一层不满足，调用都可能失败。

### Model name 和 Model ID

`Model name` 是人看的名字，例如：

```text
gpt-oss-20b
```

`Model ID` 是程序调用时用的 ID，例如：

```text
openai.gpt-oss-20b-1:0
```

SDK 调用时要使用 `Model ID`，不是 `Model name`。

### `ON_DEMAND` 和 `INFERENCE_PROFILE`

`list-foundation-models` 输出里的 `inferenceTypesSupported` 表示模型支持哪种推理调用方式。

最短理解：

```text
ON_DEMAND = 直接按次调用这个模型
INFERENCE_PROFILE = 通过一个推理配置/路由入口调用模型
```

`ON_DEMAND` 调用链路：

```text
你的代码
  -> modelId
  -> Bedrock 模型
```

特点：

- 不用提前购买容量。
- 按实际输入/输出或模型对应规则计费。
- 适合学习、实验、小流量应用。
- 调用时通常直接使用 `modelId`。

`INFERENCE_PROFILE` 调用链路：

```text
你的代码
  -> inference profile
  -> Bedrock 根据 profile 路由/管理推理
  -> 模型
```

常见用途：

- 跨 Region 推理。
- 某些新模型或特定模型必须通过 profile 调用。
- 统一管理模型调用入口。
- 更稳定地处理可用性、区域路由或容量。

本节优先使用 `ON_DEMAND`，因为它更适合先理解最小调用链路。

## 操作步骤

### 1. 重新登录 SSO

```bash
aws sso login --profile aws-learning
```

如果 SSO session 还没过期，这一步可以跳过。

### 2. 验证当前 AWS 身份

```bash
aws sts get-caller-identity --profile aws-learning
```

重点看：

```text
UserId  = 当前 SSO 用户和临时身份 ID
Account = 当前进入的 AWS account ID
Arn     = 当前实际使用的 STS assumed-role 身份
```

当前学习账号示例：

```text
Account: 089781651608
Arn: arn:aws:sts::089781651608:assumed-role/AWSReservedSSO_AdministratorAccess.../xzhu-admin
```

这说明当前不是 root，而是通过 IAM Identity Center 扮演了 `AdministratorAccess` role。

### 3. 列出当前 Region 的文本模型

```bash
aws bedrock list-foundation-models \
  --profile aws-learning \
  --region eu-central-1 \
  --by-output-modality TEXT \
  --query "modelSummaries[].[providerName,modelName,modelId,inferenceTypesSupported]" \
  --output json
```

这个命令用于观察：

```text
providerName
modelName
modelId
inferenceTypesSupported
```

### 4. 只筛选 `ON_DEMAND` 文本模型

```bash
aws bedrock list-foundation-models \
  --profile aws-learning \
  --region eu-central-1 \
  --by-output-modality TEXT \
  --by-inference-type ON_DEMAND \
  --query "modelSummaries[].[providerName,modelName,modelId]" \
  --output table
```

第 3 步看所有文本模型和推理类型。第 4 步只筛出可以直接 on-demand 调用的文本模型，更适合作为第一节调用目标。

第一节推荐使用：

```text
openai.gpt-oss-20b-1:0
```

原因：

- 支持 `ON_DEMAND`。
- 20B 比 120B 更适合学习阶段。
- 是普通文本生成模型，适合 hello world、总结、分类、结构化抽取。

暂时不要选：

```text
amazon.rerank-v1:0
cohere.rerank-v3-5:0
```

它们是 rerank / 重排序模型，不是普通聊天或总结模型。

### 5. 调用 Bedrock Runtime

项目脚本：

```text
projects/aws-ai/ai-1-bedrock-hello/bedrock_hello.py
```

运行：

```bash
uv run python projects/aws-ai/ai-1-bedrock-hello/bedrock_hello.py \
  --profile aws-learning \
  --region eu-central-1 \
  --model-id openai.gpt-oss-20b-1:0
```

重点看输出里的：

```text
ok
region
model_id
latency_ms
input_tokens
output_tokens
stop_reason
text
```

字段含义：

| 字段 | 含义 |
| --- | --- |
| `ok` | 调用是否成功 |
| `region` | 实际调用的 AWS Region |
| `model_id` | 实际调用的模型 ID |
| `latency_ms` | 请求到响应的耗时 |
| `input_tokens` | 输入 token 数 |
| `output_tokens` | 输出 token 数 |
| `stop_reason` | 模型停止原因 |
| `text` | 模型生成内容 |

常见 `stop_reason`：

```text
end_turn = 模型自然完成回答
max_tokens = 输出达到上限，被截断
```

## 代码阅读重点

打开：

```text
projects/aws-ai/ai-1-bedrock-hello/bedrock_hello.py
```

### 创建 AWS 会话

```python
session = boto3.Session(profile_name=args.profile, region_name=args.region)
```

含义：

```text
profile 决定“我是谁”
region 决定“我要去哪一个 AWS 区域”
```

### 创建 Bedrock Runtime 客户端

```python
client = session.client("bedrock-runtime")
```

这里使用 `bedrock-runtime`，因为本脚本要调用模型推理，而不是查询模型列表或管理资源。

### 组装 Converse API 请求

```python
request = {
    "modelId": args.model_id,
    "messages": [
        {
            "role": "user",
            "content": [{"text": args.prompt}],
        }
    ],
    "inferenceConfig": {
        "maxTokens": args.max_tokens,
        "temperature": args.temperature,
    },
}
```

对应关系：

```text
modelId = 调哪个模型
messages = 发给模型的对话内容
maxTokens = 最大输出长度
temperature = 随机性；越低越稳定，越高越发散
```

### 调用模型

```python
response = client.converse(**request)
```

这一步才是真正的模型推理调用。

## 失败场景

### SSO token 过期

现象：

```text
Token has expired
```

处理：

```bash
aws sso login --profile aws-learning
```

### 无效 model id

测试命令：

```bash
uv run python projects/aws-ai/ai-1-bedrock-hello/bedrock_hello.py \
  --profile aws-learning \
  --region eu-central-1 \
  --model-id invalid.provider-model \
  --prompt "test" \
  --max-tokens 20
```

常见返回：

```text
ValidationException
```

优先检查：

```text
model id 是否正确
Region 是否支持该模型
请求格式是否符合模型要求
```

### 输出被截断

如果看到：

```text
stop_reason: max_tokens
```

说明模型不是自然结束，而是达到最大输出 token 限制。

处理：

```text
调大 max_tokens
缩短 prompt
要求模型输出更紧凑
```

## 复盘问题

- `profile` 和 AWS account / IAM role 的区别是什么？
- `boto3` 和 AWS CLI 的关系是什么？
- 为什么调用模型用 `bedrock-runtime`，不是 `bedrock`？
- `Model name` 和 `Model ID` 哪个给人看，哪个给程序用？
- 为什么第一节优先选 `ON_DEMAND` 模型？
- `input_tokens` 和 `output_tokens` 为什么和成本有关？
- `stop_reason=max_tokens` 说明什么？
- `ValidationException` 出现时先查哪三件事？

## 验收标准

- [ ] 能用 `aws-learning` profile 验证当前身份。
- [ ] 能列出 Bedrock 文本模型。
- [ ] 能筛选 `ON_DEMAND` 文本模型。
- [ ] 能选出一个适合第一节的 `modelId`。
- [ ] 能运行 `bedrock_hello.py` 并成功返回模型输出。
- [ ] 能读懂响应里的 token、延迟和停止原因。
- [ ] 能解释 `bedrock` / `bedrock-runtime`、model access / IAM permission、`ON_DEMAND` / `INFERENCE_PROFILE`。

## 本节文件

- AI-1 代码：[../../projects/aws-ai/ai-1-bedrock-hello/](../../projects/aws-ai/ai-1-bedrock-hello/)
- 调用脚本：[../../projects/aws-ai/ai-1-bedrock-hello/bedrock_hello.py](../../projects/aws-ai/ai-1-bedrock-hello/bedrock_hello.py)
- 最小权限示例：[../../projects/aws-ai/ai-1-bedrock-hello/iam-policy-bedrock-invoke-example.json](../../projects/aws-ai/ai-1-bedrock-hello/iam-policy-bedrock-invoke-example.json)
