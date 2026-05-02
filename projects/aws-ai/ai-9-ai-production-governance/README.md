# AI-9: AI 生产化、观测与治理

目标：把前面 AI-1 到 AI-8 的实验能力收束成生产化 checklist。

本目录不创建云上资源，先提供模板：

| 文件 | 作用 |
| --- | --- |
| `templates/production-checklist.md` | AI 应用上线前 checklist |
| `templates/log-schema.json` | 建议日志字段 |
| `templates/cost-control-template.md` | 成本控制和预算模板 |
| `templates/cleanup-runbook.md` | 清理和事故处理 runbook |

核心关注：

```text
IAM least privilege
input validation
guardrails
logging without sensitive content
metrics and alarms
budgets and cost attribution
CloudTrail audit
secrets and encryption
retry / timeout / failure paths
cleanup runbooks
```
