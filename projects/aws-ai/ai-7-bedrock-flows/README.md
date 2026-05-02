# AI-7: Bedrock Flows / 可视化 AI 工作流

目标：学习用 Amazon Bedrock Flows 把输入、Prompt、模型和输出节点连接成一个可视化 AI workflow。

最小 flow：

```text
Flow input
  -> Prompt node
  -> Flow output
```

## 文件

| 文件 | 作用 |
| --- | --- |
| `events/minimal-topic-input.json` | 最小 Flow 测试输入 |

## 推荐资源

| 资源 | 建议名称 |
| --- | --- |
| Flow | `ai-7-topic-summary-flow` |
| Prompt node | `SummarizeTopic` |
| Alias | `ai7-dev` |
| Model | `amazon.nova-micro-v1:0` 或 Console 支持的低成本文本模型 |

## 最小测试输入

```json
{
  "topic": "Bedrock Agents and Lambda tools",
  "audience": "an engineer learning AWS AI"
}
```

Prompt node 可以写：

```text
Summarize {{topic}} for {{audience}} in three concise bullet points.
```

输入映射：

| Prompt variable | Expression |
| --- | --- |
| `topic` | `$.data.topic` |
| `audience` | `$.data.audience` |

## 清理

1. 删除 Flow alias，例如 `ai7-dev`。
2. 删除 Flow versions。
3. 删除 Flow `ai-7-topic-summary-flow`。
4. 删除自动创建的 service role，如果不再使用。

本地代码和笔记保留。
