# AWS AI 应用学习路线

目标：你已经有 AI 基础，所以这条路线不重复讲 LLM、RAG、embedding、agent 的基本原理，而是专注学习 **AWS 如何承载 AI 应用**：模型调用、权限、数据接入、serverless 集成、RAG 托管方案、agent 工具调用、监控、成本和生产化。

默认设置：

- 学习目标：掌握 AWS 上 AI 应用的工程实现，不以证书备考为主。
- 推进方式：项目驱动，每个阶段产出一个可运行、可解释、可清理的小作品。
- 技术栈：优先 `Python`、`boto3`、`Lambda`、`S3`；后续可接入任意 Web 前端或 API。
- 默认 Region：优先 `eu-central-1`，但 `Amazon Bedrock` 的模型可用性按控制台实际支持 Region 为准；如果某个模型不在 Frankfurt，可临时使用 `us-east-1` 或其他支持 Region。
- 成本策略：低成本优先；每次实验前确认预算、模型价格、调用次数、资源清理步骤。
- 主线服务：`Amazon Bedrock`、`AWS Lambda`、`Amazon S3`、`API Gateway`、`DynamoDB`、`CloudWatch`、`SQS`、`SNS`、`Step Functions`、`Bedrock Knowledge Bases`、`Bedrock Agents`、`Bedrock Guardrails`、`Bedrock Flows`、`Bedrock Evaluations`。
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
| AI-5 | Bedrock Agent 工具调用 | Bedrock Agents、Lambda、IAM、S3/DynamoDB | 一个可调用 Lambda tool 的 agent | Agent 能决定何时调用工具，并能解释 action group、alias、权限边界 |
| AI-6 | Bedrock Guardrails 安全控制 | Bedrock Guardrails、Bedrock Runtime、Knowledge Bases/Agents | 一套可测试的 guardrail | 能限制危险/越权/敏感输出，并理解 Guardrails 和 IAM 的区别 |
| AI-7 | Bedrock Flows 可视化工作流 | Bedrock Flows、Prompt、Knowledge Base、Lambda、S3 | 一个可视化 AI workflow | 能用节点连接模型、KB、Lambda，并发布/调用 flow |
| AI-8 | Bedrock Evaluation / RAG 评估 | Bedrock Evaluations、S3、Knowledge Bases、judge model | 一个小型评估集和评估报告 | 能评估模型/RAG 质量，而不是只靠肉眼试问题 |
| AI-9 | AI 生产化与治理 | CloudWatch、Budgets、Cost Explorer、CloudTrail、KMS、Secrets Manager、SSM | 生产化 checklist 和监控模板 | 能解释成本、日志、限流、权限、数据安全、重试和告警 |
| AI-10 | AWS 专用 AI API | Textract、Transcribe、Polly、Translate、Comprehend、Rekognition | 多个小 demo | 能判断何时用专用 API，何时用 Bedrock |
| AI-11 | SageMaker 总览与选型 | SageMaker AI、Bedrock、S3、IAM | SageMaker 专项路线和核心概念图 | 能解释 Bedrock 与 SageMaker 的边界 |
| AI-12 | VS Code、Domain、IAM 与 S3 | SageMaker Domain、IAM、S3、KMS、CloudWatch、VS Code | 本地 VS Code 控制 SageMaker 的安全工作区设计 | 能解释 Domain、user profile、space、execution role |
| AI-13 | Processing Jobs | SageMaker Processing、S3、CloudWatch | 一个数据预处理 job | 能把本地预处理脚本迁移到托管 job |
| AI-14 | Hugging Face Training Jobs 基础 | SageMaker Training、Hugging Face、PyTorch、S3、CloudWatch | Hugging Face training job 脚本和 artifact 设计 | 能解释 HF 模型 artifact / `model.tar.gz` 的生成链路 |
| AI-15 | 模型产物与部署准备 | SageMaker Model、Endpoint Config、Endpoint、S3、PyTorch inference | HF 模型 artifact、推理入口和部署计划 | 能解释 model.tar.gz、Model、Endpoint Config、Endpoint 的关系 |
| AI-16 | 大模型参数实验与 HPO | HPO、Training jobs、metrics、LoRA/训练参数 | 一个小规模 HF 参数实验 | 能解释 objective metric、search range、best training job 和成本放大 |
| AI-17 | Model、Endpoint Config 与 Endpoint | SageMaker Model、Endpoint、IAM、CloudWatch | 一个短时实时 endpoint | 能解释 endpoint 为什么会持续收费并能正确删除 |
| AI-18 | Inference 模式全家桶 | Real-time、Serverless、Async、Batch、MME | 推理模式选型表 | 能根据延迟、吞吐和成本选择推理方式 |
| AI-19 | Batch Transform 深入 | Batch Transform、S3、Model artifact | 一个离线批量推理 job | 能不用长期 endpoint 完成批量推理 |
| AI-20 | Model Registry | Model Package Group、Approval、Lineage | 模型版本和审批记录 | 能管理 staging / production 模型版本 |
| AI-21 | SageMaker Pipelines | Processing、Training、Evaluation、Register、Deploy | 一个端到端 ML pipeline | 能把训练流程变成可重复执行的 pipeline |
| AI-22 | Experiments、Lineage 与 Debugging | Experiments、Trials、Lineage、Debugger | 实验追踪和结果对比 | 能追踪数据、代码、参数、指标和模型来源 |
| AI-23 | Model Monitor 与 Clarify | Model Monitor、Clarify、CloudWatch | 监控与偏差/解释性模板 | 能解释数据漂移、模型质量、偏差和可解释性 |
| AI-24 | Feature Store、Ground Truth 与高级能力 | Feature Store、Ground Truth、JumpStart、AutoML、Canvas | 高级能力选型图 | 能判断哪些能力值得进入生产路线 |
| AI-25 | SageMaker Capstone | SageMaker、S3、IAM、Pipelines、Registry、Monitor | 完整端到端 ML 项目 | 能完成训练、注册、推理、监控和清理闭环 |

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

