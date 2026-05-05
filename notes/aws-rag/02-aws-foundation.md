# RAG-2：AWS 基础底座：IAM、S3、Lambda、CloudWatch

## 学习目标

本阶段目标是建立运行 AWS RAG 项目所需的云上基础。你不需要成为 AWS 全栈专家，但必须理解文档放在哪里、代码在哪里运行、权限如何控制、日志如何排查。

完成后你应该能独立说明：

- IAM 为什么是 AWS 项目的安全边界。
- S3 为什么适合作为企业文档入口。
- Lambda 适合承担哪些轻量任务。
- CloudWatch 如何帮助排查 ingestion、调用和运行问题。

## 核心理论

### 最小权限原则

RAG 系统通常会接触企业文档、模型调用权限、向量库和日志。任何一个权限过宽的角色都可能扩大风险。最小权限原则要求每个身份只拥有完成任务所需的最小操作集合。

在学习阶段，先避免使用过宽的 `AdministratorAccess` 作为默认方案。可以在实验时临时放宽，但复盘时必须写清楚后续要收紧哪些权限。

### 对象存储

S3 是 AWS 上最常见的文档落点。它适合存放 PDF、Markdown、HTML、CSV、JSON 等对象，并能和 Bedrock Knowledge Bases、Lambda、事件通知等服务组合。

对 RAG 来说，S3 不是简单的文件夹，而是知识生命周期的入口：

- 原始文档上传。
- 版本与目录组织。
- 数据源同步。
- 访问权限控制。
- 审计与日志追踪。

### 事件驱动

企业文档问答系统常见流程是“文档上传后触发处理”。Lambda 可以用于轻量事件处理，例如校验文件类型、写入元数据、触发同步任务、记录审计日志。

学习阶段不必一开始就自动化所有流程，但要理解事件驱动为什么能减少人工操作。

### 可观测性

RAG 系统出错时，问题可能来自权限、网络、模型、文档格式、检索质量或代码逻辑。CloudWatch 的价值是让你看到系统发生了什么，而不是只看到“回答不对”。

## 关键概念

- **IAM User / Role / Policy**：身份、临时角色和权限声明。
- **S3 Bucket / Object / Prefix**：存储桶、对象和逻辑路径。
- **Lambda Function**：按事件运行的无服务器函数。
- **CloudWatch Logs**：函数、服务和应用日志。
- **Region**：AWS 服务所在区域，Bedrock 模型可用性也依赖区域。
- **Least Privilege**：只授权必要操作。

## 工程取舍

- S3 适合作为文档源，但不适合直接做复杂检索。
- Lambda 适合短任务，不适合长时间批处理或重型解析。
- IAM 权限越宽，实验越省事，但上线风险越高。
- 日志越详细，排查越容易，但要避免记录敏感文档内容。

## 动手实验

1. 创建一个专门用于 RAG 学习的 S3 bucket。
2. 上传几份测试文档，按 `raw/`、`processed/`、`experiments/` 组织 prefix。
3. 创建一个 IAM role，授予读取该 bucket 的最小权限。
4. 创建一个 Lambda 测试函数，读取某个 S3 对象的 metadata。
5. 在 CloudWatch Logs 中查看 Lambda 执行日志。

## 验收标准

- 能画出 S3、IAM、Lambda、CloudWatch 在 RAG 项目中的关系。
- 能解释 IAM policy 中 action、resource、effect 的含义。
- 能上传文档到 S3，并用 Lambda 读取对象信息。
- 能在 CloudWatch 找到一次函数执行日志。

## 阶段产物

- AWS RAG 基础资源图。
- S3 文档目录规划。
- IAM 最小权限说明。
- Lambda + CloudWatch 测试记录。

## 复盘问题

- 哪些角色需要读 S3？哪些角色需要写 S3？
- 如果 Lambda 没权限读取对象，你会如何定位？
- 日志里哪些信息可以记录，哪些信息不应该记录？
- 为什么 Region 选择会影响 Bedrock 后续实验？
