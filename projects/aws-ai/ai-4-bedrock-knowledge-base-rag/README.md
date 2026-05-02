# AI-4: Bedrock Knowledge Bases / RAG

目标：用 Amazon Bedrock Knowledge Bases 构建一个托管 RAG 小实验。

推荐架构：

```text
S3 documents
  -> Bedrock Knowledge Base
  -> ingestion job
  -> embeddings
  -> vector store
  -> retrieve-and-generate
  -> answer with citations
```

本目录后续会放：

- 测试文档样例
- Knowledge Base 配置记录
- 测试问题和回答记录
- 清理记录
