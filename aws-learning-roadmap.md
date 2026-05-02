# AWS 项目式学习路线

目标：用项目把 AWS 学起来，而不是按 Console 服务列表死记。每个阶段都产出一个能运行、能解释、能清理的作品。

默认设置：

- 学习目标：项目实战，不以证书备考为主。
- 推进节奏：不规定固定时间，一项项目做完并复盘后再进入下一项。
- 技术栈：前半段练习用 `Python` 优先；从项目 6 开始围绕真实项目 `TopicFollow`，技术栈以 `Next.js / TypeScript / Postgres` 为主。
- 费用策略：低成本优先，优先 Free Tier、serverless、短时间运行资源；每个项目都必须有清理步骤。
- 服务选择：先掌握 `P0/P1` 核心服务，再通过项目接触 `P2` 架构服务；`P3/P4` 只做识别和选型理解。
- 配套笔记：服务解释参考 [aws-services-by-category.md](/Users/xzhu/Documents/AWS/aws-services-by-category.md)。

## 学习原则

| 原则 | 具体做法 |
| --- | --- |
| 项目驱动 | 每学一组服务，都用一个小项目把它们串起来 |
| 先能跑，再优化 | 先做最小可运行版本，再补安全、监控、自动化和成本治理 |
| 每项都要验收 | 不以“看过文档”为完成标准，而以“能运行、能解释、能复现”为完成标准 |
| 每项都要清理 | 所有真实部署项目都写清理资源步骤，避免持续收费 |
| 先 P0/P1 | IAM、S3、Lambda、DynamoDB、VPC、CloudWatch、CloudFront、SQS、EventBridge 先学 |
| P3/P4 谨慎 | 专项服务、停服/限制新客户服务只做识别和迁移理解 |

## 低成本规则

| 规则 | 说明 |
| --- | --- |
| 默认 Region | 优先使用 `eu-central-1`，和你当前 AWS Console 区域一致 |
| 少用常驻资源 | EC2、RDS、NAT Gateway、EKS、OpenSearch、MSK 等可能持续收费，学习时短时间开启并及时删除 |
| 优先 serverless | Lambda、API Gateway、DynamoDB、S3、EventBridge、SQS 更适合低成本学习 |
| 每次实验前 | 先确认预算告警、预计资源、清理步骤 |
| 每次实验后 | 检查 CloudFormation stack、S3 bucket、CloudWatch Logs、ECR image、ECS service、Elastic IP 是否残留 |
| 不追求生产级 | 学习项目优先理解架构，不一开始就追求高可用、多 AZ、私有子网、NAT、WAF 全套 |

### 成本决策表

| 资源 | 学习时默认策略 | 什么时候才保留 |
| --- | --- | --- |
| `RDS PostgreSQL` | staging 用最小规格，实验后删除或保留快照 | 正式迁移、恢复演练或需要持续验证数据库行为 |
| `Application Load Balancer` | 只在 ECS/正式切流阶段短期开启 | 需要稳定 HTTP/HTTPS 入口、健康检查和多 task 流量分发 |
| `ECS Fargate` | 测试 task/service 跑完就停 | 容器化迁移阶段需要长期 staging 或 production |
| `EC2` | 学习时用小规格，测试后终止 | V1 低改造迁移期间或作为临时跳板/运维机 |
| `CloudWatch Logs` | 设置较短 retention，避免无限增长 | 生产日志、迁移期间排障日志 |
| `Secrets Manager` | 只放真正需要轮换/审计的 secret | production secret、数据库密码、OAuth secret、邮件 API key |
| `NAT Gateway` | 主线避免使用 | 只有私有子网服务必须主动访问公网且没有更低成本替代时 |
| `EKS / OpenSearch / MSK` | 不进入主线 | 后续专项学习或明确业务需求出现时 |

## TopicFollow 迁移主线

从项目 6 开始，学习路线不再做新的玩具项目，而是把你现有的 `TopicFollow` 从 Hetzner 单机逐步迁到 AWS。

当前已知项目状态：

- 项目目录：`/Users/xzhu/Documents/Web_Development/topicfollow`
- 当前部署：Hetzner 单服务器，网站、Postgres 数据库、图片/上传文件都在同一台机器上。
- 应用技术栈：`Next.js 15`、`React 19`、`TypeScript`、`Postgres`。
- 当前文件存储：本地目录，生产默认类似 `/var/lib/topicfollow/uploads`。
- 当前部署方式：服务器上 `git fetch/reset`、`npm ci`、`next build`、`systemd restart`、健康检查。

推荐迁移路线：

| 阶段 | 迁移方式 | 目的 |
| --- | --- | --- |
| V1 低改造迁移 | `EC2 + RDS PostgreSQL + S3 uploads` | 最像当前 Hetzner 架构，先把系统搬到 AWS 并跑通 |
| V2 容器化迁移 | `ECR + ECS Fargate + RDS + S3` | 学容器和托管运行，减少服务器运维 |
| V3 运维完善 | `CloudWatch + Secrets Manager + CI/CD + Backup + Budget` | 让迁移后的站点可监控、可回滚、可控成本 |

### 迁移前审计清单

| 审计对象 | 需要确认的内容 | 为什么重要 |
| --- | --- | --- |
| 应用进程 | 当前 systemd service、Node.js 版本、启动命令、健康检查 URL、部署用户权限 | 决定 EC2 低改造迁移时如何复用现有启动方式 |
| Postgres | 数据库版本、数据库大小、扩展、连接数、备份位置、恢复耗时、迁移窗口 | 决定 RDS 规格、备份策略和切流前停写时间 |
| uploads | `/var/lib/topicfollow/uploads`、`public/uploads`、topic images、avatars、文件总量、最大文件、URL 规则 | 决定 S3 key 结构、迁移脚本和旧 URL 兼容策略 |
| Nginx/反向代理 | 当前域名、HTTPS、redirect、压缩、缓存、上传大小限制、代理到本地端口 | 决定 AWS 上用 ALB、CloudFront、还是 EC2 Nginx 继续承担入口 |
| cron/job | server cron、`/api/cron/*`、topic orchestrator、数据库备份、backup pull、Telegram monitor | 决定哪些迁到 EventBridge Scheduler、ECS scheduled task、CI job 或外部监控 |
| 备份 | Hetzner 保留 7 天、本地拉取保留 30 天、备份文件命名、恢复命令、恢复验证方法 | 正式迁移前必须先做恢复演练，不只确认“有备份” |
| 监控 | UptimeRobot、Telegram monitor、`/api/health`、Postgres 状态、磁盘、CPU、RAM、域名和证书过期 | 决定迁到 CloudWatch 后哪些检查不能丢 |
| 域名/SSL | `topicfollow.com`、`www.topicfollow.com`、DNS TTL、证书签发位置、回滚记录 | 决定 DNS 切流和失败回滚速度 |
| 邮件 | Resend sender domain、`RESEND_API_KEY`、inbound webhook、退订/验证邮件、DNS 记录 | 切 AWS 后仍要保证事务邮件和 webhook 正常 |
| OAuth | Google OAuth callback URL、`NEXT_PUBLIC_APP_URL`、`COOKIE_DOMAIN`、session cookie、CSRF state cookie | 域名和环境变化最容易让登录失败 |

