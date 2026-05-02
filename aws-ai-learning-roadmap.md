# AWS AI 应用学习路线

目标：你已经有 AI 基础，所以这条路线不重复讲 LLM、RAG、embedding、agent 的基本原理，而是专注学习 **AWS 如何承载 AI 应用**：模型调用、权限、数据接入、serverless 集成、RAG 托管方案、agent 工具调用、监控、成本和生产化。

默认设置：

- 学习目标：掌握 AWS 上 AI 应用的工程实现，不以证书备考为主。
- 推进方式：项目驱动，每个阶段产出一个可运行、可解释、可清理的小作品。
- 技术栈：优先 `Python`、`boto3`、`Lambda`、`S3`；后续可接入任意 Web 前端或 API。
- 默认 Region：优先 `eu-central-1`，但 `Amazon Bedrock` 的模型可用性按控制台实际支持 Region 为准；如果某个模型不在 Frankfurt，可临时使用 `us-east-1` 或其他支持 Region。
- 成本策略：低成本优先；每次实验前确认预算、模型价格、调用次数、资源清理步骤。
- 主线服务：`Amazon Bedrock`、`AWS Lambda`、`Amazon S3`、`API Gateway`、`DynamoDB`、`CloudWatch`、`SQS`、`SNS`、`Step Functions`、`Bedrock Knowledge Bases`、`Bedrock Agents`、`Bedrock Guardrails`。
- 后置学习：`SageMaker AI` 放在最后，只在需要训练/部署自定义模型或 MLOps 时深入。

## 学习原则

| 原则 | 具体做法 |
| --- | --- |
| 不从训练模型开始 | 先学 Bedrock 和托管 AI 应用能力，再学 SageMaker AI |
| 先打通运行链路 | 先让 SDK、IAM、Region、模型访问和日志跑通 |
| 优先复用已有 AWS 基础 | 复用你已经学过的 S3、Lambda、API Gateway、DynamoDB、SQS、SNS、CloudWatch |
| 每项都要可观测 | 每个 AI 调用都能看到日志、耗时、错误和大致成本 |
| 每项都要可控成本 | 限制输入长度、调用次数、模型选择和测试数据规模 |
| 每项都要清理 | 真实 AWS 资源用完后明确删除，避免持续收费 |
| 专用 API 不被 LLM 替代 | OCR、语音转写、翻译、PII 检测等先看 AWS 专用 AI API，再判断是否需要 Bedrock |

## 路线总览

| 阶段 | 项目 | 核心 AWS 服务 | 主要产出 | 完成标准 |
| --- | --- | --- | --- | --- |
| AI-1 | Bedrock 调用与权限 | Bedrock、IAM、CloudWatch、boto3 | 本地 Python 调用模型 | 能解释模型访问、Region、IAM policy、请求/响应、错误和成本 |
| AI-2 | Bedrock Serverless API | API Gateway、Lambda、Bedrock、CloudWatch | 一个 `/summarize` 或 `/extract` AI API | HTTP 请求能触发 Lambda 调 Bedrock 并返回结构化结果 |
| AI-3 | S3 AI 文档处理流水线 | S3、Lambda、Bedrock、SQS、SNS、CloudWatch | 上传文档后自动生成摘要/结构化结果 | 文件上传后自动处理，失败进入可追踪路径 |
| AI-4 | 托管 RAG 文档问答 | S3、Bedrock Knowledge Bases、Embeddings、Vector store | 对学习文档进行问答 | 能完成 ingestion、retrieve-and-generate、引用来源 |
| AI-5 | AWS 专用 AI API | Textract、Transcribe、Polly、Translate、Comprehend、Rekognition | 多个小 demo | 能判断何时用专用 API，何时用 Bedrock |
| AI-6 | Bedrock Agent 工具调用 | Bedrock Agents、Lambda、S3/DynamoDB、IAM | 一个可调用工具的 agent | Agent 能调用 Lambda tool，并有权限边界 |
| AI-7 | AI 生产化与治理 | CloudWatch、Budgets、Cost Explorer、Guardrails、KMS、Secrets Manager、SSM | 生产化 checklist 和监控模板 | 能解释成本、日志、限流、权限、guardrails、数据安全 |
| AI-8 | SageMaker AI 入门 | SageMaker AI、S3、IAM、Endpoint、Batch Transform | 一个最小训练/部署或 batch inference demo | 能判断 Bedrock 和 SageMaker AI 的选型边界 |

## AI-1：Bedrock 调用与权限

### 目标

