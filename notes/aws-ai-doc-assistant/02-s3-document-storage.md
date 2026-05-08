# 阶段 2：S3 文档存储

## 目标

会用 S3 保存用户上传的文档。第一遍优先通过 AWS Console 操作，理解每个设置；后面再用代码自动化上传、下载和生成临时访问链接。

## 要学习

- bucket
- object key
- upload / download
- private bucket
- presigned URL
- versioning
- encryption
- lifecycle rule

## 要实现

做一个最小功能：

> 上传一个 PDF / TXT / JSON 文件到 S3，然后生成一个临时下载链接。

第一遍操作方式：

- 优先使用 AWS Console
- 暂时不用 CLI 创建 bucket
- 先理解 bucket 名称、Region、公开访问、加密、版本控制这些选项

计划代码：

```text
projects/aws-ai-doc-assistant/
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

本阶段不把 S3 代码放在项目根目录，避免后续 DynamoDB、OpenSearch、Bedrock 阶段混在一起。

早期草案中的根目录代码结构已改为阶段目录：

```text
projects/aws-ai-doc-assistant/02-s3-document-storage/
  src/
    config.py
    s3_client.py
    upload_document.py
  data/
    sample.txt
```

## 练习任务

- 在 AWS Console 创建一个私有 bucket
- 确认 Region 是 `eu-central-1`
- 保持 Block Public Access 全部开启
- 保持 ACL disabled / Bucket owner enforced
- 确认默认加密是 SSE-S3
- 在 Console 上传一个测试文件
- 在 Console 查看文件详情
- 后续再用 Python `boto3` 上传文件
- 后续再生成 presigned URL

## Console 验证

- S3 Buckets 列表里能看到新 bucket
- bucket 的 Permissions 页面显示 Block Public Access 已开启
- bucket 的 Properties 页面显示默认加密已启用
- Objects 页面能看到上传的测试文件

## 实现记录

### 2026-05-06

- 使用 profile：`aws-learning`
- 使用 Region：`eu-central-1`
- 已确认可以列出当前账号的 S3 buckets
- 当前账号已有一个其他项目 bucket，本项目将创建独立 bucket，避免混用生产/历史资源
- 用户选择先用 AWS Console 学习 S3，不用 CLI 创建资源
- 已通过 AWS Console 创建本项目 bucket：`aws-ai-doc-assistant-xzhu-089781651608-eu-central-1-an`
- 已通过 AWS Console 上传第一个对象：`sample.txt`
- 已验证对象存在：大小 `470` bytes，类型 `text/plain`
- 已验证对象使用 SSE-S3 加密：`AES256`
- 已验证 bucket Block Public Access 全部开启
- 直接打开 Object URL 返回 `AccessDenied`，说明对象没有公开暴露，这是预期结果
- 已在 Console 创建 key 前缀结构并上传对象：`raw/user_001/sample.txt`
- Console 创建的“文件夹”会显示为 0 字节对象：`raw/`、`raw/user_001/`
- 真正的文档对象 key 是：`raw/user_001/sample.txt`
- 在对象详情页中，Tags 可以直接编辑；Metadata 通常不能像 Tags 一样原地编辑
- S3 user-defined metadata 需要在上传时设置，或通过重新上传/复制对象并替换 metadata 来更新
- 已重新上传 `raw/user_001/sample.txt` 并添加 user-defined metadata：
  - `user-id=user_001`
  - `document-type=sample`
  - `source=console-upload`
- 已验证 object tags 仍为空，说明 Tags 和 Metadata 是两套不同机制
- 已给 `raw/user_001/sample.txt` 添加 object tags：
  - `project=aws-ai-doc-assistant`
  - `stage=learning`
  - `owner=user_001`
- 已通过 AWS Console 创建 presigned URL
- 本次 presigned URL 设置了 `X-Amz-Expires=300`，也就是 5 分钟有效期
- 不在笔记中保存完整 presigned URL，因为它是临时访问凭证
- 已新增 Python S3 代码：
  - `projects/aws-ai-doc-assistant/02-s3-document-storage/src/config.py`
  - `projects/aws-ai-doc-assistant/02-s3-document-storage/src/s3_client.py`
  - `projects/aws-ai-doc-assistant/02-s3-document-storage/src/upload_document.py`
  - `projects/aws-ai-doc-assistant/02-s3-document-storage/src/create_presigned_url.py`
- 已用代码上传对象：`raw/user_001/sample-python.txt`
- 代码上传对象时自动写入 metadata、tags 和 SSE-S3 加密
- 已用代码生成 5 分钟有效的 presigned URL
- 已通过 `uv run python -m compileall src` 验证 Python 文件可编译
- 已将代码重构为按阶段存放：
  - `projects/aws-ai-doc-assistant/01-aws-foundation-security/`
  - `projects/aws-ai-doc-assistant/02-s3-document-storage/`

## 完成标准

- [x] 能解释 bucket 和 object key
- [x] 能在 Console 上传文件
- [x] 能确认 bucket 不是公开访问
- [x] 能确认对象使用默认加密
- [x] 能解释为什么 Object URL 直接访问会 `AccessDenied`
- [x] 能解释 S3 文件夹其实是 key prefix
- [x] 能给对象添加 user-defined metadata
- [x] 能区分 object tags 和 object metadata
- [x] 能给对象添加 tags
- [x] 能生成 presigned URL
- [x] 能用 Python 上传文件
- [x] 知道 S3 适合存文件，不适合当普通数据库

## 下一步

进入 [阶段 3：DynamoDB 元数据与会话](03-dynamodb-metadata-sessions.md)。