## AI-5：Bedrock Agent 与 Lambda 工具调用

### 为什么排在这里

你已经完成了 `Bedrock Runtime`、`Lambda API`、`S3 pipeline`、`Knowledge Base / RAG`。下一步最自然的是学习 AWS 托管 agent：让模型不仅回答问题，还能在 AWS 权限边界内决定是否调用工具。

这一节不是重新学 agent 原理，而是学习 Bedrock Agent 在 AWS 里的工程形态。

### 目标

构建一个能调用 Lambda 工具的 Bedrock Agent，并理解 Agent、Action Group、Lambda、Alias、IAM permission 的关系。

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
  -> S3 / DynamoDB / static lesson data
  -> Agent final answer
```

推荐小项目：

```text
lesson_helper_agent
```

用户问：

```text
Summarize what I learned in AI-2.
```

Agent 判断需要调用工具：

```text
get_lesson_summary(lesson_id="AI-2")
```

Lambda 返回结构化结果，Agent 再组织成自然语言回答。

### 动手任务

- [ ] 创建一个 Bedrock Agent。
- [ ] 选择一个可用的生成模型。
- [ ] 设计一个简单 action group，例如 `get_lesson_summary`。
- [ ] 用 Lambda 实现工具：根据 `lesson_id` 返回学习摘要。
- [ ] 配置 action schema，让 Agent 知道工具需要哪些参数。
- [ ] 配置 Lambda resource policy，让 Bedrock Agent 可以调用它。
- [ ] 创建 agent alias 并测试。
- [ ] 用 Console 测试 Agent 是否主动调用工具。
- [ ] 用本地 boto3 调 `InvokeAgent`。
- [ ] 记录 Agent 何时调用工具、传了什么参数、Lambda 返回什么。
- [ ] 加入最小权限：Agent 只能调用指定 Lambda，Lambda 只能访问指定 bucket/prefix 或固定数据。
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

## AI-6：Bedrock Guardrails / 安全与边界

### 目标

学习 Guardrails 在 Bedrock 中解决什么问题，以及它和 IAM、应用层校验的边界。

### 核心服务

- `Bedrock Guardrails`
- `Bedrock Runtime`
- `Bedrock Knowledge Bases`
- `Bedrock Agents`
- `CloudWatch Logs`
- `IAM`

### 推荐架构

```text
User input
  -> Guardrail checks input
  -> Bedrock model / Knowledge Base / Agent
  -> Guardrail checks output
  -> Application response
