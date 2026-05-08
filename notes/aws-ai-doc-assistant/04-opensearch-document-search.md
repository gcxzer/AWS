# 阶段 4：OpenSearch 文档检索

## 目标

理解 Amazon OpenSearch Service 在文档助手 / RAG 系统里的作用，并掌握从“文档原文”到“可搜索 chunk”的完整流程。

本阶段要学会回答：

- OpenSearch 到底是干什么的？
- 为什么 S3 和 DynamoDB 不能替代 OpenSearch？
- index、document、mapping、query 分别是什么？
- 文档为什么要切 chunk？
- OpenSearch 在 RAG 里为什么叫 retrieval 层？
- 如果真的在 AWS Console 创建 OpenSearch domain，应该怎么选配置？
- 学习结束后如何清理，避免持续计费？

## 一句话理解 OpenSearch

OpenSearch 是搜索和分析引擎。

它最擅长：

```text
从大量文本、日志、文档片段里，快速找出和查询最相关的内容。
```

它不是用来存原始文件的，也不是普通业务数据库。

在本项目里，各服务分工是：

```text
S3
保存原始文件：PDF、TXT、DOCX、图片、上传原件

DynamoDB
保存业务状态：user_id、document_id、s3_uri、status、chat history

OpenSearch
保存可搜索的文档 chunk，并负责检索相关 chunk

Bedrock
根据 OpenSearch 找到的相关 chunk 生成自然语言回答
```

## 为什么需要 OpenSearch

假设用户上传了一份很长的文档：

```text
s3://bucket/raw/user_001/aws-notes.txt
```

S3 能保存文件，但它不会理解文件内容，也不适合回答：

```text
这份文档哪里提到了 DynamoDB？
哪些段落和 presigned URL 有关？
OpenSearch 在这个系统里负责什么？
```

DynamoDB 能保存 metadata，但它不是全文搜索引擎。它适合：

```text
查 user_001 的所有文档
查 doc_001 的处理状态
查 session_001 的聊天历史
```

但它不适合：

```text
在所有文档段落里搜索 "retrieval"
根据自然语言问题找相关段落
对长文本做相关性排序
```

OpenSearch 解决的就是这个问题。

## RAG 里的 Retrieval

RAG 的核心流程：

```text
用户问题
  -> 检索相关资料
  -> 把资料放进 prompt
  -> 大模型生成回答
```

OpenSearch 位于 retrieval 层：

```text
用户问：
"OpenSearch 在这个系统里干什么？"

OpenSearch 找到：
"Amazon OpenSearch Service is used for retrieval..."

Bedrock 再基于这段上下文回答。
```

这样可以减少模型胡说，因为模型不是凭记忆猜，而是基于检索到的项目文档回答。

## 核心概念

### Domain

在 Amazon OpenSearch Service 的 Managed clusters 里，domain 就是一套 OpenSearch 集群。

可以理解成：

```text
一组由 AWS 托管的 OpenSearch 服务器 + 存储 + endpoint + Dashboards
```

学习用 domain 示例：

```text
doc-assistant-dev
```

### Endpoint

OpenSearch API 地址。

代码会向这个 endpoint 发请求：

```text
PUT /document-chunks/_doc/doc_001_chunk_001
GET /document-chunks/_search
```

### OpenSearch Dashboards

浏览器里的管理和查询界面。

可以做：

- 创建 index
- 查看 documents
- 在 Dev Tools 里跑查询
- 做可视化和 dashboard

### Index

index 是一类可搜索数据的集合。

在本项目里可以建：

```text
document-chunks
```

它专门保存文档切出来的 chunk。

类比：

```text
SQL table       -> OpenSearch index
SQL row         -> OpenSearch document
SQL column      -> OpenSearch field
```

这个类比不完全等价，但适合入门。

### Document

OpenSearch 里的 document 是一条 JSON 记录。

本项目里，一个 chunk 就是一条 OpenSearch document：

