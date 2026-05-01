# AWS 学习笔记索引

这个文件只保留目录。详细内容已经拆到 `notes/` 文件夹里，避免单个 note 太长。

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

## 相关文件

- 学习路线：[../aws-learning-roadmap.md](../aws-learning-roadmap.md)
- 服务分类说明：[../aws-services-by-category.md](../aws-services-by-category.md)
- 项目 2 本地站点：[../project-2-static-site/index.html](../project-2-static-site/index.html)
- 项目 2 README：[../project-2-static-site/README.md](../project-2-static-site/README.md)
- 项目 3 Lambda 代码：[../project-3-serverless-api/lambda_function.py](../project-3-serverless-api/lambda_function.py)
- 项目 3 README：[../project-3-serverless-api/README.md](../project-3-serverless-api/README.md)
