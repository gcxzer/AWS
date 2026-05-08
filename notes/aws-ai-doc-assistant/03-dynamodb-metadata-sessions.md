# 阶段 3：DynamoDB 元数据与会话

## 目标

用 DynamoDB 保存文档元数据和聊天记录。S3 负责保存文件本身，DynamoDB 负责保存可查询、可更新的业务状态。

## 要学习

- table
- item
- partition key
- sort key
- query vs scan
- GSI
- TTL
- on-demand capacity

## 要实现

第一步先做文档元数据表：

```text
DocAssistantDocuments
- partition key: user_id
- sort key: document_id
- title
- s3_bucket
- s3_key
- s3_uri
- status
- uploaded_at
```

这个 key 设计支持最重要的访问模式：

```text
查询某个用户的所有文档：
user_id = user_001

查询某个用户的某个文档：
user_id = user_001 AND document_id = doc_001
```

第二步再做聊天记录表：

```text
DocAssistantChatMessages
- partition key: session_id
- sort key: created_at
- user_id
- document_id
- role
- content
```

这个 key 设计支持：

```text
查询一个 session 下的所有聊天消息：
session_id = session_001
```

设计原因：

```text
session_id 把同一次对话的消息放在一起
created_at 让同一 session 内的消息按时间排序
```

计划代码：

```text
projects/aws-ai-doc-assistant/
  03-dynamodb-metadata-sessions/
    README.md
    src/
      config.py
      dynamodb_client.py
      save_document_metadata.py
      get_user_documents.py
      save_chat_message.py
```

## 练习任务

- 在 Console 创建 `DocAssistantDocuments` 表
- 插入一条文档记录
- 根据 `user_id` 查询某个用户的文档
- 根据 `user_id + document_id` 查询某个文档
- 在 Console 创建 `DocAssistantChatMessages` 表
- 存一条聊天记录
- 给临时数据加 TTL

## Console 验证

- Tables 列表中能看到 `DocAssistantDocuments`
- 表的 partition key 是 `user_id`
- 表的 sort key 是 `document_id`
- Capacity mode 使用 On-demand
- 能手动创建一条 item
- 能通过 Explore table items 查询 `user_id=user_001`

后续 Python 版本：

```bash
cd projects/aws-ai-doc-assistant/03-dynamodb-metadata-sessions
uv run python src/save_document_metadata.py
uv run python src/get_user_documents.py user_001
```

## 实现记录

### 2026-05-06

- 当前 Region：`eu-central-1`
- 当前 profile：`aws-learning`
- 已确认当前 Region 还没有 DynamoDB tables
- 阶段 3 从 Console 创建 `DocAssistantDocuments` 表开始
- 已创建表：`DocAssistantDocuments`
- 表状态：`ACTIVE`
- Key schema：`user_id` 为 partition key，`document_id` 为 sort key
- Billing mode：`PAY_PER_REQUEST`，也就是 On-demand
- 已通过 Console 创建第一条文档 metadata item：
  - `user_id=user_001`
  - `document_id=doc_001`
  - `title=sample.txt`
  - `s3_key=raw/user_001/sample.txt`
  - `status=uploaded`
- 已验证 Query 访问模式：`user_id=user_001` 返回 1 条文档记录
- 已通过 Console 创建第二条文档 metadata item：
  - `user_id=user_001`
  - `document_id=doc_002`
  - `title=sample-python.txt`
  - `s3_key=raw/user_001/sample-python.txt`
  - `status=uploaded`
- 已验证 Query 访问模式：`user_id=user_001` 返回 2 条文档记录：`doc_001`、`doc_002`
- 已验证精准 Query 访问模式：`user_id=user_001 AND document_id=doc_002` 返回 1 条文档记录
- 已新增 Python DynamoDB 代码：
  - `projects/aws-ai-doc-assistant/03-dynamodb-metadata-sessions/src/config.py`
  - `projects/aws-ai-doc-assistant/03-dynamodb-metadata-sessions/src/dynamodb_client.py`
  - `projects/aws-ai-doc-assistant/03-dynamodb-metadata-sessions/src/save_document_metadata.py`
  - `projects/aws-ai-doc-assistant/03-dynamodb-metadata-sessions/src/get_user_documents.py`
  - `projects/aws-ai-doc-assistant/03-dynamodb-metadata-sessions/src/get_document.py`
- 已通过代码写入第三条文档 metadata item：
  - `user_id=user_001`
  - `document_id=doc_003`
  - `title=sample-python-2.txt`
  - `s3_key=raw/user_001/sample-python-2.txt`
  - `status=uploaded`
- 已通过代码查询 `user_id=user_001`，返回 3 条文档记录
- 已通过代码精准读取 `doc_003`
- 已通过 `uv run python -m compileall src` 验证 Python 文件可编译
- 已创建表：`DocAssistantChatMessages`
- 表状态：`ACTIVE`
- Key schema：`session_id` 为 partition key，`created_at` 为 sort key
- Billing mode：`PAY_PER_REQUEST`，也就是 On-demand
- 已写入 `session_001` 的两条样例聊天消息：
  - `2026-05-06T15:20:00Z`，`role=user`
  - `2026-05-06T15:20:05Z`，`role=assistant`
- 已验证 Query 访问模式：`session_id=session_001` 返回完整聊天历史，并按 `created_at` 排序
- 已新增 Python 聊天记录代码：
  - `projects/aws-ai-doc-assistant/03-dynamodb-metadata-sessions/src/save_chat_message.py`
  - `projects/aws-ai-doc-assistant/03-dynamodb-metadata-sessions/src/get_chat_history.py`
- 已通过代码写入 `session_002` 的两条样例聊天消息：
  - `role=user`，`content=Summarize this document.`
  - `role=assistant`，`content=This document describes the AWS AI document assistant project.`
- 已通过代码查询 `session_002`，返回完整聊天历史，并按 `created_at` 排序
- 已再次通过 `uv run python -m compileall src` 验证 Python 文件可编译

## 完成标准

- [x] 能解释 partition key 和 sort key
- [x] 能解释 query 和 scan 的区别
- [x] 能保存文档元数据
- [x] 能保存聊天记录
- [x] 能根据访问模式解释 DynamoDB 表设计

## 下一步

进入 [阶段 4：OpenSearch 文档检索](04-opensearch-document-search.md)。
