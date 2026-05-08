# 阶段 4：OpenSearch 文档检索

这个阶段放文档检索相关代码。因为 Amazon OpenSearch Service 会持续计费，先用本地 JSON 索引做无成本 dry run，理解 `index`、`document`、`chunk` 和 `query`。后续再决定是否创建 AWS OpenSearch 资源。

计划内容：

- 文档切 chunk
- 创建本地 OpenSearch-shaped index
- 写入文档片段
- 关键词检索
- 后续扩展到向量检索

阶段笔记：

```text
../../notes/aws-ai-doc-assistant/04-opensearch-document-search.md
```

## 运行

从本阶段目录运行：

```bash
cd /Users/xzhu/Documents/AWS/projects/aws-ai-doc-assistant/04-opensearch-document-search
```

把示例文档切 chunk 并写入本地索引：

```bash
uv run python src/index_document.py data/aws-ai-doc-assistant-overview.txt --document-id doc_004
```

搜索关键词：

```bash
uv run python src/search_documents.py "OpenSearch retrieval"
```

按用户过滤搜索：

```bash
uv run python src/search_documents.py "chat history" --user-id user_001
```

## 结构

```text
04-opensearch-document-search/
  README.md
  data/
    aws-ai-doc-assistant-overview.txt
    local-search-index.json
  src/
    text_chunker.py
    local_search_index.py
    index_document.py
    search_documents.py
```