### 环境变量分组

| 分组 | 变量 | 迁移处理 |
| --- | --- | --- |
| 公开配置 | `NEXT_PUBLIC_APP_URL`、`NEXT_PUBLIC_ANALYTICS_PROVIDER`、`NEXT_PUBLIC_EMAIL_PROVIDER`、`NEXT_PUBLIC_SUPPORT_PROVIDER` | staging 和 production 分开设置，切流前检查 URL 是否指向目标域名 |
| 数据库 | `DATABASE_URL`、`TEST_DATABASE_URL` | production 指向 RDS；测试和 migration job 使用隔离数据库或只读备份 |
| 文件存储 | `UPLOADS_STORAGE_DIR`，后续新增 S3 bucket/prefix/CloudFront 配置 | V1 可保留本地目录，项目 7 后生产转为 S3/CloudFront 模型 |
| 应用 secret | `AUTH_SECRET`、`CONTENT_ADMIN_EMAILS` | 放入 Secrets Manager 或 SSM Parameter Store，不写入镜像或仓库 |
| 邮件 | `RESEND_API_KEY`、`RESEND_FROM_EMAIL`、`RESEND_FROM_NAME`、`RESEND_WEBHOOK_SECRET` | secret 进入 Secrets Manager；域名 DNS 记录切流前单独验证 |
| OAuth | `GOOGLE_CLIENT_ID`、`GOOGLE_CLIENT_SECRET` | staging 和 production 使用不同 callback 或明确区分 authorized redirect URI |
| 第三方 API | `OPENAI_API_KEY` | secret 管理，避免在测试环境无意触发高成本调用 |

### 主要迁移风险

| 风险 | 预防动作 | 回滚动作 |
| --- | --- | --- |
| 数据库丢失或迁移不完整 | 正式切流前做一次 RDS 恢复演练，记录 dump、restore、migration、health check 全流程 | DNS 切回 Hetzner，恢复 Hetzner 写入，保留 AWS 导入库用于排查 |
| 图片路径失效 | 先迁移旧 uploads，再验证 topic images、avatars、`/uploads/...` 路由和 CloudFront URL | 临时保留 Hetzner uploads 或应用回退到本地 storage adapter |
| OAuth callback 错误 | 切流前更新 Google OAuth redirect URI，检查 `NEXT_PUBLIC_APP_URL` 和 `COOKIE_DOMAIN` | Google console 回退旧 callback，DNS 回切旧站 |
| 邮件发送或 webhook 失败 | 验证 Resend sender domain、API key、webhook secret、入站 URL | 邮件入口临时指回 Hetzner 或暂停非关键邮件 |
| DNS 切流失败 | 提前降低 TTL，准备旧 A/CNAME 记录和新记录截图 | 按 Runbook 切回旧记录，等待 TTL 生效 |
| 持续收费失控 | 所有 AWS 资源加 tag，设置 Budgets，测试资源写清删除日期 | 删除测试 ALB/RDS/ECS/EC2/ECR/CloudWatch Logs，保留必要快照 |

### AWS 架构选型表

| 方案 | 适合阶段 | 优点 | 代价/风险 | 本路线决策 |
| --- | --- | --- | --- | --- |
| `EC2 + RDS + S3` | V1 低改造 | 最接近 Hetzner，迁移认知负担低，能复用 systemd/Next.js 运行方式 | 仍要管理服务器补丁、Node.js、进程、磁盘和安全组 | 项目 6 推荐先做 |
| `ECS Fargate + RDS + S3` | V2 容器化 | 不管理服务器，镜像可回滚，部署更标准 | ALB/Fargate/RDS 成本更明显，概念更多 | 项目 8 主线 |
| `App Runner + RDS + S3` | 简化备选 | 比 ECS 更简单，适合 Web app 快速托管 | 对网络、任务、后台 job、精细控制不如 ECS；仍要处理 RDS/S3/secret | 作为备选理解，不作为主线 |
| `Amplify Hosting + RDS/S3` | Next.js SSR 评估 | Next.js SSR 部署和 CI/CD 体验好 | TopicFollow 有 Postgres、uploads、cron/webhook 和迁移需求，先不作为主线 | 后续可单独评估 |
| `EKS + RDS + S3` | 云原生进阶 | Kubernetes 生态完整 | 学习和费用成本高，当前迁移没有必要 | 不进入主线 |

### 环境分层

| 环境 | 用途 | 域名/入口 | 数据和文件 |
| --- | --- | --- | --- |
| `local` | 本地开发和测试 | `localhost:3000` | 本地 Postgres 或 test DB，本地 uploads |
| `staging` | AWS 迁移验证，不接正式流量 | 临时子域名或 ALB/CloudFront 默认域名 | RDS 测试库，S3 staging prefix/bucket，脱敏或备份恢复数据 |
| `production` | 正式用户访问 | `www.topicfollow.com` | RDS production，S3 production bucket/prefix，正式 OAuth 和邮件配置 |

## 路线总览

