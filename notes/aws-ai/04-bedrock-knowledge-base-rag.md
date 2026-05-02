# AI-4：Bedrock Knowledge Bases / 托管 RAG

![AI-4 Bedrock Knowledge Base RAG flow](../../assets/ai-4-bedrock-knowledge-base-rag-flow.svg)

## 目标

学习 AWS 托管 RAG 的组件连接方式。你已经理解 RAG 原理，所以本节重点不是解释 embedding / vector search 的基础，而是掌握 Bedrock Knowledge Bases 在 AWS 里如何把这些能力托管起来。

目标链路：

```text
S3 documents
  -> Bedrock Knowledge Base
  -> ingestion job
  -> embeddings
  -> vector store
  -> retrieve-and-generate
  -> answer with citations
```

## 本节要学的 AWS 重点

- Knowledge Base 是什么。
- Data source 如何连接 S3。
- Ingestion job 做了什么。
- Embedding model 如何选择。
- Vector store 是谁创建和管理。
- Retrieve and generate 如何测试。
- Citation / source reference 怎么返回。
- 成本来自哪些组件。
- 实验结束后如何删除 Knowledge Base、vector store 和 S3 数据。

## 推荐资源命名

Region 默认使用：

```text
eu-central-1
```

学习资源建议命名：

| 资源 | 建议名称 |
| --- | --- |
| S3 bucket | `xzhu-ai-4-kb-docs-20260502` |
| S3 prefix | `docs/` |
| Knowledge Base | `ai-4-aws-notes-kb` |
| Data source | `ai-4-s3-docs` |
| IAM role | 由 Bedrock Console 自动创建，或手动创建后命名为 `ai-4-bedrock-kb-role` |

如果 S3 bucket 名称已被占用，加随机后缀。

## 推荐测试文档

本节可以先放 2-3 个小 Markdown / text 文档，例如：

```text
docs/bedrock-basics.md
docs/lambda-bedrock-api.md
docs/s3-document-pipeline.md
```

内容可以来自 AI-1、AI-2、AI-3 的学习笔记摘要。

## 职责边界

| 组件 | 职责 |
| --- | --- |
| S3 | 存放原始学习文档 |
| Knowledge Base | 管理数据源、embedding、vector store、检索配置 |
| Data source | 告诉 Knowledge Base 从哪里读文档 |
| Ingestion job | 读取文档、切分、生成 embedding、写入 vector store |
| Embedding model | 把文本 chunk 转成向量 |
| Vector store | 存向量并支持相似度检索 |
| Retrieve and generate | 根据问题检索相关片段，并调用生成模型回答 |
| Citation | 告诉回答依据来自哪些源文档或片段 |

## 操作步骤草案

1. 创建 S3 bucket。
2. 上传 2-3 个小文档到 `docs/` prefix。
3. 在 Bedrock Console 创建 Knowledge Base。
4. 选择 S3 data source。
5. 选择 embedding model。
6. 选择或创建 vector store。
7. 运行 ingestion job。
8. 在 Knowledge Base Console 测试问题。
9. 检查回答和 citations。
10. 清理 Knowledge Base、vector store、S3 数据和 IAM role。

## 待学习问题

- Knowledge Base 和普通 Bedrock model invoke 有什么不同？
- Ingestion job 什么时候需要重新跑？
- S3 文档改了以后 Knowledge Base 会自动更新吗？
- Citation 返回的 source 能不能追到具体文档？
- Knowledge Base 是训练模型吗？
- Knowledge Base、fine-tuning、prompt stuffing 的区别是什么？
- 成本来自 ingestion、embedding、vector store，还是 retrieve-and-generate？
