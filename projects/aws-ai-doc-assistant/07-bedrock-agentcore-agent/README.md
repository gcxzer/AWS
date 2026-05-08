# 阶段 7：Bedrock AgentCore Agent

这个阶段放 AgentCore 和工具调用相关内容。当前先以完整学习笔记为主，代码后续可按笔记中的结构补齐。

计划内容：

- 搜索文档工具
- 查询文档元数据工具
- 查询聊天历史工具
- 保存回答工具
- Agent 调用链路观察

阶段笔记：

```text
../../notes/aws-ai-doc-assistant/07-bedrock-agentcore-agent.md
```

## 建议代码结构

```text
07-bedrock-agentcore-agent/
  README.md
  src/
    config.py
    agent.py
    prompts.py
    tools/
      search_documents_tool.py
      list_user_documents_tool.py
      get_document_metadata_tool.py
      get_chat_history_tool.py
      save_chat_message_tool.py
      create_presigned_download_url_tool.py
    gateway/
      openapi.yaml
      tool_schemas.json
    observability/
      logging_config.py
      tracing.py
```

## 最小实现路线

```text
1. 本地 agent + 本地 tools
2. 给 tools 定义清晰 schema
3. 用 AgentCore Gateway 暴露 tools
4. 接 AgentCore Memory
5. 部署到 AgentCore Runtime
6. 接 AgentCore Identity
7. 打开 AgentCore Observability
```
