# AWS CLI 与 SSO

AWS CLI 是本机终端里的 AWS 命令行工具。它可以用 `aws ...` 命令访问 AWS 服务。

当前安装状态：

```bash
aws --version
```

输出显示已安装 AWS CLI v2：

```text
aws-cli/2.34.40
```

## 为什么 CLI 也使用 SSO

CLI 可以通过多种方式登录 AWS。学习阶段优先使用 IAM Identity Center / SSO，而不是创建长期 access key。

这样做的好处：

- 终端拿到的是临时凭证。
- 不需要把长期 access key 保存在电脑里。
- Console 和 CLI 使用同一套日常身份体系。
- 可以在 CloudTrail 里看到 CLI 和 Console 的身份来源。

## 当前 CLI profile

已创建 CLI profile：

```text
aws-learning
```

对应关系：

```text
SSO session: aws-learning
SSO region: eu-central-1
AWS account: xzhu
Permission set / role: AdministratorAccess
User: xzhu-admin
Default region: eu-central-1
Output format: json
```

验证命令：

```bash
aws sts get-caller-identity --profile aws-learning
```

验证结果说明：

- `Account`：当前 CLI 访问的是这个 AWS account。
- `Arn` 里出现 `assumed-role/AWSReservedSSO_AdministratorAccess.../xzhu-admin`，说明 CLI 使用的是 IAM Identity Center 分配出来的临时 role。
- `xzhu-admin` 表示当前调用者是日常管理员身份，不是 root。

这说明项目 1 的 CLI 验收项已经通过。

## 12 小时过期后怎么办

12 小时过后，配置不会丢，只是这次 SSO 临时登录凭证过期。

CLI 重新登录：

```bash
aws sso login --profile aws-learning
```

然后验证：

```bash
aws sts get-caller-identity --profile aws-learning
```

Console 重新登录：

```text
AWS access portal
  -> xzhu account
  -> AdministratorAccess
```

## AWS CLI 命令结构

AWS CLI 命令通常长这样：

```bash
aws <service> <operation> [options]
```

拆开看：

- `aws`：调用 AWS CLI 这个命令行工具。
- `<service>`：要操作的 AWS 服务，例如 `sts`、`s3`、`cloudtrail`、`budgets`。
- `<operation>`：要对这个服务执行的动作，例如 `get-caller-identity`、`ls`、`sync`。
- `[options]`：额外参数，例如 `--profile aws-learning`、`--region eu-central-1`。

例子：

```bash
aws sts get-caller-identity --profile aws-learning
```

意思是：

```text
aws                     使用 AWS CLI
sts                     调用 AWS STS 服务
get-caller-identity     查询当前调用者身份
--profile aws-learning  使用名为 aws-learning 的 CLI 配置
```

## 常见 AWS CLI 单词

| 单词 | 含义 |
| --- | --- |
| `aws` | AWS CLI 主命令 |
| `profile` | CLI 里的身份配置别名 |
| `region` | AWS 区域，例如 `eu-central-1` |
| `sts` | Security Token Service，负责临时身份和身份查询 |
| `s3` | Amazon S3，对象存储服务 |
| `cloudtrail` | 审计记录服务 |
| `iam` | Identity and Access Management，账号内权限系统 |
| `sso` | Single Sign-On，通过 IAM Identity Center 登录 |
| `configure` | 配置 CLI |
| `login` | 登录并获取临时凭证 |
| `ls` | list，列出资源 |
| `sync` | 同步本地目录和 S3 路径 |
| `cp` | copy，复制文件 |
| `rm` | remove，删除 |
| `get` | 获取单个信息 |
| `list` | 列出多个资源 |
| `describe` | 查看资源详细信息 |
| `create` | 创建资源 |
| `delete` | 删除资源 |
| `lookup` | 查询/查找历史记录 |
| `caller` | 当前发起 AWS API 调用的身份 |
| `identity` | 身份 |

## 常用 AWS CLI 命令

查看 AWS CLI 版本：

```bash
aws --version
```

查看当前机器上配置了哪些 profile：

```bash
aws configure list-profiles
```

使用 SSO 登录当前 profile：

```bash
aws sso login --profile aws-learning
```

查看当前 CLI 身份：

```bash
aws sts get-caller-identity --profile aws-learning
```

列出 S3 bucket：

```bash
aws s3 ls --profile aws-learning
```

把本地目录同步到 S3：

```bash
aws s3 sync ./site s3://bucket-name --profile aws-learning
```

从 CloudTrail 查询最近事件：

```bash
aws cloudtrail lookup-events --profile aws-learning
```

指定 region 运行命令：

```bash
aws s3 ls --region eu-central-1 --profile aws-learning
```

## CLI 使用习惯

学习阶段建议每条命令都显式带上：

```bash
--profile aws-learning
```

这样可以避免误用其他 AWS 身份。

在创建或删除资源前，先运行：

```bash
aws sts get-caller-identity --profile aws-learning
```

确认自己正在操作正确的 AWS account。