```json
{
  "user_id": "user_001",
  "document_id": "doc_001",
  "chunk_id": "doc_001#chunk_0001",
  "text": "Amazon OpenSearch Service is used for retrieval...",
  "source": "aws-notes.txt",
  "s3_uri": "s3://bucket/raw/user_001/aws-notes.txt"
}
```

注意：

```text
S3 里存的是原始文件。
OpenSearch 里存的是为了搜索而切出来的 chunk。
```

### Mapping

mapping 定义字段类型。

例如：

```text
user_id      keyword
document_id  keyword
chunk_id     keyword
source       keyword
s3_uri       keyword
text         text
```

为什么 `text` 和 `keyword` 不一样？

```text
text
会被分词，适合全文搜索。

keyword
不会被分词，适合精确过滤、聚合、排序。
```

所以：

```text
text = "Amazon OpenSearch Service is used for retrieval"
```

适合搜索：

```text
OpenSearch retrieval
```

而：

```text
user_id = "user_001"
```

应该用 `keyword`，因为我们要精确过滤某个用户。

### Analyzer

analyzer 是分词器。

OpenSearch 会把长文本拆成词，建立倒排索引。

例如：

```text
"OpenSearch is used for retrieval"
```

可能被拆成：

```text
opensearch
used
retrieval
```

之后搜索 `retrieval` 就能快速找到这条 document。

### Inverted Index

倒排索引是搜索引擎的核心。

普通读法是：

```text
document -> words
```

倒排索引反过来：

```text
word -> documents
```

例如：

```text
retrieval -> chunk_0002, chunk_0017, chunk_0041
dynamodb  -> chunk_0001, chunk_0012
```

所以搜索时不用扫所有文档，而是直接通过词找到候选 documents。

### Query

query 是搜索请求。

典型查询：

```json
{
  "query": {
    "match": {
      "text": "OpenSearch retrieval"
    }
  }
}
```

如果要只查某个用户的数据：

```json
{
  "query": {
    "bool": {
      "must": [
        { "match": { "text": "OpenSearch retrieval" } }
      ],
      "filter": [
        { "term": { "user_id": "user_001" } }
      ]
    }
  }
}
```

这里的区别：

```text
match
用于全文搜索，会影响相关性得分。

filter / term
用于精确过滤，不参与相关性评分。
```

### Score

OpenSearch 查询结果里通常会有 `_score`。

它表示相关性分数：

```text
分数越高，OpenSearch 认为越相关。
```

RAG 里通常取 top 3 / top 5 chunk：

```text
top_k = 3
```

再把这些 chunk 放进 prompt。

## 为什么要切 Chunk

大模型和搜索引擎都不适合直接处理整份超长文档。

原因：

- 文档太长，超过模型上下文窗口
- 整篇文档相关性太粗，无法精准定位答案
- 搜索结果应该返回小段落，而不是整本书
- chunk 可以带 source、page、section 等引用信息

一个文件会被切成多个 chunk：

```text
doc_001
  doc_001#chunk_0001
  doc_001#chunk_0002
  doc_001#chunk_0003
```

建议第一版 chunk 策略：

```text
按段落切
每个 chunk 300-800 字左右
保留 document_id、chunk_id、source、s3_uri
```

后续优化：

- overlap：相邻 chunk 重叠一小段，避免上下文断裂
- 按标题/章节切
- PDF 保留 page number
- HTML 保留 heading path
- embedding 向量检索

## 本项目数据模型

OpenSearch index：

```text
document-chunks
```

document shape：

```json
{
  "user_id": "user_001",
  "document_id": "doc_004",
  "chunk_id": "doc_004#chunk_0002",
  "text": "Amazon OpenSearch Service is used for retrieval...",
  "source": "aws-ai-doc-assistant-overview.txt",
  "s3_uri": "s3://bucket/raw/user_001/aws-ai-doc-assistant-overview.txt",
  "token_count": 58,
  "created_at": "2026-05-06T15:00:00Z"
}
```

推荐 mapping：

