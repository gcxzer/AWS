# 阶段 1：AWS 基础、安全与 CLI

## 目标

先把 AWS 使用环境搭安全，避免后面实验时产生不可控费用。

## 要学习

- AWS account
- Region
- IAM user / role / policy
- MFA
- AWS CLI
- CloudWatch
- Billing Budget

## 要实现

- 注册或确认 AWS 账号
- 开启 MFA
- 设置 Billing Budget，例如每月 10-20 美元提醒
- 安装 AWS CLI
- 优先用 IAM Identity Center / SSO 配置 AWS CLI profile
- 选择默认 Region，德国可以优先用 `eu-central-1`
- 验证当前身份

## 推荐登录方式

优先使用 IAM Identity Center / SSO。当前项目使用的 profile：

```bash
aws sso login --profile aws-learning
aws sts get-caller-identity --profile aws-learning --region eu-central-1
```

原因：

- SSO 使用临时凭证，比长期 access key 更安全
- 适合本地开发和学习项目
- 后续可以给不同项目配置不同 profile

## 验证命令

```bash
aws sts get-caller-identity
```

成功时应该能看到：

```json
{
  "UserId": "...",
  "Account": "...",
  "Arn": "..."
}
```

## 实现记录

### 2026-05-06

- 创建独立笔记目录：`notes/aws-ai-doc-assistant/`
- 创建独立代码目录：`projects/aws-ai-doc-assistant/`
- 将项目笔记拆成阶段文件
- 本地已安装 AWS CLI：`aws-cli/2.34.40`
- AWS CLI 路径：`/opt/homebrew/bin/aws`
- 当前未配置 AWS profile、access key、secret key 和 region
- 执行 `aws sts get-caller-identity` 失败，原因是本地没有 credentials
- 推荐下一步使用 `aws configure sso --profile aws-ai-doc` 配置独立 profile

### 2026-05-06 更新

- 已验证 AWS CLI 身份
- 使用 profile：`aws-learning`
- 使用 Region：`eu-central-1`
- 当前身份类型：SSO assumed role
- 当前权限集：`AdministratorAccess`
- 账号 ID 已在命令输出中出现，后续笔记不记录完整账号 ID
- 已验证 S3 只读访问：`aws s3 ls --profile aws-learning --region eu-central-1`
- 当前账号已有一个与其他项目相关的 S3 bucket，本项目不复用该 bucket

### 2026-05-06 资源盘点

- 已扫描已启用/可用的 17 个 Region
- 除 `eu-central-1` 外，未发现常见区域型资源
- `eu-central-1` 中存在 TopicFollow 相关资源：EIP、ALB、RDS、ECS、ECR、CloudFormation、SNS、Secrets Manager、CloudWatch Logs、S3 bucket
- 存在一个 CloudFront distribution；CloudFront 是全局服务，不属于某个 Region
- 该 CloudFront distribution 当前 `Enabled=false`，origin 指向一个 `eu-central-1` 的 S3 static site

## 完成标准

- [ ] AWS 账号已开启 MFA
- [ ] 已设置 Budget 提醒
- [x] AWS CLI 已安装
- [x] `aws sts get-caller-identity` 能成功返回身份信息
- [x] 知道当前使用的 Region 和 profile

## 下一步

进入 [阶段 2：S3 文档存储](02-s3-document-storage.md)。