| 阶段 | 项目 | 核心 AWS 服务 | 主要产出 | 完成标准 |
| --- | --- | --- | --- | --- |
| 1 | 账号与安全地基项目 | IAM、IAM Identity Center、MFA、Billing、Budgets、CloudTrail、CloudWatch | 安全基线和预算告警 | CLI 可访问账号，有预算告警，能解释 root user、IAM user、role |
| 2 | 静态网站发布项目 | S3、CloudFront、ACM、IAM policy、Route 53 可选 | 一个 HTTPS 静态学习主页 | 浏览器可访问，能解释 S3、CDN、证书、域名关系 |
| 3 | Python Serverless API 项目 | Lambda、API Gateway、DynamoDB、IAM Role、CloudWatch Logs | Todo/Bookmark/Learning Notes API | 支持创建、查询、删除；日志可查；权限不过度放开 |
| 4 | 文件上传与数据处理项目 | S3、Lambda trigger、SQS、SNS、EventBridge | 上传后自动处理文件并通知 | 上传文件后自动处理，失败可追踪，能解释事件驱动 |
| 5 | 数据湖入门项目 | S3、Glue Data Catalog、Athena、QuickSight/Quick 概念 | 可查询的数据湖样例 | 能用 SQL 查 S3 数据，能解释数据湖、ETL、Glue、Athena |
| 6 | TopicFollow 迁移盘点与 V1 低改造原型 | VPC、EC2、Security Group、RDS PostgreSQL、S3、CloudFront 可选 | AWS 上的 TopicFollow 低改造迁移方案和测试环境 | 测试环境能跑通 Next.js、RDS、S3 uploads，能解释和 Hetzner 单机的差异 |
| 7 | TopicFollow 图片/上传文件迁移 | S3、CloudFront、IAM policy、KMS 可选 | 本地 uploads 到 S3 的迁移方案 | 新上传文件进 S3，旧文件可访问，能解释对象存储和本地文件系统差异 |
| 8 | TopicFollow 容器化部署 | Docker、ECR、ECS Fargate、ALB、CloudWatch Logs | 容器化 TopicFollow 服务 | ECS 测试环境可访问，镜像可回滚，日志可查 |
| 9 | TopicFollow CI/CD、监控与成本治理 | GitHub Actions 或 CodeBuild/CodePipeline、CloudWatch、Secrets Manager、Budgets、Cost Explorer | 自动部署、告警、secret 管理和成本复盘 | 一次 commit 能部署测试环境，有健康检查、告警和清理清单 |
| 10 | TopicFollow AWS 正式迁移 Capstone | Route 53、ACM、CloudFront/ALB、ECS 或 EC2、RDS、S3、CloudWatch | TopicFollow 从 Hetzner 到 AWS 的完整迁移 | 有架构图、回滚方案、数据迁移步骤、切流步骤、清理旧资源计划 |

## 项目 1：账号与安全地基项目

### 目标

建立一个适合学习 AWS 的安全账号基础。这个项目不追求复杂架构，重点是避免账号一开始就踩安全和费用坑。

### 核心服务

- `IAM`
- `IAM Identity Center`
- `MFA`
- `Billing and Cost Management`
- `AWS Budgets`
- `CloudTrail`
- `CloudWatch`
- `AWS CLI`

### 动手任务

- [ ] 给 root user 开启 MFA。
- [ ] 创建日常使用的管理员身份，不用 root user 做日常操作。
- [ ] 配置 AWS CLI，并能运行 `aws sts get-caller-identity`。
- [ ] 创建预算告警，设置一个很低的学习预算阈值。
- [ ] 确认 CloudTrail 已记录账号 API 活动。
- [ ] 找到 CloudWatch Logs 和 CloudTrail Event history。
- [ ] 记录账号里最重要的安全规则：不用 root、最小权限、每个项目都能清理。

### 验收标准

- [ ] 能用 CLI 成功访问 AWS。
- [ ] 能说清楚 `root user`、`IAM user`、`IAM role`、`permission policy` 的区别。
- [ ] 有预算告警。
- [ ] 知道在哪里看账号操作记录。

### 复盘问题

- 为什么 root user 不适合日常使用？
- IAM role 和 IAM user 最大区别是什么？
- 为什么学习 AWS 第一步不是 EC2，而是 IAM 和 Billing？
- 预算告警能阻止扣费吗？如果不能，它解决什么问题？

### 清理步骤

- 本项目一般不删除 IAM 和预算基础配置。
- 删除任何临时 IAM user、临时 access key、测试 policy。
- 保留预算告警、MFA、CloudTrail 这类基础安全配置。

## 项目 2：静态网站发布项目

### 目标

发布一个静态个人学习主页，用来记录后续 AWS 项目的入口、截图、架构图和链接。

### 核心服务

- `Amazon S3`
- `Amazon CloudFront`
- `AWS Certificate Manager`
- `IAM policy`
- `Route 53` 可选

### 动手任务

- [ ] 准备一个最简单的 `index.html`，内容可以是“我的 AWS 学习主页”。
- [ ] 创建 S3 bucket 存放静态文件。
- [ ] 使用 CloudFront 分发 S3 内容。
- [ ] 如果有域名，使用 ACM 证书和 Route 53 绑定自定义域名。
- [ ] 如果没有域名，先使用 CloudFront 默认域名完成学习。
- [ ] 确认 S3 bucket 不需要公开整个 bucket，也能通过 CloudFront 访问。
- [ ] 把项目结构、访问 URL、架构图记到路线文件或 README。

### 验收标准

- [ ] 可以通过 HTTPS URL 访问页面。
- [ ] 能解释 S3 bucket 和 CloudFront distribution 的关系。
- [ ] 能解释为什么不建议直接公开 S3 bucket。
- [ ] 能说出 CDN、证书、域名解析分别解决什么问题。

### 复盘问题

- S3 是存储服务，为什么能托管静态网站？
- CloudFront 和 S3 的职责分别是什么？
- ACM 证书为什么和 HTTPS 有关？
- Route 53 是否必须使用？什么时候才需要？

### 清理步骤

- 删除 CloudFront distribution，等待禁用完成。
- 删除 S3 bucket 中的对象，再删除 bucket。
- 如果创建了 Route 53 record，删除对应记录。
- 如果申请了临时证书且不用了，删除 ACM certificate。

### 费用提醒

- S3 存储、CloudFront 请求和流量可能产生费用。
- Route 53 hosted zone 和域名会产生费用；没有域名时先跳过。

## 项目 3：Python Serverless API 项目

### 目标

用 Python 做一个最小可用的 Serverless API，例如 Todo、Bookmark 或 Learning Notes。这个项目是后面理解 API、权限、日志和自动化部署的前置练习；真实 Capstone 会换成 TopicFollow 迁移。

### 核心服务

- `AWS Lambda`
- `Amazon API Gateway`
- `Amazon DynamoDB`
- `IAM Role`
- `CloudWatch Logs`
- `boto3`

### 动手任务

- [ ] 设计一个简单数据模型：`id`、`title`、`content`、`created_at`、`updated_at`。
- [ ] 创建 DynamoDB table，使用 `id` 作为 partition key。
- [ ] 编写 Python Lambda，支持创建、查询列表、查询单条、删除。
- [ ] 用 API Gateway 暴露 HTTP API。
- [ ] 给 Lambda 配置只允许访问该 DynamoDB table 的 IAM role。
- [ ] 在 CloudWatch Logs 中查看每次 API 调用日志。
- [ ] 用 curl 或 Postman 测试 API。