```

### 动手任务

- [ ] 创建一个 Guardrail。
- [ ] 配置 denied topics，例如禁止输出账号密钥、越权操作建议或内部敏感内容。
- [ ] 配置 sensitive information filter，例如 email、phone、AWS key 风格文本。
- [ ] 配置 content filters，观察不同强度对输入和输出的影响。
- [ ] 在 Console 中测试 safe / unsafe / prompt injection 风格输入。
- [ ] 在本地脚本或 Lambda 中调用 Bedrock 时附加 guardrail。
- [ ] 对比三层边界：IAM 权限、应用层校验、Guardrails。
- [ ] 记录 Guardrails 不能解决的问题，例如业务权限、真实身份认证、成本限制。

### 验收标准

- [ ] 能解释 Guardrail 在输入和输出两个阶段分别检查什么。
- [ ] 能解释 Guardrails、IAM、应用层校验分别解决什么问题。
- [ ] 能把 Guardrail 应用到一次 Bedrock 调用。
- [ ] 能说明 Guardrails 对 citations / retrieved references 的适用边界。
- [ ] 能说出 Guardrails 的成本和误拦截风险。

### 清理步骤

- 删除 Guardrail 或保留一个通用学习版 Guardrail。
- 删除测试 Lambda / 测试脚本输出。
- 删除不再需要的 CloudWatch Log Group。

### 费用提醒

- Guardrails 调用可能产生额外费用。
- 学习阶段用短文本测试，不要批量跑大量请求。

## AI-7：Bedrock Flows / 可视化 AI 工作流

### 目标

学习用 Bedrock Flows 把 Prompt、模型、Knowledge Base、Lambda 等节点编排成可视化 AI workflow。

### 为什么不放太早

Flows 是编排层。先学了模型调用、RAG、Agent、Guardrails 后，再学 Flows 才能看懂每个节点代表什么。

### 核心服务

- `Amazon Bedrock Flows`
- `Prompt management`
- `Bedrock Knowledge Bases`
- `Bedrock Agents`
- `AWS Lambda`
- `Amazon S3`
- `IAM Role`

### 推荐架构

```text
Flow input
  -> Prompt node
  -> Knowledge Base node
  -> Lambda node
  -> Flow output
