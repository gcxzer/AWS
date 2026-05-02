# AI-12：VS Code、Domain、IAM 与 S3

## 目标

把 SageMaker 的开发入口改成本地 VS Code，而不是 Studio JupyterLab。

本节完成的是“本地控制 SageMaker 的前置环境”：

```text
Local VS Code
  -> aws-learning profile
  -> boto3 / SageMaker SDK
  -> SageMaker control plane
  -> ai-12-sagemaker-execution-role
  -> S3 artifact bucket
```

## 核心概念

| 概念 | 作用 |
| --- | --- |
| Local VS Code | 主开发入口，写 Python 脚本和项目代码 |
| `aws-learning` profile | 本地调用 AWS API 的身份 |
| SageMaker Domain | Studio 工作区、用户和权限边界 |
| User profile | Domain 里的 Studio 用户身份 |
| Execution role | SageMaker job 运行时使用的 IAM role |
| S3 artifact bucket | 保存数据、脚本、模型和输出 |

## 已创建资源

```text
AWS account: 089781651608
Region: eu-central-1

SageMaker Domain:
- Name: QuickSetupDomain-20260502T200989
- Domain ID: d-051tv5vtrxwt
- Status: InService
- URL: https://d-051tv5vtrxwt.studio.eu-central-1.sagemaker.aws

User profile:
- Name: default-20260502T200989
- Status: InService

Execution role:
- arn:aws:iam::089781651608:role/ai-12-sagemaker-execution-role

S3 bucket:
- aws-ai-sagemaker-learning-089781651608-eu-central-1-an
```

## 本地项目

目录：

```text
projects/aws-ai/ai-12-vscode-sagemaker-setup/
```

文件：

| 文件 | 作用 |
| --- | --- |
| `config.json` | 固定 profile、region、role、bucket、prefix |
| `check_environment.py` | 只读检查本地 AWS 身份、role、bucket、Domain |
| `init_s3_layout.py` | 初始化 AI-12 的 S3 prefix 目录 |

## 本地配置

```json
{
  "profile": "aws-learning",
  "region": "eu-central-1",
  "account_id": "089781651608",
  "sagemaker_role_arn": "arn:aws:iam::089781651608:role/ai-12-sagemaker-execution-role",
  "bucket": "aws-ai-sagemaker-learning-089781651608-eu-central-1-an",
  "prefix": "sagemaker/ai-12"
}
```

## 验证结果

本地 AWS 身份验证：

```bash
aws sts get-caller-identity --profile aws-learning
```

结果：

```text
Account: 089781651608
Arn: arn:aws:sts::089781651608:assumed-role/AWSReservedSSO_AdministratorAccess_ee585859764b112d/xzhu-admin
```

SageMaker Domain 验证：

```bash
aws sagemaker list-domains \
  --region eu-central-1 \
  --profile aws-learning
```

结果：

```text
d-051tv5vtrxwt  QuickSetupDomain-20260502T200989  InService
```

本地环境脚本验证：

```bash
uv run python projects/aws-ai/ai-12-vscode-sagemaker-setup/check_environment.py
```

结果确认：

```text
Local AWS identity: OK
SageMaker execution role: OK
S3 artifact location: OK
SageMaker domains: OK
```

## S3 目录结构

初始化命令：

```bash
uv run python projects/aws-ai/ai-12-vscode-sagemaker-setup/init_s3_layout.py
```

已创建：

```text
s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-12/raw/.keep
s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-12/processed/.keep
s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-12/scripts/.keep
s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-12/models/.keep
s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-12/output/.keep
```

验证命令：

```bash
aws s3 ls s3://aws-ai-sagemaker-learning-089781651608-eu-central-1-an/sagemaker/ai-12/ \
  --recursive \
  --profile aws-learning
```

## 费用状态

当前确认：

```text
Running instances: 0
未创建 JupyterLab space
未创建 endpoint
未创建 training job
未创建 processing job
```

注意：

```text
S3 .keep 对象几乎没有费用压力。
真正需要警惕的是 Endpoint、Studio app / space、notebook instance、GPU instance。
```

## AI-12 结论

AI-12 不继续使用 Studio JupyterLab。后续默认路线：

```text
本地 VS Code 写脚本
  -> 上传脚本 / 数据到 S3
  -> 创建 SageMaker Processing / Training / Batch Transform
  -> 查看 CloudWatch Logs
  -> 清理临时输出
```

下一节进入 `AI-13：Processing Jobs`。