### 验收标准

- [ ] `POST` 可以创建记录。
- [ ] `GET` 可以查询记录。
- [ ] `DELETE` 可以删除记录。
- [ ] Lambda 日志能在 CloudWatch 中查到。
- [ ] IAM 权限不是 `*:*` 通配管理员权限。

### 复盘问题

- Lambda 为什么需要 execution role？
- API Gateway 和 Lambda 的边界是什么？
- DynamoDB 和传统关系型数据库有什么不同？
- Serverless 的优点和限制分别是什么？

### 清理步骤

- 删除 API Gateway API。
- 删除 Lambda function。
- 删除 DynamoDB table。
- 删除为项目创建的 IAM role 和 policy。
- 删除不再需要的 CloudWatch Log Group。

### 费用提醒

- Lambda、API Gateway、DynamoDB、CloudWatch Logs 都可能按请求、存储或日志量收费。
- 学习时不要压测，不要创建大量日志。

## 项目 4：文件上传与数据处理项目

### 目标

做一个事件驱动的小系统：文件上传到 S3 后自动触发处理，处理结果写回 S3 或 DynamoDB，并通过通知或日志反馈。

### 核心服务

- `Amazon S3`
- `AWS Lambda`
- `S3 Event Notification`
- `Amazon SQS`
- `Amazon SNS`
- `Amazon EventBridge`
- `CloudWatch Logs`

### 动手任务

- [ ] 创建一个 input bucket 和 output bucket。
- [ ] 上传 CSV、文本或小图片文件到 input bucket。
- [ ] 配置 S3 事件触发 Lambda。
- [ ] Lambda 读取文件，做一个简单处理：统计行数、提取字段、生成摘要或转换格式。
- [ ] 处理结果写入 output bucket 或 DynamoDB。
- [ ] 增加 SQS 作为失败或异步处理缓冲。
- [ ] 使用 SNS 或 CloudWatch Logs 记录处理结果。
- [ ] 尝试用 EventBridge 理解事件路由的另一种方式。

### 验收标准

- [ ] 上传文件后能自动触发处理。
- [ ] 处理结果能在 output bucket 或 DynamoDB 看到。
- [ ] 失败时能通过日志或队列追踪。
- [ ] 能解释 S3 trigger、SQS、SNS、EventBridge 的区别。

### 复盘问题

- 什么是事件驱动架构？
- SQS 和 SNS 的区别是什么？
- EventBridge 和 S3 trigger 的关系是什么？
- 为什么异步处理通常需要失败重试或 DLQ？

### 清理步骤

- 删除 S3 event notification。
- 删除 Lambda function。
- 删除 SQS queue 和 SNS topic。
- 清空并删除 input/output bucket。
- 删除 CloudWatch Log Group。

### 费用提醒

- S3 对象、请求、Lambda 调用、SQS/SNS 请求、CloudWatch Logs 都可能收费。
- 不要上传大量或大体积文件。

## 项目 5：数据湖入门项目

### 目标

把前面项目产生的 CSV 或日志数据放到 S3，用 Glue Data Catalog 建表，用 Athena 直接 SQL 查询，理解数据湖的基本形状。

### 核心服务

- `Amazon S3`
- `AWS Glue Data Catalog`
- `AWS Glue Crawler` 可选
- `Amazon Athena`
- `Amazon QuickSight / Amazon Quick` 概念了解

### 动手任务

- [ ] 准备一份 CSV 数据，例如学习记录、API 调用记录、文件处理结果。
- [ ] 上传到 S3，按 `year/month/day` 或项目名组织目录。
- [ ] 用 Glue Data Catalog 创建 table。
- [ ] 用 Athena 查询 S3 中的数据。
- [ ] 写 3 条 SQL：总数统计、按日期聚合、按类型筛选。
- [ ] 了解 QuickSight/Quick 如何连接数据源做 dashboard，但不强制部署。

### 验收标准

- [ ] Athena 能查询 S3 数据。
- [ ] 能解释 S3、Glue Data Catalog、Athena 的关系。
- [ ] 能说清楚 ETL、数据湖、数据仓库的区别。
- [ ] 能说明为什么 Parquet 通常比 CSV 更适合分析。

### 复盘问题

- Athena 为什么不需要你启动数据库服务器？
- Glue Data Catalog 存的是数据本身，还是元数据？
- 数据湖和数据仓库分别适合什么？
- 查询 S3 数据时，为什么扫描数据量会影响成本？

### 清理步骤

- 删除 Athena 查询结果 bucket 或清理其中对象。
- 删除 Glue database 和 table。
- 删除测试 S3 数据。
- 删除不再需要的 CloudWatch Logs。

### 费用提醒

- Athena 按扫描数据量收费，学习时用小文件。
- Glue crawler、S3 存储、查询结果也可能产生费用。

## 项目 6：TopicFollow 迁移盘点与 V1 低改造原型

### 目标

先不急着重构架构，而是把 Hetzner 单机上的 TopicFollow 拆成三块：`应用`、`数据库`、`图片/uploads 文件`。当前真实状态是：网站、PostgreSQL 数据库、图片/uploads 都在 Hetzner 服务器上。项目 6 的目标不是正式迁移，而是先用 AWS 上最容易理解的低改造架构跑通一个 `staging` 测试环境。

推荐 V1 架构：

- Next.js 应用：`EC2` 上运行 `next start`，尽量复用现有 systemd 部署方式。
- 数据库：`Amazon RDS for PostgreSQL`。
- 上传文件：项目 6 只盘点和临时验证本地 uploads 行为，不把 `S3` 当成已完成目标；项目 7 再正式迁移到 `S3`。
- 入口：测试阶段可先用 EC2 public DNS 或临时子域名，不急着切正式域名。

### 核心服务

- `Amazon VPC`
- `Subnet`
- `Security Group`
- `Amazon EC2`
- `Amazon RDS for PostgreSQL`
- `Amazon S3`，项目 6 只做备份/文件迁移设计，不作为应用正式依赖
- `CloudWatch`
- `AWS Systems Manager Session Manager`
- `AWS Backup` 或 RDS automated backups

### 动手任务