```

### 动手任务

- [ ] 创建一个最小 Flow。
- [ ] 理解 Flow、Node、Connection、Input、Output。
- [ ] 添加 Prompt node，调用一个基础模型。
- [ ] 添加 Knowledge Base node，复用或临时创建一个小 KB。
- [ ] 可选添加 Lambda node，做简单数据转换。
- [ ] 发布 Flow 版本或 alias。
- [ ] 用 Console 测试 Flow。
- [ ] 用 API 或 SDK 调用 Flow。
- [ ] 记录 Flow 和 Step Functions 的区别。

### 验收标准

- [ ] 能解释 Flow 是 workflow，不是模型本身。
- [ ] 能把多个 AI 步骤连接起来。
- [ ] 能说明 Flow 适合低代码 AI 编排，什么时候应该用 Step Functions 或自己写后端。
- [ ] 能解释 Flow 的成本来自它调用的底层资源。

### 清理步骤

- 删除 Flow / Flow alias。
- 删除临时 Knowledge Base / Lambda / S3 资源。
- 删除自动创建的 service role，如果不再使用。

### 费用提醒

- Flow 本身的成本通常来自被它调用的模型、Knowledge Base、Lambda、S3 等资源。
- 不保留临时 KB 或 vector store。

## AI-8：Bedrock Evaluations / 模型与 RAG 评估

### 目标

从“我问了几个问题感觉还行”升级到“我有测试集和评估结果”。重点学习 Bedrock 如何评估模型、Knowledge Base 和 RAG 效果。

### 核心服务

- `Amazon Bedrock Evaluations`
- `Amazon S3`
- `Bedrock Knowledge Bases`
- `Judge model`
- `IAM Service Role`

### 推荐输入数据

先做一个很小的评估集：

```json
[
  {
    "question": "How does the S3 document pipeline work?",
    "expected_source": "s3-document-pipeline.md",
    "expected_answer": "S3 ObjectCreated triggers Lambda, Lambda calls Bedrock, writes summary to output bucket."
  }
]
```

### 动手任务

- [ ] 准备 5-10 条问题和期望答案。
- [ ] 准备 S3 bucket 存评估数据和评估报告。
- [ ] 创建模型评估或 RAG 评估 job。
- [ ] 尝试 retrieve-only evaluation。
- [ ] 尝试 retrieve-and-generate evaluation。
- [ ] 查看评估报告，记录哪些问题检索错、哪些问题生成错。
- [ ] 对比不同 top_k / prompt / 模型的结果。

### 验收标准

- [ ] 能解释 model evaluation 和 RAG evaluation 的区别。
- [ ] 能解释 retrieve-only 与 retrieve-and-generate evaluation 的区别。
- [ ] 能用评估结果指导下一步改 chunking、prompt、top_k 或模型选择。
- [ ] 能说明评估也会产生模型调用和 S3 成本。

### 清理步骤

- 删除评估 job 产生的临时 S3 数据。
- 删除临时 IAM service role。
- 删除临时 Knowledge Base 或 vector store。

### 费用提醒

- Evaluation 可能调用 generator model 和 judge model。
- 学习阶段只用极小测试集。

## AI-9：AI 生产化、观测与治理

### 目标

把“能跑”提升到“可控、可观测、可解释、可治理”。这是 AWS AI 工程里最重要的一层，但放在 Agent、Guardrails、Flows、Evaluation 之后更合理，因为这时你已经见过足够多的 AI 运行形态。

### 核心服务

- `CloudWatch Logs`
- `CloudWatch Metrics`
- `AWS Budgets`
- `Cost Explorer`
- `CloudTrail`
- `IAM Access Analyzer`
- `Secrets Manager`
- `SSM Parameter Store`
- `AWS KMS`
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

### 验收标准

- [ ] 有一份 AI API 生产化 checklist。
- [ ] 有一份日志字段规范。
- [ ] 有一份成本估算和预算告警策略。
- [ ] 有一份最小权限 IAM 示例。
- [ ] 能说明哪些数据可以存，哪些数据不应该长期保存。
- [ ] 能说明生产 AI 应用的主要故障点和成本风险。

### 清理步骤

- 删除测试 alarm。
- 删除测试 secret/parameter。
- 删除不再需要的 log group。
- 保留预算告警和通用 checklist。

### 费用提醒

- CloudWatch Logs 和 Alarm 也会收费。
- Secrets Manager 按 secret 计费；学习阶段可以评估 SSM Parameter Store 是否足够。

## AI-10：AWS 专用 AI API / 可选分支

### 目标

建立 AWS AI 服务选型能力：哪些需求应该用专用 AI API，哪些才需要 Bedrock。

这一节放到后面，因为它不是 Bedrock 主线，但很适合补全 AWS AI 工具箱。

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

## SageMaker AI 专项路线：AI-11 到 AI-25

### 总目标

SageMaker AI 不压缩成一节。它是一整套 ML / MLOps 平台，学习目标是跑通并理解完整链路：

```text
数据 -> 处理 -> 训练 -> 调参 -> 注册 -> 部署 -> 批量推理 -> 监控 -> 治理 -> 清理
```

SageMaker 专项不重新讲机器学习理论，也不再围绕传统表格模型展开。后续主线默认是：本地 VS Code 写代码，用 SageMaker 托管 Hugging Face 模型的处理、训练、部署和治理。

重点放在 AWS 工程形态：

- 数据和模型 artifact 为什么通常在 S3。
- training job、processing job、endpoint、batch transform 分别是什么。
- IAM execution role、KMS、VPC、CloudWatch 在 SageMaker 里怎么起作用。
- endpoint 为什么会持续收费，如何设计低成本学习路径。
- model registry、pipeline、monitor、clarify 如何组成 MLOps 闭环。

### Bedrock 与 SageMaker 的边界

| 需求 | 优先选择 |
| --- | --- |
| 调用托管大模型做总结、问答、RAG、agent、flow | Bedrock |
| OCR、翻译、语音、PII、图片识别 | AWS 专用 AI API |
| 训练自己的模型 | SageMaker |
| 部署自己的模型 endpoint | SageMaker |
| 离线批量推理 | SageMaker Batch Transform |
| 需要模型版本、审批、pipeline、monitor | SageMaker |

### SageMaker 主线架构

```text
Raw data in S3
  -> Processing job
  -> Training job
  -> Model artifact in S3
  -> Model Registry
  -> Batch Transform or Endpoint
  -> Model Monitor / CloudWatch
  -> Retraining pipeline
