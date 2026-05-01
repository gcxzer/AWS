# Project 2: Static Site On S3 And CloudFront

目标：发布一个最小 AWS 学习主页，用 S3 存静态文件，用 CloudFront 提供 HTTPS 访问。

## 当前本地文件

```text
project-2-static-site/
  index.html
  README.md
  assets/
    static-site-flow.svg
```

## 学习目标

- 理解 S3 bucket 和 object。
- 理解 CloudFront distribution 和 origin。
- 理解为什么 S3 bucket 不应该直接公开。
- 使用 AWS CLI 上传静态文件。
- 写清楚资源清理步骤，避免持续收费。

## 低成本约束

- 暂时不购买域名。
- 暂时不使用 Route 53。
- 暂时不申请自定义 ACM certificate。
- 使用 CloudFront 默认域名完成 HTTPS 访问。
- 项目完成后可以删除 CloudFront distribution 和 S3 bucket。

## 上线前检查

```bash
aws sts get-caller-identity --profile aws-learning
```

确认输出中的 `Arn` 类似：

```text
assumed-role/AWSReservedSSO_AdministratorAccess.../xzhu-admin
```

这表示当前 CLI 使用的是 IAM Identity Center 的日常管理员身份，不是 root。

## 后续部署步骤草案

当前 bucket：

```text
xzhu-aws-learning-static-site-20260501
```

```bash
aws s3 sync ./project-2-static-site s3://xzhu-aws-learning-static-site-20260501 --exclude "README.md" --profile aws-learning
```

当前 CloudFront distribution：

```text
Distribution name: aws-learning-static-site
Distribution ID: E3M6RP17632GUT
Distribution domain: dmt8742p7dnze.cloudfront.net
URL: https://dmt8742p7dnze.cloudfront.net/
```

CloudFront 已配置 S3 bucket 作为 origin，并允许 CloudFront 访问私有 bucket。

更新本地文件后，运行：

```bash
aws s3 sync ./project-2-static-site s3://xzhu-aws-learning-static-site-20260501 --exclude "README.md" --profile aws-learning
aws cloudfront create-invalidation --distribution-id E3M6RP17632GUT --paths "/*" --profile aws-learning
```

自动化部署后续在 CI/CD 项目中再做。

## 清理步骤草案

- Disable CloudFront distribution。
- 等待 distribution 状态变为 disabled。
- Delete CloudFront distribution。
- 清空 S3 bucket。
- Delete S3 bucket。
- 回到 CloudTrail Event history 确认删除操作有记录。

## 复盘问题

- S3 和 CloudFront 分别负责什么？
- 为什么不直接公开 S3 bucket？
- CloudFront 默认域名和自定义域名有什么区别？
- 为什么删除 CloudFront 通常要先 disable？
- 哪些资源可能产生持续费用？
