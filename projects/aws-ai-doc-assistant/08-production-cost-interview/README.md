# 阶段 8：生产化、成本与面试准备

这个阶段放生产化辅助脚本和项目交付材料。当前阶段笔记已经包含生产化、安全、成本、IAM、清理和面试讲法。

计划内容：

- 成本清理脚本
- IAM 最小权限说明
- 架构文档
- 面试讲稿
- 复现步骤

阶段笔记：

```text
../../notes/aws-ai-doc-assistant/08-production-cost-interview.md
```

## 建议目录结构

```text
08-production-cost-interview/
  README.md
  docs/
    architecture.md
    interview-notes.md
    iam-least-privilege.md
    cost-control.md
  scripts/
    cleanup.sh
```

## 面试核心说法

```text
S3 stores raw documents.
DynamoDB stores metadata and chat history.
OpenSearch retrieves relevant chunks.
Bedrock generates grounded answers.
AgentCore turns the fixed RAG flow into a production-ready agent with Runtime, Gateway, Memory, Identity, and Observability.
```