```

### 学习原则

- 先 batch，后 realtime。
- 先小数据，后 pipeline。
- 默认从本地 VS Code 发起 SageMaker SDK / boto3 调用。
- 先 Hugging Face / PyTorch 框架容器，后自定义容器。
- 先短时 endpoint，后 serverless / async / autoscaling。
- 每节必须记录 IAM、S3、CloudWatch、费用点和清理顺序。
- Studio JupyterLab / Code Editor 只作为可选工具，不作为主开发入口。
- 任何 endpoint、Studio app、notebook、large instance 用完立刻停止或删除。

### AI-11：SageMaker 总览与选型

目标：建立完整地图，先知道 SageMaker 的组件名字、成本风险和清理顺序。

动手任务：

- [ ] 阅读 SageMaker 控制台首页，定位 Studio、Training、Inference、Pipelines、Model Registry。
- [ ] 画出 Bedrock、专用 AI API、SageMaker 的选型边界。
- [ ] 记录 endpoint、Studio app / space、training job、batch transform 的计费差异。
- [ ] 写一份 SageMaker 资源清理顺序。

验收标准：

- [ ] 能解释 SageMaker 不是“大模型服务”，而是 ML 平台。
- [ ] 能解释 training job、model artifact、model、endpoint config、endpoint 的关系。
- [ ] 能说出 endpoint 为什么最容易忘记收费。

### AI-12：VS Code、Domain、IAM 与 S3

目标：理解 SageMaker 工作环境和权限边界，同时明确主开发入口是本地 VS Code，而不是 Studio JupyterLab。

核心概念：

- `Domain`
- `User profile`
- `Space`
- `Studio app`，只作为可选云端 IDE 和费用风险点
- `Local VS Code`
- `Execution role`
- `S3 default bucket`
- `KMS key`
- `CloudWatch Logs`

动手任务：

- [ ] 在 Console 中观察 SageMaker Domain / Studio 的创建入口，但不依赖 Studio JupyterLab 写代码。
- [ ] 设计一个最小权限 execution role。
- [ ] 在本地 VS Code 中保留 SageMaker SDK / boto3 脚本。
- [ ] 设计 S3 artifact 目录结构，例如 `s3://bucket/sagemaker/ai-12/`。
- [ ] 记录哪些资源会持续收费，哪些只是配置。

验收标准：

- [ ] 能解释用户登录 Studio 和 job 执行 role 是两层权限。
- [ ] 能解释为什么不用 Studio JupyterLab 也能从本地 VS Code 创建 SageMaker jobs。
- [ ] 能解释为什么训练数据、脚本、模型 artifact 通常放 S3。

### AI-13：Processing Jobs

目标：把本地数据预处理脚本迁移到托管计算。

推荐项目：

```text
读取本地或 S3 中的 JSONL / 文本样本
  -> 清洗、截断、切分 train/test
  -> 输出 Hugging Face datasets 风格数据到 S3
```

动手任务：

- [ ] 准备一个小 JSONL / 文本数据集。
- [ ] 在本地 VS Code 写 preprocessing 脚本。
- [ ] 用 SageMaker Processing job 执行。
- [ ] 输出 train/test 到 S3。
- [ ] 查看 CloudWatch Logs。

验收标准：