- [ ] 画出当前 Hetzner 架构：Next.js、Postgres、本地 uploads、systemd、Nginx/反向代理、域名、备份。
- [ ] 整理 TopicFollow 必需环境变量：`DATABASE_URL`、`UPLOADS_STORAGE_DIR`、`AUTH_SECRET`、`RESEND_API_KEY`、Google OAuth 等。
- [ ] 整理完整生产环境变量：`NEXT_PUBLIC_APP_URL`、`COOKIE_DOMAIN`、`DATABASE_URL`、`UPLOADS_STORAGE_DIR`、`AUTH_SECRET`、`CONTENT_ADMIN_EMAILS`、`RESEND_API_KEY`、`RESEND_FROM_EMAIL`、`RESEND_WEBHOOK_SECRET`、`OPENAI_API_KEY`、Google OAuth、support/privacy/legal 相关变量。
- [ ] 设计 AWS V1 目标架构图：EC2 + RDS + 临时本地 uploads + CloudWatch；S3 只作为项目 7 的目标存储层标注。
- [ ] 建立 `staging` 概念：使用临时域名或 AWS 默认入口，不改 `www.topicfollow.com` 正式 DNS。
- [ ] staging 使用独立数据库、独立 uploads 目录、独立环境变量；导入生产备份后必须禁用真实邮件、真实 webhook、topic digest、topic orchestrator 等会产生副作用的 job。
- [ ] 创建低规格 EC2 测试机，安装 Node.js 和项目依赖。
- [ ] 创建 RDS PostgreSQL 测试库，不导入生产数据时可先用空库跑 migration。
- [ ] 从现有 Hetzner 备份或本地拉取备份中选择一个测试备份，导入 RDS staging，记录 restore 命令和耗时。
- [ ] 导入后运行 `npm run db:migrate`，再访问 `/api/health`，确认数据库连接和 content mode。
- [ ] 配置 EC2 security group，只开放 HTTP/HTTPS 和必要 SSH；RDS 只允许 EC2 访问。
- [ ] 配置 SSM Session Manager 作为 SSH 替代学习点，记录什么时候可以关闭公网 SSH。
- [ ] 在 EC2 上部署 TopicFollow 测试环境，跑 `npm ci`、`npm run db:migrate`、`npm run build`、`npm start`。
- [ ] 访问 `/api/health`，确认 app、database、environment issues 状态。
- [ ] 记录和 Hetzner 单机相比，哪些职责从服务器转移给 AWS 托管服务。

### 验收标准

- [ ] AWS 测试环境能访问 TopicFollow 首页和 `/api/health`。
- [ ] Next.js 应用能连接 RDS PostgreSQL。
- [ ] 至少完成一次 RDS staging 恢复演练，并记录恢复步骤。
- [ ] staging 环境不影响 Hetzner production 域名和用户。
- [ ] staging 不发送真实用户邮件，不接收生产 webhook，不运行会改写生产语义的后台 job。
- [ ] 能通过 SSH 或 SSM Session Manager 进入 EC2，并解释两者安全差异。
- [ ] 能解释 VPC、Subnet、Security Group、EC2、RDS 的关系。
- [ ] 能说明为什么 RDS 不应该暴露给公网。
- [ ] 有一张 Hetzner 当前架构图和一张 AWS V1 目标架构图。

### 复盘问题

- Hetzner 单机架构里，应用、数据库、图片分别耦合在哪里？
- EC2 迁移和 ECS/App Runner 迁移相比，哪个改造小？哪个运维少？
- RDS 帮你接管了哪些数据库运维责任？
- RDS 仍然有哪些成本和安全风险？
- staging 和 production 的环境变量、数据库、文件 bucket 为什么必须分开？
- 为什么 staging 导入生产数据后必须关闭真实邮件、webhook 和定时任务？
- 如果恢复备份后 `/api/health` 返回 `503`，第一批排查点是什么？

### 清理步骤

- 停止或终止测试 EC2。
- 删除临时 EBS volume、Elastic IP、Security Group。
- 删除测试 RDS instance 和 snapshot，除非明确要保留备份。
- 删除临时 S3 bucket。
- 删除不再需要的 CloudWatch Log Group。

### 费用提醒

- EC2、EBS、RDS、Elastic IP、CloudWatch Logs 都可能持续收费。
- RDS 是本阶段最容易忘记并持续收费的资源；测试结束后要明确删除或保留原因。

## 项目 7：TopicFollow 图片/上传文件迁移

### 目标

把 TopicFollow 当前服务器本地 uploads 迁移到 `S3`，让图片和上传文件不再依赖单台服务器磁盘。这是从单机走向可迁移、可扩展架构的关键一步。

当前代码现状：

- 上传写入逻辑集中在 `src/lib/storage/blob.ts`，默认生产目录类似 `/var/lib/topicfollow/uploads`。
- 公开读取路径由 `src/app/uploads/[...path]/route.ts` 读取本地文件并返回响应。
- 迁移目标不是简单把目录搬走，而是把“文件存储层”抽象成 S3/CloudFront 可替换模型。

### 核心服务

- `Amazon S3`
- `Amazon CloudFront`
- `IAM policy`
- `AWS KMS` 可选
- `AWS CLI`
- `CloudWatch Logs`
- `CloudFront Origin Access Control`，推荐用于让 CloudFront 访问私有 S3 bucket

### 动手任务

- [ ] 盘点当前上传文件来源：`public/uploads`、生产 `UPLOADS_STORAGE_DIR`、topic images、avatars。
- [ ] 盘点数据库里保存图片/附件引用的字段，确认保存的是 `/uploads/...`、完整 URL，还是其他 pathname。
- [ ] 设计 S3 key 结构，例如 `uploads/topic-images/...`、`uploads/avatars/...`。
- [ ] 创建私有 S3 bucket，不直接公开 bucket；CloudFront 访问 S3 时优先使用 OAC。
- [ ] 为应用创建最小权限 IAM policy：只允许读写指定 bucket/prefix。
- [ ] 设计应用层 storage adapter：本地文件系统和 S3 两种实现，staging/production 用 S3。
- [ ] 决定长期 URL 策略：数据库保存稳定 `object key`，展示层拼接 CloudFront URL 或通过 helper 转换。
- [ ] 迁移旧文件：用 `aws s3 sync` 或脚本从 Hetzner uploads 同步到 S3。
- [ ] 决定公开访问方式：CloudFront 分发 S3，或由应用生成受控 URL。
- [ ] 更新数据库里保存的文件 URL 或 pathname 规则，避免硬编码旧服务器路径和旧域名。
- [ ] 保留旧 `/uploads/...` 路径兼容策略：临时 redirect 到 CloudFront，或在应用层将旧 path 映射到 S3 object。
- [ ] 制定回滚策略：S3 写入失败时如何回退本地 adapter，旧图片如何临时从 Hetzner 服务。
- [ ] 验证新上传文件进入 S3，旧图片仍能访问；抽样检查 topic images、avatars、feedback attachments。