先把 AWS 上调用基础模型的最小闭环跑通。重点不是 prompt 技巧，而是 AWS 侧的 `model access`、`Region`、`IAM`、`SDK`、`quota`、`CloudWatch` 和成本。

### 核心服务

- `Amazon Bedrock`
- `Amazon Bedrock Runtime`
- `IAM`
- `CloudWatch`
- `AWS CLI`
- `boto3`

### 动手任务

- [ ] 在 Bedrock 控制台确认当前 Region 支持哪些模型。
- [ ] 开通或确认需要使用的模型访问权限。
- [ ] 用 `aws-learning` profile 验证 CLI 身份。
- [ ] 创建最小权限 IAM policy，允许调用指定 Bedrock model。
- [ ] 本地 Python 脚本调用 Bedrock，完成文本总结。
- [ ] 再做两个任务：分类、结构化 JSON 抽取。
- [ ] 记录一次成功响应：model id、输入长度、输出长度、延迟、费用估算。
- [ ] 故意触发一次错误，例如错误 model id、权限不足或超长输入，并记录排查路径。

### 验收标准

- [ ] 本地脚本能稳定调用 Bedrock。
- [ ] 能解释 `bedrock` 和 `bedrock-runtime` 的区别。
- [ ] 能解释为什么模型访问和 IAM 权限是两件事。
- [ ] 能说明当前使用的 Region 和 model id。
- [ ] 能说出一次调用的大致成本由什么决定。

### 清理步骤

- 删除临时 IAM policy 或 role。
- 删除本地临时输出文件。
- 保留学习脚本和 README。

### 费用提醒

- Bedrock 按模型、输入 token、输出 token 或其他模型计费方式收费。
- 学习阶段限制输入文本长度和循环调用次数。

## AI-2：Bedrock Serverless API

### 目标

把模型调用放到真实 AWS API 架构里，而不是只在本地脚本里跑。

### 核心服务

- `API Gateway`
- `AWS Lambda`
- `Amazon Bedrock`
- `IAM Role`
- `CloudWatch Logs`
- `DynamoDB` 或 `S3` 可选

### 推荐架构

```text
Client / curl
  -> API Gateway HTTP API
  -> Lambda
  -> Bedrock Runtime
  -> CloudWatch Logs
```

可选结果存储：

```text
Lambda
  -> DynamoDB 保存请求摘要
  -> S3 保存完整输入输出
```

### 动手任务

- [ ] 创建 Lambda execution role，只允许调用指定 Bedrock model。
- [ ] 编写 Lambda，支持 `POST /summarize`。
- [ ] 用 API Gateway 暴露 HTTP endpoint。
- [ ] 加入基础输入校验：空文本、超长文本、无效 JSON。
- [ ] 设置 Lambda timeout，观察模型调用延迟。
- [ ] 在 CloudWatch Logs 记录 request id、任务类型、耗时、错误类型，不记录敏感全文。
- [ ] 可选：把请求 metadata 保存到 DynamoDB。
- [ ] 用 curl 测试成功、失败和超长输入三类请求。

### 验收标准

- [ ] HTTP API 可以触发 Bedrock 调用。
- [ ] Lambda 的 IAM 权限不是管理员通配权限。
- [ ] CloudWatch Logs 能看到每次调用的关键信息。
- [ ] 能解释 API Gateway、Lambda、Bedrock 的职责边界。
- [ ] 能说明 Lambda timeout、模型延迟和用户体验之间的关系。

### 清理步骤

- 删除 API Gateway API。
- 删除 Lambda function。
- 删除临时 IAM role/policy。
- 删除 DynamoDB table 或 S3 测试对象。
- 删除不再需要的 CloudWatch Log Group。

### 费用提醒

- API Gateway、Lambda、Bedrock、CloudWatch Logs、DynamoDB/S3 都可能收费。
- 不做压测，不开放无限制公网测试接口。

## AI-3：S3 AI 文档处理流水线

### 目标

把 AI 调用变成事件驱动的文件处理系统：文件上传后自动完成摘要、分类或结构化抽取。

### 核心服务

- `Amazon S3`
- `AWS Lambda`
- `Amazon Bedrock`
- `Amazon SQS`
- `Amazon SNS`
- `CloudWatch Logs`
- `Step Functions` 可选

### 推荐架构

```text
S3 input bucket
  -> ObjectCreated event
  -> Lambda
  -> Bedrock
  -> S3 output bucket
  -> SNS notification
  -> SQS DLQ for failure tracking
```

长文档或多步骤任务可升级为：

```text
S3
  -> Lambda starter
  -> Step Functions
  -> chunk / summarize / merge
  -> S3 output
```

