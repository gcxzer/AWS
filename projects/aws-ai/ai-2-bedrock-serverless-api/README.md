# AI-2: Bedrock Serverless API

目标：把 AI-1 的本地 Bedrock 调用封装成一个 HTTP API。

推荐架构：

```text
Client / curl
  -> API Gateway HTTP API
  -> Lambda
  -> Bedrock Runtime
  -> CloudWatch Logs
```

本目录后续会放：

- Lambda handler
- 本地测试 event
- IAM policy 示例
- 部署和清理命令
