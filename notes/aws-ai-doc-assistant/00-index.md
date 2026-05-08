# AWS AI 文档助手笔记索引

这个目录只记录 `AWS AI 文档助手` 这个独立项目的学习和实现过程。

代码目录：

- [../../projects/aws-ai-doc-assistant/](../../projects/aws-ai-doc-assistant/)

## 阶段笔记

1. [阶段 1：AWS 基础、安全与 CLI](01-aws-foundation-security.md)
2. [阶段 2：S3 文档存储](02-s3-document-storage.md)
3. [阶段 3：DynamoDB 元数据与会话](03-dynamodb-metadata-sessions.md)
4. [阶段 4：OpenSearch 文档检索](04-opensearch-document-search.md)
5. [阶段 5：Bedrock 模型调用](05-bedrock-model-inference.md)
6. [阶段 6：RAG 流程整合](06-rag-pipeline-integration.md)
7. [阶段 7：Bedrock AgentCore Agent](07-bedrock-agentcore-agent.md)
8. [阶段 8：生产化、成本与面试准备](08-production-cost-interview.md)

## 最终项目目标

做一个命令行版 AWS AI 文档助手：

```text
用户上传文档
  -> S3 保存原始文件
  -> DynamoDB 保存文档元数据
  -> OpenSearch 保存文档切片并支持检索
  -> Bedrock 根据检索上下文生成答案
  -> AgentCore 将搜索、查询、保存等能力封装成 Agent 工具
```

## 推荐节奏

- 第 1 周：AWS 基础、安全、CLI、Budget
- 第 2 周：S3
- 第 3 周：DynamoDB
- 第 4 周：OpenSearch
- 第 5 周：Bedrock
- 第 6 周：RAG 整合
- 第 7 周：AgentCore
- 第 8 周：整理 README、架构图、面试讲稿、清理脚本

## 当前状态

- [ ] 阶段 1：AWS 基础、安全与 CLI
- [ ] 阶段 2：S3 文档存储
- [ ] 阶段 3：DynamoDB 元数据与会话
- [ ] 阶段 4：OpenSearch 文档检索
- [ ] 阶段 5：Bedrock 模型调用
- [ ] 阶段 6：RAG 流程整合
- [ ] 阶段 7：Bedrock AgentCore Agent
- [ ] 阶段 8：生产化、成本与面试准备
