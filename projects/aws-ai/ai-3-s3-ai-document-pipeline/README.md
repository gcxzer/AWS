# AI-3: S3 AI Document Pipeline

目标：上传文档到 S3 后，自动触发 Lambda 调用 Bedrock 生成摘要，并把结果写回 S3。

推荐架构：

```text
S3 input bucket
  -> ObjectCreated event
  -> Lambda
  -> Bedrock Runtime
  -> S3 output bucket
  -> CloudWatch Logs
```

本目录后续会放：

- Lambda handler
- S3 event 示例
- IAM policy 示例
- 测试文档样例
- 部署和清理记录
