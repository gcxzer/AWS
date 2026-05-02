# AWS 学习笔记索引

这个文件只保留 AWS 主线目录。详细内容已经拆到 `notes/aws-main/` 文件夹里，避免单个 note 太长。

## 笔记目录

1. [AWS 身份与权限](01-identity-and-access.md)
   - root user、MFA、AWS account
   - IAM Identity Center、user、group、permission set、assignment
   - IAM role、临时凭证、12 小时 session
   - IAM 与 IAM Identity Center 的关系

2. [CloudTrail 基础概念](02-cloudtrail.md)
   - Event history / Ereignisverlauf
   - Trail / Pfad
   - Insights
   - CloudTrail Lake

3. [AWS CLI 与 SSO](03-aws-cli-sso.md)
   - AWS CLI 安装与 profile
   - `aws-learning` SSO 配置
   - 12 小时过期后如何重新登录
   - 常用 CLI 命令和单词解释

4. [项目 2：静态网站发布项目](04-project-2-static-site.md)
   - 静态网页、S3、EC2/VPS 的区别
   - S3 bucket、object、bucket 类型和收费
   - CloudFront distribution、origin、缓存、默认域名
   - 为什么静态网站用 CloudFront，而不是 API Gateway
   - 当前项目资源、验收结果和清理步骤

5. [项目 3：Python Serverless API](05-project-3-serverless-api.md)
   - API Gateway、Lambda、DynamoDB
   - 请求线、权限线、日志线、管理操作线
   - 为什么后端 API 用 API Gateway，而不是直接用 CloudFront
   - IAM Role、CloudWatch Logs、boto3
   - API Gateway route / integration / stage
   - Serverless 后端和传统服务器后端的区别
   - Learning Notes API 当前资源清单和常见混淆点

6. [项目 4：文件上传与数据处理](06-project-4-file-processing.md)
   - S3 ObjectCreated event、Lambda trigger、CloudWatch Logs
   - input bucket 和 output bucket 的职责拆分
   - SQS、SNS、EventBridge 在事件驱动系统里的区别
   - 文件处理结果、失败追踪和清理步骤

7. [项目 5：数据湖入门](07-project-5-data-lake.md)
   - S3 作为数据湖存储层
   - Glue Data Catalog、database、table、schema、metadata
   - Athena 用 SQL 查询 S3 文件
   - CSV、Parquet、partition、schema-on-read
   - Quick / QuickSight 在 BI dashboard 层的位置

8. [项目 6：TopicFollow 迁移盘点与 V1 低改造原型](08-project-6-topicfollow-migration.md)

## 相关文件

- 学习路线：[../../aws-learning-roadmap.md](../../aws-learning-roadmap.md)
- 服务分类说明：[../../aws-services-by-category.md](../../aws-services-by-category.md)
- 项目 2 本地站点：[../../projects/aws-main/project-2-static-site/index.html](../../projects/aws-main/project-2-static-site/index.html)
- 项目 2 README：[../../projects/aws-main/project-2-static-site/README.md](../../projects/aws-main/project-2-static-site/README.md)
- 项目 3 Lambda 代码：[../../projects/aws-main/project-3-serverless-api/lambda_function.py](../../projects/aws-main/project-3-serverless-api/lambda_function.py)
- 项目 3 README：[../../projects/aws-main/project-3-serverless-api/README.md](../../projects/aws-main/project-3-serverless-api/README.md)
- 项目 4 Lambda 代码：[../../projects/aws-main/project-4-file-processing/lambda_function.py](../../projects/aws-main/project-4-file-processing/lambda_function.py)
- 项目 4 README：[../../projects/aws-main/project-4-file-processing/README.md](../../projects/aws-main/project-4-file-processing/README.md)
- 项目 5 笔记：[07-project-5-data-lake.md](07-project-5-data-lake.md)
- 项目 5 架构图：[../../assets/project-5-data-lake-flow.svg](../../assets/project-5-data-lake-flow.svg)
- 项目 6 笔记：[08-project-6-topicfollow-migration.md](08-project-6-topicfollow-migration.md)