```json
{
  "mappings": {
    "properties": {
      "user_id": { "type": "keyword" },
      "document_id": { "type": "keyword" },
      "chunk_id": { "type": "keyword" },
      "source": { "type": "keyword" },
      "s3_uri": { "type": "keyword" },
      "token_count": { "type": "integer" },
      "created_at": { "type": "date" },
      "text": { "type": "text" }
    }
  }
}
```

## Console 创建真实 OpenSearch Domain 流程

注意：OpenSearch domain 会持续计费。学习时建议创建、练习、截图/记录、然后删除。

入口：

```text
AWS Console
-> OpenSearch Service
-> Managed clusters
-> Domains
-> Create domain
```

### 1. Name

```text
Domain name:
doc-assistant-dev
```

domain name 是 OpenSearch 集群名，不是 index 名。

### 2. Domain Creation Method

选择：

```text
Standard create
```

原因：

```text
Easy create 会替你隐藏很多配置。
Standard create 能看到实例、存储、网络、安全这些核心概念。
```

### 3. Engine Options

选择 Console 提供的最新 OpenSearch 版本。

例如：

```text
OpenSearch_3.5
```

学习新项目可以选最新版本。

### 4. Network

有两种：

```text
VPC access
Public access
```

生产环境通常选：

```text
VPC access
```

因为它只允许 VPC 内部访问，更安全。

学习阶段为了直接打开 Dashboards，可以选：

```text
Public access
```

但必须配合：

- HTTPS
- Fine-grained access control
- Master user
- Access policy

### 5. IP Address Type

如果选 Public access，通常可以选：

```text
IPv4 only
```

如果是 VPC access，而你的 VPC/subnet 没有 IPv6，不要选 dual-stack。

截图里出现的：

```text
Dual-stack mode
```

表示 IPv4 和 IPv6 都支持。它要求 VPC/subnet 有 IPv6 配置。学习阶段不需要复杂化。

### 6. Fine-grained Access Control

开启：

```text
Enable fine-grained access control
```

它提供 OpenSearch 内部权限控制，例如：

- 谁能登录 Dashboards
- 谁能读写某个 index
- 谁是管理员
- 字段级/文档级权限

学习阶段建议：

```text
Create master user
```

不要选 IAM ARN 作为 master user，除非你熟悉 IAM role/user ARN 和访问策略。

示例：

```text
Master username:
admin

Master password:
自己设置强密码，不写进笔记
```

### 7. Deployment / Capacity

学习用最低配置即可。

建议：

```text
Deployment option:
Domain without standby

Availability Zone:
1-AZ

Data nodes:
1

Instance type:
t3.small.search 或页面中最小可选实例
```

不要为了学习开 Multi-AZ with Standby。那是生产高可用配置，成本更高。

### 8. Storage

学习用：

```text
EBS enabled:
Yes

Volume type:
gp3 或 gp2

Volume size:
10 GiB
```

### 9. Encryption

建议全部开启：

```text
Encryption at rest:
Enabled

Node-to-node encryption:
Enabled

Require HTTPS:
Enabled
```

### 10. Access Policy

如果页面有：

```text
Only use fine-grained access control
```

可以选它。

如果要求自定义 access policy，学习阶段可以先使用限制较宽但依赖 master user 的策略。生产环境不要这样做。

更安全的做法是限制到自己的 IP，但家庭/移动网络 IP 可能变化。

### 11. Logs

学习阶段可以先不开：

```text
CloudWatch logs:
Disabled
```

生产环境建议开启 slow logs、application logs、audit logs。

### 12. 创建并等待

点击：

```text
Create
```

等待：

```text
Status = Active
```

通常需要 10-20 分钟，有时更久。

创建完成后记录：

```text
Domain endpoint
Dashboards URL
```

不要在公开笔记里记录 master password。

## 在 Dashboards 里创建 Index

进入：

```text
OpenSearch Dashboards URL
```

用 master username/password 登录。

打开：

```text
Dev Tools
```

创建 index：

