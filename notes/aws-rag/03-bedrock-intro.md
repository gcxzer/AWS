# RAG-3：Bedrock 入门：模型调用、权限、boto3

## 学习目标

本阶段目标是跑通 Amazon Bedrock 的最小调用链路。你要理解模型调用不是“发个 prompt”这么简单，还包括模型权限、区域、请求格式、token、延迟、成本和错误处理。

完成后你应该能做到：

- 在 AWS 中启用需要的 Bedrock 模型访问权限。
- 用 boto3 调用 Bedrock Runtime。
- 分清文本生成模型和 embedding 模型的用途。
- 解释一次模型请求从客户端到 Bedrock 的基本生命周期。

## 核心理论

### 模型调用链路

一次 Bedrock 调用通常包括：

1. 客户端创建 AWS session。
2. boto3 使用当前凭证签名请求。
3. 请求发送到指定 Region 的 Bedrock Runtime。
4. Bedrock 校验 IAM 权限和模型访问权限。
5. 模型执行推理。
6. 返回结构化响应、错误或流式内容。

这个链路里任何一环出错，表现都可能只是“调用失败”。所以学习时要刻意记录 Region、model id、IAM action、请求 body 和错误信息。

### Token 和 Context

LLM 不是直接理解无限文本，而是在 context window 内处理 token。RAG 后续会把检索到的 chunk 拼进 prompt，因此 context 是稀缺资源。

工程上要关注：

- 输入 token 决定上下文容量和成本。
- 输出 token 决定回答长度、延迟和成本。
- prompt 中证据越多，不一定越好，可能稀释重点。

### 文本生成 vs Embedding

文本生成模型负责回答、总结、改写和推理。Embedding 模型负责把文本转为向量，供检索使用。

二者在 RAG 中承担不同职责：

- Embedding 影响“能不能找到对的材料”。
- 生成模型影响“能不能基于材料写出好的答案”。

### 权限模型

Bedrock 调用通常需要 IAM 权限，例如 `bedrock:InvokeModel`。同时，一些模型还需要在控制台启用 model access。权限通过不代表模型可用，模型可用也不代表权限足够。

## 关键概念

- **Bedrock Runtime**：运行模型推理的接口。
- **Model ID**：指定要调用的模型。
- **Inference Parameters**：温度、最大输出长度等模型参数。
- **Embedding Model**：把文本转换为向量表示。
- **IAM Action**：例如 `bedrock:InvokeModel`。
- **Region Availability**：不同模型在不同区域可用性不同。

## 工程取舍

- 大模型能力更强，但通常成本和延迟更高。
- 小模型更便宜更快，但复杂推理和表达可能弱。
- 高 temperature 更有创造性，但事实型问答更容易漂移。
- RAG 问答通常更偏低 temperature，以减少不必要发挥。

## 动手实验

1. 在 Bedrock 控制台确认模型访问权限。
2. 用 boto3 调用一个文本生成模型，输入一个简单问题。
3. 用 boto3 调用一个 embedding 模型，输入一段短文本并查看向量维度。
4. 记录不同参数对输出长度、稳定性和延迟的影响。
5. 故意使用错误 model id 或缺少权限的角色，观察错误信息。

## 验收标准

- 能成功运行一次 Bedrock 文本生成调用。
- 能成功运行一次 embedding 调用。
- 能解释 model id、Region、IAM 权限之间的关系。
- 能说出生成模型和 embedding 模型在 RAG 中的职责边界。

## 阶段产物

- Bedrock CLI Demo。
- 模型调用参数说明。
- 常见错误记录表，包括权限、Region、model id、请求格式。

## 复盘问题

- 为什么 RAG 需要 embedding 模型，而不只需要生成模型？
- 如果 Bedrock 报权限错误，你会从哪些地方排查？
- 什么场景需要更大模型？什么场景小模型足够？
- token 成本如何影响后续 chunk 和 top-k 设计？
