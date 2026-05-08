# 阶段 3：DynamoDB 元数据与会话

这个阶段放 DynamoDB 相关代码。第一遍先通过 Console 建表和手动写入 item，理解 key 设计；之后再用 Python 写入和查询。

计划内容：

- 创建文档元数据表：`DocAssistantDocuments`
- 保存 `document_id`、`user_id`、`s3_uri`、`status`
- 保存聊天会话记录
- 练习 Query、Scan、GSI 和 TTL

## 第一张表

```text
Table name: DocAssistantDocuments
Partition key: user_id (String)
Sort key: document_id (String)
Capacity mode: On-demand
```

先支持两个访问模式：

```text
列出某个用户的文档：
user_id = user_001

读取某个用户的某个文档：
user_id = user_001 AND document_id = doc_001
```

阶段笔记：

```text
../../notes/aws-ai-doc-assistant/03-dynamodb-metadata-sessions.md
```

## 代码练习

从本阶段目录运行：

```bash
cd /Users/xzhu/Documents/AWS/projects/aws-ai-doc-assistant/03-dynamodb-metadata-sessions
```

保存一条文档 metadata：

```bash
uv run python src/save_document_metadata.py
```

查询某个用户的全部文档：

```bash
uv run python src/get_user_documents.py user_001
```

查询某个具体文档：

```bash
uv run python src/get_document.py doc_003 --user-id user_001
```

保存聊天消息：

```bash
uv run python src/save_chat_message.py --session-id session_002 --role user --content "Summarize this document."
uv run python src/save_chat_message.py --session-id session_002 --role assistant --content "This document describes the AWS AI document assistant project."
```

查询聊天历史：

```bash
uv run python src/get_chat_history.py session_002
```

## 代码结构

```text
src/
  config.py
  dynamodb_client.py
  save_document_metadata.py
  get_user_documents.py
  get_document.py
  save_chat_message.py
  get_chat_history.py
```
