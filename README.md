# AWS 学习笔记入口

这个仓库放 AWS 学习路线、项目笔记和 TopicFollow 生产迁移记录。现在 README 只做入口，不再把所有图堆在一页里。

## 我现在想解决什么问题

| 我卡住的问题 | 去哪里看 |
| --- | --- |
| TopicFollow 现在到底跑在 AWS 的哪些组件上 | [TopicFollow AWS 生产架构](topicfollow-aws-architecture.md) |
| 用户访问网站时，请求怎么从 Cloudflare 到 ECS | [TopicFollow AWS 生产架构](topicfollow-aws-architecture.md#一用户访问网站这条线) |
| ACM、Cloudflare Full strict、ALB HTTPS 证书是什么关系 | [TopicFollow AWS 生产架构](topicfollow-aws-architecture.md#二cloudflareacmalb-https-这条线) |
| 安全组、子网、ALB、ECS、RDS 怎么挡流量 | [TopicFollow AWS 生产架构](topicfollow-aws-architecture.md#三网络子网和安全组) |
| git push 后网站怎么自动部署 | [TopicFollow AWS 生产架构](topicfollow-aws-architecture.md#五代码上线这条线) |
| 新 topic 怎么经过 pipeline 写入 RDS | [TopicFollow AWS 生产架构](topicfollow-aws-architecture.md#六topic-内容写库这条线) |
| hero 图片怎么上传 S3 并更新数据库 | [TopicFollow AWS 生产架构](topicfollow-aws-architecture.md#七hero-图片这条线) |
| AWS 基础服务之间是什么关系 | [AWS 概念心智模型图册](aws-concepts-mental-models.md) |
| Account、Region、AZ、VPC、Subnet 是什么关系 | [AWS 概念心智模型图册](aws-concepts-mental-models.md#2-资源空间和网络边界) |
| EC2、ECS、Fargate 怎么区分 | [AWS 概念心智模型图册](aws-concepts-mental-models.md#3-入口计算和部署) |
| S3、EBS、EFS、RDS、DynamoDB、ElastiCache 怎么选 | [AWS 概念心智模型图册](aws-concepts-mental-models.md#4-存储数据库和数据湖) |
| IAM、Security Group、KMS、Secrets Manager 怎么分工 | [AWS 概念心智模型图册](aws-concepts-mental-models.md#5-安全权限和观测) |
| CloudWatch、CloudTrail、Config、成本、备份怎么理解 | [AWS 概念心智模型图册](aws-concepts-mental-models.md#6-运维成本可靠性和-ai) |
| Bedrock、SageMaker、Amazon Q 怎么区分 | [AWS 概念心智模型图册](aws-concepts-mental-models.md#6-运维成本可靠性和-ai) |
| 一次 Web 请求在 AWS 里怎么走、怎么排错 | [AWS 概念心智模型图册](aws-concepts-mental-models.md#7-一次-web-请求生命周期) |
| IAM 为什么会 AccessDenied | [AWS 概念心智模型图册](aws-concepts-mental-models.md#8-iam-权限判定流程) |
| SQS、EventBridge、Lambda、Step Functions 怎么串异步流程 | [AWS 概念心智模型图册](aws-concepts-mental-models.md#9-serverless-异步流程) |
| CI/CD 和 IaC 分别改什么 | [AWS 概念心智模型图册](aws-concepts-mental-models.md#10-cicd-和-iac-流程) |
| Docker image、ECR、ECS task 和两个 role 怎么连起来 | [AWS 概念心智模型图册](aws-concepts-mental-models.md#11-ecr-image-到-ecs-task-的两个-role) |
| AWS 监控、日志、审计、安全、成本分别看什么 | [AWS 概念心智模型图册](aws-concepts-mental-models.md#12-监控和可观测性地图) |
| 高可用、备份、RTO/RPO 怎么一起理解 | [AWS 概念心智模型图册](aws-concepts-mental-models.md#13-可靠性和恢复流程) |

## 主文档

- [TopicFollow AWS 生产架构](topicfollow-aws-architecture.md)
  - 只讲当前 TopicFollow 真实生产链路。
  - 重点是 Cloudflare、ACM、ALB、ECS、RDS、S3、GitHub Actions、ECS one-off task。
  - 也记录哪些旧路径已经不再使用，例如 Hetzner、SSH 上传、服务器本地 uploads。

- [AWS 概念心智模型图册](aws-concepts-mental-models.md)
  - 只讲通用 AWS 概念。
  - 先按账号、网络、计算、存储、安全、运维、AI 建立分层。
  - 再用 Web 请求、IAM 判权、异步任务、CI/CD、ECS role、监控、可靠性恢复流程图串起来。

## 学习路线

- [AWS 主线学习路线](aws-learning-roadmap.md)
- [AWS AI 学习路线](aws-ai-learning-roadmap.md)
- [AWS RAG 学习路线](aws-rag-learning-roadmap.md)
- [AWS 服务分类速查](aws-services-by-category.md)

## 项目和课程笔记

- [AWS 主线笔记目录](notes/aws-main/00-index.md)
- [AWS AI 笔记目录](notes/aws-ai/00-index.md)
- [AWS RAG 笔记目录](notes/aws-rag/00-index.md)
- [Project 10: TopicFollow production migration](notes/aws-main/12-project-10-topicfollow-production-migration.md)

## 图片管理规则

- 当前 README 不直接承载大图，只负责导航。
- TopicFollow 当前生产架构图放在 [TopicFollow AWS 生产架构](topicfollow-aws-architecture.md)。
- 通用概念图放在 [AWS 概念心智模型图册](aws-concepts-mental-models.md)。
- `assets/` 里只保留仍被 README、主文档、notes 或 projects 引用的图片。
