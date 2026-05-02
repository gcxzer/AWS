# CloudTrail 基础概念

CloudTrail 可以理解成 AWS 的审计记录系统。它记录 AWS account 里发生的控制面操作，例如谁登录了 Console、谁创建了用户、谁分配了权限、谁创建或删除了资源。

CloudTrail 主要回答这些问题：

- 谁做了这个操作？
- 什么时间做的？
- 从哪个 IP 或入口做的？
- 用的是 root、SSO role、IAM user，还是 AWS service？
- 对哪个 AWS service 或资源做了什么？

CloudTrail 不是应用日志。它记录的是 AWS 账号和服务 API 层面的操作。以后如果 Lambda 代码运行报错，那类运行日志通常在 CloudWatch Logs 里看。

## Event history / Ereignisverlauf

Event history 是 CloudTrail 自动提供的最近 90 天管理事件记录。新 AWS account 默认就可以查看，不需要先创建 trail。

在德语界面里叫：

```text
Ereignisverlauf
```

它适合项目 1 阶段使用，因为我们现在只需要确认 AWS 正在记录账号活动。

当前已经看到的事件包括：

- `ConsoleLogin`：登录 AWS Console。
- `GetSigninToken`：登录流程获取 token。
- `Federate`：通过 IAM Identity Center / SSO 联合登录。
- `CreateAccountAssignment`：给 group/user 分配 AWS account 和 permission set。

查看事件详情时重点看：

- `Ereignisname`：事件名。
- `Ereigniszeit`：发生时间。
- `Benutzername`：谁触发的。
- `Ereignisquelle`：事件来自哪个 AWS service。
- `Quell-IP-Adresse`：来源 IP。
- `User agent`：通过浏览器、CLI、SDK 或 AWS 内部服务触发。

## Trail / Pfad

Trail 是一种长期保存 CloudTrail 事件的配置。创建 trail 后，CloudTrail 可以持续把事件日志投递到指定的 S3 bucket，也可以选择发送到 CloudWatch Logs 或 EventBridge。

Trail 适合这些场景：

- 需要保存超过 90 天的审计日志。
- 公司或合规要求保留操作证据。
- 想把日志集中到 S3 后做长期分析。
- 想将关键操作发送到 CloudWatch Logs 或 EventBridge 做告警和自动化。

学习项目 1 阶段暂时不创建 trail，因为它会引入额外资源，例如 S3 bucket、日志存储、CloudWatch Logs，可能带来额外费用和清理负担。

## Insights

CloudTrail Insights 用于发现异常 API 活动，例如某个 API 调用量突然变高，或者错误率突然异常。

它适合更成熟的安全监控场景。学习阶段暂时不启用，因为它不是项目 1 的必要内容，而且可能产生额外费用。

## CloudTrail Lake

CloudTrail Lake 是更高级的审计日志分析服务。它把事件放入 event data store，然后可以用 SQL 查询大量审计日志。

可以把它理解成：

```text
CloudTrail Lake = 用来查询审计日志的数据湖
```

相关菜单：

- `Lake > Dashboards`：Lake 的分析看板。
- `Lake > Abfrage`：查询 Lake 数据。
- `Lake > Ereignisdatenspeicher`：event data store，Lake 里的事件存储库。
- `Lake > Integrationen`：接入外部或非 AWS 事件源。

当前不使用 CloudTrail Lake。页面顶部提示 CloudTrail Lake 将从 2026-05-31 开始不再向新客户开放，所以这条学习路线不依赖它。以后如果需要类似长期查询能力，可以优先考虑 S3 + Athena、CloudWatch 或其他日志分析方案。

## 当前学习结论

项目 1 只需要掌握：

```text
Event history = AWS 自动提供的最近 90 天账号操作记录
Trail = 把 CloudTrail 日志长期投递到 S3 / CloudWatch Logs
Lake = 用 SQL 查询审计日志的数据湖，高级功能，暂时跳过
```

当前已完成：

- 找到 CloudTrail `Ereignisverlauf`。
- 看到了 `ConsoleLogin`、`Federate`、`GetSigninToken` 等登录相关事件。
- 看到了 `CreateAccountAssignment` 等权限分配相关事件。
- 确认 CloudTrail 正在记录账号活动。