### 验收标准

- [ ] 新上传的 topic image/avatar 保存到 S3。
- [ ] 旧 uploads 迁移后仍能在页面显示。
- [ ] 数据库中长期保存的不是脆弱的旧服务器绝对路径。
- [ ] `/uploads/...` 旧路径有兼容策略，不会在切流当天大量 404。
- [ ] S3 bucket 不需要 public write，也不把长期 access key 写进代码。
- [ ] CloudFront 能读取私有 S3 bucket，用户不能绕过 CloudFront 任意写入 bucket。
- [ ] 能解释 S3 object key、bucket policy、IAM policy、CloudFront 的关系。
- [ ] 有一份旧文件迁移清单和回滚办法。

### 复盘问题

- S3 和服务器本地文件系统最大的差异是什么？
- 图片 URL 应该存完整 URL，还是存 object key？各有什么代价？
- 为什么 S3 bucket 不建议直接全公开？
- CloudFront 在图片访问里解决了什么？
- 为什么容器化之前最好先把 uploads 从本地磁盘迁走？

### 清理步骤

- 删除测试上传文件。
- 删除测试 CloudFront distribution。
- 删除测试 S3 bucket 或清空测试 prefix。
- 删除临时 IAM user/access key。
- 保留生产 bucket 前，确认 lifecycle、加密、权限都符合预期。

### 费用提醒

- S3 存储、请求、CloudFront 流量、KMS 请求可能收费。
- 不要把大量历史图片反复同步到多个测试 bucket。

## 项目 8：TopicFollow 容器化部署

### 目标

把 TopicFollow 从“服务器上直接 npm build + systemd restart”升级为容器镜像部署。学习重点是 `Docker image`、`ECR`、`ECS task`、`Fargate`、`ALB` 和日志。

推荐学习路径：先本地 Docker 跑通，再 ECR，再 ECS Fargate 测试环境。`App Runner` 可以作为更简单的备选，但主线用 ECS Fargate 学习容器架构。

注意：项目 8 必须先做网络和成本决策。Fargate task 如果放在私有 subnet，通常需要 NAT Gateway 或等价出网方案来拉镜像、访问外部 API。NAT Gateway 对学习项目可能偏贵，所以这里要明确选择：低成本继续 EC2，还是接受 ECS/Fargate 的网络成本并记录原因。

### 核心服务

- `Docker`
- `Amazon ECR`
- `Amazon ECS`
- `AWS Fargate`
- `Application Load Balancer`
- `CloudWatch Logs`
- `IAM task role`
- `Amazon EventBridge Scheduler`
- `RDS PostgreSQL`
- `S3`

### 动手任务

- [ ] 为 TopicFollow 设计 `Dockerfile`：安装依赖、build Next.js、production start。
- [ ] 本地构建镜像并运行，确认 `/api/health` 正常。
- [ ] 明确容器运行时环境变量，不把 `.env.production` 打进镜像。
- [ ] 创建 ECR repository，推送 TopicFollow 镜像。
- [ ] 创建 ECS cluster、task definition、service。
- [ ] 配置 task role，让应用访问 S3 和必要 AWS 服务。
- [ ] 做 ECS 网络决策：public subnet + public IP、private subnet + NAT Gateway、VPC endpoints，或暂时保留 EC2；记录安全性和成本取舍。
- [ ] 通过 ALB 暴露 ECS service。
- [ ] 配置 CloudWatch Logs 收集容器日志。
- [ ] 盘点后台任务迁移：server cron、`/api/cron/send-topic-digests`、`/api/cron/purge-deleted-accounts`、topic orchestrator、backup pull。
- [ ] 为可容器化的后台任务设计 ECS scheduled task；为 HTTP cron 设计 EventBridge Scheduler 调用方案。
- [ ] 演示一次镜像版本更新和回滚。

### 验收标准

- [ ] TopicFollow 镜像本地可运行。
- [ ] 镜像能推送到 ECR。
- [ ] ECS Fargate 测试环境可访问 `/api/health`。
- [ ] 已记录 ECS 出网方案和 NAT Gateway/ALB/Fargate 的持续费用风险。
- [ ] 容器日志能在 CloudWatch Logs 查看。
- [ ] 至少有一个后台 job 的 AWS 迁移方案：ECS scheduled task、EventBridge Scheduler 或 CI job。
- [ ] 能解释 image、container、ECR repository、task definition、service、cluster、ALB 的区别。

### 复盘问题

- 容器化后，EC2 systemd 部署方式被哪些 AWS 组件替代？
- Fargate 解决了哪些服务器运维问题？
- task role 和 execution role 有什么区别？
- 为什么环境变量和 secret 不应该打进 Docker image？
- 为什么 Fargate 私有 subnet 往往会引入 NAT Gateway 成本？
- HTTP cron、server cron、ECS scheduled task、EventBridge Scheduler 分别适合什么？

### 清理步骤

- 删除 ECS service。
- 停止 running task。
- 删除 ALB、target group、listener。
- 删除 ECS cluster。
- 删除 ECR repository 中测试镜像，再删除 repository。
- 删除项目相关 CloudWatch Log Group。
- 删除临时 IAM role。

### 费用提醒

- Fargate、ALB、CloudWatch Logs、ECR、RDS 都可能持续收费。
- ALB 即使流量很小也会收费；测试完要清理。

## 项目 9：TopicFollow CI/CD、监控与成本治理

### 目标

把 TopicFollow AWS 测试环境从“手动部署”变成“可重复部署、可观察、可控成本”。这一阶段不急着切正式流量，先把发布和运维基本功补齐。

### 核心服务

- `GitHub Actions` 或 `AWS CodeBuild / CodePipeline`
- `IAM deployment role`
- `CloudWatch Logs`
- `CloudWatch Alarms`
- `CloudTrail`
- `AWS Secrets Manager`
- `SSM Parameter Store` 可选
- `CloudFormation / AWS CDK / Terraform`
- `AWS Budgets`
- `Cost Explorer`

### 动手任务