- [ ] 能解释 processing job 和 Lambda 的区别。
- [ ] 能解释 processing input / output 如何映射到容器路径。

### AI-14：Hugging Face Training Jobs 基础

目标：准备并理解一次 Hugging Face 模型相关的最小训练或打包任务，知道它如何产出可被 SageMaker 使用的模型 artifact。

推荐项目：

```text
从 Hugging Face 选择一个小型开源模型
  -> 用 SageMaker Hugging Face / PyTorch training job 跑通训练或轻量微调
  -> 输出 model.tar.gz 到 S3
```

动手任务：

- [ ] 准备训练数据到 S3。
- [ ] 在本地 VS Code 准备 SageMaker Hugging Face / PyTorch training job 脚本。
- [ ] 明确当前是否有 training quota；没有 quota 时不强行运行 job。
- [ ] 记录 `HF_MODEL_ID`、entry point、requirements、instance type、role、input channels、output path。
- [ ] 查看 CloudWatch Logs 和 training metrics。
- [ ] 下载或查看 S3 中的 `model.tar.gz`。

验收标准：

- [ ] 能解释 training job 是临时计算，跑完停止。
- [ ] 能解释 model artifact 只是文件，不是在线服务。
- [ ] 能解释 Hugging Face Hub 模型、S3 artifact、SageMaker Model 三者不是一回事。

### AI-15：模型产物与部署准备

目标：理解 Hugging Face 训练产物如何变成 SageMaker 可部署资源，但先不创建 endpoint。

核心关系：

```text
model.tar.gz in S3
  -> SageMaker Model
  -> Endpoint Configuration
  -> Endpoint
  -> InvokeEndpoint
```

动手任务：

- [ ] 解释 `model.tar.gz` 里模型权重、tokenizer、`code/inference.py` 的作用。
- [ ] 写一个 SageMaker 推理入口 `inference.py` 骨架。
- [ ] 写一个只打印 API request 的 deployment dry-run 脚本。
- [ ] 记录 endpoint 为什么是持续计费资源。

验收标准：

- [ ] 能解释 `model.tar.gz`、SageMaker Model、Endpoint Config、Endpoint 不是一回事。
- [ ] 能说清楚部署前必须确认 artifact、quota 和删除计划。

### AI-16：Hyperparameter Tuning

目标：理解 SageMaker 自动调参如何启动多个 training jobs。主线仍然用 Hugging Face 小规模参数实验，不用传统表格模型。

动手任务：

- [ ] 选择一个 objective metric，例如 eval loss / accuracy / latency proxy。
- [ ] 定义 2 到 3 个 Hugging Face 训练参数范围，例如 learning rate、batch size、epoch。
- [ ] 启动一个小规模 tuning job。
- [ ] 找到 best training job。
- [ ] 对比普通 training job 和 tuning job 的成本。

验收标准：

- [ ] 能解释 objective metric、parameter range、max jobs、parallel jobs。
- [ ] 能说明 HPO 为什么可能快速放大成本。

### AI-17：Model、Endpoint Config 与 Endpoint

目标：理解实时部署链路，并安全地短时测试。

核心关系：

```text
model.tar.gz in S3
  -> SageMaker Model
  -> Endpoint Configuration
  -> Endpoint
```

动手任务：

- [ ] 用 AI-14 的 artifact 创建 Model。
- [ ] 创建 endpoint config。
- [ ] 部署一个小 instance endpoint。
- [ ] 调用一次 inference。
- [ ] 立刻删除 endpoint、endpoint config、model。

验收标准：

- [ ] 能解释 endpoint 是持续运行资源。
- [ ] 能按正确顺序清理部署资源。

### AI-18：Inference 模式全家桶

目标：建立推理方式选型能力。

| 推理方式 | 适合场景 |
| --- | --- |
| Real-time endpoint | 低延迟同步请求 |
| Serverless inference | 间歇性流量，减少空闲成本 |
| Asynchronous inference | 请求耗时长，结果异步返回 |
| Batch Transform | 离线批量推理 |
| Multi-model endpoint | 多个模型共享 endpoint |

动手任务：

