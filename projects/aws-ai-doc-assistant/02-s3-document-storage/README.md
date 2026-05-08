# 阶段 2：S3 文档存储

这一阶段实现 S3 的最小代码闭环：

- 上传文件到私有 bucket
- 写入 user-defined metadata
- 写入 object tags
- 使用 SSE-S3 加密
- 生成短时间有效的 presigned URL

## 当前配置

```text
profile: aws-learning
region: eu-central-1
bucket: aws-ai-doc-assistant-xzhu-089781651608-eu-central-1-an
```

## 运行

从本阶段目录运行：

```bash
cd /Users/xzhu/Documents/AWS/projects/aws-ai-doc-assistant/02-s3-document-storage
```

上传文件：

```bash
uv run python src/upload_document.py data/sample.txt --key raw/user_001/sample-python.txt
```

生成 5 分钟有效的 presigned URL：

```bash
uv run python src/create_presigned_url.py raw/user_001/sample-python.txt --expires-in 300
```

检查 Python 文件能编译：

```bash
uv run python -m compileall src
```

不要把 presigned URL 长期保存到笔记或代码里。它是临时访问凭证，过期前拿到链接的人可以读取对应对象。

## 结构

```text
02-s3-document-storage/
  README.md
  data/
    sample.txt
  src/
    config.py
    s3_client.py
    upload_document.py
    create_presigned_url.py
```