### 动手任务

- [ ] 创建 input bucket 和 output bucket。
- [ ] 上传 `.txt`、`.md` 或小 `.csv` 文件。
- [ ] S3 event 触发 Lambda。
- [ ] Lambda 读取文件内容，调用 Bedrock 生成摘要。
- [ ] 结果写入 output bucket，例如 `processed/<key>.summary.json`。
- [ ] 增加错误处理：解析失败、文件过大、Bedrock 调用失败。
- [ ] 配置 SQS DLQ 或失败记录。
- [ ] 配置 SNS 成功通知或只在 CloudWatch Logs 记录结果。
- [ ] 记录幂等策略：同一个文件重复上传时如何避免重复处理或覆盖混乱。

### 验收标准

- [ ] 上传文件后自动生成 AI 处理结果。
- [ ] 失败路径可追踪。
- [ ] 结果 JSON 包含 source key、model id、created_at、summary。
- [ ] 能解释 S3 event、Lambda、SQS、SNS 在这条链路里的职责。
- [ ] 能说明什么时候 Lambda 不够用，需要 Step Functions 或异步 job。

### 清理步骤

- 删除 S3 event notification。
- 删除 Lambda function。
- 删除 SQS queue 和 SNS topic。
- 清空并删除 input/output bucket。
- 删除 CloudWatch Log Group。

### 费用提醒

- Bedrock 调用和 CloudWatch Logs 是本项目最容易被忽略的成本。
- 不上传大文件，不批量跑大量历史数据。

## AI-4：Bedrock Knowledge Bases / 托管 RAG

### 目标

学习 AWS 托管 RAG 的组件连接方式。你已经懂 RAG，所以重点放在 Bedrock Knowledge Bases 如何管理数据源、embedding、向量存储、同步任务、检索和引用。

### 核心服务

- `Amazon Bedrock Knowledge Bases`
- `Amazon S3`
- `Embeddings model`
- Bedrock 支持的 `Vector store`
- `IAM Role`
- `CloudWatch`

### 推荐输入数据

- AWS 学习笔记 Markdown。
- 项目 README。
- 少量 PDF 或文本资料。

### 推荐架构

```text
Learning docs in S3
  -> Bedrock Knowledge Base data source
  -> ingestion job
  -> embeddings
  -> vector store
  -> retrieve-and-generate
  -> answer with citations
```

### 动手任务

- [ ] 创建一个专用 S3 bucket 或 prefix 存放学习文档。
- [ ] 创建 Knowledge Base。
- [ ] 选择 embeddings model。
- [ ] 选择 Bedrock 当前支持的 vector store。
- [ ] 配置 data source 指向 S3。
- [ ] 执行 ingestion job。
- [ ] 在控制台或 SDK 中测试 10 个问题。
- [ ] 检查回答是否带 source citation。
- [ ] 对比两类问题：资料里有答案的问题、资料里没有答案的问题。
- [ ] 记录 hallucination、引用缺失、文档切分不佳等问题。

### 验收标准

- [ ] Knowledge Base 能基于 S3 文档回答问题。
- [ ] 回答能返回来源引用。
- [ ] 能解释 ingestion、embedding、vector store、retrieve、generate 的 AWS 组件对应关系。
- [ ] 能说明 RAG 和 fine-tuning 在 AWS 实现上的差异。
- [ ] 能说明 Knowledge Bases 的托管便利性和可控性限制。

### 清理步骤

- 删除 Knowledge Base。
- 删除或清空 vector store 相关资源。
- 删除 S3 测试文档。
- 删除临时 IAM role。
- 删除不再需要的 CloudWatch Logs。

### 费用提醒

- 成本可能来自 embeddings、模型调用、vector store、S3 存储和请求。
- 学习阶段只放少量文档。

## AI-5：AWS 专用 AI API

### 目标

建立 AWS AI 服务选型能力：哪些需求应该用专用 AI API，哪些才需要 Bedrock。

### 核心服务和小项目

| 服务 | 小项目 | 学习重点 |
| --- | --- | --- |
| `Amazon Textract` | 从 PDF/图片中抽取文字、表格或表单字段 | 同步/异步调用、S3 输入输出、结构化结果 |
| `Amazon Transcribe` | 音频转文字 | S3 音频输入、转写 job、结果 JSON |
| `Amazon Polly` | 文本转语音 | voice、engine、音频输出格式、S3 保存 |
| `Amazon Translate` | 批量翻译文本 | 语言代码、术语表、批处理 |
| `Amazon Comprehend` | 实体、关键词、情绪、PII 检测 | NLP 专用 API 和 LLM 的边界 |
| `Amazon Rekognition` | 图片标签、物体识别、内容审核 | 图片输入、置信度、审核场景 |

