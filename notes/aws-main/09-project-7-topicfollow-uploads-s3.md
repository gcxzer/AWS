# 项目 7：TopicFollow 图片/上传文件迁移到 S3

目标：把 TopicFollow 的 uploads 从单台服务器本地磁盘迁到 S3，让图片和用户上传文件不再依赖 EC2/Hetzner 的某个目录。这个项目先做 staging 方案和验证，不直接切 production。

## 当前状态

项目 6 已经验证过 TopicFollow 可以在 AWS staging 跑通：

```text
Browser
  -> EC2 Nginx
  -> Next.js
  -> RDS PostgreSQL
  -> EC2 local uploads
```

项目 6 结束时，AWS staging 资源已删除，Hetzner production 没有修改。

项目 7 当前收口状态：

```text
S3 bucket 曾创建并同步 uploads，现已删除
IAM policy / EC2 role / ECS task role 曾通过 Console 手动创建，现已删除
TopicFollow 代码已支持 local / s3 两种 uploads backend
跳过重新创建 EC2 staging 验证
项目 10 正式迁移时重新创建全新的 production AWS 资源
```

生产 uploads 当前事实：

| 项目 | 当前值 |
| --- | --- |
| Hetzner uploads 目录 | `/var/lib/topicfollow/uploads` |
| 文件数量 | `71` |
| 文件大小 | `8.3M` |
| 当前文件类型 | topic hero images，均为 `webp` |
| 当前路径形状 | `/uploads/topics/topic-<slug>/hero.webp` |
| 数据库引用 | `topics.hero_image` 有 `71` 条 `/uploads/...` |
| 额外 metadata | `topics.hero_image_download_url` 有 `18` 条 `/uploads/...` |

2026-05-03 实际重新从 Hetzner 同步 uploads 时，本地同步目录和 S3 均观察到 `73` 个对象，总大小 `8420936` bytes。相比 2026-05-01 的 `71` 个文件，多出的对象应来自生产期间新增 topic hero images；这说明项目 7 后续需要支持最终 cutover 前的最后一次增量 sync。

## 为什么要迁到 S3

本地磁盘适合单机，但不适合云上可迁移架构：

| 本地 uploads | S3 uploads |
| --- | --- |
| 绑在某台服务器上 | 独立于 EC2/ECS |
| 服务器删了文件就没了 | 对象存储持久保存 |
| 多台服务器之间难同步 | 所有应用实例读写同一个 bucket |
| 容器重启或换节点会丢本地文件 | 容器无状态更容易 |

## 当前代码入口

当前上传写入集中在：

```text
src/lib/storage/blob.ts
```

当前行为：

```text
uploadPublicBlob(pathname, file)
  -> writeLocalUpload(pathname, file)
  -> /var/lib/topicfollow/uploads/<pathname>
  -> 返回 /uploads/<pathname>
```

当前公开读取路径：

```text
src/app/uploads/[...path]/route.ts
```

当前行为：

```text
GET /uploads/topics/topic-example/hero.webp
  -> readFile(/var/lib/topicfollow/uploads/topics/topic-example/hero.webp)
  -> Response(image/webp)
```

调用方：

| 功能 | key/path 形状 | 代码入口 |
| --- | --- | --- |
| Topic hero image | `topics/<topic-slug>/hero.webp` | `src/app/account/content/actions.ts` |
| Avatar | `avatars/<user-id>-<random>.<ext>` | `src/lib/account/avatar-storage.ts` |
| Feedback attachment | `feedback/<user-id>-<random>.<ext>` | `src/lib/contact/feedback-attachments.ts` |

## 目标架构

项目 7 staging 目标：

```text
Browser
  -> /uploads/... legacy path
  -> Next.js compatibility route
  -> S3 object

New upload
  -> Next.js server action
  -> S3 PutObject
  -> database stores stable /uploads/... path
```

后续 production 目标可以再加 CloudFront：

```text
Browser
  -> CloudFront
  -> private S3 bucket
```

项目 7 先不强行上 CloudFront，先把 S3 storage adapter 跑通。CloudFront + OAC 可以作为第二阶段。

## S3 key 结构

推荐保持和旧路径兼容：

| 旧 public URL | S3 object key |
| --- | --- |
| `/uploads/topics/topic-example/hero.webp` | `uploads/topics/topic-example/hero.webp` |
| `/uploads/avatars/user-abc.webp` | `uploads/avatars/user-abc.webp` |
| `/uploads/feedback/file.webp` | `uploads/feedback/file.webp` |

这样 `/uploads/...` route 可以直接映射到 S3 key：

```text
/uploads/<path>
  -> s3://<bucket>/uploads/<path>
```

## 环境变量草案

| 变量 | 用途 |
| --- | --- |
| `UPLOADS_STORAGE_BACKEND` | `local` 或 `s3` |
| `UPLOADS_STORAGE_DIR` | local backend 使用 |
| `UPLOADS_S3_BUCKET` | S3 bucket 名 |
| `UPLOADS_S3_REGION` | S3 region，例如 `eu-central-1` |
| `UPLOADS_S3_PREFIX` | 推荐 `uploads` |
| `UPLOADS_PUBLIC_BASE_URL` | 可选；有 CloudFront 后填 CDN 域名 |

项目 7 staging 可以先让数据库继续保存 `/uploads/...`，这样旧 URL 不需要批量改库。

## 实施顺序