- [ ] 选择 CI/CD 主线：优先 GitHub Actions；想练 AWS 原生再做 CodeBuild/CodePipeline。
- [ ] 建立 deployment role，不使用 root access key 或个人长期管理员 key。
- [ ] CI 中运行质量门禁：`npm test`、`npm run test:pages`、`npm run lint`、`npm run build`。
- [ ] 部署到 ECS 或 EC2 测试环境。
- [ ] 把 `DATABASE_URL`、`AUTH_SECRET`、`RESEND_API_KEY`、Google OAuth secret 放入 Secrets Manager 或 SSM。
- [ ] 把 staging 和 production secret 分开命名，避免 CI/CD 或任务定义误用生产 secret。
- [ ] 为 staging 配置“无真实副作用”策略：不发真实用户邮件，不接生产 webhook，不运行生产 digest/topic orchestrator。
- [ ] 配置 `/api/health` 健康检查。
- [ ] 为 5xx、任务重启、RDS 连接失败、磁盘/内存异常设置 CloudWatch Alarm。
- [ ] 建立 IaC 最小边界：至少用一种工具记录 VPC、安全组、RDS、S3、ECS、IAM、CloudWatch 的目标配置，不只靠控制台点击。
- [ ] 做监控映射：把 UptimeRobot、Telegram monitor、Postgres 状态、磁盘、CPU、RAM、备份新鲜度、域名/SSL 到期检查映射到 AWS 或外部监控。
- [ ] 用 Cost Explorer 标记并复盘 TopicFollow 相关费用。
- [ ] 写 AWS 资源清单：哪些必须保留，哪些测试后必须删除。

### 验收标准

- [ ] 一次 commit 能触发测试和部署。
- [ ] 失败时能从 CI 日志或 CloudWatch Logs 定位原因。
- [ ] secret 不再散落在部署脚本或镜像里。
- [ ] staging 和 production 的 secret、数据库、bucket、cron/job 配置不会互相串用。
- [ ] 有至少 3 个关键告警：应用健康、错误率、数据库/运行环境。
- [ ] 有一份 IaC 或资源定义草案，能复现关键基础设施。
- [ ] 有一份 Hetzner 监控到 AWS 监控的映射表。
- [ ] 有 TopicFollow AWS 月度成本复盘表。

### 复盘问题

- 现有 Hetzner `deploy-production.sh` 迁到 AWS 后哪些步骤还保留？哪些被替代？
- GitHub Actions 和 CodePipeline 各自适合什么？
- Secrets Manager 和 SSM Parameter Store 怎么选？
- 监控、日志、告警和健康检查分别解决什么问题？
- staging 为什么要默认关闭真实邮件、webhook 和生产后台任务？
- 哪些资源必须用 IaC 管理，哪些临时实验资源可以手动创建？

### 清理步骤

- 删除测试 pipeline/build project。
- 删除测试 deployment role 和临时 access key。
- 删除测试 CloudWatch Alarm 和 Log Group。
- 删除不再使用的 secret 或 parameter。
- 保留预算告警、CloudTrail 和生产必要日志。

### 费用提醒

- Secrets Manager、CloudWatch Logs、CloudWatch Alarms、CodeBuild、ALB、ECS、RDS 都可能持续收费。
- 监控资源也要纳入成本复盘，不要只看计算和数据库。

## 项目 10：TopicFollow AWS 正式迁移 Capstone

### 目标

完成一次真实生产迁移：把 TopicFollow 从 Hetzner 单机切到 AWS。这个项目是整条路线的 Capstone，重点不是“用最多服务”，而是能安全迁移、能回滚、能解释、能控制成本。

### 推荐目标架构

- 入口：`Route 53` + `ACM` + `CloudFront` 或 `Application Load Balancer`。
- 应用：优先使用项目 8 跑通的 `ECS Fargate`；低改造备选是 `EC2`。
- 数据库：`RDS PostgreSQL`。
- 图片和上传文件：`S3` + `CloudFront`。
- 密钥：`Secrets Manager` 或 `SSM Parameter Store`。
- 日志和监控：`CloudWatch Logs` + `CloudWatch Alarms`。
- 部署：`GitHub Actions` 或 `CodePipeline/CodeBuild`。

### 正式切流检查清单

| 项目 | 必须确认 |
| --- | --- |
| 应用 URL | `NEXT_PUBLIC_APP_URL` 指向正式域名，不再指向 staging 或 Hetzner 临时地址 |
| Cookie | `COOKIE_DOMAIN` 与正式域名匹配，登录后刷新和跨页面访问不丢 session |
| Google OAuth | Google Console 中 authorized redirect URI 包含新的正式 callback URL |
| Resend | sender domain DNS 记录正确，`RESEND_API_KEY`、`RESEND_WEBHOOK_SECRET`、inbound webhook URL 已切到新环境 |
| HTTPS | ACM 证书已签发，CloudFront/ALB 使用正确证书 |
| DNS | TTL 已提前降低，旧记录和新记录都截图保存，回滚命令或操作步骤已写入 Runbook |
| 数据库 | Hetzner 写入冻结窗口明确，最终备份已导出，RDS production 导入完成，migration 已跑，切流后写入只进入 AWS |
| uploads | S3 文件数量、抽样图片、avatars、topic images 验证通过 |
| 监控 | `/api/health`、CloudWatch Alarm、外部监控、备份检查都启用 |
| 成本 | RDS、ALB、ECS/Fargate 或 EC2、CloudWatch Logs、Secrets Manager、S3、CloudFront 都有 tag 和预算告警 |

### 动手任务

- [ ] 写迁移 Runbook：准备、冻结窗口、备份、数据导入、文件同步、验证、DNS 切换、回滚。
- [ ] 正式迁移前降低 DNS TTL，并记录旧记录、新记录和回滚步骤。
- [ ] 设置写入冻结窗口：暂停 Hetzner 上会写数据库的应用入口和后台 job，避免 AWS 与 Hetzner 双写。
- [ ] 从 Hetzner 导出最终 Postgres 备份。
- [ ] 导入到 RDS 测试库，跑 migrations 和健康检查。
- [ ] 将最终备份导入 RDS production，跑 migrations 和健康检查。
- [ ] 同步 uploads 到 S3，并验证页面图片；必要时在冻结窗口内做最后一次增量 sync。
- [ ] 在 AWS 生产环境部署 TopicFollow。
- [ ] 配置正式域名、HTTPS、OAuth callback URL、cookie domain。
- [ ] 验证 Resend 发送域名、webhook、密码重置、账号验证、topic digest 邮件。
- [ ] 验证所有 cron/job：digests、deleted account purge、topic orchestrator、备份和监控日报。
- [ ] 切换 DNS 前，用临时域名或 host override 做完整验证。
- [ ] 设置短 TTL，执行 DNS 切流。
- [ ] 切流后 Hetzner 旧服务进入观察期，但应保持只读或暂停写入，作为短期回滚路径。
- [ ] 完成后整理架构图、成本表、迁移复盘。

