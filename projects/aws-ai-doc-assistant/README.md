# AWS AI 文档助手

这个目录只放实际代码。实现过程、学习笔记和踩坑记录按阶段放在：

```text
../../notes/aws-ai-doc-assistant/00-index.md
```

## 目标

做一个命令行版 AWS AI 文档助手：

1. 文档上传到 S3
2. 文档元数据保存到 DynamoDB
3. 文档内容切分后写入 OpenSearch
4. 用户提问时从 OpenSearch 检索相关段落
5. 使用 Bedrock 生成回答
6. 后续升级为 Bedrock AgentCore 工具调用流程

## 阶段结构

```text
projects/aws-ai-doc-assistant/
  README.md
  01-aws-foundation-security/
  02-s3-document-storage/
  03-dynamodb-metadata-sessions/
  04-opensearch-document-search/
  05-bedrock-model-inference/
  06-rag-pipeline-integration/
  07-bedrock-agentcore-agent/
  08-production-cost-interview/
```

每个阶段目录只放该阶段相关代码、样例数据和 README。阶段笔记放在：

```text
../../notes/aws-ai-doc-assistant/
```

## 当前阶段

当前正在做：

```text
02-s3-document-storage/
```

## 阶段 1：AWS 基础、安全与 CLI

主要通过 Console 和只读命令完成，不放业务代码。

验证身份：

```bash
aws sts get-caller-identity --profile aws-learning --region eu-central-1
```

## 阶段 2：S3 代码练习

进入阶段目录：

```bash
cd /Users/xzhu/Documents/AWS/projects/aws-ai-doc-assistant/02-s3-document-storage
```

当前 S3 代码使用：

```text
profile: aws-learning
region: eu-central-1
bucket: aws-ai-doc-assistant-xzhu-089781651608-eu-central-1-an
```

上传文件，并写入 metadata 和 tags：

```bash
uv run python src/upload_document.py data/sample.txt --key raw/user_001/sample-python.txt
```

生成 5 分钟有效的 presigned URL：

```bash
uv run python src/create_presigned_url.py raw/user_001/sample-python.txt --expires-in 300
```

不要把 presigned URL 长期保存到笔记或代码里。它是临时访问凭证，过期前拿到链接的人可以读取对应对象。