```json
PUT document-chunks
{
  "mappings": {
    "properties": {
      "user_id": { "type": "keyword" },
      "document_id": { "type": "keyword" },
      "chunk_id": { "type": "keyword" },
      "source": { "type": "keyword" },
      "s3_uri": { "type": "keyword" },
      "token_count": { "type": "integer" },
      "created_at": { "type": "date" },
      "text": { "type": "text" }
    }
  }
}
```

查看 index：

```json
GET document-chunks
```

## 写入第一条 Document

```json
PUT document-chunks/_doc/doc_004_chunk_0001
{
  "user_id": "user_001",
  "document_id": "doc_004",
  "chunk_id": "doc_004#chunk_0001",
  "text": "Amazon OpenSearch Service is used for retrieval. The application splits each document into smaller chunks and returns the chunks that match a user's question.",
  "source": "aws-ai-doc-assistant-overview.txt",
  "s3_uri": "s3://bucket/raw/user_001/aws-ai-doc-assistant-overview.txt",
  "token_count": 31,
  "created_at": "2026-05-06T15:00:00Z"
}
```

再写一条：

```json
PUT document-chunks/_doc/doc_004_chunk_0002
{
  "user_id": "user_001",
  "document_id": "doc_004",
  "chunk_id": "doc_004#chunk_0002",
  "text": "Amazon DynamoDB stores document metadata and chat history. The document table can list all documents for a user.",
  "source": "aws-ai-doc-assistant-overview.txt",
  "s3_uri": "s3://bucket/raw/user_001/aws-ai-doc-assistant-overview.txt",
  "token_count": 24,
  "created_at": "2026-05-06T15:01:00Z"
}
```

## 搜索

全文搜索：

```json
GET document-chunks/_search
{
  "query": {
    "match": {
      "text": "OpenSearch retrieval"
    }
  }
}
```

按用户过滤：

```json
GET document-chunks/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "text": "chat history"
          }
        }
      ],
      "filter": [
        {
          "term": {
            "user_id": "user_001"
          }
        }
      ]
    }
  }
}
```

只返回需要字段：

```json
GET document-chunks/_search
{
  "_source": ["document_id", "chunk_id", "text", "source"],
  "query": {
    "match": {
      "text": "Bedrock answers"
    }
  },
  "size": 3
}
```

这就是 RAG 里的 top-k retrieval：

```text
size = 3
```

表示取最相关的 3 个 chunk。

## 本地 Dry Run 代码

为了不依赖正在运行的 OpenSearch domain，本阶段也保留了一套本地 dry run 代码。

代码目录：

```text
projects/aws-ai-doc-assistant/04-opensearch-document-search/
```

文件：

```text
data/aws-ai-doc-assistant-overview.txt
src/text_chunker.py
src/local_search_index.py
src/index_document.py
src/search_documents.py
```

运行：

```bash
cd projects/aws-ai-doc-assistant/04-opensearch-document-search
uv run python src/index_document.py data/aws-ai-doc-assistant-overview.txt --document-id doc_004
uv run python src/search_documents.py "OpenSearch retrieval"
```

本地 index 文件：

```text
data/local-search-index.json
```

它模拟 OpenSearch index 里的 documents：

```json
{
  "user_id": "user_001",
  "document_id": "doc_004",
  "chunk_id": "doc_004#chunk_0002",
  "text": "Amazon OpenSearch Service is used for retrieval...",
  "source": "aws-ai-doc-assistant-overview.txt",
  "s3_uri": null,
  "token_count": 58
}
```

本地 dry run 和真实 OpenSearch 的对应关系：

```text
local-search-index.json      -> OpenSearch index
JSON list item               -> OpenSearch document
text 字段                    -> text field
user_id/document_id/chunk_id -> keyword fields
search_documents.py          -> _search query
score                        -> _score
```

## 和前面阶段如何串起来

完整流程：

```text
S3:
保存原始文件 raw/user_001/sample.txt

DynamoDB:
保存文档 metadata
document_id = doc_001
s3_uri = s3://...
status = uploaded

OpenSearch:
读取原文
切成 chunk
写入 document-chunks index
每个 chunk 都带 user_id/document_id/source/s3_uri

Bedrock:
用户提问
先从 OpenSearch 找 top-k chunk
再把 chunk 放进 prompt 生成答案
```

