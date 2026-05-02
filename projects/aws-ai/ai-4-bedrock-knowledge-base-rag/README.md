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

## 实验资源

```text
Knowledge Base: ai-4-aws-notes-kb
Knowledge Base ID: BHDJUFWYDC
Region: eu-central-1
S3 data source: s3://xzhu-ai-4-kb-docs-20260502/docs/
Embedding model: Titan Embeddings v2.0
Vector store: Amazon S3 Vectors
Generation model: openai.gpt-oss-20b-1:0
```

## 本地脚本

只检索 source chunks：

```bash
uv run python projects/aws-ai/ai-4-bedrock-knowledge-base-rag/kb_retrieve.py
```

检索并生成答案：

```bash
uv run python projects/aws-ai/ai-4-bedrock-knowledge-base-rag/kb_retrieve_and_generate.py
```

两个脚本默认使用：

```text
profile: aws-learning
region: eu-central-1
knowledge_base_id: BHDJUFWYDC
```