### 动手任务

- [ ] 每个服务只做一个最小 demo。
- [ ] 记录输入格式、输出格式、IAM 权限、是否需要 S3。
- [ ] 记录同步调用和异步 job 的差异。
- [ ] 把结果保存为 JSON，方便后续用 Athena 或 Bedrock 分析。
- [ ] 写一张选型表：专用 API、Bedrock、SageMaker AI 分别适合什么。

### 验收标准

- [ ] 至少完成 3 个专用 AI API demo。
- [ ] 能解释 Textract 和 Rekognition 的区别。
- [ ] 能解释 Transcribe 和 Polly 的方向差异。
- [ ] 能解释 Comprehend 和 Bedrock 在文本分析上的取舍。
- [ ] 能判断一个需求是否需要 LLM。

### 清理步骤

- 删除 S3 测试输入输出。
- 删除临时 IAM role/policy。
- 删除不再需要的 CloudWatch Logs。

### 费用提醒

- 这些服务通常按页数、分钟数、字符数、图片数量或请求量计费。
- 不上传长音频、大 PDF 或大量图片。

## AI-6：Bedrock Agent 与工具调用

### 目标

学习 AWS 托管 agent 形态，以及 agent 如何安全调用 Lambda 工具。

### 核心服务

- `Amazon Bedrock Agents`
- `AWS Lambda`
- `IAM`
- `S3` 或 `DynamoDB`
- `CloudWatch Logs`
- `Bedrock Guardrails` 可选

### 推荐架构

```text
User
  -> Bedrock Agent
  -> Action group
  -> Lambda tool
  -> S3 / DynamoDB
  -> Agent final answer
```

### 动手任务

- [ ] 创建一个 Bedrock Agent。
- [ ] 设计一个简单 action group，例如 `get_document_summary`。
- [ ] 用 Lambda 实现工具：读取 S3 中某个文件的 metadata 或摘要。
- [ ] 配置 Lambda resource policy，让 Bedrock Agent 可以调用它。
- [ ] 创建 agent alias 并测试。
- [ ] 记录 agent 何时调用工具、传了什么参数、Lambda 返回什么。
- [ ] 加入最小权限：agent 只能调用指定 Lambda，Lambda 只能访问指定 bucket/prefix。
- [ ] 可选：加入 Guardrails，限制敏感输出或越权回答。

### 验收标准

- [ ] Agent 能成功调用 Lambda tool。
- [ ] CloudWatch Logs 能看到工具调用日志。
- [ ] 能解释 action group、schema、agent alias、Lambda permission 的关系。
- [ ] 能说明 agent 的权限边界在哪里。
- [ ] 能说出 Bedrock Agent 和自己写 agent orchestration 的取舍。

### 清理步骤

- 删除 agent alias 和 agent。
- 删除 Lambda function。
- 删除临时 IAM role/policy。
- 删除测试 S3/DynamoDB 资源。
- 删除 CloudWatch Log Group。

### 费用提醒

- 成本可能来自模型推理、agent 调用、Lambda、日志和底层数据服务。
- agent 测试时限制多轮对话次数。

## AI-7：AI 生产化与治理

### 目标

把“能跑”提升到“可控、可观测、可解释、可治理”。这是 AWS AI 工程里最重要的一层。

### 核心服务

- `CloudWatch Logs`
- `CloudWatch Metrics`
- `AWS Budgets`
- `Cost Explorer`
- `Bedrock Guardrails`
- `IAM Access Analyzer`
- `Secrets Manager`
- `SSM Parameter Store`
- `AWS KMS`
- `CloudTrail`
- `X-Ray` 可选

### 动手任务

- [ ] 为 AI API 设计日志字段：request_id、user_id/hash、task、model_id、latency_ms、input_size、output_size、error_type。
- [ ] 不在日志里保存敏感原文，除非有明确脱敏和保留策略。
- [ ] 设计成本记录：按请求估算 token 或字符数，记录模型和调用次数。
- [ ] 配置预算告警。
- [ ] 为 Lambda/Bedrock 错误设置 CloudWatch Alarm。
- [ ] 记录常见错误处理：throttling、timeout、model not available、validation error、access denied。
- [ ] 设计 retry/backoff 策略，避免失败时疯狂重试烧钱。
- [ ] 整理 prompt、输入、输出是否需要加密保存。
- [ ] 对 secret 使用 Secrets Manager 或 SSM，不写入代码。
- [ ] 评估是否需要 KMS、VPC endpoint、private networking。
- [ ] 尝试 Bedrock Guardrails，并记录适合和不适合的场景。

