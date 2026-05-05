# RAG-6：自定义 RAG Pipeline：解析、切分、检索、生成

## 学习目标

本阶段目标是从零实现一个最小可用 RAG pipeline。不是为了替代 Bedrock Knowledge Bases，而是为了理解托管服务背后发生了什么，并在需要更强可控性时知道如何设计。

完成后你应该能说明：

- RAG pipeline 每个组件的输入和输出。
- 文档解析、切分、embedding、检索、生成之间如何衔接。
- 自定义 pipeline 比托管方案多了哪些责任。
- 为什么要把 retrieval 和 generation 解耦调试。

## 核心理论

### Pipeline 思维

RAG 不是一个单点功能，而是一条数据和请求链路。典型 pipeline 分为离线和在线两部分：

- **离线部分**：文档解析、清洗、切分、embedding、入库。
- **在线部分**：query 处理、检索、rerank、prompt 组装、模型生成、引用返回。

把链路拆开，才能定位质量问题来自哪里。

### 文档解析

文档解析决定知识能否进入系统。PDF、HTML、Markdown、CSV、Office 文档的结构差异很大。解析质量差会造成标题丢失、表格错乱、页眉页脚噪声和段落顺序错误。

工程上要记录原始文档、解析文本和 chunk 之间的映射关系，否则后续 citation 很难可信。

### 切分策略

切分不是简单截断。好的 chunk 应该语义完整、长度适中、可追溯来源，并尽量保留标题层级。

常见设计：

- 保留文档标题、章节标题作为上下文。
- 控制 chunk token 长度。
- 使用 overlap 防止跨段信息断裂。
- 为每个 chunk 保存 source、page、section、offset 等元数据。

### Prompt Assembly

Prompt assembly 是把问题、系统指令、检索证据和回答格式要求组合起来。RAG prompt 应该明确要求模型：

- 只基于提供的资料回答。
- 证据不足时说无法判断。
- 给出引用来源。
- 不要把常识或猜测伪装成文档事实。

## 关键概念

- **Loader**：读取不同格式文档。
- **Parser**：抽取文本和结构。
- **Splitter**：切分 chunk。
- **Embedder**：生成向量。
- **Vector Index**：保存并查询向量。
- **Retriever**：返回相关 chunk。
- **Prompt Builder**：组装模型输入。
- **Answer Generator**：调用模型生成回答。

## 工程取舍

- 自定义 pipeline 灵活，但维护成本高。
- 托管方案省心，但调参和底层控制有限。
- 解析越精细，质量可能越好，但开发成本更高。
- prompt 约束越强，幻觉更少，但回答可能更保守。

## 动手实验

实现一个最小 pipeline：

1. 从本地或 S3 读取 Markdown/TXT/PDF 文档。
2. 把文档切成 chunk，并保存 source metadata。
3. 调用 embedding 模型生成向量。
4. 使用本地向量索引或轻量数据库做相似度检索。
5. 把 top-k chunk 拼入 prompt。
6. 调用 Bedrock 生成答案。
7. 返回答案和引用来源。

## 验收标准

- 能跑通完整 query -> retrieve -> generate 流程。
- 能单独打印检索到的 chunk。
- 能比较自定义 pipeline 与 Knowledge Bases 在同一问题上的差异。
- 能说明自定义 pipeline 的新增维护责任。

## 阶段产物

- 自定义 RAG Demo。
- pipeline 架构图。
- 与 Bedrock Knowledge Bases 的对比表。
- prompt 模板和 chunk metadata 示例。

## 复盘问题

- 自定义 pipeline 中最容易出错的是哪一环？
- 为什么要先看检索结果，再看生成答案？
- 如果 citation 要精确到页码，需要在解析阶段保存什么信息？
- 哪些需求会迫使你从托管方案转向自定义方案？
