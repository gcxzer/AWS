# 阶段 6：RAG 流程整合

这个阶段放端到端 RAG 整合相关内容。当前先以架构和流程笔记为主，代码后续可按笔记中的结构补齐。

计划内容：

- 上传文档
- 切分文档
- 检索相关 chunk
- 拼接上下文
- 调用 Bedrock 生成答案
- 保存问答记录

阶段笔记：

```text
../../notes/aws-ai-doc-assistant/06-rag-pipeline-integration.md
```

## 建议代码结构

```text
06-rag-pipeline-integration/
  README.md
  data/
    sample.txt
  src/
    config.py
    s3_store.py
    dynamodb_store.py
    search_store.py
    bedrock_llm.py
    text_extractor.py
    text_chunker.py
    prompt_builder.py
    upload_document.py
    index_document.py
    ask_question.py
```

## 两条主流程

```text
Ingestion pipeline:
upload -> S3 -> DynamoDB metadata -> chunk -> OpenSearch -> status=indexed

Query pipeline:
question -> OpenSearch retrieval -> Bedrock answer -> DynamoDB chat history
```
