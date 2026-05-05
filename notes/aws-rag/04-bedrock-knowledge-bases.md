# RAG-4：托管式 RAG：Bedrock Knowledge Bases

## 学习目标

本阶段目标是使用 Amazon Bedrock Knowledge Bases 跑通托管式 RAG。你要理解它帮你托管了哪些环节，也要知道哪些环节仍然需要你设计、测试和负责。

完成后你应该能解释：

- 文档如何从 S3 进入 Knowledge Base。
- ingestion、parser、chunking、embedding、vector store 的职责。
- Retrieve 和 RetrieveAndGenerate 的差异。
- citation 如何产生，以及为什么仍要验证可信度。

## 核心理论

### 托管式 RAG 架构

Bedrock Knowledge Bases 把 RAG 的多段流程托管起来：连接数据源、解析文档、切分 chunk、生成 embedding、写入向量库、执行检索，并可直接结合生成模型返回带引用的答案。

托管式方案的价值是降低工程复杂度，让你先把业务问题跑通。但托管不等于不用设计，尤其是文档质量、chunk 策略、metadata、测试集和权限边界仍然需要你掌握。

### Ingestion

Ingestion 是把原始文档变成可检索知识的过程，通常包括：

1. 读取数据源中的文档。
2. 解析文档内容。
3. 按策略切分为 chunk。
4. 用 embedding 模型生成向量。
5. 写入向量存储。

当答案质量不好时，问题可能出现在 ingestion 的任意环节，而不是只出在生成模型。

### Retrieve vs RetrieveAndGenerate

`Retrieve` 只负责取回相关 chunk。它适合调试检索质量，观察系统到底找到了哪些证据。

`RetrieveAndGenerate` 会先检索，再调用模型生成自然语言回答，并返回引用。它适合构建最终问答体验。

工程上建议先调好 Retrieve，再看 RetrieveAndGenerate。否则很容易把“检索错了”和“生成写坏了”混在一起。

### Citation

Citation 是企业问答中非常关键的可信度机制。它让用户看到答案依据来自哪里。但 citation 必须被验证：

- 引用是否真的支持答案。
- 引用是否覆盖回答中的关键事实。
- 是否存在回答正确但引用不充分。
- 是否存在引用正确但模型额外编造。

## 关键概念

- **Knowledge Base**：托管知识库。
- **Data Source**：例如 S3 bucket 或 prefix。
- **Ingestion Job**：同步和处理文档的任务。
- **Parser**：把文档格式解析成文本或结构化内容。
- **Chunking Strategy**：切分文档的策略。
- **Vector Store**：存放 embedding 的向量数据库。
- **Retrieve**：只检索相关材料。
- **RetrieveAndGenerate**：检索并生成答案。

## 工程取舍

- 托管式 RAG 更快落地，但底层可控性较弱。
- 自建 pipeline 更灵活，但需要自己维护解析、索引、检索和评估。
- Retrieve 调试成本低，适合定位问题。
- RetrieveAndGenerate 用户体验完整，但更难拆分错误来源。

## 动手实验

1. 准备一组测试文档并上传到 S3。
2. 创建 Bedrock Knowledge Base，连接 S3 数据源。
3. 选择 embedding 模型和向量存储方案。
4. 运行 ingestion job，确认文档同步完成。
5. 使用 Retrieve 测试 10 个问题，记录返回 chunk。
6. 使用 RetrieveAndGenerate 测试同一批问题，记录答案和 citation。

## 验收标准

- 能完成文档 ingestion。
- 能用 Retrieve 查看命中的 chunk。
- 能用 RetrieveAndGenerate 生成带 citation 的答案。
- 能指出至少 3 个影响 Knowledge Base 答案质量的因素。

## 阶段产物

- 第一个托管式企业文档问答 Demo。
- Knowledge Base 架构图。
- 10 个问题的检索结果和回答记录。
- Citation 可信度检查表。

## 复盘问题

- 如果 Retrieve 没找到正确 chunk，可能是什么原因？
- 如果 Retrieve 找对了，但答案仍然错，可能是什么原因？
- 托管 Knowledge Base 替你解决了什么？没有替你解决什么？
- 哪些指标能说明 ingestion 是成功的？