### 验收标准

- [ ] 正式域名访问 AWS 版本 TopicFollow。
- [ ] 登录、Google OAuth、账号页、topic 页面、搜索、图片、邮件发送、健康检查都正常。
- [ ] RDS 数据和 S3 文件迁移完整。
- [ ] 切流后没有 AWS 与 Hetzner 双写；回滚方案明确说明哪些数据会丢失或需要补同步。
- [ ] cron/job 和邮件链路在 AWS 环境中正常。
- [ ] 有明确回滚方案。
- [ ] 有完整 README/Runbook：部署步骤、迁移步骤、清理步骤、成本说明、服务选型解释。
- [ ] 能解释为什么选择 ECS/EC2、RDS、S3、CloudFront，而不是继续单机部署。

### 复盘问题

- 这次迁移最大的风险是什么：数据库、文件、域名、OAuth、邮件，还是成本？
- 哪些组件从“自己运维”变成了“AWS 托管”？
- 如果 DNS 已切到 AWS 但需要回滚，数据库和 uploads 如何避免数据分叉？
- 如果访问量增长，哪些组件先扩容？
- 如果要进一步降低成本，可以合并或替换哪些服务？
- 如果要进一步提高可靠性，需要增加哪些能力？

### 清理步骤

- 删除所有测试 ECS service、EC2 instance、ALB、ECR 测试镜像。
- 删除临时 RDS instance 和 snapshot，保留正式备份策略。
- 删除测试 S3 bucket 或临时 prefix。
- 删除临时 CloudFront distribution。
- 删除临时 IAM role、access key、Security Group。
- 确认 Hetzner 旧服务观察期结束后再下线或降级。

### 费用提醒

- 生产迁移后，长期费用主要来自 RDS、ECS/Fargate 或 EC2、ALB、CloudFront、S3、CloudWatch、Secrets Manager。
- RDS、ALB、NAT Gateway、EKS、OpenSearch 是最容易让学习预算失控的服务；本路线不把 NAT Gateway、EKS、OpenSearch 放入 TopicFollow 主线。

## 可选分支路线

主线完成后，再按兴趣选择分支。分支不需要全部做完。

| 分支 | 项目 | 核心服务 | 适合什么时候做 |
| --- | --- | --- | --- |
| 数据/AI | 文档摘要或学习资料问答 | S3、Glue、Athena、Bedrock、Lambda | 想往数据分析、RAG、生成式 AI 方向走 |
| DevOps/容器 | 容器平台进阶 | ECS 深入、EKS 入门、CDK、CloudWatch、蓝绿部署 | 想往平台工程、DevOps、云原生方向走 |
| IoT | 模拟设备上传温度数据 | IoT Core、Lambda、DynamoDB、IoT Rules | 想理解设备连接、MQTT、物联网数据流 |
| 游戏开发 | 游戏服务架构理解 | GameLift Servers、GameLift Streams、DynamoDB、S3、CloudFront | 对多人游戏服务器或云游戏串流感兴趣 |

### 数据/AI 分支建议

- [ ] 用 S3 存放学习文档或日志。
- [ ] 用 Glue/Athena 查询结构化数据。
- [ ] 用 Bedrock 做文档摘要或问答。
- [ ] 复盘：Athena、Bedrock、SageMaker、Quick 分别适合什么。

### DevOps/容器分支建议

- [ ] 用 CDK 或 CloudFormation 管理一个小项目。
- [ ] 深入 ECS service、task autoscaling、deployment rollback。
- [ ] 只做 EKS 入门，不长期保留集群。
- [ ] 复盘：ECS、EKS、Lambda、App Runner 的选型差异。

### IoT 分支建议

- [ ] 用本地 Python 脚本模拟设备发送 MQTT 消息。
- [ ] IoT Core 接收消息并通过 rule 写入 DynamoDB。
- [ ] Lambda 处理异常温度。
- [ ] 复盘：IoT Core、Device Management、Device Defender 的区别。

### 游戏开发分支建议

- [ ] 先阅读 GameLift Servers 和 GameLift Streams 的概念，不急着部署。
- [ ] 用架构图描述多人游戏服务器需要哪些组件。
- [ ] 复盘：GameLift Servers 托管服务器，GameLift Streams 串流应用画面。

## 最终能力清单

完成主线后，你应该能独立解释和实践这些能力：

- [ ] 账号安全：MFA、IAM user、IAM role、policy、最小权限。
- [ ] 成本控制：预算告警、Cost Explorer、持续收费资源识别。
- [ ] 静态发布：S3、CloudFront、ACM、Route 53 的关系。
- [ ] Serverless API：API Gateway、Lambda、DynamoDB、CloudWatch Logs。
- [ ] 事件驱动：S3 event、SQS、SNS、EventBridge、失败处理。
- [ ] 数据湖入门：S3、Glue Data Catalog、Athena、ETL/ELT。
- [ ] 网络基础：VPC、Subnet、Security Group、公有访问风险。
- [ ] 传统计算：EC2、EBS、SSH、服务部署。
- [ ] 容器基础：Docker、ECR、ECS、Fargate、容器日志。
- [ ] CI/CD：source、build、deploy、artifact、deployment role。
- [ ] 安全运维：CloudTrail、CloudWatch、Access Analyzer、Secrets Manager、KMS。
- [ ] 真实迁移：能把单机应用拆成应用、数据库、文件、域名、密钥、监控和部署流水线。
- [ ] TopicFollow 架构：能解释 Hetzner 单机、EC2 低改造迁移、ECS Fargate 容器化迁移之间的取舍。
- [ ] 切流能力：能写 DNS/OAuth/邮件/证书/回滚 checklist，并在 staging 先验证。
- [ ] 运维迁移：能把 cron、备份、健康检查、Telegram/UptimeRobot 监控映射到 AWS 或外部监控。
- [ ] IaC 意识：能说明哪些资源应该用 CDK/CloudFormation/Terraform 固化，哪些只是临时实验资源。
- [ ] 架构表达：能画架构图、写 README、解释服务选型和替代方案。
- [ ] 资源清理：每个项目结束后能确认没有不必要资源残留。

## 每个项目完成时的固定复盘模板

复制下面这段到每个项目的 README 或学习日志里：

```markdown
## 项目复盘

### 我用了哪些 AWS 服务？

- 

### 为什么选择这些服务？

- 

### 这些服务之间如何通信？

- 

### 哪些资源可能持续收费？

- 

### 我如何清理资源？

- 

### 如果重做一次，我会改什么？

- 

### 我现在能解释的概念

- 
```
