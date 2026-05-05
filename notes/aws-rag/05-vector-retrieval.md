# RAG-5：向量检索核心：Embedding、OpenSearch、pgvector

## 学习目标

本阶段目标是理解 RAG 检索层的核心原理。你不需要推导复杂数学，但要知道 embedding、相似度、top-k、metadata、ANN/HNSW 如何影响最终答案。

完成后你应该能解释：

- 为什么语义检索需要 embedding。
- chunk size 和 top-k 为什么会影响召回和噪声。
- metadata filter 如何缩小检索范围。
- 什么时候需要 OpenSearch、pgvector 或其他向量库。

## 核心理论

### Embedding 表示

Embedding 是把文本映射到高维向量空间。语义接近的文本在向量空间中距离更近，因此可以用向量相似度找到“意思相关”的片段。

它解决的是关键词检索难以处理的问题，例如同义词、改写、自然语言问题和文档表达不一致。但 embedding 也会失败，例如数字、代码、专有名词、表格细节和强结构化条件。

### 相似度和 Top-k

检索通常会返回最相关的前 k 个 chunk。top-k 太小，可能漏掉关键证据；top-k 太大，可能把噪声塞进 prompt，导致模型分心或误答。

工程上要把 top-k 当作可调参数，而不是固定真理。它需要结合文档类型、chunk 大小、问题复杂度和 context window 一起调。

### Chunk Size

chunk 是 RAG 检索的基本单位。chunk 太小，语义不完整；chunk 太大，检索不精准，还会浪费 token。

常见策略包括：

- 按固定 token 或字符数切分。
- 按标题、段落、章节结构切分。
- 使用 overlap 保留上下文连续性。
- 为 chunk 附加 metadata，例如文档名、章节、日期、权限标签。

### ANN 与 HNSW

当向量数量很大时，精确搜索成本高，通常会使用近似最近邻搜索。HNSW 是常见 ANN 算法之一，用图结构提升检索速度。

学习阶段重点理解取舍：ANN 提升速度，但可能牺牲少量召回；索引参数会影响构建时间、查询延迟、内存和质量。

## 关键概念

- **Vector Similarity**：向量相似度，例如 cosine similarity。
- **Top-k**：返回前 k 个相关结果。
- **Recall**：应该找到的内容是否被找到了。
- **Precision**：找到的内容里有多少真的相关。
- **Metadata Filter**：按文档属性过滤检索范围。
- **Hybrid Search**：结合关键词检索和向量检索。
- **OpenSearch**：常用于搜索和向量检索的服务。
- **pgvector**：PostgreSQL 中的向量检索扩展。

## 工程取舍

- 纯向量检索适合语义问题，但可能漏掉精确关键词。
- 关键词检索适合精确匹配，但不擅长语义改写。
- hybrid search 更稳，但系统复杂度更高。
- metadata filter 可以提升精准度，但依赖高质量元数据。
- 向量库选择要考虑规模、成本、运维、延迟和 AWS 集成。

## 动手实验

1. 准备一批文档，按不同 chunk size 切分。
2. 对同一批问题分别测试不同 top-k。
3. 为文档添加 metadata，例如文档类型、部门、年份。
4. 对比不使用 metadata filter 和使用 filter 的结果。
5. 记录哪些问题适合向量检索，哪些更适合关键词或结构化查询。

## 验收标准

- 能解释 embedding 检索和关键词检索的差异。
- 能说明 chunk size 太大或太小的后果。
- 能用实验记录证明 top-k 会影响答案质量。
- 能设计一套基础 metadata 字段。

## 阶段产物

- 检索实验表。
- chunk 策略对比记录。
- metadata 设计草案。
- 向量库选型对比说明。

## 复盘问题

- 为什么“语义相近”不一定代表“答案正确”？
- top-k 增大后，答案一定会更好吗？
- 哪些字段适合作为 metadata？
- 什么情况下应该用 hybrid search？
