# 阶段 1：AWS 基础、安全与 CLI

这一阶段主要通过 AWS Console 和少量只读验证完成，不放业务代码。

## 已完成

- AWS CLI 可用
- SSO profile 可用：`aws-learning`
- 默认学习 Region：`eu-central-1`
- 已确认 S3 访问可用
- 已做跨 Region 资源盘点

## 验证命令

```bash
aws sts get-caller-identity --profile aws-learning --region eu-central-1
```

阶段笔记：

```text
../../notes/aws-ai-doc-assistant/01-aws-foundation-security.md
```