- [ ] 写一张选型表：延迟、吞吐、成本、输入大小、结果返回方式。
- [ ] 选择一个场景说明为什么不用 real-time endpoint。

验收标准：

- [ ] 能根据业务需求选推理模式。
- [ ] 能解释 async inference 和 batch transform 的区别。

### AI-19：Batch Transform 深入

目标：不用长期 endpoint 完成离线推理。

动手任务：

- [ ] 准备批量输入文件到 S3。
- [ ] 用已有 model artifact 启动 batch transform job。
- [ ] 查看输出 S3 文件。
- [ ] 查看 job logs。
- [ ] 删除输出和临时资源。

验收标准：

- [ ] 能解释 batch transform 为什么适合学习和离线任务。
- [ ] 能解释 batch input、transform job、batch output 的关系。

### AI-20：Model Registry

目标：理解模型版本和审批。

动手任务：

- [ ] 创建 model package group。
- [ ] 注册一个模型版本。
- [ ] 记录 metrics、artifact、approval status。
- [ ] 模拟 `PendingManualApproval` 到 `Approved`。

验收标准：

- [ ] 能解释 model registry 和 S3 model artifact 的区别。
- [ ] 能解释 staging / production 模型版本管理。

### AI-21：SageMaker Pipelines

目标：把 Processing、Training、Evaluation、Register 串成可重复流程。

推荐 pipeline：

```text
Processing
  -> Training
  -> Evaluation
  -> Condition
  -> Register Model
```

动手任务：

- [ ] 定义 pipeline parameters。
- [ ] 创建 processing step。
- [ ] 创建 training step。
- [ ] 创建 evaluation step。
- [ ] 用 condition step 决定是否注册模型。

验收标准：

- [ ] 能解释 pipeline 和 Step Functions 的关系与区别。
- [ ] 能解释为什么 MLOps 需要可重复 pipeline。

### AI-22：Experiments、Lineage 与 Debugging

目标：让训练结果可比较、可追踪。

动手任务：

- [ ] 为 training jobs 记录 experiment / trial。
- [ ] 比较不同参数下的指标。
- [ ] 查看 lineage：数据、代码、artifact、模型之间的关系。
- [ ] 了解 Debugger / Profiler 能捕获哪些训练信号。

验收标准：

- [ ] 能解释为什么不能只靠文件名管理实验。
- [ ] 能追踪一个模型来自哪份数据、哪次训练、哪些参数。

### AI-23：Model Monitor 与 Clarify

目标：理解上线后的模型质量、安全和公平性。

Model Monitor 关注：

- 数据质量。
- 数据漂移。
- 模型质量。
- 偏差漂移。

Clarify 关注：

- bias detection。
- feature attribution。
- explainability。

动手任务：

- [ ] 了解 endpoint data capture。
- [ ] 设计 baseline dataset。
- [ ] 设计 CloudWatch alarm。
- [ ] 写一份模型监控 checklist。

验收标准：

- [ ] 能解释模型上线后为什么仍然需要监控。
- [ ] 能解释 data drift 和 model quality drift 的区别。

### AI-24：Feature Store、Ground Truth 与高级能力

目标：知道 SageMaker 生态里哪些高级能力解决什么问题，不急着全部实操。

| 能力 | 解决什么 |
| --- | --- |
| Feature Store | 训练和推理共用特征，减少 train/serve skew |
| Ground Truth | 数据标注 |
| JumpStart | 预训练模型和解决方案模板 |
| Autopilot / AutoML | 自动建模 baseline |
| Canvas | 低代码 ML |
| Distributed training | 大规模训练 |
| Custom containers | 完全自定义训练/推理环境 |

验收标准：

- [ ] 能判断哪些高级能力当前需要，哪些暂时只了解。
- [ ] 能解释 Feature Store 为什么是生产 ML 的数据治理组件。

### AI-25：SageMaker Capstone

目标：完成一个端到端 SageMaker 项目。

推荐项目：

```text
Hugging Face 文本模型
  -> Processing
  -> Training / Fine-tuning or packaging
  -> Evaluation
  -> Model Registry
  -> Batch Transform
  -> 可选短时 Endpoint
  -> Monitor checklist
  -> Cleanup report
```

