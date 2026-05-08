# 阶段 5：Bedrock 模型调用

这个阶段放 Bedrock 模型调用相关内容。当前先以学习笔记为主，代码后续可按笔记中的结构补齐。

计划内容：

- 调用 Bedrock 模型
- 组织 prompt
- 记录输入输出
- 处理模型调用错误

阶段笔记：

```text
../../notes/aws-ai-doc-assistant/05-bedrock-model-inference.md
```

## 建议代码结构

```text
05-bedrock-model-inference/
  README.md
  data/
    sample_context.txt
  src/
    config.py
    bedrock_client.py
    ask_bedrock.py
    answer_with_context.py
```

## 推荐 API

阶段 5 优先学习：

```text
Converse API
```

原因：

- 统一消息格式
- 适合对话和 RAG 问答
- 更容易在不同模型之间切换

低层 API：

```text
InvokeModel
```

适合需要直接使用模型特定请求格式的场景。