## 成本注意

OpenSearch domain 是长时间运行资源。

主要成本来源：

- data node 实例小时
- EBS 存储
- Multi-AZ / standby 节点
- 数据传输
- CloudWatch logs

OpenSearch Serverless 主要成本来源：

- OCU
- 存储
- 数据传输

学习建议：

```text
创建前确认预算提醒
只创建最小配置
练习完成后删除 domain
不要长期闲置
```

## 清理流程

Console 删除：

```text
OpenSearch Service
-> Managed clusters
-> Domains
-> doc-assistant-dev
-> Delete
```

删除前确认：

```text
domain name = doc-assistant-dev
不是生产 domain
不是 TopicFollow 资源
```

删除后检查：

```text
Domains 列表里没有 doc-assistant-dev
```

如果使用 Serverless collection，也要删除：

- collection
- data access policy
- network policy
- encryption policy

## 实现记录

### 2026-05-06

- 已确认阶段 4 的目标是学习真实 OpenSearch 文档检索
- 已说明 Amazon OpenSearch Service 可能持续计费
- 已记录 Console 创建 Managed domain 的完整流程
- 已记录 OpenSearch domain、endpoint、Dashboards、index、document、mapping、query、score 等核心概念
- 已记录 RAG 中 OpenSearch 作为 retrieval 层的职责
- 已记录真实 Dashboards Dev Tools 中创建 index、写入 document、执行 search query 的示例
- 已保留无成本本地 dry run 代码：
  - `projects/aws-ai-doc-assistant/04-opensearch-document-search/src/text_chunker.py`
  - `projects/aws-ai-doc-assistant/04-opensearch-document-search/src/local_search_index.py`
  - `projects/aws-ai-doc-assistant/04-opensearch-document-search/src/index_document.py`
  - `projects/aws-ai-doc-assistant/04-opensearch-document-search/src/search_documents.py`
- 已新增示例文档：
  - `projects/aws-ai-doc-assistant/04-opensearch-document-search/data/aws-ai-doc-assistant-overview.txt`
- 已通过 `uv run python -m compileall src` 验证 Python 文件可编译
- 已索引示例文档为 3 个 chunk：
  - `doc_004#chunk_0001`
  - `doc_004#chunk_0002`
  - `doc_004#chunk_0003`
- 已验证关键词搜索：
  - `OpenSearch retrieval` 命中 `doc_004#chunk_0002`
  - `chat history` 命中 `doc_004#chunk_0001` 和 `doc_004#chunk_0003`
- 本轮最终清理时确认没有创建同名前缀的 OpenSearch domain 或 OpenSearch Serverless collection

## 完成标准

- [x] 能解释 OpenSearch 是搜索和分析引擎
- [x] 能解释 S3、DynamoDB、OpenSearch、Bedrock 的分工
- [x] 能解释 OpenSearch 在 RAG 中负责 retrieval
- [x] 能解释 domain、endpoint、Dashboards
- [x] 能解释 index 和 document
- [x] 能解释 mapping、text、keyword
- [x] 能解释为什么要切 chunk
- [x] 能写入文档 chunk
- [x] 能按关键词搜索
- [x] 能按 `user_id` 过滤搜索结果
- [x] 能说明 Console 创建 OpenSearch domain 的关键配置
- [x] 能说明 OpenSearch 资源的成本风险和清理流程

## 下一步

进入 [阶段 5：Bedrock 模型调用](05-bedrock-model-inference.md)。

阶段 5 会把 retrieval 结果交给模型：

```text
OpenSearch 找相关 chunk
Bedrock 根据 chunk 生成回答
```

## 参考资料

- [Amazon OpenSearch Service Developer Guide](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html)
- [Creating and managing Amazon OpenSearch Service domains](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/createupdatedomains.html)
- [Fine-grained access control in Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html)
- [Indexing data in Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/indexing.html)
- [Amazon OpenSearch Service pricing](https://aws.amazon.com/opensearch-service/pricing/)