验收标准：

- [ ] 能从 S3 数据开始，产出模型 artifact。
- [ ] 能注册模型版本。
- [ ] 能完成 batch transform。
- [ ] 能选择是否部署 endpoint，并知道如何删除。
- [ ] 能写出完整 IAM、成本、日志、清理记录。

### SageMaker 清理总顺序

每次 SageMaker 实验结束都按这个顺序检查：

1. 删除 realtime endpoint。
2. 删除 endpoint configuration。
3. 删除 SageMaker model。
4. 停止或删除 Studio app、notebook、space。
5. 删除 processing / training / transform job 的临时 S3 输入输出。
6. 删除不再需要的 model artifacts。
7. 删除临时 model package / package group。
8. 删除临时 pipeline。
9. 删除临时 IAM policy / role。
10. 删除不再需要的 CloudWatch Log Group，或设置 retention。

### SageMaker 费用重点

- Endpoint、notebook、Studio app、space 可能持续收费。
- Training、processing、transform 是 job 型资源，按运行时间和实例计费。
- HPO 会启动多个 training jobs，成本会放大。
- S3 artifact、CloudWatch Logs、ECR images、KMS requests 也可能产生费用。
- 学习阶段优先小实例、小数据、短时间运行。

## 推荐推进顺序

主线：

```text
AI-1 Bedrock SDK 调用
  -> AI-2 Lambda + Bedrock API
  -> AI-3 S3 文档处理流水线
  -> AI-4 Bedrock Knowledge Bases / RAG
  -> AI-5 Bedrock Agent + Lambda 工具
  -> AI-6 Guardrails
  -> AI-7 Flows
  -> AI-8 Evaluations
  -> AI-9 生产化与治理
```

后置分支：

```text
AI-10 专用 AI API
  -> AI-11 SageMaker 总览与选型
  -> AI-12 VS Code / Domain / IAM / S3
  -> AI-13 Processing Jobs
  -> AI-14 Training Jobs
  -> AI-15 Training containers
  -> AI-16 Hyperparameter Tuning
  -> AI-17 Endpoint deployment
  -> AI-18 Inference modes
  -> AI-19 Batch Transform
  -> AI-20 Model Registry
  -> AI-21 Pipelines
  -> AI-22 Experiments / Lineage
  -> AI-23 Model Monitor / Clarify
  -> AI-24 Advanced SageMaker
  -> AI-25 SageMaker Capstone
```

如果只想快速形成 AWS AI 应用能力，优先完成 `AI-1` 到 `AI-9`。`AI-10` 是专用 AI API 选型补充。`AI-11` 到 `AI-25` 是 SageMaker 专项，按 ML / MLOps 深度学习。

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
- Bedrock Agents action groups: https://docs.aws.amazon.com/bedrock/latest/userguide/agents-action-create.html
- Bedrock Guardrails: https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html
- Bedrock Flows: https://docs.aws.amazon.com/bedrock/latest/userguide/flows.html
- Bedrock Evaluations: https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html
- Bedrock or SageMaker AI decision guide: https://docs.aws.amazon.com/decision-guides/latest/bedrock-or-sagemaker/bedrock-or-sagemaker.html
- Amazon SageMaker AI getting started: https://aws.amazon.com/sagemaker/ai/getting-started/
- Amazon SageMaker AI features: https://aws.amazon.com/sagemaker/ai/features/
- SageMaker Processing: https://docs.aws.amazon.com/sagemaker/latest/dg/processing-job.html
- SageMaker Training: https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-training.html
- SageMaker Hyperparameter Tuning: https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning.html
- SageMaker Inference: https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html
- SageMaker Batch Transform: https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html
- SageMaker Model Registry: https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html
- SageMaker Pipelines: https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html
- SageMaker Experiments: https://docs.aws.amazon.com/sagemaker/latest/dg/experiments.html
- SageMaker Model Monitor: https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html
- SageMaker Clarify: https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-feature-attribute-shap-baselines.html
- SageMaker Feature Store: https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html
- SageMaker Ground Truth: https://docs.aws.amazon.com/sagemaker/latest/dg/sms.html