1. 创建私有 S3 bucket，开启 block public access。已创建：`topicfollow-uploads-20260503-089781651608-eu-central-1-an`。
2. 上传 Hetzner uploads 到 S3 staging bucket。已同步到 `s3://topicfollow-uploads-20260503-089781651608-eu-central-1-an/uploads/`。
3. 对比文件数量和抽样对象。已观察到 `Total Objects: 73`、`Total Size: 8420936`。
4. 创建最小权限 IAM policy 和运行角色。已通过 Console 手动创建 policy、EC2 role、ECS task role。
5. 在代码里加 storage adapter：local 和 s3。已在本地 TopicFollow 代码中实现；默认仍为 `local`。
6. `/uploads/[...path]` route 在 S3 backend 时读取 S3。已实现并本地验证。
7. 新上传 topic hero / avatar / feedback attachment 写入 S3。写入入口继续复用 `uploadPublicBlob()`；需要在 staging app 上进一步验证实际上传表单。
8. 本地测试已完成；重新创建 EC2 staging 测试已跳过，后续正式部署时再做。
9. 设计 CloudFront + OAC 公开读取方式。
10. 已清理项目 7 staging S3 bucket 和 IAM role/policy；项目 10 正式迁移时重新创建全新资源。

## 验收标准

- S3 里对象数量和 Hetzner uploads 文件数量一致。
- 旧 `/uploads/topics/.../hero.webp` 路径仍能访问。
- 新上传 topic hero image 后，S3 出现新 object。
- 应用不再依赖 EC2 本地 `/var/lib/topicfollow/uploads`。
- S3 bucket 不公开写入，不把长期 access key 写进代码。

## 清理结果

项目 7 staging AWS 资源已清理：

- CloudFront distribution：未创建。
- S3 bucket `topicfollow-uploads-20260503-089781651608-eu-central-1-an`：已清空并删除。
- IAM role `TopicFollowStagingEc2Role`：已删除。
- IAM role `TopicFollowStagingEcsTaskRole`：已删除。
- IAM policy `TopicFollowStagingUploadsS3Access`：已删除。
- 长期 access key：未创建。
- EC2/RDS/ECS：项目 7 未创建新的运行资源。

## 曾创建资源

| 资源 | 名称 | 用途 |
| --- | --- | --- |
| S3 bucket | `topicfollow-uploads-20260503-089781651608-eu-central-1-an` | Project 7 staging uploads bucket，已删除 |
| IAM policy | `TopicFollowStagingUploadsS3Access` | 手动创建；允许读写 staging bucket 的 `uploads/*`，已删除 |
| EC2 role | `TopicFollowStagingEc2Role` | 手动创建；trusted service 是 `ec2.amazonaws.com`，已删除 |
| ECS task role | `TopicFollowStagingEcsTaskRole` | 手动创建；trusted service 是 `ecs-tasks.amazonaws.com`，已删除 |

验证结果：

| 检查 | 结果 |
| --- | --- |
| Region | `eu-central-1` |
| Block Public Access | `BlockPublicAcls=true`, `IgnorePublicAcls=true`, `BlockPublicPolicy=true`, `RestrictPublicBuckets=true` |
| Default encryption | `SSE-S3` / `AES256`, bucket key enabled |
| Sample object | `uploads/topics/topic-2026-bulgarian-presidential-election/hero.webp` |
| Sample content type | `image/webp` |
| Sample size | `106276` bytes |

IAM 手动创建记录：

| 检查 | 目标状态 |
| --- | --- |
| IAM policy | 只允许 `s3:ListBucket`, `s3:GetBucketLocation`, `s3:GetObject`, `s3:PutObject`, `s3:DeleteObject` |
| Policy 范围 | bucket `topicfollow-uploads-20260503-089781651608-eu-central-1-an` 的 `uploads/` prefix |
| EC2 role | attach `TopicFollowStagingUploadsS3Access` |
| ECS task role | attach `TopicFollowStagingUploadsS3Access` |
| Access key | 不创建长期 access key |

本地代码验证：

| 检查 | 结果 |
| --- | --- |
| 新依赖 | `@aws-sdk/client-s3` |
| 默认行为 | `UPLOADS_STORAGE_BACKEND` 未设置时继续使用 local uploads |
| `npm run build` | 通过 |
| 临时本地服务 | `UPLOADS_STORAGE_BACKEND=s3`，端口 `3005` |
| S3 route 测试 | `GET /uploads/topics/topic-2026-bulgarian-presidential-election/hero.webp` 返回 `200 OK` |
| 返回类型 | `image/webp` |
| 返回大小 | `106276` bytes，和 S3 object 一致 |
| 临时服务 | 已停止 |

## 撤销记录和当前结论

2026-05-03 曾通过 CLI 自动创建 IAM policy、EC2 role、EC2 instance profile、ECS task role。因为学习节奏需要改回 Console 手动操作，这批自动创建的 IAM 资源已删除；随后 IAM policy、EC2 role、ECS task role 已由你在 AWS Console 手动重新创建。

| 项目 | 状态 |
| --- | --- |
| CLI 自动创建的 IAM policy `TopicFollowStagingUploadsS3Access` | 已删除 |
| Console 手动创建的 IAM policy `TopicFollowStagingUploadsS3Access` | 已删除 |
| CLI 自动创建的 EC2 role `TopicFollowStagingEc2Role` | 已删除 |
| Console 手动创建的 EC2 role `TopicFollowStagingEc2Role` | 已删除 |
| EC2 instance profile `TopicFollowStagingEc2InstanceProfile` | 已删除 |
| CLI 自动创建的 ECS task role `TopicFollowStagingEcsTaskRole` | 已删除 |
| Console 手动创建的 ECS task role `TopicFollowStagingEcsTaskRole` | 已删除 |
| 本地 TopicFollow S3 adapter 代码改动 | 当前保留，后续部署时通过环境变量启用 |