### 验收标准

- [ ] 有一份 AI API 生产化 checklist。
- [ ] 有一份日志字段规范。
- [ ] 有一份成本估算和预算告警策略。
- [ ] 有一份最小权限 IAM 示例。
- [ ] 能解释 Guardrails、IAM、应用层校验分别解决什么问题。
- [ ] 能说明哪些数据可以存，哪些数据不应该长期保存。

### 清理步骤

- 删除测试 alarm。
- 删除测试 secret/parameter。
- 删除不再需要的 log group。
- 保留预算告警和通用 checklist。

### 费用提醒

- CloudWatch Logs 和 Alarm 也会收费。
- Secrets Manager 按 secret 计费；学习阶段可以评估 SSM Parameter Store 是否足够。

## AI-8：SageMaker AI 入门

### 目标

最后再学习 SageMaker AI。这里重点不是重新学机器学习，而是理解 AWS 的训练、部署、批处理和 MLOps 平台。

### 什么时候需要 SageMaker AI

适合：

- 需要训练或微调自己的模型。
- 需要部署自定义模型 endpoint。
- 需要 batch transform。
- 需要 model registry、pipeline、实验追踪。
- 需要更完整的 MLOps 工作流。

不优先适合：

- 只是调用大模型做总结、问答、RAG、agent。
- 只是做 OCR、语音转写、翻译、PII 检测。
- 没有自定义训练数据或模型部署需求。

### 核心服务

- `Amazon SageMaker AI`
- `S3`
- `IAM Role`
- `Training job`
- `Model artifact`
- `Endpoint`
- `Batch Transform`
- `CloudWatch Logs`

### 动手任务

- [ ] 创建一个最小 notebook 或本地脚本，准备小数据集到 S3。
- [ ] 跑一个最小 training job，输出 model artifact 到 S3。
- [ ] 部署一个临时 endpoint。
- [ ] 调用 endpoint 完成一次 inference。
- [ ] 删除 endpoint，避免持续收费。
- [ ] 尝试 batch transform，对一批数据离线推理。
- [ ] 记录 SageMaker AI role、S3 artifact、training job、endpoint 的关系。

### 验收标准

- [ ] 能跑通一次 training job 或 batch inference。
- [ ] 能解释 model artifact 为什么通常放在 S3。
- [ ] 能解释 endpoint 为什么会持续收费。
- [ ] 能说清 Bedrock 和 SageMaker AI 的选型边界。

### 清理步骤

- 删除 endpoint。
- 删除 endpoint configuration。
- 删除 model。
- 删除 training job 产生的临时 S3 artifact。
- 删除临时 notebook/instance/space。
- 删除不再需要的 CloudWatch Log Group。

### 费用提醒

- SageMaker endpoint 是持续运行资源，最容易忘记收费。
- 学习阶段优先短时间运行，完成后立刻删除。

## 推荐推进顺序

最短主线：

```text
AI-1 Bedrock SDK 调用
  -> AI-2 Lambda + Bedrock API
  -> AI-3 S3 文档处理流水线
  -> AI-4 Bedrock Knowledge Bases / RAG
  -> AI-7 生产化与治理
```

扩展主线：

```text
AI-5 专用 AI API
  -> AI-6 Bedrock Agent
  -> AI-8 SageMaker AI
```

如果只想快速形成 AWS AI 应用能力，优先完成 `AI-1` 到 `AI-4`，再补 `AI-7`。

## 固定复盘模板

每个 AI 项目完成后复制这段：

```markdown
## 项目复盘

### 我用了哪些 AWS 服务？

-

### 为什么选择这些服务？

-

### 这些服务之间如何通信？

-

### IAM 权限边界是什么？

-

### 哪些资源或调用会产生费用？

-

### 我如何观察日志、错误和延迟？

-

### 我如何清理资源？

-

### 这个项目如果进入生产，还缺什么？

-

### 我现在能解释的 AWS AI 概念

-
```

## 官方参考

- Amazon Bedrock: https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html
- Amazon Bedrock Quickstart: https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html
- Bedrock Knowledge Bases: https://docs.aws.amazon.com/bedrock/latest/userguide/kb-how-it-works.html
- Bedrock or SageMaker AI decision guide: https://docs.aws.amazon.com/decision-guides/latest/bedrock-or-sagemaker/bedrock-or-sagemaker.html
- Amazon SageMaker AI getting started: https://aws.amazon.com/sagemaker/ai/getting-started/
