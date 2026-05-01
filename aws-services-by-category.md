# AWS 服务分类速查表

目标：按 AWS Console 的 category 梳理服务，帮助快速分辨每个服务“是什么、适合做什么、和相近服务有什么区别”。

当前整理范围：`Datenverarbeitung / Compute / 计算`、`Container / 容器`、`Speicherung / Storage / 存储`、`Datenbank / Database / 数据库`、`Migration & Transfer / 迁移与传输`、`Netzwerk & Bereitstellung von Inhalten / Networking & Content Delivery / 网络与内容分发`、`Entwicklertools / Developer Tools / 开发者工具`、`Kundenaktivierung / Customer Enablement / 客户赋能`、`Blockchain / 区块链`、`Satelliten / Satellite / 卫星`、`Quantum Technologies / 量子技术`、`Management & Governance / 管理与治理`、`Media Services / 媒体服务`、`Machine Learning / 机器学习`、`Analysen / Analytics / 分析`、`Sicherheit, Identität & Compliance / Security, Identity & Compliance / 安全、身份与合规`、`Cloud-Finanzverwaltung / Cloud Financial Management / 云财务管理`、`Mobil / Mobile / 移动`、`Anwendungsintegration / Application Integration / 应用集成`、`Geschäftsanwendungen / Business Applications / 业务应用`、`Endbenutzer-Datenverarbeitung / End User Computing / 终端用户计算`、`Internet of Things / IoT / 物联网`、`Spieleentwicklung / Game Development / 游戏开发`。

重要性标记：`P0 核心必学` = 学 AWS 必须先掌握；`P1 常用优先` = 项目里很常见，建议早学；`P2 进阶架构` = 有一定基础后再学；`P3 专项场景` = 特定行业/企业/迁移/科研场景；`P4 存量/谨慎` = 新项目要谨慎，通常因为访问限制、停止支持或更适合存量系统。

Console 入口：https://eu-central-1.console.aws.amazon.com/console/services?region=eu-central-1

## 术语约定：Image、Picture、Graph 不要混用

| 英文词 | 本文中文名 | 在 AWS 里的意思 | 不要混淆成 |
| --- | --- | --- | --- |
| Image | 镜像 | 服务器镜像 AMI、容器镜像 Docker/OCI image，用来复制运行环境 | 图片、照片、图表 |
| Picture / Photo | 图片/照片文件 | 存在 S3 里的普通图片文件，例如 `.jpg`、`.png` | AMI 镜像、容器镜像 |
| Graph | 图数据/关系图/图数据库 | 节点和边组成的数据关系模型，例如 Neptune、知识图谱 | 图片、镜像 |
| Diagram / Chart | 架构图/图表 | 用来展示结构、流程或指标的可视化图 | 图数据库、镜像 |

## 常见云计算和 AWS 缩写

| 名词/缩写 | 中文理解 | 一句话解释 | 在本文里常见于 |
| --- | --- | --- | --- |
| SaaS | 软件即服务 | Software as a Service，用户直接使用厂商提供的软件，不用自己部署服务器和应用，例如企业邮箱、CRM、在线 BI | AWS Marketplace、AppFabric、AppFlow、Amazon Quick |
| PaaS | 平台即服务 | Platform as a Service，云厂商托管运行平台，你主要交付代码或应用配置 | Elastic Beanstalk、App Runner、Amplify |
| IaaS | 基础设施即服务 | Infrastructure as a Service，云厂商提供虚拟机、网络、磁盘等基础资源，你负责较多系统运维 | EC2、VPC、EBS |
| Serverless | 无服务器 | 不是没有服务器，而是你不用管理服务器；按请求、事件或用量运行和计费 | Lambda、Fargate、Athena、Glue、Step Functions |
| Managed service | 托管服务 | AWS 帮你管理底层服务器、补丁、扩缩容或高可用，你专注使用服务能力 | RDS、EKS、OpenSearch Service、Amazon MQ、MSK |
| CI/CD | 持续集成/持续交付或部署 | Continuous Integration / Continuous Delivery or Deployment，把代码自动构建、测试、发布 | CodeBuild、CodePipeline、CodeDeploy、Amplify Hosting |
| API | 应用程序接口 | 程序之间调用功能或交换数据的接口，例如 REST、GraphQL、SDK 调用 | API Gateway、AppSync、Amazon Connect、Bedrock |
| SDK | 软件开发工具包 | 某种语言里的 AWS 调用库，让代码能调用 AWS API | Chime SDK、Amazon Q、各类 AWS SDK |
| CLI | 命令行工具 | 在终端里用命令操作 AWS 资源，常见是 `aws` CLI | CloudShell、IAM、S3、EC2 |
| IaC | 基础设施即代码 | Infrastructure as Code，用代码定义云资源，便于版本管理、复用和自动部署 | CloudFormation、CDK、Infrastructure Composer |
| IAM | 身份与访问管理 | 控制谁可以对哪些 AWS 资源做什么操作 | IAM、IAM Identity Center、RAM、KMS |
| Role | 角色 | 一种可被服务、用户或账号临时扮演的身份，常用于跨账号访问和服务权限 | Lambda role、EC2 instance profile、跨账号访问 |
| Policy | 权限策略 | 用 JSON 规则描述允许或拒绝哪些操作、资源和条件 | IAM、KMS、S3 bucket policy |
| SSO | 单点登录 | Single Sign-On，一次登录后访问多个账号或应用 | IAM Identity Center、企业身份源 |
| RBAC | 基于角色的访问控制 | Role-Based Access Control，按“管理员、开发者、只读用户”等角色授权 | EKS、Verified Permissions、企业应用权限 |
| ABAC | 基于属性的访问控制 | Attribute-Based Access Control，按标签、部门、环境、租户等属性动态授权 | IAM tag、Verified Permissions |
| VPC | 虚拟私有云网络 | 你在 AWS 里的私有网络边界，包含子网、路由、安全组等 | VPC、EC2、RDS、EKS |
| Subnet | 子网 | VPC 中某个 AZ 里的 IP 地址范围，可分公有/私有子网 | VPC、EC2、RDS、EKS |
| Security Group | 安全组 | 实例/网卡级别的虚拟防火墙，控制入站和出站流量 | EC2、RDS、ECS、EKS |
| CDN | 内容分发网络 | 把静态资源、视频、API 响应缓存到离用户近的边缘节点，提高速度和可用性 | CloudFront、Media Services |
| DNS | 域名解析系统 | 把域名解析成 IP 或其他记录，让用户能通过域名访问服务 | Route 53、Global Resolver |
| TLS/SSL | 传输加密协议 | HTTPS 背后的加密协议，用证书保护浏览器和服务之间的通信 | Certificate Manager、CloudFront、ALB、API Gateway |
| ETL | 抽取、转换、加载 | Extract, Transform, Load，先取数据、清洗转换，再写入目标数据湖/数仓 | Glue、DataBrew、EMR、AppFlow |
| ELT | 抽取、加载、转换 | Extract, Load, Transform，先把原始数据放入数仓/数据湖，再在目标系统里转换 | Redshift、Athena、Lake Formation |
| Data lake | 数据湖 | 把原始或半结构化数据集中存储，通常以 S3 为底座 | S3、Glue Data Catalog、Lake Formation、Athena |
| Data warehouse | 数据仓库 | 为结构化分析和 BI 优化的数据库/分析平台 | Redshift、QuickSight/Quick |
| BI | 商业智能 | 报表、仪表盘、指标分析和自助分析 | QuickSight / Amazon Quick |
| Pub/Sub | 发布订阅 | 发布者把消息发到主题，多个订阅者各自接收 | SNS、AppSync Events、EventBridge |
| Queue | 队列 | 消息先进先出或近似有序排队，消费者慢慢处理，用于解耦和削峰 | SQS、Amazon MQ |
| Event-driven | 事件驱动 | 系统发生事件后自动触发后续动作，而不是一直轮询 | EventBridge、Lambda、Step Functions |

## Category: Datenverarbeitung / Compute / 计算

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P0 核心必学 | EC2 | 弹性云服务器，也就是可租用的虚拟机 | 运行 Web 服务、后台程序、数据库、中间件、批处理程序等 | 需要完全控制操作系统、网络、软件安装、实例规格时 | 最灵活、最底层；你负责更多运维，例如补丁、扩缩容、监控和安全配置 |
| P2 进阶架构 | Lightsail | 简化版 VPS 云服务器套餐 | 快速部署个人网站、WordPress、小型应用、开发测试环境 | 想用固定月费、简单控制台、少配置的服务器时 | 比 EC2 更容易上手，但可定制性和企业级网络能力弱一些 |
| P0 核心必学 | Lambda | 无服务器函数计算 | 运行事件触发的小段代码，例如处理上传文件、API 请求、定时任务 | 代码短、请求波动大、不想管理服务器时 | 不需要管理实例；按调用和运行时间计费；不适合长时间常驻进程 |
| P2 进阶架构 | Batch | 托管批处理作业调度服务 | 执行大量离线任务，例如数据处理、渲染、科学计算、队列作业 | 有很多任务需要排队、并行执行、自动分配算力时 | 关注“作业队列和调度”；底层可使用 EC2、Spot 或 Fargate |
| P2 进阶架构 | Elastic Beanstalk | 应用部署和托管平台 | 部署 Web 应用/API，并自动创建 EC2、负载均衡、Auto Scaling 等资源 | 想部署应用，但不想手动拼装一堆基础设施时 | 比 EC2 更自动化；比 Lambda/App Runner 更接近传统应用部署模式 |
| P3 专项场景 | Serverless Application Repository | 无服务器应用模板仓库 | 查找、发布、复用 Lambda 相关的 serverless 应用 | 想快速使用别人封装好的 serverless 组件或模板时 | 它不是运行环境，而是 serverless 应用的仓库和分发入口 |
| P3 专项场景 | AWS Outposts | 把 AWS 基础设施放到本地机房 | 在本地运行 AWS 风格的计算、存储和网络资源 | 有低延迟、本地数据驻留、混合云要求时 | 不是普通云上服务；硬件部署在你的数据中心，但由 AWS 管理 |
| P2 进阶架构 | EC2 Image Builder | 自动化构建机器镜像（Image） | 创建、测试、分发 AMI（服务器镜像）或容器镜像 | 需要标准化服务器镜像、定期打补丁、统一基础环境时 | 这里的 Image 是“可启动/可运行环境的镜像”，不是图片，也不是图数据库 |
| P1 常用优先 | AWS App Runner | 托管容器/Web 应用运行服务 | 从源代码或容器镜像（Image）快速运行 Web 服务/API | 想部署容器化 Web 应用，但不想管理 ECS、负载均衡和扩缩容细节时 | 比 ECS 更简单；比 Elastic Beanstalk 更偏现代容器和托管运行 |
| P3 专项场景 | AWS Parallel Computing Service | 托管高性能并行计算集群服务 | 使用 Slurm 运行 HPC 工作负载，例如科学仿真、工程建模、大规模并行任务 | 需要 HPC 集群、队列、计算节点组和高性能存储集成时 | 比 Batch 更偏传统 HPC/Slurm 集群体验；Batch 更通用批处理 |
| P2 进阶架构 | AWS Global View | 跨 Region 资源查看和搜索视图 | 在一个控制台查看多个 Region 的 EC2、VPC 等资源摘要 | 想检查账号里不同 Region 有哪些资源时 | 它是只读视图，不负责创建、修改或运行计算资源 |

### Compute 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要一台可完全控制的云服务器 | EC2 |
| 我要最简单地搭一个小网站或 WordPress | Lightsail |
| 我要运行事件触发的小函数 | Lambda |
| 我要跑大量离线任务或批处理队列 | Batch |
| 我要部署传统 Web 应用，但少管基础设施 | Elastic Beanstalk |
| 我要复用别人做好的 serverless 应用模板 | Serverless Application Repository |
| 我要把 AWS 能力放到本地机房 | AWS Outposts |
| 我要标准化 AMI/镜像（Image）构建流程 | EC2 Image Builder |
| 我要快速部署容器化 Web 服务/API | AWS App Runner |
| 我要跑 Slurm/HPC 并行计算集群 | AWS Parallel Computing Service |
| 我要跨 Region 查看资源分布 | AWS Global View |

### Compute 学习顺序建议

1. 先学 `EC2`：理解实例、AMI、EBS、安全组、Key Pair、VPC 子网。
2. 再学 `Lambda`：理解 serverless、事件触发、IAM Role、CloudWatch Logs。
3. 然后比较 `Elastic Beanstalk`、`App Runner`、`Lightsail`：它们都是为了减少部署复杂度，但抽象层不同。
4. 有批处理需求时学 `Batch`；有科研/工程 HPC 需求时学 `AWS Parallel Computing Service`。
5. 最后看 `Outposts`、`EC2 Image Builder`、`AWS Global View` 这类更偏基础设施治理和运维的服务。

## Category: Container / 容器

容器服务主要解决三件事：`容器镜像（Image）放哪里`、`容器怎么调度运行`、`是否需要 Kubernetes/OpenShift 生态`。

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P1 常用优先 | Amazon ECS | AWS 原生容器编排服务 | 运行和扩展容器化应用，管理 task、service、cluster | 想运行容器，但不想直接管理 Kubernetes 复杂度时 | 比 EKS 简单，深度集成 AWS；容器调度模型是 AWS 自己的 ECS task/service |
| P1 常用优先 | Amazon EKS | 托管 Kubernetes 服务 | 在 AWS 上运行 Kubernetes 集群和容器化应用 | 团队已经使用 Kubernetes，或需要 Kubernetes 生态、Helm、Operator、标准 API 时 | 比 ECS 更标准、更开放，但学习和运维复杂度更高 |
| P3 专项场景 | Red Hat OpenShift Service on AWS | AWS 上的托管 OpenShift | 运行 Red Hat OpenShift/Kubernetes 应用平台 | 企业已经采用 OpenShift、需要 Red Hat 支持和 OpenShift 开发生态时 | 底层仍基于 Kubernetes，但体验、工具链和企业治理更偏 Red Hat OpenShift |
| P0 核心必学 | Amazon ECR | 容器镜像仓库（Image Registry） | 存储、扫描、管理和分发 Docker/OCI 容器镜像 | 你已经把应用打包成可运行的容器镜像，需要一个私有镜像仓库时 | 这里的镜像是 container image，不是图片文件；ECS/EKS/ROSA 负责运行或编排容器 |

### Container 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要简单地在 AWS 上运行容器 | Amazon ECS |
| 我要使用标准 Kubernetes | Amazon EKS |
| 我要使用企业级 OpenShift 平台 | Red Hat OpenShift Service on AWS |
| 我要保存和分发容器镜像（Image） | Amazon ECR |

### Container 学习顺序建议

1. 先理解 `Docker image（容器镜像）`、`container`、`registry`、`cluster`、`task/pod` 这些基础概念。
2. 学 `Amazon ECR`：理解 repository、image tag、镜像扫描、权限。这里的 image tag 是“镜像标签”，不是图片标签。
3. 学 `Amazon ECS + AWS Fargate`：这是 AWS 容器入门最顺的一条路。
4. 再学 `Amazon EKS`：理解 Kubernetes 的 pod、deployment、service、ingress、node group。
5. 最后看 `Red Hat OpenShift Service on AWS`：它更偏企业级 OpenShift 平台场景。

备注：`AWS Fargate` 经常和 `ECS/EKS` 一起出现，它是无服务器容器运行引擎，但不在你这张 Container category 截图的服务列表里，所以这里不把它作为单独服务行。

## Category: Speicherung / Storage / 存储

存储服务主要先分清三类：`对象存储`、`文件存储`、`备份/灾备/混合云存储`。

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P0 核心必学 | Amazon S3 | 对象存储服务 | 存储任意数量的文件/对象，例如图片/照片文件、日志、备份、数据湖、静态网站文件 | 需要便宜、耐用、可无限扩展的通用存储时 | S3 里的图片通常是普通文件，不是 AMI/container image 这种“镜像” |
| P1 常用优先 | Amazon EFS | 弹性共享文件系统 | 给 EC2、ECS、EKS、Lambda 等挂载共享 NFS 文件系统 | 多台 Linux 服务器或容器需要同时读写同一套文件时 | EFS 是文件存储，像共享网盘；S3 是对象存储，不适合直接当 POSIX 文件系统 |
| P2 进阶架构 | Amazon FSx | 托管高性能/企业文件系统 | 使用托管的 Windows File Server、Lustre、NetApp ONTAP、OpenZFS 等文件系统 | 需要特定文件系统能力，例如 SMB、HPC 高性能、NetApp 兼容、OpenZFS 特性时 | 比 EFS 更“专用”；EFS 偏通用 NFS，FSx 偏特定企业或高性能文件系统 |
| P1 常用优先 | Amazon S3 Glacier | S3 的低成本归档存储类别 | 长期保存很少访问的数据，例如合规归档、历史日志、长期备份 | 数据要保存很多年，但不常读取，并且可以接受较慢恢复时 | 属于 S3 生态的归档层；比 S3 Standard 便宜，但有最短存储期和恢复时间/费用差异 |
| P3 专项场景 | AWS Storage Gateway | 本地机房连接 AWS 存储的网关 | 让本地应用通过文件、卷或磁带接口使用云存储 | 有本地系统暂时不能迁移，但想把数据备份/扩展到 AWS 时 | 它是混合云桥梁，不是单纯的云上存储桶或文件系统 |
| P1 常用优先 | AWS Backup | 集中式备份管理服务 | 给多个 AWS 服务统一配置备份计划、保留策略、跨 Region/跨账号备份 | 想统一管理 EC2/EBS、RDS、DynamoDB、EFS、S3 等资源备份时 | Backup 管“备份策略和恢复点”；S3/EFS/FSx 是被保护的数据源或存储服务 |
| P2 进阶架构 | Recycle Bin | AWS 资源回收站 | 防止误删 EBS volume、EBS snapshot、EBS-backed AMI，并在保留期内恢复 | 担心误删关键磁盘、快照或 AMI 时 | 它不是备份系统；更像删除保护缓冲区，依赖保留规则 |
| P2 进阶架构 | AWS Elastic Disaster Recovery | 弹性灾难恢复服务 | 持续复制服务器到 AWS，灾难时启动恢复实例 | 需要为本地或云上服务器做灾备，降低停机和数据丢失风险时 | Backup 偏备份与恢复点管理；Elastic Disaster Recovery 偏整机/应用级灾难切换和演练 |

### Storage 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要存图片/照片文件、普通文件、日志、数据湖、静态网站资源 | Amazon S3 |
| 我要多台 Linux 主机/容器共享一个文件系统 | Amazon EFS |
| 我要 Windows 文件共享、Lustre HPC、NetApp 或 OpenZFS | Amazon FSx |
| 我要长期低成本归档，读取不频繁 | Amazon S3 Glacier |
| 我要把本地机房存储和 AWS 云存储连接起来 | AWS Storage Gateway |
| 我要集中管理多个 AWS 服务的备份策略 | AWS Backup |
| 我要防止误删 EBS 卷、快照或 AMI | Recycle Bin |
| 我要做服务器级灾难恢复和故障切换演练 | AWS Elastic Disaster Recovery |

### Storage 学习顺序建议

1. 先学 `Amazon S3`：理解 bucket、object、key、storage class、versioning、lifecycle、bucket policy。
2. 再学 `EFS` 和 `FSx`：重点比较对象存储和文件存储的区别，以及 NFS/SMB/HPC 场景。
3. 学 `S3 Glacier`：理解归档层、恢复时间、最低存储期限、生命周期规则。
4. 学 `AWS Backup` 和 `Recycle Bin`：区分“正式备份”和“误删保留”。
5. 最后看 `Storage Gateway` 和 `AWS Elastic Disaster Recovery`：它们更偏混合云、迁移、备份和灾备架构。

## Category: Datenbank / Database / 数据库

数据库服务先分清数据模型：`关系型`、`键值/文档/宽列/图数据（Graph）/时序`、`缓存/内存数据库`、`专用企业数据库`。

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P0 核心必学 | Aurora and RDS | 托管关系型数据库 | 运行 MySQL、PostgreSQL、MariaDB、Oracle、SQL Server，以及 Aurora MySQL/PostgreSQL 兼容数据库 | 需要 SQL、事务、表关系、成熟数据库生态时 | RDS 管传统数据库引擎；Aurora 是 AWS 自研的高性能 MySQL/PostgreSQL 兼容引擎 |
| P1 常用优先 | Amazon ElastiCache | 托管缓存/内存数据存储 | 使用 Valkey、Redis OSS 或 Memcached 做缓存、会话、排行榜、热点数据加速 | 数据库读压力大，想用缓存降低延迟和成本时 | ElastiCache 偏缓存；MemoryDB 偏可持久化的主数据库 |
| P3 专项场景 | Amazon Neptune | 托管图数据库（Graph Database） | 存储和查询高度关联的数据，例如知识图谱、推荐、欺诈检测、社交关系 | 关系本身比单条记录更重要，需要高效遍历节点和边时 | 这里的 Graph 是“关系图/图数据”，不是图片，也不是镜像 |
| P2 进阶架构 | Amazon DocumentDB | MongoDB 兼容的托管文档数据库 | 存储 JSON 类文档数据，支持灵活 schema 的应用 | 应用天然以 JSON/document 建模，或想迁移 MongoDB 兼容工作负载时 | DocumentDB 是文档模型；DynamoDB 是键值/文档 NoSQL，但建模方式和查询限制不同 |
| P3 专项场景 | Amazon Keyspaces | Cassandra 兼容的托管宽列数据库 | 运行 Apache Cassandra 兼容工作负载 | 已经使用 Cassandra，或需要宽列模型、大规模写入、可预测扩展时 | 比自己管 Cassandra 集群更省运维；和 DynamoDB 都是 NoSQL，但 API/数据模型不同 |
| P3 专项场景 | Amazon Timestream | 托管时序数据库 | 存储和分析按时间产生的数据，例如 IoT 指标、监控、设备遥测 | 数据天然带时间戳，需要按时间窗口查询、聚合和降采样时 | 专门优化时序数据；不适合通用业务关系模型 |
| P0 核心必学 | Amazon DynamoDB | Serverless NoSQL 键值/文档数据库 | 构建高并发、低延迟、自动扩展的应用数据层 | 需要毫秒级性能、大规模吞吐、少运维的 key-value/document 访问时 | 不支持传统 SQL join；需要按访问模式设计主键和索引 |
| P2 进阶架构 | Amazon Aurora DSQL | Serverless 分布式关系型数据库 | 构建高可用、强一致、PostgreSQL 兼容的分布式事务应用 | 需要关系型 SQL + serverless + 单 Region 或多 Region 主动主动高可用时 | 比传统 Aurora/RDS 更偏分布式、serverless 和多 Region 强一致事务场景 |
| P2 进阶架构 | Amazon MemoryDB | 可持久化的内存数据库 | 使用 Valkey/Redis OSS API 构建超低延迟主数据库 | 既想要 Redis/Valkey 的速度，又需要 Multi-AZ 持久化和恢复能力时 | MemoryDB 可作为主数据库；ElastiCache 通常作为缓存层 |
| P3 专项场景 | Oracle Database@AWS | AWS 数据中心内的 Oracle Exadata/Autonomous Database 服务 | 运行 Oracle Exadata、RAC 等企业 Oracle 数据库工作负载 | 已有关键 Oracle 数据库，希望迁到 AWS 但保持 Oracle Exadata/OCI 托管能力时 | 不是 RDS for Oracle；它是 AWS 与 Oracle 合作，把 OCI 管理的 Oracle 数据库放在 AWS 数据中心内 |

### Database 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要传统 SQL 关系型数据库 | Aurora and RDS |
| 我要给应用加缓存 | Amazon ElastiCache |
| 我要存关系网络、知识图谱、推荐关系（Graph） | Amazon Neptune |
| 我要 MongoDB 兼容文档数据库 | Amazon DocumentDB |
| 我要 Cassandra 兼容数据库 | Amazon Keyspaces |
| 我要存 IoT/监控这类时间序列数据 | Amazon Timestream |
| 我要超大规模低延迟 NoSQL | Amazon DynamoDB |
| 我要 serverless 分布式关系型数据库 | Amazon Aurora DSQL |
| 我要 Redis/Valkey 风格但可持久化的主数据库 | Amazon MemoryDB |
| 我要迁移或运行 Oracle Exadata/RAC 工作负载 | Oracle Database@AWS |

### Database 学习顺序建议

1. 先学 `Aurora and RDS`：理解关系型数据库、实例、集群、读副本、备份、Multi-AZ。
2. 再学 `DynamoDB`：重点理解 NoSQL 访问模式、主键、二级索引、按需容量。
3. 学 `ElastiCache` 和 `MemoryDB`：区分缓存层和可持久化内存数据库。
4. 按数据模型补充 `DocumentDB`、`Keyspaces`、`Neptune`、`Timestream`。
5. 最后看 `Aurora DSQL` 和 `Oracle Database@AWS`：它们更偏新型分布式数据库和企业 Oracle 场景。

## Category: Migration & Transfer / 迁移与传输

迁移与传输服务主要分成四类：`迁移规划`、`服务器/应用迁移`、`数据库迁移`、`数据传输和特殊平台现代化`。

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P2 进阶架构 | AWS Migration Hub | 迁移项目总控台 | 发现现有服务器、规划迁移、跟踪多个工具的迁移进度 | 迁移项目涉及多台服务器、多套应用、多种迁移工具时 | 它偏管理和可视化，不直接搬数据或复制服务器 |
| P2 进阶架构 | AWS Application Migration Service | 应用/服务器 lift-and-shift 迁移服务 | 把物理机、虚拟机或云服务器复制并转换成 AWS 上的 EC2 | 想快速 rehost，大量服务器原样迁到 AWS 时 | 偏整机/应用服务器迁移；DMS 偏数据库迁移 |
| P2 进阶架构 | Application Discovery Service | 迁移发现和评估服务 | 收集本地服务器、数据库、性能和依赖关系数据 | 迁移前不知道有哪些服务器、负载和依赖关系时 | 它用于迁移前盘点；Migration Hub 用来汇总和跟踪迁移 |
| P1 常用优先 | AWS Database Migration Service | 数据库迁移服务 | 迁移关系型数据库、数据仓库、NoSQL 和其他数据存储 | 要把 Oracle、SQL Server、MySQL、PostgreSQL 等迁到 AWS 或换引擎时 | DMS 搬数据库数据并支持异构迁移；Application Migration Service 搬服务器 |
| P2 进阶架构 | AWS Transfer Family | 托管文件传输服务 | 用 SFTP、FTPS、FTP、AS2 或 Web 上传/下载 S3/EFS 文件 | 企业已有文件交换流程，想迁到 AWS 但保留原协议和客户端时 | 它是文件传输入口；DataSync 更偏大规模数据同步/迁移任务 |
| P3 专项场景 | AWS Snow Family | 物理设备数据迁移和边缘计算 | 用 Snowcone/Snowball Edge 等设备离线搬大量数据，或在弱联网环境运行边缘计算 | 网络太慢、数据量太大、地点偏远或需要离线迁移时 | DataSync 走网络传输；Snow Family 通过物理设备运输数据 |
| P1 常用优先 | AWS DataSync | 高速在线数据同步服务 | 在本地存储、AWS 存储和其他云存储之间复制文件/对象数据 | 要把 NFS/SMB/HDFS/Object 数据快速传到 S3/EFS/FSx 等时 | 比手写脚本更可靠，带校验、加密、调度和增量同步 |
| P3 专项场景 | AWS Transform | AI 驱动的迁移与现代化助手 | 用 agentic AI 帮助评估、规划和执行 VMware、.NET、mainframe 等工作负载转型 | 迁移/现代化项目复杂，想减少人工分析和改造工作时 | 它偏 AI 辅助转型流程；具体运行平台可能仍是 EC2、Mainframe Modernization、EVS 等 |
| P3 专项场景 | AWS Mainframe Modernization | 大型机应用现代化服务 | 评估、重构或重新平台化 COBOL/PL/I 等 mainframe 应用到 AWS | 企业有 IBM mainframe/大型机应用要迁移或现代化时 | 比普通服务器迁移更专门，面向大型机语言、运行时和迁移模式 |
| P3 专项场景 | Amazon Elastic VMware Service | 在 AWS 上运行 VMware Cloud Foundation | 在 EC2 bare metal + VPC 中部署和运行 VMware Cloud Foundation 环境 | 已有 VMware 运维体系，想迁到 AWS 但保留 VCF 工具和运行方式时 | 比直接迁到 EC2 改动更小；但仍需要管理 VMware/VCF 环境 |

### Migration & Transfer 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要统一跟踪迁移项目进度 | AWS Migration Hub |
| 我要迁移前盘点服务器、数据库和依赖关系 | Application Discovery Service |
| 我要把服务器原样迁到 AWS EC2 | AWS Application Migration Service |
| 我要迁移数据库或换数据库引擎 | AWS Database Migration Service |
| 我要保留 SFTP/FTP/AS2 文件交换流程 | AWS Transfer Family |
| 我要离线搬大量数据或在边缘环境处理数据 | AWS Snow Family |
| 我要通过网络高速同步文件/对象数据 | AWS DataSync |
| 我要用 AI 辅助迁移评估和现代化 | AWS Transform |
| 我要迁移/现代化大型机应用 | AWS Mainframe Modernization |
| 我要在 AWS 上运行 VMware Cloud Foundation | Amazon Elastic VMware Service |

### Migration & Transfer 学习顺序建议

1. 先学 `Migration Hub` 和 `Application Discovery Service`：理解迁移盘点、应用分组、依赖关系和迁移跟踪。
2. 学 `AWS Application Migration Service`：掌握 rehost/lift-and-shift 的基本路线。
3. 学 `AWS Database Migration Service`：理解同构/异构数据库迁移、持续复制和 cutover。
4. 学 `DataSync`、`Transfer Family`、`Snow Family`：区分在线同步、协议型文件传输、物理设备离线传输。
5. 最后看 `AWS Transform`、`AWS Mainframe Modernization`、`Amazon Elastic VMware Service`：它们更偏大型迁移和企业现代化项目。

## Category: Netzwerk & Bereitstellung von Inhalten / Networking & Content Delivery / 网络与内容分发

网络与内容分发服务先分清五件事：`云内网络`、`公网加速/CDN`、`DNS`、`API 入口`、`混合云/专用连接/恢复控制`。

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P0 核心必学 | Amazon VPC | AWS 里的虚拟私有网络 | 创建子网、路由表、安全组、NAT、互联网网关、VPC Endpoint 等网络基础设施 | 几乎所有云上应用都需要隔离网络、私有 IP、入站/出站访问控制时 | VPC 是基础网络边界；Direct Connect/VPN/Transit Gateway 等通常连接到 VPC |
| P1 常用优先 | Amazon CloudFront | 全球 CDN 内容分发网络 | 缓存和加速网站静态资源、图片/照片文件、视频、API、动态内容 | 用户分布在多个地区，想降低访问延迟、减少源站压力时 | CloudFront 缓存 HTTP 内容；Global Accelerator 加速 TCP/UDP 应用入口，不以缓存为核心 |
| P1 常用优先 | Amazon API Gateway | 托管 API 入口服务 | 创建、发布、保护、监控 REST、HTTP、WebSocket API | 想把 Lambda、容器、EC2 或后端服务暴露成可管理 API 时 | API Gateway 管 API 层能力；CloudFront 管内容分发，ALB/NLB 更偏负载均衡 |
| P2 进阶架构 | AWS Direct Connect | 本地机房到 AWS 的专线连接 | 通过专用网络连接本地网络和 AWS VPC/公共 AWS 服务 | 需要稳定带宽、更低延迟、更可预测网络质量，或不想走公网时 | 比 VPN 更稳定、更大带宽，但需要专线接入；VPN 更快上手、成本低 |
| P4 存量/谨慎 | AWS App Mesh | 服务网格 | 控制和观测微服务之间的通信、流量拆分、重试、可视化 | 已有 ECS/EKS/EC2 微服务，需要统一 service-to-service 流量治理时 | App Mesh 偏服务间通信；注意 AWS 已公告 2026-09-30 结束支持，新项目需谨慎评估替代方案 |
| P2 进阶架构 | AWS Global Accelerator | 全球网络入口加速 | 使用 Anycast 静态 IP，把用户流量走 AWS 全球骨干网转发到健康的区域端点 | 全球用户访问 ALB、NLB、EC2、EIP 等应用，希望提高可用性和延迟表现时 | 不缓存内容；更像全球级入口和流量加速，CloudFront 更像 CDN |
| P0 核心必学 | Amazon Route 53 | 托管 DNS、域名注册和健康检查 | 管理域名解析、DNS 记录、流量路由、健康检查 | 需要把域名指向网站/API/负载均衡器，或做加权、延迟、故障转移路由时 | Route 53 是权威 DNS；Route 53 Global Resolver 是递归 DNS resolver，面向客户端解析请求 |
| P3 专项场景 | AWS Data Transfer Terminal | 实体地点高速数据传输终端 | 预约 AWS 提供的物理地点，带存储设备过去，通过高速连接上传/下载数据到 AWS | 数据量很大、网络上传太慢，但不想走 Snow 设备寄送流程时 | Snow Family 是寄送物理设备；Data Transfer Terminal 是你带设备到 AWS 终端现场传输 |
| P2 进阶架构 | Amazon Route 53 Global Resolver | 全球 Anycast DNS Resolver | 让本地、分支、远程客户端安全解析公网域名和 Route 53 私有托管区域域名 | 需要统一的企业 DNS 解析、安全过滤、DoH/DoT、跨地域高可用解析时 | 它是递归解析器；Route 53 hosted zone 是权威 DNS；VPC Resolver 主要服务 VPC 内资源 |
| P2 进阶架构 | AWS Cloud Map | 服务发现 | 把服务逻辑名映射到后端资源，并通过 API 或 DNS 发现健康实例 | 微服务、ECS 任务、EC2 实例或其他资源需要动态注册和发现时 | Cloud Map 解决“服务在哪里”；App Mesh 解决“服务之间流量怎么治理” |
| P3 专项场景 | AWS RTB Fabric | 实时竞价流量专用连接网络 | 为 AdTech 的实时竞价应用提供安全、低延迟、私有网络连接 | SSP、DSP、广告服务器等需要处理 OpenRTB 请求且对毫秒级延迟敏感时 | 非通用网络服务；它专门优化 RTB 流量，不托管应用逻辑 |
| P2 进阶架构 | Amazon Application Recovery Controller | 应用恢复控制器 ARC | 为跨 AZ/跨 Region 应用提供 zonal shift、zonal autoshift、routing control、region switch 等恢复能力 | 高可用应用需要演练和执行故障切换、把流量从故障区域切走时 | Route 53/Global Accelerator 负责路由流量；ARC 更偏恢复编排和安全切流控制 |

### Networking & Content Delivery 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要设计 AWS 云内网络、子网和路由 | Amazon VPC |
| 我要给网站、图片/照片文件、视频或 API 做全球加速和缓存 | Amazon CloudFront |
| 我要发布和管理 REST/HTTP/WebSocket API | Amazon API Gateway |
| 我要本地机房通过专线连 AWS | AWS Direct Connect |
| 我要治理微服务之间的调用流量 | AWS App Mesh |
| 我要全球静态 IP 入口和低延迟转发，但不需要缓存 | AWS Global Accelerator |
| 我要管理域名、DNS 记录和健康检查 | Amazon Route 53 |
| 我要带硬盘去 AWS 实体地点高速上传/下载数据 | AWS Data Transfer Terminal |
| 我要为本地/远程客户端提供安全统一 DNS resolver | Amazon Route 53 Global Resolver |
| 我要让微服务动态发现彼此 | AWS Cloud Map |
| 我要连接实时竞价 RTB 应用 | AWS RTB Fabric |
| 我要做跨 AZ/跨 Region 应用恢复和切流控制 | Amazon Application Recovery Controller |

### Networking & Content Delivery 学习顺序建议

1. 先学 `Amazon VPC`：理解 CIDR、subnet、route table、security group、NACL、internet gateway、NAT gateway、VPC endpoint。
2. 学 `Route 53` 和 `CloudFront`：理解 DNS 如何把用户带到入口，CDN 如何缓存和加速内容。
3. 学 `API Gateway`、`Global Accelerator`：区分 API 管理、HTTP/CDN 加速、TCP/UDP 全球入口加速。
4. 学 `Direct Connect`、`Route 53 Global Resolver`：进入混合云网络、企业 DNS、安全解析场景。
5. 再看 `Cloud Map`、`App Mesh`：它们偏微服务服务发现和服务间流量治理。
6. 最后看 `Data Transfer Terminal`、`RTB Fabric`、`Application Recovery Controller`：它们更偏大数据现场传输、AdTech 专用网络和高可用恢复控制。

## Category: Entwicklertools / Developer Tools / 开发者工具

开发者工具先分清五件事：`代码仓库`、`构建/测试`、`部署/流水线`、`云端开发环境`、`可观测性/配置/AI 辅助开发与运维`。

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P2 进阶架构 | AWS CodeCommit | 托管 Git 代码仓库 | 私有保存和协作管理源代码、文档、二进制文件 | 想把 Git 仓库放在 AWS 内，并使用 IAM、CloudTrail、VPC Endpoint 等 AWS 集成时 | CodeCommit 管代码版本；CodeBuild 管构建；CodePipeline 管发布流程 |
| P1 常用优先 | AWS CodeBuild | 托管构建服务 | 编译代码、运行测试、生成可部署 artifact | 不想自己维护 Jenkins/build server，只需要按需执行构建任务时 | CodeBuild 是 CI 里的“构建/测试执行器”；CodePipeline 是编排整条流水线 |
| P1 常用优先 | AWS CodeDeploy | 自动化部署服务 | 部署应用到 EC2、本地服务器、Lambda、ECS，并支持滚动/蓝绿/金丝雀部署 | 想降低手动发布风险、支持回滚和健康检查时 | CodeDeploy 关注“怎么把新版本放到运行环境”；CodeBuild 关注“怎么把代码构建出来” |
| P1 常用优先 | AWS CodePipeline | 持续交付流水线编排服务 | 串联 source、build、test、approval、deploy 等阶段 | 需要自动化完整软件发布流程时 | 它是 CI/CD 编排器，常把 CodeCommit、CodeBuild、CodeDeploy、第三方 Git 服务串起来 |
| P4 存量/谨慎 | AWS Cloud9 | 浏览器里的云端 IDE | 在云端写代码、运行终端、调试应用 | 想快速获得带终端的在线开发环境，或教学/临时开发时 | 更像云 IDE；CloudShell 是轻量命令行，不是完整 IDE。注意：AWS Cloud9 对新客户访问有限制 |
| P0 核心必学 | AWS CloudShell | AWS 控制台里的浏览器 Shell | 直接在控制台运行 AWS CLI、脚本、常用 Linux 命令 | 想临时执行命令、排查资源、无需本地配置 AWS CLI 时 | CloudShell 是命令行环境；Cloud9 是完整 IDE；Kiro 是本地/独立 agentic IDE |
| P2 进阶架构 | AWS X-Ray | 分布式追踪服务 | 跟踪请求经过哪些服务、耗时在哪里、错误在哪里 | 微服务、Lambda、API、后端调用链复杂，需要定位延迟和错误时 | X-Ray 是 tracing；CloudWatch 更偏日志、指标、告警。注意：X-Ray SDK/Daemon 已进入维护模式，AWS 建议迁移到 OpenTelemetry |
| P3 专项场景 | AWS FIS | 故障注入/混沌工程服务 | 对真实 AWS 资源执行故障实验，验证系统韧性 | 想演练实例中断、网络故障、容量下降等场景时 | FIS 主动制造受控故障；X-Ray/CloudWatch 主要观察故障后的表现 |
| P2 进阶架构 | AWS Infrastructure Composer | 可视化 IaC 设计工具 | 拖拽式设计 AWS 架构，并生成/同步 CloudFormation 或 SAM 模板 | 想用图形界面理解和创建基础设施代码，尤其是 serverless 应用时 | 它不是部署平台本身；生成的 IaC 通常由 CloudFormation/SAM/CDK/流水线部署 |
| P2 进阶架构 | AWS App Studio | 生成式 AI 企业应用构建服务 | 用自然语言创建内部业务应用和流程应用 | IT、数据、架构等技术人员想快速做企业内部工具，但不想手写完整应用时 | App Studio 面向应用生成和托管；Infrastructure Composer 面向 AWS 基础设施图和 IaC |
| P3 专项场景 | AWS DevOps Agent | AI 运维/DevOps 代理 | 自动调查事故、关联监控/代码/部署数据、给出修复和预防建议 | 想缩短 MTTR、做 SRE on-demand 查询、跨 AWS/多云/本地调查问题时 | Amazon Q Developer 偏开发和 AWS 问答；DevOps Agent 偏生产运维、事故调查和可靠性改进 |
| P1 常用优先 | AWS AppConfig | 功能开关和动态配置服务 | 安全发布 feature flag、运行时配置、限流参数、allow/block list | 想改变应用行为但不重新部署代码，且需要渐进发布和自动回滚时 | CodeDeploy 发布代码；AppConfig 发布配置和功能开关 |
| P2 进阶架构 | AWS CodeArtifact | 托管软件包仓库 | 存储和共享 npm、Maven、PyPI、NuGet 等依赖包 | 想管理私有依赖、缓存公共依赖、控制软件供应链访问时 | CodeArtifact 管 package/artifact；CodeCommit 管源代码 |
| P1 常用优先 | Amazon Q Developer | 生成式 AI 开发助手 | 在 IDE、AWS Console、文档、聊天工具里回答 AWS/代码问题、补全代码、生成/升级/扫描代码 | 想让 AI 帮你理解 AWS、写代码、排查资源、做安全扫描和代码升级时 | Q Developer 是开发助手；Kiro 是完整 agentic IDE；DevOps Agent 是生产运维代理 |
| P4 存量/谨慎 | Amazon CodeCatalyst | 一体化软件开发协作平台 | 项目管理、代码协作、CI/CD workflow、开发环境、AWS 账号连接 | 现有团队已经在用 CodeCatalyst，希望在一个平台里管理软件交付时 | 更像完整 DevOps 平台；CodePipeline/CodeBuild/CodeDeploy 是更细粒度的 AWS CI/CD 服务。注意：CodeCatalyst 已关闭新客户访问，不计划新增功能 |
| P2 进阶架构 | Kiro | AI 驱动的 agentic IDE | 用 specs、hooks、agentic chat、MCP 等方式把需求从原型推进到可维护代码 | 想在 IDE 里用 AI 做需求拆解、设计、编码、测试、文档，并保持工程结构时 | Kiro 是 IDE/开发工作台；Amazon Q Developer 是可嵌入 IDE/控制台的 AI 助手 |

### Developer Tools 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要 AWS 托管 Git 仓库 | AWS CodeCommit |
| 我要自动构建和测试代码 | AWS CodeBuild |
| 我要自动部署到 EC2/Lambda/ECS/本地服务器 | AWS CodeDeploy |
| 我要编排完整 CI/CD 流水线 | AWS CodePipeline |
| 我要浏览器里的云端 IDE | AWS Cloud9 |
| 我要在控制台里临时跑 AWS CLI 命令 | AWS CloudShell |
| 我要看请求链路、延迟和服务调用关系 | AWS X-Ray |
| 我要做受控故障演练/混沌工程 | AWS FIS |
| 我要可视化设计 AWS 架构并生成 CloudFormation/SAM | AWS Infrastructure Composer |
| 我要用自然语言生成内部业务应用 | AWS App Studio |
| 我要 AI 帮我调查生产事故和可靠性问题 | AWS DevOps Agent |
| 我要功能开关、动态配置和安全渐进发布 | AWS AppConfig |
| 我要托管 npm/Maven/PyPI/NuGet 等包 | AWS CodeArtifact |
| 我要 AI 帮我写代码、查 AWS、做代码升级/扫描 | Amazon Q Developer |
| 我要一体化 DevOps 平台，但团队已有 CodeCatalyst 空间 | Amazon CodeCatalyst |
| 我要 agentic IDE 做规格驱动开发 | Kiro |

### Developer Tools 学习顺序建议

1. 先学 `CodeCommit`、`CodeBuild`、`CodeDeploy`、`CodePipeline`：理解 source、build、deploy、pipeline 四段式 CI/CD。
2. 再学 `CloudShell`：它是 AWS 学习和排障时最常用的轻量命令行入口。
3. 学 `CodeArtifact` 和 `AppConfig`：一个管依赖包供应链，一个管运行时配置和 feature flag。
4. 学 `X-Ray` 和 `AWS FIS`：一个观察请求链路，一个主动验证韧性。
5. 学 `Infrastructure Composer` 和 `App Studio`：分别理解“可视化 IaC”和“AI 生成业务应用”。
6. 最后看 `Amazon Q Developer`、`AWS DevOps Agent`、`Kiro`：它们代表 AWS 开发/运维工具正在转向 AI agent 化。

### Developer Tools 状态备注

- `AWS Cloud9`：AWS 官网显示 Cloud9 不再对新客户开放，已有客户可继续使用。
- `Amazon CodeCatalyst`：AWS 文档显示自 2025-11-07 起关闭新客户访问，现有客户可继续使用已有 spaces，但不计划新增功能。
- `AWS CodeCommit`：AWS 曾在 2024-07-25 关闭新客户访问；AWS DevOps Blog 和文档历史显示 2025-11-25 起重新对新客户开放。若不同页面提示不一致，以当前控制台、账号可用性和最新 AWS 公告为准。
- `AWS X-Ray`：X-Ray 服务仍可用，但 AWS 文档提示 X-Ray SDK/Daemon 自 2026-02-25 进入维护模式，并建议迁移到 OpenTelemetry 相关方案。

## Category: Kundenaktivierung / Customer Enablement / 客户赋能

客户赋能类服务和 program 主要不是“创建云资源”，而是帮助你获得专家、支持、运营托管、创业积分和组织内部知识协作。

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P4 存量/谨慎 | AWS IQ | AWS 专家任务市场 | 找 AWS Certified 专家按项目提供实操帮助，并通过 AWS 账号付款 | 遇到具体 AWS 项目卡点，需要外部专家代做或指导时 | 它不是技术资源服务，而是专家服务市场。注意：AWS IQ 将于 2026-05-28 停止支持 |
| P3 专项场景 | AWS Managed Services | AWS 托管运营服务 AMS | 由 AWS 帮企业做基础设施运营管理、监控、补丁、备份、安全、事件响应、成本优化等 | 企业希望降低 AWS 运营负担，并引入标准化运营最佳实践时 | AMS 是运营托管服务；AWS Support 是支持计划；Professional Services 偏咨询/项目交付 |
| P2 进阶架构 | AWS Activate for Startups | 创业公司扶持计划 | 为符合条件的 startup 提供 AWS credits、资源、技术支持和创业生态权益 | 早期创业公司想降低云成本、获得 up to 100,000 USD credits 和成长资源时 | Activate 是 program/credits，不是某个云资源；它抵扣的是符合条件的 AWS 使用成本 |
| P3 专项场景 | AWS re:Post Private | 企业私有技术社区 | 给企业创建私有版 re:Post，用于内部知识库、问答、AWS 专家协作和技术内容沉淀 | 企业有很多团队使用 AWS，希望集中沉淀组织内部云知识时 | re:Post 是公共社区；re:Post Private 是企业私有社区，通常面向 Enterprise 支持客户 |
| P1 常用优先 | AWS Support | AWS 支持计划 | 提供账号/账单/技术支持、Trusted Advisor、AWS Health、专家响应、TAM、事件支持等 | 生产环境需要官方支持、故障响应、架构建议或关键活动保障时 | Support 是支持订阅层级；AMS 是代运营；AWS IQ 是找第三方专家做具体任务 |

### Customer Enablement 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要找 AWS 专家帮我完成具体项目任务 | AWS IQ |
| 我要 AWS 帮企业持续运营云环境 | AWS Managed Services |
| 我的 startup 想申请 AWS credits | AWS Activate for Startups |
| 企业内部想建立私有 AWS 知识社区 | AWS re:Post Private |
| 我要官方技术支持、响应时间和专家指导 | AWS Support |

### Customer Enablement 状态备注

- `AWS IQ`：AWS 文档显示将于 2026-05-28 停止支持；2025-05-20 起不再接受新专家注册。
- `AWS Support`：当前 AWS Support 计划包含 `Basic`、`Business Support+`、`Enterprise Support`、`Unified Operations`。AWS 文档显示旧的 `Developer Support` 和 `Business Support` 将于 2027-01-01 停止支持。
- `AWS Activate for Startups`：具体 credits 金额、资格、有效期和可抵扣服务会随 program 条款变化，申请前以 AWS Activate 页面为准。

## Category: Blockchain / 区块链

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P3 专项场景 | Amazon Managed Blockchain | 托管区块链基础设施 AMB | 访问公共区块链节点/API，或创建私有 Hyperledger Fabric 网络 | 要构建 Web3 应用、查询链上数据、提交交易，或需要许可型私有区块链网络时 | 它提供区块链节点/API/网络基础设施；不是普通数据库，也不是加密货币交易所 |

### Blockchain 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要访问 Bitcoin/Ethereum 等公共链数据或节点 | Amazon Managed Blockchain Access / Query |
| 我要创建企业内部许可型区块链网络 | Amazon Managed Blockchain with Hyperledger Fabric |

## Category: Satelliten / Satellite / 卫星

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P3 专项场景 | AWS Ground Station | 托管卫星地面站 | 预约 AWS 全球地面站天线，与卫星通信、下行数据、上行命令，并把数据接入 S3/EC2 等 AWS 服务 | 卫星运营商、遥感/气象/地理空间团队需要接收和处理卫星数据时 | 它替代自建地面站基础设施；不是普通网络传输服务，也不是数据分析服务本身 |

### Satellite 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要从卫星接收数据或向卫星发送命令 | AWS Ground Station |
| 我要把卫星数据接入 AWS 后继续处理 | AWS Ground Station + S3/EC2/Lambda/数据分析服务 |

## Category: Quantum Technologies / 量子技术

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P3 专项场景 | Amazon Braket | 托管量子计算服务 | 设计、模拟、运行量子算法，并访问不同类型的量子计算硬件和模拟器 | 研究量子算法、做量子计算 PoC、学习 NISQ 时代的量子/经典混合算法时 | Braket 是量子计算实验平台；它不是通用 EC2 算力，也不是生产数据库/分析服务 |

### Quantum Technologies 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要学习或实验量子算法 | Amazon Braket notebooks / SDK |
| 我要先用模拟器测试量子线路 | Amazon Braket simulators |
| 我要把算法跑到真实量子硬件上 | Amazon Braket QPU providers |

## Category: Management & Governance / 管理与治理

管理与治理类服务主要解决：`多账号治理`、`监控可观测`、`基础设施即代码`、`资源合规`、`运维自动化`、`成本/容量优化`、`事件响应`、`配额/许可/通知`。

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P0 核心必学 | AWS Organizations | 多账号集中管理 | 创建和组织 AWS 账号、统一账单、使用 OU 和 SCP/RCP 做账号级治理 | 账号越来越多，需要统一管理权限边界、账单和组织结构时 | Organizations 是多账号底座；Control Tower 在它之上提供 landing zone 和 guardrails |
| P0 核心必学 | Amazon CloudWatch | 监控、日志、指标、告警和可观测性平台 | 收集 metrics/logs/traces，创建 dashboard/alarm，监控应用和基础设施 | 想知道系统是否健康、哪里慢、哪里报错、什么时候告警时 | CloudWatch 偏运行时观测；CloudTrail 偏审计 API 行为；Config 偏资源配置状态 |
| P1 常用优先 | AWS Auto Scaling | 自动扩缩容规划 | 根据策略和指标自动扩展 EC2 Auto Scaling、ECS、DynamoDB、Aurora replicas 等资源 | 流量变化明显，希望自动扩容保性能、缩容省成本时 | Auto Scaling 调整容量；Compute Optimizer 根据历史使用给资源规格建议 |
| P0 核心必学 | AWS CloudFormation | 基础设施即代码 IaC | 用模板定义和部署 AWS 资源栈、StackSets、变更集 | 想可重复、可审计地创建和更新基础设施时 | CloudFormation 是 IaC 执行引擎；Infrastructure Composer 是可视化生成/编辑 IaC 的工具 |
| P1 常用优先 | AWS Config | 资源配置记录和合规评估 | 记录资源配置历史、关系变化，用规则和 conformance packs 检查合规 | 需要回答“这个资源以前是什么配置”“是否违反规则”时 | Config 看资源配置和合规；CloudTrail 看谁在什么时候调用了什么 API |
| P2 进阶架构 | AWS Service Catalog | 受控 IT 服务目录 | 让管理员发布批准过的产品/模板，让用户自助部署但受约束 | 企业想让团队自助创建资源，同时保持标准化和合规时 | Service Catalog 管“可被自助部署的标准产品”；CloudFormation 管底层资源模板 |
| P1 常用优先 | AWS Systems Manager | 统一运维管理平台 | 管理 EC2、on-prem、multicloud 节点，运行命令、Session Manager、Patch、Automation、Parameter Store 等 | 想不用 SSH 堡垒机也能批量运维、打补丁、跑自动化任务时 | Systems Manager 是运维工具箱；Incident Manager 是其中偏事故响应的一项能力 |
| P1 常用优先 | AWS Trusted Advisor | 最佳实践检查和建议 | 检查成本、性能、可靠性、安全、运营卓越、服务限制，并给优化建议 | 想快速发现账号里的常见风险、浪费和配额问题时 | Trusted Advisor 给建议；Compute Optimizer 更专注计算资源 rightsizing |
| P1 常用优先 | AWS Control Tower | 多账号 landing zone 和治理护栏 | 快速建立安全合规的多账号环境，提供 Account Factory、controls、dashboard | 企业从一开始就想规范地搭建 AWS 多账号体系时 | Control Tower 编排 Organizations、IAM Identity Center、Service Catalog 等服务 |
| P2 进阶架构 | AWS Well-Architected Tool | 架构最佳实践评审工具 | 按 Well-Architected 六大支柱评估 workload，记录风险和改进项 | 想系统性检查架构是否安全、可靠、高效、节省成本、可持续时 | Well-Architected Tool 偏架构评审；Trusted Advisor 偏账号资源自动检查 |
| P2 进阶架构 | Amazon Q Developer in chat applications | ChatOps 助手，原 AWS Chatbot | 在 Slack、Microsoft Teams、Chime 中接收 AWS 通知、运行 AWS CLI、询问 Amazon Q | 团队希望在聊天工具里处理告警、事件和 AWS 操作时 | 2025-02-19 从 AWS Chatbot 改名；它是聊天集成，不是完整 IDE 里的 Amazon Q Developer |
| P3 专项场景 | AWS Launch Wizard | 工作负载部署向导 | 根据最佳实践自动部署 SQL Server、SAP、Active Directory 等复杂企业工作负载 | 想少踩坑地部署复杂企业应用基础设施时 | Launch Wizard 是面向特定工作负载的部署向导；CloudFormation 是通用 IaC |
| P1 常用优先 | AWS Compute Optimizer | 计算资源规格优化建议 | 分析 EC2、EBS、Lambda、ECS Fargate、RDS/Aurora、许可证等使用情况，推荐合适规格 | 想降低成本、发现 idle 资源、改善 price-performance 时 | Compute Optimizer 给 rightsizing 建议；Auto Scaling 执行容量伸缩 |
| P1 常用优先 | AWS Resource Groups & Tag Editor | 资源分组和标签管理 | 按 tag 或 CloudFormation stack 组织资源，批量管理标签 | 资源多了以后，需要按项目、环境、Owner、成本中心管理时 | Resource Groups 负责分组视图；Tag Editor 负责批量打标签 |
| P2 进阶架构 | Amazon Managed Grafana | 托管 Grafana 可视化 | 创建 Grafana workspace，查询和可视化 CloudWatch、Prometheus、X-Ray、OpenSearch 等数据 | 团队习惯用 Grafana 看 dashboard，但不想自己运维 Grafana 服务时 | Grafana 偏可视化；Prometheus 偏指标采集/查询模型；CloudWatch 是 AWS 原生观测平台 |
| P2 进阶架构 | Amazon Managed Service for Prometheus | 托管 Prometheus 指标服务 | 以 Prometheus 兼容方式采集、存储、查询容器/应用指标 | Kubernetes/EKS 或容器环境已使用 Prometheus 生态时 | Prometheus 是指标后端；Grafana 常用来展示 Prometheus 数据 |
| P2 进阶架构 | AWS Resilience Hub | 应用韧性管理中心 | 定义 RTO/RPO，评估应用韧性，生成改进建议，并可关联 FIS 实验 | 想持续评估应用是否能承受 AZ/Region/组件故障时 | Resilience Hub 评估和管理韧性；ARC 负责切流恢复控制；FIS 负责故障实验 |
| P2 进阶架构 | AWS Systems Manager Incident Manager | 事故响应管理 | 响应计划、联系人/on-call、升级、自动 runbook、事件时间线和复盘分析 | 生产事故需要自动拉人、协作、执行恢复步骤和复盘时 | Incident Manager 是事故流程工具；CloudWatch/EventBridge 可触发 incident |
| P3 专项场景 | AWS for SAP | SAP on AWS 方案入口 | 提供 SAP 工作负载迁移、运行、现代化的架构、工具、合作伙伴和最佳实践 | 企业运行 SAP HANA、NetWeaver、RISE/GROW with SAP 等 SAP 工作负载时 | 它是 SAP 专项方案入口，不是单个底层资源服务 |
| P3 专项场景 | AWS Telco Network Builder | 电信网络部署和生命周期管理 | 为通信服务商自动部署、管理、扩展 5G 网络功能和网络服务 | CSP 想在 AWS 上按 ETSI 描述部署 RAN/Core/IMS 等网络功能时 | 面向电信行业；不是通用容器编排，也不是普通 VPC 网络管理 |
| P1 常用优先 | AWS Health Dashboard | AWS 服务和账号健康事件视图 | 查看 AWS 服务事件、账号资源受影响情况、计划维护和健康通知 | 想知道 AWS 侧事件是否影响自己的资源或账号时 | Health 偏 AWS 服务/资源健康；CloudWatch 偏你的应用和资源指标 |
| P4 存量/谨慎 | AWS Proton | 平台工程自助部署模板 | 平台团队定义 serverless/container 应用模板，开发者自助部署环境和服务 | 已经使用 Proton 的团队需要管理模板化应用部署时 | 注意：AWS Proton 将于 2026-10-07 停止支持，2025-10-07 后新客户不能注册 |
| P3 专项场景 | AWS Sustainability | AWS 可持续性和碳排放数据 | 查看 AWS 使用带来的碳排放估算、按服务/Region 分析、导出报告 | 组织需要做云碳排放披露、ESG 或可持续性优化时 | Sustainability 看环境影响；Cost Explorer 看费用；Trusted Advisor 看技术最佳实践 |
| P1 常用优先 | AWS User Notifications | AWS 通知集中管理 | 集中配置和接收 AWS Health、CloudWatch alarm、Support case 等通知 | 想把 AWS 通知发到控制台通知中心、邮件、聊天应用、移动推送时 | User Notifications 管通知路由；SNS/EventBridge 是更底层的事件/消息能力 |
| P3 专项场景 | AWS Partner Central | AWS 合作伙伴门户 | AWS Partner 管理合作关系、项目、权益、培训、co-sell、Marketplace 相关入口 | 公司是 AWS Partner，需要管理与 AWS 的合作和销售活动时 | Partner Central 面向合作伙伴业务流程，不是普通客户资源管理服务 |
| P0 核心必学 | AWS CloudTrail | API 活动审计日志 | 记录用户、角色或 AWS 服务的 API 调用，用于审计、安全调查和合规 | 想知道“谁在什么时候对什么资源做了什么操作”时 | CloudTrail 看行为审计；Config 看资源状态；CloudWatch 看运行指标和日志 |
| P2 进阶架构 | AWS License Manager | 软件许可证管理 | 集中跟踪 Microsoft、SAP、Oracle、IBM 等许可证，管理 BYOL 和合规 | 企业有商业软件许可证，希望避免超用、错报或审计风险时 | License Manager 管许可证；AWS Marketplace 管购买软件和订阅 |
| P1 常用优先 | AWS Resource Explorer | 跨服务资源搜索发现 | 像搜索引擎一样按名称、ID、tag 等查找账号内 AWS 资源 | 资源分散在多个 Region/服务里，想快速定位资源时 | Resource Explorer 搜索资源；Resource Groups 组织资源；Config 记录资源配置历史 |
| P1 常用优先 | Service Quotas | 服务配额管理 | 查看默认/已应用配额，监控使用率，申请 quota increase | 遇到资源数量、API、容量限制，或上线前要确认配额时 | Service Quotas 管限额申请；Trusted Advisor 也能提示部分 service limits 风险 |

### Management & Governance 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要管理多个 AWS 账号、OU、SCP 和统一账单 | AWS Organizations |
| 我要搭建企业多账号 landing zone | AWS Control Tower |
| 我要监控指标、日志、告警、dashboard | Amazon CloudWatch |
| 我要记录 API 审计日志 | AWS CloudTrail |
| 我要记录资源配置历史和合规状态 | AWS Config |
| 我要用模板创建和更新基础设施 | AWS CloudFormation |
| 我要批量运维服务器、打补丁、远程命令、Session Manager | AWS Systems Manager |
| 我要账号最佳实践检查 | AWS Trusted Advisor |
| 我要评审架构风险和 Well-Architected 六大支柱 | AWS Well-Architected Tool |
| 我要找资源、分组资源、批量打标签 | AWS Resource Explorer / Resource Groups & Tag Editor |
| 我要看配额并申请提升 | Service Quotas |
| 我要优化 EC2/Lambda/EBS/RDS 等规格和成本 | AWS Compute Optimizer |
| 我要用 Grafana/Prometheus 观测容器指标 | Amazon Managed Grafana / Amazon Managed Service for Prometheus |
| 我要做事故响应和 on-call 流程 | AWS Systems Manager Incident Manager |
| 我要评估应用韧性和 RTO/RPO | AWS Resilience Hub |
| 我要在 Slack/Teams 里收 AWS 通知和执行 ChatOps | Amazon Q Developer in chat applications |
| 我要看 AWS 服务健康事件 | AWS Health Dashboard |

### Management & Governance 学习顺序建议

1. 先学 `Organizations`、`Control Tower`：理解 AWS 多账号治理的地基。
2. 学 `CloudTrail`、`Config`、`CloudWatch`：分别对应审计行为、资源状态、运行观测。
3. 学 `CloudFormation`、`Service Catalog`、`Systems Manager`：分别对应 IaC、受控自助部署、运维自动化。
4. 学 `Trusted Advisor`、`Compute Optimizer`、`Service Quotas`、`License Manager`：处理优化、配额和许可证治理。
5. 学 `Resource Explorer`、`Resource Groups & Tag Editor`：资源多了以后，它们会变得非常实用。
6. 最后看 `Resilience Hub`、`Incident Manager`、`Health Dashboard`、`User Notifications`：这是可靠性和事件响应闭环。

### Management & Governance 状态备注

- `Amazon Q Developer in chat applications`：2025-02-19 从 `AWS Chatbot` 改名，部分 URL、IAM 名称、service principal 仍可能保留 `chatbot`。
- `AWS Proton`：AWS 文档显示 2025-10-07 后新客户不能注册，2026-10-07 停止支持；已有基础设施不会因为 Proton 停服自动删除，但不能继续用 Proton 管理。
- `AWS Resource Explorer`：AWS 文档显示自 2025-10-06 起首次访问即可默认获得基础搜索能力；跨 Region/多账号搜索仍需额外配置。
- `AWS Auto Scaling`：如果只想用 predictive scaling，AWS 文档建议优先直接在 Auto Scaling 资源上配置预测扩缩，而不是只依赖 scaling plan。

## Category: Media Services / 媒体服务

媒体服务主要围绕一条视频链路来理解：`采集/传入`、`转码`、`直播编码`、`封装和源站`、`分发/互动播放`、`广告插入`、`渲染/媒体 AI/硬件设备`。

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P2 进阶架构 | Amazon Kinesis Video Streams | 设备视频流采集和实时处理 | 从摄像头、车载设备、无人机、Webcam 等采集实时视频/音频/时序媒体数据，并做实时或批量分析 | IoT 摄像头、安防、车载视频、机器视觉，需要把设备端视频可靠送到 AWS 时 | 偏“设备到云”的视频数据流；MediaLive 偏广播级直播编码；IVS 偏面向观众的互动直播 |
| P2 进阶架构 | AWS Elemental MediaConvert | 文件视频转码服务 | 把已有视频文件转成不同码率、格式、分辨率、字幕、DRM、ABR 输出 | 有 VOD 视频库、上传后转码、生成 HLS/DASH/MP4 等多端播放版本时 | 处理“文件”；MediaLive 处理“实时直播流”；MediaPackage 负责封装和源站 |
| P2 进阶架构 | AWS Elemental MediaLive | 实时直播视频编码服务 | 把直播输入转换成可用于广播和流媒体分发的输出格式 | 做体育赛事、发布会、电视台频道、7x24 直播，需要稳定直播编码时 | MediaLive 是 live encoder；MediaConnect 负责高质量直播信号传输；MediaPackage 负责下游封装 |
| P2 进阶架构 | AWS Elemental MediaPackage | 即时封装和视频源站 | 对直播/VOD 做 HLS、DASH、CMAF 等 just-in-time packaging、DRM 和 origin 输出 | 同一份视频要适配多种播放器/CDN，同时需要可靠源站和内容保护时 | MediaPackage 面向播放端格式和源站；MediaConvert/MediaLive 负责转码/编码 |
| P4 存量/谨慎 | AWS Elemental MediaStore | 低延迟视频对象存储源站 | 曾用于保存直播切片等碎片视频文件，提供低延迟读写和强一致性 | 仅用于理解或维护历史架构；新项目不要选它 | AWS 已在 2025-11-13 停止支持 MediaStore；普通对象存储优先看 S3，媒体源站优先看 MediaPackage/CloudFront |
| P2 进阶架构 | AWS Elemental MediaTailor | 服务器端广告插入和频道组装 | 在 OTT 视频中插入个性化广告，或用 VOD 内容组装线性频道 | 需要直播/VOD 变现、SSAI、广告追踪、FAST/线性频道时 | MediaTailor 管广告和频道组装；MediaPackage 管封装和 origin；CloudFront 管 CDN 分发 |
| P3 专项场景 | AWS Elemental Appliances & Software | Elemental 硬件/软件采购入口 | 通过 AWS 控制台确认和下单 AWS Elemental 本地硬件设备和软件 | 广播电视、体育赛事、媒体机构需要本地编码/转码/处理设备时 | 这是本地设备/软件订购入口，不是普通云上托管媒体服务 |
| P2 进阶架构 | Amazon Interactive Video Service | 低延迟互动直播服务 IVS | 快速创建互动直播频道、实时音视频房间、聊天和观众体验 | 做直播互动、在线活动、社交直播、直播电商、多人连麦等面向用户的产品时 | IVS 是面向应用和观众体验的一站式互动直播；MediaLive/Package 更偏专业媒体工作流组件 |
| P3 专项场景 | AWS Elemental Inference | 媒体内容 AI 分析 | 对视频、音频、图片应用机器学习模型，用于自动分析、分类和洞察；也可配合 MediaLive 做智能裁剪、事件剪辑 | 需要从媒体内容中自动识别事件、做智能画面裁剪或生成片段时 | 它是媒体 AI 能力；不是通用 SageMaker 训练平台，也不是视频转码服务 |
| P3 专项场景 | AWS Deadline Cloud | 云端渲染农场 | 管理 DCC/CG/VFX/动画渲染项目、farm、queue、fleet 和 render job | 影视、动画、游戏、建筑可视化等需要临时大规模渲染算力时 | Deadline Cloud 管渲染作业和算力农场；EC2 只是底层算力；Batch 更通用，不专门面向 DCC 渲染管线 |
| P2 进阶架构 | AWS Elemental MediaConnect | 高质量直播信号传输 | 把高质量 live video 从本地送入 AWS，并安全分发到 AWS 内外多个目的地 | 广播级直播信号贡献传输、跨 Region/跨账号/云内外分发直播源时 | MediaConnect 管“信号传输”；MediaLive 管“直播编码”；MediaPackage 管“封装和源站” |

### Media Services 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要从摄像头/设备把实时视频传到 AWS | Kinesis Video Streams |
| 我要处理上传后的视频文件/VOD 转码 | AWS Elemental MediaConvert |
| 我要做专业直播编码 | AWS Elemental MediaLive |
| 我要把直播/VOD 封装成 HLS/DASH/CMAF 并做源站 | AWS Elemental MediaPackage |
| 我要给 OTT 视频插入广告或组装线性频道 | AWS Elemental MediaTailor |
| 我要做面向用户的低延迟互动直播 | Amazon Interactive Video Service |
| 我要可靠传输广播级直播信号 | AWS Elemental MediaConnect |
| 我要云端渲染动画、VFX、CG 镜头 | AWS Deadline Cloud |
| 我要本地 Elemental 硬件或软件 | AWS Elemental Appliances & Software |
| 我要对视频/音频/图片做媒体 AI 分析 | AWS Elemental Inference |
| 我看到 MediaStore 旧架构 | 只做存量理解；新项目不要选 MediaStore |

### Media Services 学习顺序建议

1. 先学 `MediaConvert`：最容易上手，理解 input、job、output、codec、container、HLS/DASH。
2. 再学 `MediaLive` + `MediaPackage`：这是一条典型直播链路，前者编码，后者封装和做 origin。
3. 学 `CloudFront` 配合媒体服务：真正面向用户分发时，CDN 通常会接在 MediaPackage、S3 或 IVS 后面。
4. 学 `IVS`：如果目标是互动直播产品，它比手动拼 MediaLive/MediaPackage/播放器更快。
5. 最后按场景看 `Kinesis Video Streams`、`MediaConnect`、`MediaTailor`、`Deadline Cloud`、`Elemental Inference` 和本地 Elemental 设备。

### Media Services 状态备注

- `AWS Elemental MediaStore`：AWS 官方文档显示已在 2025-11-13 停止支持；2026 年的新项目应避免使用，优先评估 `S3`、`MediaPackage`、`CloudFront` 等替代方案。
- `AWS Elemental MediaPackage`：当前新建资源主要看 MediaPackage v2；AWS 文档说明 v1 和 v2 的 URL/ARN/API 不同，且没有自动迁移流程。
- `Amazon IVS`：更适合应用内互动直播和低延迟观众体验；如果你在做广播级直播制作链路，通常还是看 `MediaLive`、`MediaPackage`、`MediaConnect`。

## Category: Machine Learning / 机器学习

机器学习分类先分成六条线：`自建/训练/部署 ML 模型`、`直接调用的 AI API`、`生成式 AI 和 Agent`、`企业搜索/知识助手`、`医疗与生命科学`、`工业/边缘设备智能`。

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P0 核心必学 | Amazon SageMaker AI | 托管机器学习平台 | 构建、训练、调优、部署和管理自定义 ML/AI 模型，支持 notebook、training job、endpoint、pipeline、MLOps 等 | 你有自己的数据和模型，需要完整 ML 生命周期、可控训练和生产部署时 | SageMaker AI 偏自定义模型训练/部署；Bedrock 偏调用和定制基础模型；2024-12-03 从 Amazon SageMaker 改名为 Amazon SageMaker AI |
| P3 专项场景 | Amazon Augmented AI | 人工审核闭环 A2I | 为 ML 预测结果加入 human review workflow，在低置信度或高风险场景让人审核 | OCR、图像识别、内容审核、审批流等需要人机协作确认结果时 | A2I 不是模型本身，而是“人审工作流”；常和 Textract、Rekognition、自定义模型一起用 |
| P4 存量/谨慎 | Amazon CodeGuru | ML 驱动的代码审查/性能分析工具 | 通过 CodeGuru Reviewer/Profiler/Security 发现代码缺陷、性能瓶颈或安全问题 | 主要用于理解或维护已有 CodeGuru 集成 | 新项目优先看 Amazon Q Developer 和 Amazon Inspector；CodeGuru Reviewer 已进入维护模式，CodeGuru Security 已停止支持 |
| P2 进阶架构 | Amazon DevOps Guru | ML 运维异常检测 | 分析 CloudWatch、CloudTrail 等运行数据，发现异常、创建 insight、给出修复建议 | 生产系统指标很多，希望自动发现潜在故障、缩短排障时间时 | CloudWatch 负责监控和告警；DevOps Guru 在监控数据之上做 ML 异常分析和建议 |
| P1 常用优先 | Amazon Comprehend | 通用自然语言处理 NLP | 从文本中识别实体、关键词、语言、情绪、PII、语法，并可做自定义分类和实体识别 | 需要快速分析评论、工单、社交文本、文档内容，但不想自己训练 NLP 模型时 | Comprehend 是预置 NLP API；Bedrock 更偏生成、总结、问答；Comprehend Medical 专门处理临床文本 |
| P4 存量/谨慎 | Amazon Forecast | 时间序列预测服务 | 基于历史时间序列生成需求、库存、流量、容量等预测 | 仅适合已有 Forecast 客户维护存量预测工作流 | AWS 文档显示 Amazon Forecast 已不再接受新客户；新项目优先评估 SageMaker AI、AutoGluon 或业务分析工具 |
| P4 存量/谨慎 | Amazon Fraud Detector | 托管欺诈检测模型 | 用历史欺诈数据训练模型，结合规则对交易、注册、账号行为做风险判断 | 仅适合已有 Fraud Detector 客户继续维护 | AWS 已从 2025-11-07 起不再接受新客户；替代方案可看 SageMaker AI/AutoGluon、AWS WAF Fraud Control 等 |
| P2 进阶架构 | Amazon Kendra | 企业语义搜索和 RAG 索引 | 连接文档库、知识库、S3、SharePoint 等数据源，建立智能搜索和检索增强生成索引 | 想让员工或应用从企业文档中找到准确答案，或给 Bedrock/Q Business 做 RAG 检索层时 | Kendra 是搜索/检索和索引层；Q Business 是面向终端员工的企业 AI 助手 |
| P2 进阶架构 | Amazon Personalize | 个性化推荐服务 | 基于用户行为、商品、内容和实时事件生成推荐、重排和用户分群 | 电商、媒体、内容平台需要“猜你喜欢”“相似内容”“下一步最佳行动”时 | Personalize 是推荐系统服务；SageMaker AI 可以自建推荐模型但运维更多 |
| P1 常用优先 | Amazon Polly | 文本转语音 TTS | 把文本转换成自然语音，支持多语言、多声音、神经/生成式语音 | 需要朗读文章、语音播报、客服语音、无障碍、IoT 语音输出时 | Polly 是 text-to-speech；Transcribe 是 speech-to-text |
| P1 常用优先 | Amazon Rekognition | 图像和视频识别 | 检测物体、场景、人脸、名人、不安全内容、图片/视频中的文本等 | 需要给图片或视频加标签、审核内容、做人脸比对或视觉搜索时 | Rekognition 是通用视觉分析；Textract 专门做文档 OCR、表格和表单抽取 |
| P1 常用优先 | Amazon Textract | 文档 OCR 和结构化抽取 | 从扫描件、PDF、表格、表单、发票、收据、证件中提取文字和结构化字段 | 需要把纸质/图片/PDF 文档转成可查询、可自动处理的数据时 | Textract 面向文档理解；Rekognition 的文字检测更偏图片/视频视觉分析 |
| P1 常用优先 | Amazon Transcribe | 语音转文字 ASR | 把实时音频或 S3 中的音频/视频文件转写成文本，支持说话人区分、PII 处理等 | 会议记录、客服录音、字幕、语音搜索、语音分析时 | Transcribe 是 speech-to-text；Polly 是 text-to-speech；Comprehend 可继续分析转写后的文本 |
| P1 常用优先 | Amazon Translate | 机器翻译 | 实时或批量翻译文本/文档，构建多语言应用和内容流 | 网站、客服、邮件、知识库、用户生成内容需要多语言支持时 | Translate 改变语言；Comprehend 分析文本含义；Bedrock 可做更自由的生成式翻译但成本和可控性不同 |
| P4 存量/谨慎 | AWS Panorama | 边缘计算机视觉设备/服务 | 在本地边缘设备上运行计算机视觉应用，连接摄像头并做低延迟推理 | 仅适合已有 Panorama 客户迁移或维护现有边缘视觉方案 | AWS Panorama 将于 2026-05-31 停止支持，2025-05-20 起不再接受新客户；新项目看 SageMaker、IoT Greengrass、ECS/EKS Anywhere 等替代 |
| P4 存量/谨慎 | Amazon Monitron | 工业设备状态监测套件 | 使用专用传感器、网关和 ML 检测电机、泵、轴承等设备异常 | 仅适合已有 Monitron 客户继续使用已有传感器和项目 | Amazon Monitron 自 2024-10-31 起不再接受新客户；它是端到端硬件+软件方案，不是通用 ML 平台 |
| P3 专项场景 | AWS HealthLake | FHIR 医疗数据湖 | 使用 FHIR R4 存储、分析、共享医疗数据，并支持医疗 NLP 和多模态分析 | 医疗机构需要做医疗数据互操作、患者数据平台、临床数据分析时 | HealthLake 管结构化/非结构化健康数据；HealthImaging 管 DICOM 影像；HealthOmics 管组学数据和生信流程 |
| P4 存量/谨慎 | Amazon Lookout for Equipment | 工业设备异常检测 | 用传感器历史数据训练模型，监测固定工业设备异常和潜在故障 | 仅适合已有 Lookout for Equipment 客户维护预测性维护流程 | AWS 文档显示 2024-10-17 后不再接受新客户，2026-10-07 停止支持；新项目需评估 IoT/SageMaker/合作伙伴方案 |
| P1 常用优先 | Amazon Q Business | 企业知识 AI 助手 | 连接企业数据源，按权限回答问题、总结文档、生成内容和完成任务 | 企业想让员工用自然语言访问内部文档、知识库、SaaS 数据和业务信息时 | Q Business 是完整企业助手；Kendra 更偏搜索/RAG 索引；Bedrock 用来构建自定义生成式 AI 应用 |
| P3 专项场景 | AWS HealthOmics | 组学数据和生信工作流平台 | 运行 WDL/Nextflow/CWL 生信工作流，存储和分析 genomics/omics 数据 | 基因组、临床诊断、药物发现、农业生物研究需要大规模生信计算时 | HealthOmics 管组学数据和工作流；Bio Discovery 是抗体/药物发现应用；SageMaker AI 管通用 ML |
| P2 进阶架构 | Amazon Nova Act | 浏览器 UI 工作流 AI Agent | 用自然语言和 Python 定义 agent，在浏览器中执行表单填写、数据提取、采购、QA 测试等 UI 工作流 | 需要自动化没有稳定 API、必须操作网页 UI 的重复业务流程时 | Nova Act 专注可靠浏览器/UI 自动化；AgentCore 是更通用的 agent 运行、工具、身份、记忆和观测平台 |
| P0 核心必学 | Amazon Bedrock | 生成式 AI 基础模型平台 | 调用、评估、定制和编排来自 Amazon/Anthropic/Meta/Mistral 等提供方的 foundation models，构建生成式 AI 应用 | 要做聊天、总结、RAG、内容生成、agent、代码/文档助手，而不想自己托管大模型时 | Bedrock 提供托管 FM 和生成式 AI 构建块；SageMaker AI 负责自定义 ML 训练和部署；Amazon Q 是基于 Bedrock 的成品助手 |
| P1 常用优先 | Amazon Bedrock AgentCore | 生产级 AI Agent 平台 | 为任意框架和模型的 agent 提供 Runtime、Memory、Gateway、Identity、Browser、Code Interpreter、Observability 等能力 | 已经有 agent 原型，需要安全、可观测、可扩展地部署到生产时 | Bedrock Agents 更偏在 Bedrock 内构建 agent；AgentCore 更偏生产运行和治理，支持多框架、多模型和 MCP |
| P1 常用优先 | Amazon Q | AWS 生成式 AI 助手入口 | 在 AWS 控制台、文档、IDE、聊天应用或业务场景中提供问答、开发、运维、分析等助手能力 | 学 AWS、查资源、写代码、排障、理解成本或使用 AWS 服务时 | Amazon Q 是助手家族入口；Q Developer 偏开发/运维，Q Business 偏企业知识，Bedrock 是构建这些能力的底层生成式 AI 平台 |
| P3 专项场景 | Amazon Comprehend Medical | 医疗文本 NLP | 从英文临床文本中提取疾病、药物、检查、PHI，并映射到 RxNorm、ICD-10-CM、SNOMED CT 等医学本体 | 医疗记录、病历摘要、临床文本分析、编码辅助等医疗场景时 | 它是医疗专用 NLP，不替代专业医疗判断；普通文本分析用 Comprehend，医疗数据平台用 HealthLake |
| P1 常用优先 | Amazon Lex | 语音/文本聊天机器人 | 构建客服、预约、IT helpdesk、订单查询等对话式界面，支持 NLU、ASR、Lambda 集成 | 想用语音或文字 bot 引导用户完成任务，而不是自由问答时 | Lex 管可控的对话流程和 intent/slot；Q Business 更像企业知识问答助手；Bedrock 可构建更开放的生成式 bot |
| P3 专项场景 | Amazon Bio Discovery | AI 药物发现应用 | 让科学家访问生物 AI 模型和 agent，设计抗体候选、连接湿实验室验证，并把实验结果反馈到下一轮优化 | 生命科学/药物发现团队做抗体设计、候选筛选和 lab-in-the-loop 实验时 | Bio Discovery 是面向药物发现的成品应用；HealthOmics 管生信工作流；Bedrock/SageMaker AI 更通用 |
| P3 专项场景 | AWS HealthImaging | 医疗影像云存储和分析 | 以 PB 规模存储、检索、流式访问和分析 DICOM 医疗影像数据 | 医院、PACS/VNA、影像 AI、长期医学影像归档需要上云时 | HealthImaging 管医疗影像；HealthLake 管 FHIR 健康数据；HealthOmics 管组学数据 |

### Machine Learning 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要自己训练、调优、部署 ML 模型 | Amazon SageMaker AI |
| 我要调用大模型/生成式 AI API | Amazon Bedrock |
| 我要把 agent 原型安全部署到生产 | Amazon Bedrock AgentCore |
| 我要企业内部知识问答助手 | Amazon Q Business |
| 我要在 AWS 控制台/IDE/文档里用 AI 助手 | Amazon Q / Amazon Q Developer |
| 我要做图像/视频识别 | Amazon Rekognition |
| 我要从 PDF、扫描件、表单、发票抽取数据 | Amazon Textract |
| 我要语音转文字 | Amazon Transcribe |
| 我要文字转语音 | Amazon Polly |
| 我要机器翻译 | Amazon Translate |
| 我要文本情绪、实体、PII、关键词分析 | Amazon Comprehend |
| 我要医疗文本实体和医学本体映射 | Amazon Comprehend Medical |
| 我要构建客服/预约/任务型聊天机器人 | Amazon Lex |
| 我要企业语义搜索或 RAG 检索层 | Amazon Kendra |
| 我要推荐系统 | Amazon Personalize |
| 我要人审 ML 结果 | Amazon Augmented AI |
| 我要医疗 FHIR 数据平台 | AWS HealthLake |
| 我要医学影像云平台 | AWS HealthImaging |
| 我要组学/生信工作流 | AWS HealthOmics |
| 我要 AI 辅助抗体/药物发现 | Amazon Bio Discovery |
| 我要自动化浏览器 UI 任务 | Amazon Nova Act |
| 我看到 Forecast/Fraud Detector/CodeGuru/Panorama/Monitron/Lookout for Equipment | 先当存量服务理解，新项目谨慎选择 |

### Machine Learning 学习顺序建议

1. 先学 `SageMaker AI` 和 `Bedrock`：一个代表自定义 ML 生命周期，一个代表生成式 AI 平台。
2. 学常用 AI API：`Rekognition`、`Textract`、`Transcribe`、`Polly`、`Translate`、`Comprehend`，这些最容易做出可见功能。
3. 学企业知识和 bot：`Kendra`、`Q Business`、`Lex`，理解搜索、RAG、企业助手、任务型对话的区别。
4. 学 agent：`Bedrock AgentCore`、`Nova Act`、`Amazon Q`，理解 tool use、memory、browser automation、生产治理。
5. 最后按行业补充：医疗生命科学看 `HealthLake`、`HealthOmics`、`HealthImaging`、`Comprehend Medical`、`Bio Discovery`；工业设备看 `Monitron`、`Lookout for Equipment` 的存量架构。

### Machine Learning 状态备注

- `Amazon SageMaker AI`：2024-12-03 从原 `Amazon SageMaker` 改名；CLI、API namespace、CloudFormation 资源、控制台 URL 等仍保留 `sagemaker` 字样。
- `Amazon CodeGuru`：CodeGuru Reviewer 自 2025-11-07 起不能创建新的 repository association，进入维护模式；CodeGuru Security 已在 2025-11-20 停止支持。新项目优先看 `Amazon Q Developer` 和 `Amazon Inspector Code Security`。
- `Amazon Forecast`：AWS 文档显示自 2024-07-25 起不再接受新客户，已有客户可继续使用。
- `Amazon Fraud Detector`：AWS 文档显示自 2025-11-07 起不再接受新客户，已有客户可继续使用。
- `AWS Panorama`：2025-05-20 起不再接受新客户，2026-05-31 停止支持。
- `Amazon Monitron`：2024-10-31 起不再接受新客户，已有客户可继续使用。
- `Amazon Lookout for Equipment`：2024-10-17 起不再接受新客户，2026-10-07 停止支持。
- `AWS HealthLake`、`AWS HealthOmics`、`AWS HealthImaging`、`Amazon Comprehend Medical`：这些服务不是医疗建议、诊断或治疗替代品；用于临床或患者护理场景时需要专业人员审核。
- `Amazon Nova Act`：AWS 文档显示当前支持 Region 为 `US East (N. Virginia)`，实际可用性以控制台为准。

## Category: Analysen / Analytics / 分析

分析类服务可以按数据链路理解：`采集/流式传输`、`ETL/数据集成`、`数据湖治理`、`查询/数仓/大数据计算`、`搜索与日志分析`、`BI 可视化`、`数据共享/协作`、`行业分析平台`。

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P0 核心必学 | Amazon Athena | Serverless SQL 查询服务 | 直接用 SQL 查询 S3、Glue Data Catalog、Iceberg 表和多种联邦数据源，也支持 Athena for Apache Spark | 想快速分析 S3 数据湖里的 CSV/Parquet/JSON/Iceberg 数据，不想维护集群时 | Athena 是即查即用；Redshift 是长期运行的数仓；EMR/Flink 更适合复杂大数据或流计算 |
| P0 核心必学 | Amazon Redshift | 云数据仓库 | 构建 PB 级数据仓库、SQL 分析、BI 报表、Redshift Serverless、Spectrum 查询数据湖 | 企业要做高性能结构化分析、事实表/维表、BI 仪表盘和数据集市时 | Redshift 是数仓；Athena 查询 S3 更轻量；SageMaker/Quick 可以在上层消费分析结果 |
| P4 存量/谨慎 | Amazon CloudSearch | 托管搜索服务 | 为网站或应用建立全文搜索、过滤、排序、地理位置搜索等能力 | 仅适合已有 CloudSearch 客户维护旧搜索域 | AWS 已在 2024-07-25 关闭新客户访问；新项目优先看 Amazon OpenSearch Service 或 Amazon Kendra |
| P1 常用优先 | Amazon OpenSearch Service | 托管搜索、日志和分析引擎 | 托管 OpenSearch/旧 Elasticsearch 集群，用于日志分析、全文搜索、可观测性、点击流分析 | 需要搜索引擎、日志分析平台、OpenSearch Dashboards 或 Elasticsearch 兼容生态时 | OpenSearch 偏搜索/日志/近实时分析；CloudSearch 是旧搜索服务；Kendra 偏企业语义搜索/RAG |
| P1 常用优先 | Amazon Kinesis Data Streams | 实时数据流基础服务 | 持续采集和处理日志、点击流、IoT、市场数据等实时记录，支持多个消费者读取 | 需要低延迟、可多消费者处理的实时数据管道时 | Kinesis Data Streams 存储可重放数据流；Data Firehose 负责自动投递到目标；Flink 负责复杂流计算 |
| P1 常用优先 | Amazon Quick Sight / QuickSight | BI 仪表盘和可视化 | 创建交互式 dashboard、SPICE 内存分析、嵌入式分析、自然语言 BI 问答 | 业务用户要看报表、指标、图表、经营看板或把 BI 嵌入应用时 | QuickSight 已作为 Amazon Quick Sight 继续存在；Amazon Quick 是更大的生成式 AI 分析平台 |
| P2 进阶架构 | AWS Data Exchange | 第三方/跨组织数据交换 | 订阅、授权、共享来自 AWS Marketplace 或其他组织的数据集，支持文件、API、S3、Redshift、Lake Formation 等数据类型 | 需要购买外部数据、给客户/伙伴授权数据，或管理数据产品分发时 | Data Exchange 管数据产品和授权；DataZone 管组织内部数据目录和治理；Clean Rooms 管隐私保护协作分析 |
| P1 常用优先 | AWS Lake Formation | 数据湖权限治理 | 对 S3 数据湖和 Glue Data Catalog 做集中权限、列/行/单元格级访问控制、跨账号共享 | 数据湖进入多人、多团队、多账号使用阶段，需要细粒度治理时 | Lake Formation 管数据湖权限；Glue 管数据目录和 ETL；DataZone 管业务目录、项目和数据订阅流程 |
| P2 进阶架构 | Amazon MSK | 托管 Apache Kafka | 运行兼容 Apache Kafka 的托管集群、Serverless Kafka、MSK Connect、Replicator | 团队已有 Kafka 生态、客户端、connector，想减少自建 Kafka 运维时 | MSK 是 Kafka 兼容；Kinesis Data Streams 是 AWS 原生流；Data Firehose 是投递服务 |
| P2 进阶架构 | AWS Glue DataBrew | 可视化数据准备 | 用点选式界面清洗、标准化、转换数据，生成 recipe 和 profile，不写代码做数据准备 | 数据分析师想清洗数据但不想写 Spark/SQL/Python ETL 时 | DataBrew 偏可视化清洗；AWS Glue 是完整 serverless 数据集成和 ETL 平台 |
| P4 存量/谨慎 | Amazon FinSpace | 金融行业时间序列/kdb 分析平台 | 为资本市场客户管理和分析实时/历史金融时间序列数据，托管 kdb Insights | 仅适合已有 FinSpace 客户维护金融数据分析工作流 | Amazon FinSpace 2025-10-07 起不再接受新客户，2026-10-07 停止支持；新项目优先看 SageMaker、EMR、Athena、Redshift 等替代组合 |
| P2 进阶架构 | Amazon Managed Service for Apache Flink | 托管流计算 | 用 Apache Flink 的 Java/Scala/Python/SQL 处理和分析实时流数据，做窗口、聚合、实时指标和 dashboard | 需要复杂事件处理、状态流计算、实时特征/指标、低延迟分析时 | Flink 负责计算；Kinesis/MSK 负责流数据来源；Data Firehose 负责投递 |
| P1 常用优先 | Amazon EMR | 托管大数据集群平台 | 运行 Apache Spark、Hadoop、Hive、Presto/Trino 等大数据框架，处理海量数据 | 需要开源大数据生态、可控集群、复杂 Spark 作业或迁移 Hadoop/Spark 工作负载时 | EMR 更像托管开源大数据平台；Glue 更 serverless ETL；Athena 更轻量 SQL 查询 |
| P2 进阶架构 | AWS Clean Rooms | 隐私保护数据协作空间 | 多方在不暴露底层数据的情况下做联合分析、受控 SQL/PySpark 查询、差分隐私、Clean Rooms ML | 广告、营销、合作伙伴分析、数据联盟等需要“可合作但不共享原始数据”时 | Clean Rooms 解决跨组织安全协作；Data Exchange 解决数据授权/售卖；Entity Resolution 可用于匹配共同实体 |
| P1 常用优先 | Amazon SageMaker | 数据、分析和 AI 统一平台 | 新一代 SageMaker 统一数据湖、SQL 分析、数据处理、AI/ML、生成式 AI 和治理能力，入口是 SageMaker Unified Studio | 想在一个环境里同时做数据发现、SQL 分析、数据处理、模型开发和生成式 AI 应用时 | 这里是新版 Amazon SageMaker 平台；前面 ML 章节的 SageMaker AI 是其机器学习训练/部署能力 |
| P2 进阶架构 | AWS Entity Resolution | 实体匹配和记录链接 | 在多个数据源之间匹配、链接、增强同一客户/产品/业务实体，支持规则、ML 和数据提供商匹配 | 客户 360、广告归因、主数据管理、跨渠道身份匹配时 | Entity Resolution 解决“这些记录是不是同一个实体”；Clean Rooms 解决“多方怎么安全协作分析” |
| P0 核心必学 | AWS Glue | Serverless 数据集成和 ETL | 数据发现、Glue Data Catalog、crawler、Spark/Ray ETL、流式 ETL、数据质量、连接器和工作流 | 要把多来源数据清洗、转换、编目并送入数据湖/数仓时 | Glue 是数据工程中枢；DataBrew 是可视化数据准备；Lake Formation 在 Glue Catalog 基础上做权限治理 |
| P1 常用优先 | Amazon Data Firehose | 实时数据投递服务 | 把流数据自动投递到 S3、Redshift、OpenSearch、Splunk、Iceberg 表、HTTP endpoint 等目标，可做简单转换 | 想把日志/事件/指标稳定送到存储或分析系统，不想自己写消费者程序时 | Firehose 负责投递；Kinesis Data Streams/MSK 负责流缓冲和多消费者；Flink 负责复杂处理 |
| P1 常用优先 | Amazon DataZone | 数据目录、发现、共享和治理 | 建立业务数据目录、项目空间、数据发布/订阅、访问审批和跨数据源治理 | 企业数据资产多，希望让业务用户能发现、申请、使用和协作处理数据时 | DataZone 面向业务数据治理和自助发现；Lake Formation 管底层数据权限；Glue Catalog 管技术元数据 |
| P1 常用优先 | Amazon Quick | 生成式 AI 驱动的 BI/分析平台 | 连接多种数据源，创建 dashboard、自动化工作流、数据发现、研究分析，并通过 AI agent 做自然语言分析 | 想让非技术用户通过自然语言分析数据、自动化业务流程、协作生成洞察时 | Amazon Quick 是新平台；QuickSight 已更名为 Amazon Quick Sight，并作为 Quick 的可视化组件继续存在 |

### Analytics 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要直接用 SQL 查 S3 数据湖 | Amazon Athena |
| 我要企业数据仓库和高性能 BI 查询 | Amazon Redshift |
| 我要做 serverless ETL、crawler、数据目录 | AWS Glue |
| 我要治理 S3 数据湖权限 | AWS Lake Formation |
| 我要做业务数据目录、数据发现和订阅 | Amazon DataZone |
| 我要做 BI 仪表盘和嵌入式分析 | Amazon Quick Sight / QuickSight |
| 我要生成式 AI 分析平台和业务 agent | Amazon Quick |
| 我要日志搜索、全文搜索、OpenSearch Dashboard | Amazon OpenSearch Service |
| 我要采集实时流，多个消费者读取 | Amazon Kinesis Data Streams |
| 我要把流数据自动投递到 S3/Redshift/OpenSearch 等 | Amazon Data Firehose |
| 我要使用 Kafka 生态 | Amazon MSK |
| 我要复杂实时流计算 | Amazon Managed Service for Apache Flink |
| 我要跑 Spark/Hadoop/Trino 等大数据作业 | Amazon EMR |
| 我要不写代码清洗数据 | AWS Glue DataBrew |
| 我要跨组织隐私保护联合分析 | AWS Clean Rooms |
| 我要匹配同一客户/产品/实体记录 | AWS Entity Resolution |
| 我要订阅或授权外部数据产品 | AWS Data Exchange |
| 我要统一数据、分析和 AI 开发体验 | Amazon SageMaker |
| 我看到 CloudSearch 或 FinSpace | 当存量服务理解，新项目谨慎选择 |

### Analytics 学习顺序建议

1. 先学 `S3 + Glue Data Catalog + Athena`：这是 AWS 数据湖分析入门主线。
2. 再学 `Redshift` 和 `Quick/QuickSight`：理解数仓和 BI 可视化。
3. 学 `Glue`、`Lake Formation`、`DataZone`：分别对应数据集成、底层权限治理、业务数据治理。
4. 学实时链路：`Kinesis Data Streams`、`Data Firehose`、`MSK`、`Managed Service for Apache Flink`。
5. 最后按场景看 `OpenSearch`、`EMR`、`Clean Rooms`、`Entity Resolution`、`Data Exchange`、`SageMaker`、`DataBrew`。

### Analytics 状态备注

- `Amazon QuickSight / Amazon Quick`：AWS 文档显示 QuickSight 已更名并扩展为 `Amazon Quick`；原 QuickSight 能力作为 `Amazon Quick Sight` 继续存在，现有 QuickSight API/SDK/集成继续工作。
- `Amazon SageMaker`：这里指 re:Invent 2024 后的新一代统一平台，用于 data、analytics、AI；`Amazon SageMaker AI` 是其中负责构建、训练和部署 ML/FM 的能力。
- `Amazon CloudSearch`：AWS 已在 2024-07-25 关闭新客户访问；现有客户可继续使用，但 AWS 不计划新增功能。
- `Amazon FinSpace`：AWS 文档显示 2025-10-07 起不再接受新客户，2026-10-07 停止支持；Dataset Browser 更早已在 2025-03-26 停用。
- `AWS Glue for Ray`：AWS 文档显示 2026-04-30 起不再对新客户开放；这影响的是 Glue 的 Ray 引擎能力，不等于 AWS Glue 整体停用。

## Category: Sicherheit, Identität & Compliance / Security, Identity & Compliance / 安全、身份与合规

安全类服务可以按六条主线理解：`身份与访问控制`、`密钥/证书/加密`、`威胁检测与漏洞管理`、`网络与应用防护`、`合规审计`、`事件响应与开发安全`。

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P1 常用优先 | AWS Resource Access Manager | 跨账号资源共享 | 把 VPC 子网、Transit Gateway、Route 53 Resolver 规则、License Manager 配置等支持的资源共享给其他账号、OU 或组织 | 多账号架构里想“资源只建一份，多账号共同使用”时 | RAM 管资源共享；IAM 管权限；Organizations 管账号组织结构 |
| P1 常用优先 | Amazon Cognito | 应用用户身份系统 | 为 Web/移动应用提供注册、登录、用户池、身份池、OAuth/OIDC/SAML 联邦和社交登录 | 你在做面向客户或用户的 App，需要用户认证、JWT token、临时 AWS 凭证时 | Cognito 管应用终端用户；IAM 管 AWS 资源访问；IAM Identity Center 管员工/组织用户登录 AWS 和企业应用 |
| P0 核心必学 | AWS Secrets Manager | 密钥和凭证托管 | 保存、读取、轮换数据库密码、API key、OAuth token 等 secret，避免把凭证写进代码 | 应用需要运行时安全获取敏感配置，并希望自动轮换凭证时 | Secrets Manager 管 secret 生命周期；KMS 管加密密钥；Parameter Store 也可存配置但轮换和 secret 管理能力较轻 |
| P1 常用优先 | Amazon GuardDuty | 威胁检测 | 持续分析 CloudTrail、VPC Flow Logs、DNS、EKS/ECS/EC2 runtime、S3 malware 等数据源，发现可疑行为 | 想快速获得账号、网络、工作负载层面的威胁检测，不想自建 SIEM 规则时 | GuardDuty 发现威胁；Security Hub/Hub CSPM 聚合和关联 findings；Detective 帮你调查根因 |
| P1 常用优先 | Amazon Inspector | 漏洞管理 | 自动发现并扫描 EC2、ECR 容器镜像、Lambda 的软件漏洞和网络暴露 | 需要持续知道哪些 workload 有 CVE、暴露端口或容器镜像风险时 | Inspector 看漏洞和暴露面；GuardDuty 看异常行为和威胁；Security Hub 汇总风险 |
| P2 进阶架构 | Amazon Macie | S3 敏感数据发现 | 用机器学习和模式匹配发现 S3 中的 PII、凭证、财务数据等敏感信息，并监控 bucket 安全风险 | 组织有大量 S3 数据，想知道哪里存了敏感数据、哪些 bucket 风险高时 | Macie 聚焦 S3 数据安全和敏感数据；S3 Block Public Access/Access Analyzer 更偏访问风险 |
| P0 核心必学 | AWS IAM Identity Center | 员工单点登录和多账号访问中心 | 连接企业身份源，集中管理员工访问 AWS 账号、Amazon Quick、Kiro 等 AWS managed applications | 多账号环境、公司员工登录 AWS Console/CLI、需要 SSO 和 permission set 时 | IAM Identity Center 管 workforce access；IAM role 是最终落到账号里的权限载体；Cognito 管 App 用户 |
| P1 常用优先 | AWS Certificate Manager | 托管 TLS 证书 | 创建、导入、续期公有/私有 SSL/TLS X.509 证书，给 ALB、CloudFront、API Gateway 等服务使用 | 网站、API、CDN、负载均衡需要 HTTPS 证书，且希望自动续期时 | ACM 管证书生命周期；AWS Private CA 建私有 CA；KMS 管数据加密密钥 |
| P0 核心必学 | AWS Key Management Service | 托管加密密钥服务 | 创建和控制 KMS keys，用于 S3、EBS、RDS、DynamoDB、Secrets Manager 等服务加密和签名 | 任何生产系统需要数据加密、密钥策略、审计、跨服务集成时 | KMS 是通用托管密钥服务；CloudHSM 是专属 HSM；Payment Cryptography 是支付行业加密 |
| P3 专项场景 | AWS CloudHSM | 专属硬件安全模块 | 在 AWS 云中使用单租户 HSM，自己控制密钥、算法、用户和应用集成 | 合规要求必须使用专属 HSM，或需要 PKCS#11/JCE/CNG/KSP 等 HSM 接口时 | 比 KMS 控制权更高但运维责任更重；不是一般应用加密的首选 |
| P2 进阶架构 | AWS Directory Service | 托管目录和 Active Directory 集成 | 使用 AWS Managed Microsoft AD、AD Connector、Simple AD，把 AD/LDAP 身份接入 AWS 应用和 Windows workload | 企业已有 Microsoft AD，或需要在 AWS 上运行 AD-aware 应用、WorkSpaces、Windows 域加入时 | Directory Service 管目录；IAM Identity Center 管员工访问 AWS 账号和应用；Cognito 管外部 App 用户 |
| P2 进阶架构 | AWS Firewall Manager | 多账号安全策略集中管理 | 跨 AWS Organizations 统一管理 WAF、Shield Advanced、安全组、Network Firewall、Route 53 Resolver DNS Firewall 等策略 | 多账号/多资源环境里想统一下发和持续维护网络安全策略时 | Firewall Manager 是管理平面；WAF/Shield/Network Firewall 是具体防护能力 |
| P2 进阶架构 | AWS Artifact | 合规报告和协议中心 | 下载 AWS ISO、SOC、PCI 等安全合规报告、认证文件，并管理部分 AWS 协议 | 审计、供应商安全评估、客户合规问卷需要 AWS 官方证明材料时 | Artifact 提供 AWS 合规材料；Audit Manager 帮你收集你自己 AWS 使用情况的审计证据 |
| P2 进阶架构 | Amazon Detective | 安全调查和根因分析 | 从 CloudTrail、VPC Flow Logs、GuardDuty findings 等数据构建行为图，帮助分析可疑活动的上下文 | GuardDuty/Security Hub 告警很多，需要快速看攻击路径、关联实体、时间线和根因时 | Detective 用于调查；GuardDuty 用于检测；Security Lake 用于集中存储安全日志 |
| P3 专项场景 | AWS Signer | 代码签名 | 托管代码签名证书和签名流程，确保 Lambda、IoT 等代码包来自可信发布者且未被篡改 | 需要发布前强制代码签名、满足供应链安全或合规要求时 | Signer 管代码完整性；CodePipeline/CodeBuild 管 CI/CD；Inspector/Code Security 查漏洞 |
| P2 进阶架构 | Amazon Security Lake | 安全数据湖 | 把 AWS、SaaS、本地和第三方安全日志集中到你账号里的 S3 数据湖，并转换为 OCSF/Parquet | 安全团队要集中保存、查询、订阅、长期分析安全日志和事件时 | Security Lake 存和标准化安全数据；Security Hub 聚合 findings；Detective 做调查视图 |
| P3 专项场景 | AWS Security Agent | 开发生命周期安全 Agent | 根据组织安全要求做设计/代码安全审查、按需渗透测试，并可接入 GitHub 生成修复建议 | 希望把安全评审和渗透测试前移到设计、PR 和部署验证阶段时 | 它偏应用安全和 SDLC；Inspector 偏已部署 workload 漏洞；Q Developer 偏开发辅助 |
| P2 进阶架构 | Amazon Verified Permissions | 应用细粒度授权 | 用 Cedar policy 管理自建应用里的 RBAC/ABAC/关系型授权决策，把授权逻辑从业务代码中抽离 | SaaS、多租户应用、复杂资源权限、需要集中 policy decision point 时 | Verified Permissions 管应用内授权；Cognito/IAM Identity Center 负责认证或身份来源；IAM 管 AWS 资源权限 |
| P2 进阶架构 | AWS Audit Manager | 审计证据自动收集 | 基于框架持续收集 AWS 使用证据，支持合规评估、控制项审阅、审计报告生成 | 需要应对 SOC2、PCI、HIPAA、GDPR、CIS 等审计，减少手工取证时 | Audit Manager 收集你环境的证据；Artifact 下载 AWS 自身的合规报告 |
| P1 常用优先 | AWS Security Hub CSPM | 云安全态势管理 | 基于 AWS FSBP、CIS、PCI、NIST 等标准做持续配置检查、评分、finding 聚合和自动化 | 想知道账号/组织配置是否符合安全最佳实践和合规基线时 | CSPM 偏 posture/compliance checks；Security Hub 偏统一关联和响应关键安全风险 |
| P0 核心必学 | AWS IAM | AWS 访问控制基础 | 管理 IAM user、group、role、policy、permission boundary、STS、Access Analyzer 等 | 任何 AWS 学习和生产环境都必须先掌握，尤其是 least privilege 和 role assumption | IAM 是 AWS 资源权限底座；IAM Identity Center 是员工 SSO；Cognito 是应用用户身份 |
| P1 常用优先 | AWS WAF & AWS Shield | Web 防火墙和 DDoS 防护 | WAF 过滤 HTTP/HTTPS 请求、SQLi/XSS/bot 等；Shield 提供 DDoS 防护，Advanced 有增强防护和响应支持 | 保护 CloudFront、ALB、API Gateway、AppSync、Cognito user pool 等公网入口时 | WAF 主要管 L7 Web 请求规则；Shield 管 DDoS；Firewall Manager 统一管理这些策略 |
| P1 常用优先 | AWS Security Hub | 安全风险统一视图和响应 | 聚合 GuardDuty、Inspector、Macie、Security Hub CSPM 等 findings，关联暴露风险，帮助排序和响应关键问题 | 安全服务开多了以后，需要一个统一入口看优先级、自动化工作流和运营响应时 | Security Hub 与 Security Hub CSPM 互补；AWS 官方建议两者都启用以获得完整体验 |
| P3 专项场景 | AWS Private Certificate Authority | 私有证书颁发机构 | 创建私有 root/subordinate CA，签发内部 TLS、设备、用户、代码签名等 X.509 证书 | 企业内部 PKI、mTLS、IoT 设备证书、私有服务间认证需要自有 CA 时 | Private CA 建 CA 层级；ACM 管证书申请/部署/续期；KMS 不负责颁发证书 |
| P3 专项场景 | AWS Payment Cryptography | 支付加密和支付 HSM 能力 | 为发卡、收单、支付网络等场景提供 PIN、CVV、ARQC、DUKPT、TR-31/TR-34 等支付密码学操作 | 金融支付系统需要符合 PCI 标准的支付交易加密和密钥管理时 | 它是支付专用加密；KMS 是通用数据加密；CloudHSM 是专属通用 HSM |
| P2 进阶架构 | AWS Security Incident Response | 托管安全事件响应 | 帮助准备、分诊、升级、调查账号接管、数据泄露、勒索软件等安全事件，并提供安全响应工程师支持 | 组织希望有 AWS 原生的事件响应流程、case 管理和专家协助时 | 它是响应服务；GuardDuty/Inspector/Macie/Security Hub 负责发现和排序风险 |

### Security, Identity & Compliance 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要控制谁能访问 AWS 资源 | AWS IAM |
| 我要给员工做 AWS 多账号 SSO | AWS IAM Identity Center |
| 我要跨账号共享资源 | AWS Resource Access Manager |
| 我要给自己的 App 做用户注册登录 | Amazon Cognito |
| 我要保存和轮换数据库密码/API key | AWS Secrets Manager |
| 我要管理数据加密密钥 | AWS Key Management Service |
| 我要专属 HSM 或更强密钥控制 | AWS CloudHSM |
| 我要给网站/API/负载均衡配置 HTTPS 证书 | AWS Certificate Manager |
| 我要建立企业内部私有 CA | AWS Private Certificate Authority |
| 我要接入 Microsoft AD/LDAP | AWS Directory Service |
| 我要检测账号和 workload 的可疑行为 | Amazon GuardDuty |
| 我要扫描 EC2/ECR/Lambda 漏洞 | Amazon Inspector |
| 我要发现 S3 里的敏感数据 | Amazon Macie |
| 我要按安全标准检查配置和合规基线 | AWS Security Hub CSPM |
| 我要统一关联和响应安全 findings | AWS Security Hub |
| 我要调查告警背后的时间线和根因 | Amazon Detective |
| 我要集中保存和查询安全日志 | Amazon Security Lake |
| 我要保护 Web/API 入口和抵御 DDoS | AWS WAF & AWS Shield |
| 我要跨组织统一下发 WAF/Shield/Network Firewall 等策略 | AWS Firewall Manager |
| 我要下载 AWS 官方合规报告 | AWS Artifact |
| 我要自动收集自己环境的审计证据 | AWS Audit Manager |
| 我要做代码签名和供应链完整性控制 | AWS Signer |
| 我要给自建应用做细粒度授权 | Amazon Verified Permissions |
| 我要做支付行业 PIN/CVV/ARQC 等加密 | AWS Payment Cryptography |
| 我要安全事件响应和专家协助 | AWS Security Incident Response |
| 我要把安全评审和渗透测试前移到开发流程 | AWS Security Agent |

### Security, Identity & Compliance 学习顺序建议

1. 先学 `IAM`、`IAM Role`、`Policy`、`STS`、`least privilege`，这是所有 AWS 服务的权限基础。
2. 再学 `IAM Identity Center`、`Organizations`、`Resource Access Manager`，理解多账号和员工访问治理。
3. 学 `KMS`、`Secrets Manager`、`ACM`：分别对应加密密钥、secret 生命周期、TLS 证书。
4. 学入口防护和检测：`WAF & Shield`、`GuardDuty`、`Inspector`、`Macie`。
5. 学安全运营闭环：`Security Hub CSPM`、`Security Hub`、`Detective`、`Security Lake`、`Security Incident Response`。
6. 最后按企业/行业场景补：`Directory Service`、`Firewall Manager`、`Artifact`、`Audit Manager`、`Private CA`、`CloudHSM`、`Payment Cryptography`、`Signer`、`Verified Permissions`、`Security Agent`。

### Security, Identity & Compliance 状态备注

- `IAM`、`IAM Identity Center`、`Cognito` 不要混：IAM 管 AWS 资源权限；IAM Identity Center 管员工/组织用户访问 AWS 账号和 AWS managed applications；Cognito 管你自己 App 的终端用户登录。
- `KMS`、`CloudHSM`、`AWS Payment Cryptography`、`Private CA`、`ACM` 不要混：KMS 是通用托管密钥；CloudHSM 是专属 HSM；Payment Cryptography 是支付交易密码学；Private CA 是私有证书颁发机构；ACM 是证书生命周期管理。
- `Security Hub CSPM` 和 `Security Hub` 是互补服务：CSPM 做安全态势、标准控制项和合规检查；Security Hub 做统一风险视图、关联和响应。AWS 官方文档建议两者都启用以获得最佳体验。
- `GuardDuty`、`Inspector`、`Macie` 是不同检测源：GuardDuty 检测威胁行为，Inspector 扫漏洞和暴露面，Macie 发现 S3 敏感数据。
- `WAF & Shield`：WAF 是 Web 应用防火墙，Shield 是 DDoS 防护；多账号统一管理时再上 `Firewall Manager`。
- `AWS Security Agent`：官方文档描述它面向应用开发生命周期安全审查和按需渗透测试；当前文档中的代码仓库集成明确提到支持 GitHub。

## Category: Cloud-Finanzverwaltung / Cloud Financial Management / 云财务管理

云财务管理类服务主要解决三件事：`买什么`、`花了多少`、`成本如何分摊和优化`。

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P1 常用优先 | AWS Marketplace | 第三方软件、数据和服务市场 | 查找、购买、部署和管理第三方 AMI、SaaS、容器、数据产品、专业服务等，费用合并到 AWS 账单 | 需要采购安全、监控、数据库、BI、DevOps、行业软件或商业数据产品时 | Marketplace 是采购和订阅入口；AWS Data Exchange 更聚焦数据产品；Billing 管账单 |
| P3 专项场景 | AWS Billing Conductor | 自定义账单/内部结算 | 为合作伙伴转售、企业 showback/chargeback 创建 pro forma 成本视图、billing group、pricing plan、custom line item | 需要按内部业务单元、客户、子公司重算或展示成本，不直接按 AWS 原始账单给使用方看时 | Billing Conductor 不改变 AWS 实际账单；它创建第二套 pro forma 成本数据 |
| P0 核心必学 | AWS Billing and Cost Management | AWS 账单和成本管理总入口 | 查看账单、发票、付款、成本分析、Cost Explorer、Budgets、Cost Anomaly Detection、Savings Plans、Reservations、成本标签和导出 | 任何 AWS 账号都要用来控制费用、查账、预测支出、发现异常和做成本优化 | 这是财务管理总控制台；Marketplace 是买第三方产品；Billing Conductor 是高级内部结算建模 |

### Cloud Financial Management 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要看 AWS 花了多少钱、账单和发票 | AWS Billing and Cost Management |
| 我要做预算、成本分析、异常检测和节省建议 | AWS Billing and Cost Management |
| 我要购买第三方软件、SaaS、AMI、数据或服务 | AWS Marketplace |
| 我要给内部团队/客户做 showback 或 chargeback | AWS Billing Conductor |

### Cloud Financial Management 学习顺序建议

1. 先学 `Billing and Cost Management`：看账单、Cost Explorer、Budgets、成本分配标签、Savings Plans/Reservations。
2. 再看 `AWS Marketplace`：理解第三方产品会如何进入 AWS bill，以及 AMI/SaaS/数据产品的订阅方式。
3. 最后看 `Billing Conductor`：它更偏组织级 FinOps、合作伙伴转售和内部成本分摊。

### Cloud Financial Management 状态备注

- `Billing and Cost Management` 是一组功能集合，不是单一小工具；里面包含 Billing、Cost Explorer、Budgets、Data Exports、Cost Anomaly Detection、Savings Plans、Reservations 等。
- `Billing Conductor` 生成的是 `pro forma` 成本数据，不会改变 AWS 给你的实际应付账单。
- `AWS Marketplace` 里的软件或 SaaS 费用会出现在 AWS 账单里，但产品许可、支持责任和服务条款要看具体卖家的 offer。

## Category: Mobil / Mobile / 移动

移动类目里的服务不只服务手机 App，也经常用于 Web 前端、实时 API、跨设备测试和地理位置功能。

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P1 常用优先 | AWS Amplify | 前端/移动全栈开发和托管平台 | 托管 React、Next.js、Vue、Angular、Nuxt 等 Web 应用，提供 Git-based CI/CD、分支环境、全栈 serverless 后端和客户端库 | 想快速做 Web/移动应用，并把认证、API、存储、部署、预览环境串起来时 | Amplify 是面向前端开发者的组合体验；AppSync 是 GraphQL/PubSub API；Cognito 是身份服务 |
| P1 常用优先 | AWS AppSync | Serverless GraphQL 和实时 Pub/Sub API | 创建 GraphQL API、合并 API、订阅实时数据、WebSocket Pub/Sub、连接 DynamoDB/Lambda/OpenSearch/RDS 等数据源 | 前端需要一个统一 API 层，或者需要实时协作、聊天、通知、状态更新时 | AppSync 管 API 和实时通信；API Gateway 更通用 REST/HTTP/WebSocket；Amplify 可以使用 AppSync 作为后端 |
| P2 进阶架构 | AWS Device Farm | 真机 App 测试农场 | 在 AWS 托管的真实 Android/iOS 设备上自动化测试或远程交互测试移动/Web 应用 | 想在大量真实设备上跑 Appium/Espresso/XCUITest 等测试，或复现某机型问题时 | Device Farm 做测试；Amplify 做开发部署；CloudWatch/Synthetics 更偏 Web 可用性监控 |
| P2 进阶架构 | Amazon Location Service | 地图、地点、路线、围栏和追踪 | 给应用加入地图、地址搜索/地理编码、路径规划、geofence、设备/资产位置追踪 | 外卖、物流、出行、门店查找、资产追踪、位置提醒等 LBS 场景 | Location 提供地理位置能力；EventBridge 可接收 geofence 事件；不是通用数据库或 BI 地理分析平台 |

### Mobile 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要快速开发和部署前端/移动全栈应用 | AWS Amplify |
| 我要给前端提供 GraphQL API 或实时订阅 | AWS AppSync |
| 我要在真实手机和平板上测试 App | AWS Device Farm |
| 我要地图、地址搜索、路线、围栏、位置追踪 | Amazon Location Service |

### Mobile 学习顺序建议

1. 先学 `Amplify`：它最贴近日常前端/移动开发工作流。
2. 再学 `AppSync`：理解 GraphQL schema、resolver、authorization、subscription 和 Pub/Sub。
3. 有地图/物流/位置需求时学 `Amazon Location Service`。
4. App 进入测试和发布阶段后学 `Device Farm`，把真实设备测试放进 CI/CD。

### Mobile 状态备注

- `Amplify` 现在常见两条线：Amplify Hosting 负责 Git-based 托管和 CI/CD；Amplify Gen 2 使用 TypeScript code-first 定义后端。
- `AppSync` 不只是 GraphQL 查询；AWS 文档显示 2025-03-13 起可以用 AppSync Events 构建基于 WebSocket 的实时 Pub/Sub API。
- `Device Farm` 官方文档写明当前只在 `us-west-2` Oregon 区域可用；跨区域项目也要按这个区域创建测试资源。
- `Amazon Location Service` 的 Places、Maps、Routes API 有新版文档；旧版文档页面会提示跳转到新版 API 说明。

## Category: Anwendungsintegration / Application Integration / 应用集成

应用集成类服务可以按消息模式理解：`编排流程`、`发布订阅`、`队列缓冲`、`事件路由`、`托管消息代理`、`SaaS 数据同步`、`数据管道调度`、`B2B/EDI 集成`。

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P0 核心必学 | AWS Step Functions | Serverless 工作流编排 | 用状态机把 Lambda、ECS、Glue、Batch、Bedrock、SNS、SQS、EventBridge 等步骤串成可视化流程，支持重试、分支、并行、人工回调 | 业务流程有多个步骤、失败处理、等待、审批、长流程或微服务编排时 | Step Functions 管“步骤顺序和状态”；EventBridge 管“事件路由”；SQS/SNS 管“消息传递” |
| P2 进阶架构 | Amazon AppFlow | SaaS 与 AWS 数据集成 | 在 Salesforce、ServiceNow、Zendesk、Slack 等 SaaS 与 S3、Redshift、Snowflake 等之间创建无代码数据流 | 想把 SaaS 数据定时/按需同步到数据湖或数仓，不想自己写连接器时 | AppFlow 偏 SaaS 数据同步；EventBridge 偏事件驱动；Glue 偏通用 ETL 和数据工程 |
| P2 进阶架构 | Amazon MQ | 托管消息代理 | 托管 Apache ActiveMQ Classic 或 RabbitMQ broker，支持标准消息协议，迁移现有消息中间件 | 已有 JMS/AMQP/MQTT/STOMP/RabbitMQ/ActiveMQ 应用，希望少改代码迁移到 AWS 时 | Amazon MQ 适合兼容传统 broker；SQS/SNS 是云原生托管消息服务，运维更轻 |
| P1 常用优先 | Amazon SNS | 发布订阅通知服务 | 把消息发布到 topic，再 fan-out 给 SQS、Lambda、HTTP/S、Email、SMS、Firehose、移动推送等订阅者 | 一个事件要同时通知多个系统、用户或通道时 | SNS 是 pub/sub fan-out；SQS 是队列缓冲；EventBridge 是更强的事件路由和 schema/filtering |
| P0 核心必学 | Amazon SQS | 托管消息队列 | 在生产者和消费者之间异步传递消息，解耦系统，支持 Standard/FIFO queue、DLQ、visibility timeout | 需要削峰填谷、异步处理、任务队列、失败重试、消费者慢慢处理时 | SQS 是队列；SNS 是广播；EventBridge 是事件总线；Amazon MQ 是兼容传统 broker |
| P4 存量/谨慎 | Amazon Simple Workflow Service | 老一代分布式工作流服务 | 协调有顺序/并行步骤的后台任务，维护任务状态，由 worker 和 decider 共同推进流程 | 主要用于维护已有 SWF 系统 | AWS 文档建议大多数工作流和编排需求优先考虑 Step Functions |
| P2 进阶架构 | Amazon Managed Workflows for Apache Airflow | 托管 Apache Airflow | 运行、调度、监控 Airflow DAG，编排数据工程、ETL、ML、跨系统批处理任务 | 团队已有 Airflow/Python DAG 生态，或需要大量数据管道调度和开源 operator 时 | MWAA 偏数据管道调度；Step Functions 偏 serverless 应用流程编排；Glue Workflows 偏 Glue 内部 ETL 编排 |
| P3 专项场景 | AWS B2B Data Interchange | 托管 B2B/EDI 文档转换 | 在 EDI 标准如 X12、EDIFACT、HL7v2 与 JSON/XML 之间自动转换和生成交易文档 | 供应链、零售、医疗、物流等要和交易伙伴交换 EDI 文档时 | B2B Data Interchange 管 EDI 转换；Transfer Family 管文件传输；AppFlow 管 SaaS 数据流 |
| P0 核心必学 | Amazon EventBridge | Serverless 事件总线、Pipes 和 Scheduler | 从 AWS 服务、自有应用、SaaS 接收事件，按规则过滤、转换并路由到目标；也可用 Pipes 做点对点集成、Scheduler 做定时调用 | 构建事件驱动架构、跨服务自动化、SaaS 事件接入、定时任务、点对点无代码管道时 | EventBridge 是事件路由中心；SNS 更像主题广播；SQS 是队列；Step Functions 是流程编排 |

### Application Integration 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要把多个步骤编排成可靠流程 | AWS Step Functions |
| 我要一个事件广播给多个订阅方 | Amazon SNS |
| 我要异步队列、削峰填谷、失败重试 | Amazon SQS |
| 我要事件驱动架构、事件过滤和路由 | Amazon EventBridge |
| 我要点对点集成并加过滤/转换/增强 | Amazon EventBridge Pipes |
| 我要定时触发任务 | Amazon EventBridge Scheduler |
| 我要兼容 RabbitMQ/ActiveMQ 或传统消息协议 | Amazon MQ |
| 我要 SaaS 数据同步到 S3/Redshift/Snowflake | Amazon AppFlow |
| 我要托管 Airflow DAG 和数据管道调度 | Amazon MWAA |
| 我要 EDI 和 JSON/XML 文档转换 | AWS B2B Data Interchange |
| 我看到 SWF | 当存量工作流服务理解，新项目优先看 Step Functions |

### Application Integration 学习顺序建议

1. 先学 `SQS`：理解队列、消费者、visibility timeout、DLQ、Standard/FIFO。
2. 再学 `SNS`：理解 topic、subscription、fan-out，以及 SNS 到 SQS 的组合。
3. 学 `EventBridge`：理解 event bus、rule、event pattern、target、Pipes、Scheduler。
4. 学 `Step Functions`：理解 Standard/Express workflow、state、retry/catch、Map/Parallel、service integration。
5. 再按场景补 `Amazon MQ`、`AppFlow`、`MWAA`、`B2B Data Interchange`；`SWF` 主要读懂历史系统即可。

### Application Integration 状态备注

- `SNS`、`SQS`、`EventBridge` 不要混：SNS 是发布订阅广播；SQS 是队列缓冲；EventBridge 是事件总线和事件路由，还包含 Pipes 与 Scheduler。
- `Step Functions` 和 `EventBridge` 不要混：Step Functions 负责“一个流程内部的步骤和状态”；EventBridge 负责“不同系统之间事件如何路由”。
- `Amazon MQ` 适合迁移 RabbitMQ/ActiveMQ 等 broker 应用；如果是新建云原生异步系统，通常先看 SQS/SNS/EventBridge。
- `Amazon SWF`：AWS 官方文档写明大多数工作流和编排需求建议考虑 `AWS Step Functions`；新项目一般不从 SWF 起步。
- `Amazon EventBridge` 是 CloudWatch Events 的演进；旧 CloudWatch Events API 仍兼容，但新能力主要加在 EventBridge。
- `Amazon MWAA`：Amazon Managed Workflows for Apache Airflow 是托管 Airflow 环境；AWS 文档也出现 `Amazon MWAA Serverless` 作为新的部署选项，实际可用性以所在 Region 控制台为准。

## Category: Geschäftsanwendungen / Business Applications / 业务应用

业务应用类服务主要面向最终业务团队：`联络中心`、`邮件和客户触达`、`办公协作`、`安全通信`、`SaaS 互联`、`行业业务应用`。

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P2 进阶架构 | Amazon Connect Customer Profiles | 客户 360 资料 | 把 Amazon Connect 联系记录和 Salesforce、Zendesk、ServiceNow 等 CRM/外部数据合并成统一客户档案 | 呼叫中心坐席需要在一个界面看到客户身份、历史联系、案例、订单和属性时 | Customer Profiles 管客户资料；Amazon Connect 管联络中心；Pinpoint/Connect outbound campaigns 管主动触达 |
| P4 存量/谨慎 | Amazon Chime | 在线会议、聊天和通话应用 | 会议、视频、语音、聊天、屏幕共享等企业协作 | 只用于理解旧系统或迁移遗留环境 | Amazon Chime 服务已在 2026-02-20 停止支持；需要嵌入实时音视频能力时看 Amazon Chime SDK |
| P1 常用优先 | Amazon Simple Email Service | 大规模邮件发送/接收服务 | 发送交易邮件、营销邮件、通知邮件，也可接收邮件并触发后端流程 | 应用需要稳定发送验证码、订单确认、通知、newsletter，或处理入站邮件时 | SES 是开发者邮件基础设施；WorkMail 是企业邮箱；Pinpoint 邮件触达进入迁移期 |
| P4 存量/谨慎 | Amazon WorkDocs | 企业文档存储和协作 | 文件存储、共享、评论、审阅、WorkDocs Drive | 仅用于识别或迁移遗留 WorkDocs 数据 | AWS General Reference 显示 Amazon WorkDocs 已在 2025-04-25 full shutdown |
| P4 存量/谨慎 | Amazon WorkMail | 托管企业邮箱和日历 | 企业邮件、日历、联系人，兼容 Outlook、移动设备和 IMAP | 仅适合已有 WorkMail 客户规划迁移 | 2026-04-30 起不再接受新客户，2027-03-31 停止支持；新项目看第三方邮箱或托管协作套件 |
| P3 专项场景 | Amazon Connect Health | 医疗场景 AI 联络中心应用 | 基于 Amazon Connect 自动化患者互动、预约管理、身份验证，并辅助临床记录 | 医疗机构希望把语音患者服务、EHR/FHIR、临床文档辅助结合起来时 | 属于医疗行业专用业务应用；不是通用 Amazon Connect，也不是医疗诊断设备 |
| P3 专项场景 | Amazon Connect Decisions | 供应链 AI 决策应用 | 用 AI teammates 做需求预测、供应计划、异常监控、根因分析和决策执行 | 供应链团队希望把计划、预测、库存和 ERP/规划系统中的决策流程智能化时 | 名字里有 Connect，但不是呼叫中心；它是供应链 planning/decisioning 应用 |
| P4 存量/谨慎 | Amazon Pinpoint | 客户触达、旅程和营销活动 | 用户分群、campaign、journey、消息模板、analytics，跨 email/SMS/push/voice/custom channel 触达 | 主要用于已有 Pinpoint 项目迁移 | 2025-05-20 起不再接受新客户，2026-10-30 停止支持；消息通道迁到 AWS End User Messaging，邮件迁到 SES，营销旅程迁到 Amazon Connect |
| P3 专项场景 | AWS Wickr | 端到端加密安全通信 | 加密消息、群聊、语音/视频、文件共享、屏幕共享、数据保留和审计 | 政府、金融、法律、应急等需要强安全通信和留痕控制的组织 | Wickr 是安全协作应用；Chime 是会议应用；Chime SDK 是嵌入式实时通信组件 |
| P2 进阶架构 | AWS AppFabric | SaaS 应用互联和安全/生产力层 | 连接多个 SaaS 应用，标准化安全数据，也提供生成式 AI 生产力能力 | IT/安全团队想统一管理 SaaS 应用事件，或让员工跨 SaaS 应用完成任务时 | AppFabric 连 SaaS 应用；AppFlow 同步 SaaS 数据；Security Lake 存安全日志 |
| P1 常用优先 | AWS End User Messaging | 终端用户消息通道 | 发送 SMS、MMS、语音、移动 Push、WhatsApp/Social、OTP、号码验证等 A2P 消息 | 应用要给用户发验证码、提醒、营销短信、推送、WhatsApp 消息或语音通知时 | 这是 Pinpoint 消息通道的延续；SES 负责邮件；Pinpoint 的 engagement 功能在迁移/停服路径中 |
| P2 进阶架构 | Amazon Chime SDK | 嵌入式实时通信 SDK | 给自己的 Web/移动应用加入音频、视频、屏幕共享、消息、媒体管道、PSTN 音频能力 | 要自己做远程医疗、在线课堂、客服视频、协作工具或游戏语音时 | Chime SDK 是开发组件；Amazon Chime 应用已停止支持；不要把 SDK 和 Chime App 混为一谈 |

### Business Applications 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要发交易邮件、通知邮件、营销邮件 | Amazon SES |
| 我要发 SMS/MMS/Push/WhatsApp/OTP/语音 | AWS End User Messaging |
| 我要做联络中心客户 360 档案 | Amazon Connect Customer Profiles |
| 我要医疗患者互动和临床文档辅助 | Amazon Connect Health |
| 我要供应链预测、计划和 AI 决策 | Amazon Connect Decisions |
| 我要端到端加密企业通信 | AWS Wickr |
| 我要连接多个 SaaS 做安全/生产力治理 | AWS AppFabric |
| 我要在自己 App 里嵌入音视频/消息能力 | Amazon Chime SDK |
| 我看到 Chime、WorkDocs、WorkMail、Pinpoint | 先看状态备注，新项目通常不要从这些服务起步 |

### Business Applications 学习顺序建议

1. 先学 `SES` 和 `End User Messaging`：一个负责邮件，一个负责 SMS/Push/WhatsApp/语音等消息通道。
2. 再学 `Amazon Connect Customer Profiles`：理解联络中心里的客户档案和外部 CRM 数据整合。
3. 学 `Chime SDK`：理解嵌入式实时通信和已经停服的 Chime 应用之间的区别。
4. 按行业补充 `Connect Health`、`Connect Decisions`、`Wickr`、`AppFabric`。
5. `Chime`、`WorkDocs`、`WorkMail`、`Pinpoint` 重点学习迁移和历史架构，不作为新项目首选。

### Business Applications 状态备注

- `Amazon Connect Customer`：控制台截图里的名称很可能是 `Amazon Connect Customer Profiles` 的截断显示；这里按官方文档中的 Customer Profiles 解释。
- `Amazon Chime`：AWS 文档显示服务已在 2026-02-20 停止支持；这不影响 `Amazon Chime SDK` 服务本身，但 `Amazon Chime SDK - Proxy Sessions` 已在 2026-03-31 full shutdown。
- `Amazon WorkDocs`：AWS General Reference 的 full shutdown 列表显示 Amazon WorkDocs 已在 2025-04-25 full shutdown。
- `Amazon WorkMail`：2026-04-30 起不再接受新客户，2027-03-31 停止支持；今天是 2026-04-30，正好进入“不接受新客户”的时间点。
- `Amazon Pinpoint`：2025-05-20 起不再接受新客户，2026-10-30 停止支持；SMS、Voice、Mobile Push、OTP、Phone Number Validate 等 API 迁到 `AWS End User Messaging`，邮件场景优先迁到 `SES`。
- `Amazon Connect Health`：官方文档强调它不是 medical device，AI 生成信息可能有错误，临床文档和患者护理需要医疗专业人员审核。
- `Amazon Connect Decisions`：官方文档显示当前支持 `US East (N. Virginia)` 和 `Europe (Ireland)`，并要求 IAM Identity Center 与实例在同一 Region。

## Category: Endbenutzer-Datenverarbeitung / End User Computing / 终端用户计算

终端用户计算类服务主要解决企业员工如何安全访问桌面、应用和浏览器：`云桌面`、`应用流式传输`、`浏览器隔离`、`终端硬件`。

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P1 常用优先 | Amazon WorkSpaces | 云桌面/虚拟桌面 | 为员工提供 Windows、Amazon Linux、Ubuntu、Rocky Linux、RHEL 等云端桌面，支持 Personal/Pools、按月/按小时计费 | 远程办公、临时人员、呼叫中心、开发桌面、安全隔离办公环境时 | WorkSpaces 提供完整桌面；WorkSpaces Applications 只流式传输应用；Secure Browser 只隔离浏览器 |
| P2 进阶架构 | Amazon WorkSpaces Applications | 桌面应用流式传输 | 把 Windows/Linux 桌面应用从 AWS 流式传输给用户，用户无需本地安装应用 | 企业有专业软件、旧 Windows 应用、开发/设计工具，希望集中交付和管理时 | 原 AppStream 2.0 体系；它传应用，不是完整桌面；比 WorkSpaces 更轻 |
| P4 存量/谨慎 | Amazon WorkSpaces Thin Client | AWS 云桌面专用瘦客户端设备 | 小型硬件终端连接 WorkSpaces、WorkSpaces Applications、Secure Browser，减少本地数据和设备管理 | 只适合已有设备客户规划替代方案 | 2026-04-20 起不再接受新客户，2027-03-31 停止支持；新项目看第三方瘦客户端或普通受管设备 |
| P2 进阶架构 | Amazon WorkSpaces Secure Browser | 云端隔离浏览器 | 从一次性云端容器运行浏览器，把网页内容流式传输给用户，保护私有网站/SaaS/互联网访问 | 供应商访问内网 Web、员工访问高风险网站、SaaS 数据防外泄、无需 VPN 的浏览器访问时 | Secure Browser 隔离浏览器；WorkSpaces 是完整桌面；Applications 是桌面应用流 |

### End User Computing 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要给员工提供完整云桌面 | Amazon WorkSpaces |
| 我要只交付某些桌面应用 | Amazon WorkSpaces Applications |
| 我要隔离浏览器访问网站/SaaS/内网 Web | Amazon WorkSpaces Secure Browser |
| 我看到 WorkSpaces Thin Client | 当存量硬件和迁移场景理解，新项目谨慎 |

### End User Computing 学习顺序建议

1. 先学 `WorkSpaces`：理解目录、用户、bundle、协议、镜像、Personal 和 Pools。
2. 再学 `WorkSpaces Secure Browser`：理解 browser isolation、门户、策略、剪贴板/文件传输控制。
3. 有传统桌面应用交付需求时学 `WorkSpaces Applications`。
4. `WorkSpaces Thin Client` 重点看停止支持时间线和替代方案。

### End User Computing 状态备注

- `WorkSpaces Applications` 文档仍大量保留 `AppStream 2.0` 路径和术语；学习时把它理解成 AWS 应用流式传输服务。
- `WorkSpaces Thin Client`：AWS 文档显示 2026-04-20 起不再接受新客户，2027-03-31 停止支持；这不代表 WorkSpaces、WorkSpaces Applications、WorkSpaces Secure Browser 停用。
- `WorkSpaces Secure Browser` 以前叫 `Amazon WorkSpaces Web`；现在官方名称是 Amazon WorkSpaces Secure Browser。

## Category: Internet of Things / IoT / 物联网

IoT 类服务可以按设备生命周期理解：`连接设备`、`管理设备`、`保护设备`、`边缘运行`、`工业数据建模`、`数字孪生`、`事件检测`、`车联网数据采集`。

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P1 常用优先 | AWS IoT Device Defender | IoT 设备安全审计和异常检测 | 审计 IoT policy/cert/config，监控云端和设备端安全指标，检测异常行为并触发告警/缓解动作 | 设备数量多、证书和策略复杂，需要持续检查设备安全基线和异常流量时 | Device Defender 管安全；Device Management 管运维；IoT Core 管连接和消息 |
| P1 常用优先 | AWS IoT Device Management | IoT 设备运维管理 | 通过 Jobs、Fleet indexing、Software Package Catalog、Commands 等能力管理、搜索、更新和远程操作设备 | 需要 OTA 更新、批量操作、查找设备状态、按属性/影子/连接状态组织设备时 | Device Management 管设备生命周期；IoT Core 提供 registry、shadow、message broker；Defender 管安全 |
| P2 进阶架构 | AWS IoT Greengrass | IoT 边缘运行时 | 在本地设备上运行组件、Lambda、Docker/native 进程，做本地消息、数据处理、ML 推理，并同步到云 | 设备需要离线运行、本地低延迟处理、边缘聚合、工厂/网关部署时 | Greengrass 在边缘运行应用；IoT Core 在云端连接设备；SiteWise Edge 偏工业数据采集 |
| P2 进阶架构 | AWS IoT SiteWise | 工业设备数据采集和资产建模 | 从 OPC UA、SiteWise Edge、API 等收集工业数据，建立 asset model，计算指标，做工业监控 | 制造、能源、公用事业、楼宇等需要采集设备时序数据和 OEE/MTBF 等指标时 | SiteWise 管工业资产和时序数据；TwinMaker 用这些数据构建数字孪生可视化 |
| P0 核心必学 | AWS IoT Core | IoT 设备连接和消息中心 | 用 MQTT/MQTT over WebSocket/HTTPS/LoRaWAN 连接设备，管理 thing、证书、policy、shadow、rules engine | 任何 AWS IoT 方案的设备接入、消息发布订阅、规则转发和设备身份基础 | IoT Core 是底座；Device Management/Defender/Greengrass/SiteWise 都围绕它扩展能力 |
| P2 进阶架构 | AWS IoT TwinMaker | 工业数字孪生建模和可视化 | 把设备、空间、流程、传感器、摄像头、SiteWise/Kinesis Video 等数据建成数字孪生，并在 Grafana/3D 场景展示 | 工厂、楼宇、能源设施要做运营数字孪生、3D 场景监控、跨数据源可视化时 | TwinMaker 负责数字孪生和场景；SiteWise 负责工业数据采集/建模；Grafana 负责展示 |
| P2 进阶架构 | AWS IoT Events | IoT 复杂事件检测 | 根据传感器数据和状态机 detector model 识别故障、状态变化和异常事件，并触发 SNS/Lambda/SQS/IoT Core 等动作 | 设备/工业流程有多传感器条件、状态转移、故障预警和告警自动化时 | IoT Events 管设备状态和事件检测；EventBridge 管通用事件路由；CloudWatch Alarms 管指标阈值 |
| P4 存量/谨慎 | AWS IoT FleetWise | 车联网数据采集和建模 | 从车辆采集、建模、筛选和上传 CAN/车载数据，用于车队健康、驾驶辅助、自动驾驶分析 | 只适合已有 FleetWise 客户继续使用或迁移参考 | 2026-04-30 起不再对新客户开放；新车联网方案可参考 Connected Mobility on AWS Guidance 组合 IoT Core/Kafka/Flink/S3 等能力 |

### IoT 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要让设备安全连接 AWS 并发布/订阅消息 | AWS IoT Core |
| 我要批量更新、搜索、远程操作设备 | AWS IoT Device Management |
| 我要审计设备安全配置和检测异常行为 | AWS IoT Device Defender |
| 我要在边缘设备本地运行逻辑/容器/ML | AWS IoT Greengrass |
| 我要采集工业设备数据、建资产模型和指标 | AWS IoT SiteWise |
| 我要做工厂/楼宇/设施数字孪生 | AWS IoT TwinMaker |
| 我要按设备状态机识别复杂事件 | AWS IoT Events |
| 我要采集车辆数据 | 已有客户看 AWS IoT FleetWise，新客户看 Connected Mobility guidance |

### IoT 学习顺序建议

1. 先学 `IoT Core`：thing、certificate、policy、MQTT topic、shadow、rules engine。
2. 再学 `Device Management` 和 `Device Defender`：一个管运维，一个管安全。
3. 学 `Greengrass`：理解边缘运行、component、deployment、离线/本地处理。
4. 工业场景学 `SiteWise`、`IoT Events`、`TwinMaker`。
5. 车联网场景再看 `IoT FleetWise` 的历史能力和可替代架构。

### IoT 状态备注

- `AWS IoT Core` 是 IoT 底座；不要把它和 `AWS IoT` 这个产品族总称混在一起。
- `AWS IoT Greengrass V1` 将在 2026-10-07 停止支持；新项目使用 Greengrass V2。
- `Fleet Hub for AWS IoT Device Management` 已在 2025-10-18 full shutdown；这不等于 IoT Device Management 整体停用。
- `AWS IoT FleetWise`：2026-04-30 起不再对新客户开放；已有客户可继续使用，但 AWS 文档说明不会再新增功能。
- `AWS IoT TwinMaker` 官方文档提醒它不应用于会导致严重人身伤害、死亡或财产/环境损害的危险或关键系统运行，也不能替代人类对物理系统安全状态的监控。

## Category: Spieleentwicklung / Game Development / 游戏开发

游戏开发类目目前主要分两类：`多人游戏服务器托管` 和 `云游戏/互动应用流式传输`。

| 重要性 | AWS 服务 | 中文理解 | 主要用途 | 适合什么时候用 | 和相近服务的区别 |
| --- | --- | --- | --- | --- | --- |
| P2 进阶架构 | Amazon GameLift Servers | 托管多人游戏服务器 | 部署、运行、扩缩容 session-based multiplayer game server，支持 managed EC2、containers、Anywhere、FleetIQ、FlexMatch | 游戏需要低延迟专用服务器、全球匹配、玩家会话、自动扩缩容和服务器进程管理时 | GameLift Servers 托管“游戏服务器”；普通 EC2/ECS 也能跑服务器但要自己做会话、匹配、伸缩和运维 |
| P3 专项场景 | Amazon GameLift Streams | 云游戏/互动应用流式传输 | 直接从 AWS 云端运行 Windows/Linux/Proton 应用或游戏，把 1080p/60fps 低延迟画面流到浏览器 | 想让用户无需下载即可试玩/游玩游戏，或流式传输交互式 3D/仿真应用时 | GameLift Streams 流式传输“画面和交互”；GameLift Servers 托管多人游戏后端服务器 |

### Game Development 快速选择

| 需求 | 优先看 |
| --- | --- |
| 我要托管多人游戏专用服务器、匹配和玩家会话 | Amazon GameLift Servers |
| 我要把游戏或互动应用云端运行并串流到浏览器 | Amazon GameLift Streams |

### Game Development 学习顺序建议

1. 先学 `GameLift Servers`：理解 fleet、build/container、game session、player session、placement queue、FlexMatch、Anywhere。
2. 再学 `GameLift Streams`：理解 application、stream group、stream session、capacity、S3 应用包、区域和成本。
3. 补充周边 AWS 服务：`DynamoDB/Aurora DSQL` 存玩家状态，`S3/CloudFront` 分发资源，`Cognito` 做玩家身份，`Kinesis/S3` 做游戏分析，`Chime SDK` 做语音。

### Game Development 状态备注

- `Amazon GameLift Servers` 是原 Amazon GameLift 游戏服务器能力的新命名方式，文档中仍会看到 `gamelift` 相关 API/路径。
- `Amazon GameLift Streams` 不是游戏服务器托管，而是云端运行应用并把交互画面流给玩家/用户；成本重点在 stream capacity 和 idle capacity。

## 参考资料

- AWS Global View 文档：https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/global-view.html
- AWS Parallel Computing Service 文档：https://docs.aws.amazon.com/pcs/latest/userguide/what-is-service.html
- AWS Containers 概览：https://docs.aws.amazon.com/whitepapers/latest/aws-overview/containers.html
- AWS 容器服务选择指南：https://docs.aws.amazon.com/decision-guides/latest/containers-on-aws-how-to-choose/choosing-aws-container-service.html
- Containers on AWS：https://aws.amazon.com/containers/
- Amazon S3 文档：https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html
- Amazon EFS 文档：https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html
- Amazon FSx for Windows File Server 文档：https://docs.aws.amazon.com/fsx/latest/WindowsGuide/what-is.html
- Amazon S3 Glacier 存储类别文档：https://docs.aws.amazon.com/AmazonS3/latest/userguide/glacier-storage-classes.html
- AWS Storage Gateway 文档：https://docs.aws.amazon.com/storagegateway/latest/tgw/WhatIsStorageGateway.html
- AWS Backup 文档：https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html
- Recycle Bin 文档：https://docs.aws.amazon.com/ebs/latest/userguide/recycle-bin.html
- AWS Elastic Disaster Recovery 文档：https://docs.aws.amazon.com/drs/latest/userguide/what-is-drs.html
- Amazon Aurora 文档：https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html
- Amazon ElastiCache 文档：https://docs.aws.amazon.com/AmazonElastiCache/latest/UserGuide/RedisAOF.html
- Amazon Neptune 文档：https://docs.aws.amazon.com/neptune/latest/userguide/intro.html
- Amazon DocumentDB 文档：https://docs.aws.amazon.com/documentdb/latest/developerguide/what-is.html
- Amazon Keyspaces 文档：https://docs.aws.amazon.com/keyspaces/latest/devguide/what-is-keyspaces.html
- Amazon Timestream 文档：https://docs.aws.amazon.com/timestream/latest/developerguide/what-is-timestream.html
- Amazon DynamoDB 文档：https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
- Amazon Aurora DSQL 文档：https://docs.aws.amazon.com/aurora-dsql/latest/userguide/what-is-aurora-dsql.html
- Amazon MemoryDB 文档：https://docs.aws.amazon.com/memorydb/latest/devguide/what-is-memorydb.html
- Oracle Database@AWS 公告：https://aws.amazon.com/about-aws/whats-new/2026/04/oracle-database-aws-available-twelve-regions/
- AWS Migration Hub 文档：https://docs.aws.amazon.com/migrationhub/latest/ug/whatishub.html
- AWS Application Migration Service 文档：https://docs.aws.amazon.com/mgn/latest/ug/what-is-application-migration-service.html
- AWS Application Discovery Service 文档：https://docs.aws.amazon.com/application-discovery/latest/userguide/what-is-appdiscovery.html
- AWS Database Migration Service 文档：https://docs.aws.amazon.com/dms/latest/userguide/Welcome.html
- AWS Transfer Family 文档：https://docs.aws.amazon.com/transfer/latest/userguide/what-is-aws-transfer-family.html
- AWS Snow Family 文档：https://docs.aws.amazon.com/zh_cn/whitepapers/latest/how-aws-pricing-works/aws-snow-family.html
- AWS DataSync 文档：https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html
- AWS Transform 文档：https://docs.aws.amazon.com/transform/latest/userguide/what-is-service.html
- AWS Mainframe Modernization 文档：https://docs.aws.amazon.com/m2/latest/userguide/what-is-m2.html
- Amazon Elastic VMware Service 文档：https://docs.aws.amazon.com/evs/latest/userguide/what-is-evs.html
- Amazon VPC 文档：https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html
- Amazon CloudFront 文档：https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html
- Amazon API Gateway 文档：https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html
- AWS Direct Connect 文档：https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html
- AWS App Mesh 文档：https://docs.aws.amazon.com/app-mesh/latest/userguide/what-is-app-mesh.html
- AWS Global Accelerator 文档：https://docs.aws.amazon.com/global-accelerator/latest/dg/what-is-global-accelerator.html
- Amazon Route 53 文档：https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html
- AWS Data Transfer Terminal 文档：https://docs.aws.amazon.com/datatransferterminal/latest/userguide/what-is-dtt.html
- Amazon Route 53 Global Resolver 文档：https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/gr-what-is-global-resolver.html
- AWS Cloud Map 文档：https://docs.aws.amazon.com/cloud-map/latest/dg/what-is-cloud-map.html
- AWS RTB Fabric 文档：https://docs.aws.amazon.com/rtb-fabric/latest/userguide/what-is-rtb-fabric.html
- Amazon Application Recovery Controller 文档：https://docs.aws.amazon.com/r53recovery/latest/dg/what-is-route53-recovery.html
- AWS CodeCommit 文档：https://docs.aws.amazon.com/codecommit/latest/userguide/welcome.html
- AWS CodeCommit 恢复 GA 公告：https://aws.amazon.com/blogs/devops/aws-codecommit-returns-to-general-availability/
- AWS CodeBuild 文档：https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html
- AWS CodeDeploy 文档：https://docs.aws.amazon.com/codedeploy/latest/userguide/welcome.html
- AWS CodePipeline 文档：https://docs.aws.amazon.com/en_en/codepipeline/latest/userguide/concepts-continuous-delivery-integration.html
- AWS Cloud9 文档：https://docs.aws.amazon.com/cloud9/latest/user-guide/welcome.html
- AWS Cloud9 产品页：https://aws.amazon.com/cloud9/
- AWS CloudShell 文档：https://docs.aws.amazon.com/cloudshell/latest/userguide/welcome.html
- AWS X-Ray 文档：https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html
- AWS FIS 文档：https://docs.aws.amazon.com/fis/latest/userguide/what-is.html
- AWS Infrastructure Composer 文档：https://docs.aws.amazon.com/infrastructure-composer/latest/dg/what-is-composer.html
- AWS App Studio 文档：https://docs.aws.amazon.com/appstudio/latest/userguide/welcome.html
- AWS DevOps Agent 文档：https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent.html
- AWS AppConfig 文档：https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html
- AWS CodeArtifact 文档：https://docs.aws.amazon.com/codeartifact/latest/ug/welcome.html
- Amazon Q Developer 文档：https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/what-is.html
- Amazon CodeCatalyst 文档：https://docs.aws.amazon.com/codecatalyst/latest/userguide/welcome.html
- Amazon CodeCatalyst 迁移说明：https://docs.aws.amazon.com/codecatalyst/latest/userguide/migration.html
- Kiro 文档：https://kiro.dev/docs/
- Kiro 身份认证说明：https://kiro.dev/docs/getting-started/authentication/
- AWS IQ 文档：https://docs.aws.amazon.com/aws-iq/latest/user-guide/what-is-aws-iq.html
- AWS IQ 停止支持说明：https://docs.aws.amazon.com/aws-iq/latest/experts-user-guide/aws-iq-end-of-support.html
- AWS Managed Services 文档：https://docs.aws.amazon.com/managedservices/latest/userguide/what-is-ams.html
- AWS Activate for Startups：https://aws.amazon.com/activate
- AWS Activate Credits：https://aws.amazon.com/startups/credits
- AWS re:Post Private 文档：https://docs.aws.amazon.com/repostprivate/latest/userguide/what-is.html
- AWS Support plans 文档：https://docs.aws.amazon.com/awssupport/latest/user/aws-support-plans.html
- AWS Support plans 比较：https://aws.amazon.com/premiumsupport/plans
- Amazon Managed Blockchain 文档：https://docs.aws.amazon.com/managed-blockchain/latest/hyperledger-fabric-dev/what-is-managed-blockchain.html
- AWS Ground Station 文档：https://docs.aws.amazon.com/ground-station/latest/ug/what-is.html
- Amazon Braket 文档：https://docs.aws.amazon.com/braket/latest/developerguide/what-is-braket.html
- AWS Organizations 文档：https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html
- Amazon CloudWatch 文档：https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html
- AWS Auto Scaling 文档：https://docs.aws.amazon.com/autoscaling/plans/userguide/what-is-a-scaling-plan.html
- AWS CloudFormation 入门：https://docs.aws.amazon.com/console/cloudformation
- AWS Config 文档：https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html
- AWS Service Catalog 文档：https://docs.aws.amazon.com/servicecatalog/latest/adminguide/introduction.html
- AWS Systems Manager 文档：https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html
- AWS Trusted Advisor：https://aws.amazon.com/trustedadvisor/
- AWS Control Tower 文档：https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html
- AWS Well-Architected Tool 文档：https://docs.aws.amazon.com/wellarchitected/latest/userguide/intro.html
- Amazon Q Developer in chat applications 文档：https://docs.aws.amazon.com/chatbot/latest/adminguide/what-is.html
- Amazon Q Developer in chat applications 改名说明：https://docs.aws.amazon.com/chatbot/latest/adminguide/service-rename.html
- AWS Launch Wizard for SAP 文档：https://docs.aws.amazon.com/launchwizard/latest/userguide/launch-wizard-sap
- AWS Compute Optimizer 文档：https://docs.aws.amazon.com/compute-optimizer/latest/ug/what-is-compute-optimizer.html
- AWS Resource Groups 文档：https://docs.aws.amazon.com/ARG/latest/userguide/resource-groups.html
- AWS Tag Editor 文档：https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html
- Amazon Managed Grafana 文档：https://docs.aws.amazon.com/grafana/latest/userguide/what-is-Amazon-Managed-Service-Grafana.html
- Amazon Managed Service for Prometheus 文档：https://docs.aws.amazon.com/prometheus/latest/userguide/what-is-Amazon-Managed-Service-Prometheus.html
- AWS Resilience Hub 文档：https://docs.aws.amazon.com/resilience-hub/latest/userguide/what-is.html
- AWS Systems Manager Incident Manager 文档：https://docs.aws.amazon.com/incident-manager/latest/userguide/what-is-incident-manager.html
- AWS for SAP 概览：https://docs.aws.amazon.com/sap/latest/general/overview-sap-on-aws.html
- AWS Telco Network Builder 文档：https://docs.aws.amazon.com/tnb/latest/ug/what-is-tnb.html
- AWS Health 文档：https://docs.aws.amazon.com/health/latest/ug/what-is-aws-health.html
- AWS Proton 文档：https://docs.aws.amazon.com/proton/latest/userguide/Welcome.html
- AWS Proton 停止支持说明：https://docs.aws.amazon.com/proton/latest/userguide/proton-end-of-support.html
- AWS Sustainability 文档：https://docs.aws.amazon.com/sustainability/latest/userguide/what-is-sustainability.html
- AWS User Notifications 文档：https://docs.aws.amazon.com/notifications/latest/userguide/what-is-service.html
- AWS Partner Central 文档：https://docs.aws.amazon.com/partner-central/latest/getting-started/what-is-partner-central.html
- AWS CloudTrail 文档：https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html
- AWS License Manager 文档：https://docs.aws.amazon.com/license-manager/latest/userguide/license-manager.html
- AWS Resource Explorer 文档：https://docs.aws.amazon.com/resource-explorer/latest/userguide/welcome.html
- Service Quotas 文档：https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html
- Amazon Kinesis Video Streams 文档：https://docs.aws.amazon.com/en_us/kinesisvideostreams/latest/dg/what-is-kinesis-video.html
- AWS Elemental MediaConvert 文档：https://docs.aws.amazon.com/mediaconvert/latest/ug/what-is.html
- AWS Elemental MediaLive 文档：https://docs.aws.amazon.com/medialive/latest/ug/what-is.html
- AWS Elemental MediaPackage 文档：https://docs.aws.amazon.com/mediapackage/latest/userguide/what-is.html
- AWS Elemental MediaStore 文档：https://docs.aws.amazon.com/mediastore/latest/ug/what-is.html
- AWS Elemental MediaStore 停止支持说明：https://docs.aws.amazon.com/managedservices/latest/userguide/elemental-media-store.html
- AWS Elemental MediaTailor 文档：https://docs.aws.amazon.com/mediatailor/latest/ug/what-is.html
- AWS Elemental Appliances & Software 文档：https://docs.aws.amazon.com/elemental-appliances-software/latest/ug/what-is.html
- Amazon IVS Low-Latency Streaming 文档：https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/what-is.html
- Amazon IVS Real-Time Streaming 文档：https://docs.aws.amazon.com/ivs/latest/RealTimeUserGuide/what-is.html
- AWS Elemental Inference 文档：https://docs.aws.amazon.com/elemental-inference/latest/userguide/what-is.html
- AWS Elemental Inference 与 MediaLive：https://docs.aws.amazon.com/medialive/latest/ug/elemental-inference.html
- AWS Deadline Cloud 文档：https://docs.aws.amazon.com/deadline-cloud/latest/userguide/what-is-deadline-cloud.html
- AWS Elemental MediaConnect 文档：https://docs.aws.amazon.com/mediaconnect/latest/ug/what-is.html
- Amazon SageMaker AI 文档：https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html
- 下一代 Amazon SageMaker 文档：https://docs.aws.amazon.com/next-generation-sagemaker/latest/userguide/what-is-sagemaker.html
- Amazon Augmented AI API 文档：https://docs.aws.amazon.com/augmented-ai/2019-11-07/APIReference/Welcome.html
- Amazon CodeGuru Reviewer 文档：https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/welcome.html
- Amazon CodeGuru Reviewer 可用性变更：https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/codeguru-reviewer-availability-change.html
- Amazon CodeGuru Security 停止支持说明：https://docs.aws.amazon.com/codeguru/latest/security-ug/end-of-support.html
- Amazon DevOps Guru 文档：https://docs.aws.amazon.com/devops-guru/latest/userguide/welcome.html
- Amazon Comprehend 文档：https://docs.aws.amazon.com/comprehend/latest/dg/what-is.html
- Amazon Forecast 文档：https://docs.aws.amazon.com/forecast/latest/dg/what-is-forecast.html
- Amazon Forecast 文档历史：https://docs.aws.amazon.com/forecast/latest/dg/doc-history.html
- Amazon Fraud Detector 文档：https://docs.aws.amazon.com/frauddetector/latest/ug/what-is-frauddetector.html
- Amazon Fraud Detector 可用性变更：https://docs.aws.amazon.com/frauddetector/latest/ug/frauddetector-availability-change.html
- Amazon Kendra 文档：https://docs.aws.amazon.com/kendra/latest/dg/what-is-kendra.html
- Amazon Kendra 工作原理：https://docs.aws.amazon.com/kendra/latest/dg/how-it-works.html
- Amazon Personalize 文档：https://docs.aws.amazon.com/personalize/latest/dg/what-is-personalize.html
- Amazon Polly 文档：https://docs.aws.amazon.com/polly/latest/dg/what-is.html
- Amazon Rekognition 文档：https://docs.aws.amazon.com/rekognition/latest/dg/what-is.html
- Amazon Textract 文档：https://docs.aws.amazon.com/textract/latest/dg/what-is.html
- Amazon Transcribe 文档：https://docs.aws.amazon.com/transcribe/latest/dg/what-is.html
- Amazon Translate 文档：https://docs.aws.amazon.com/translate/latest/dg/what-is.html
- AWS Panorama 停止支持说明：https://docs.aws.amazon.com/panorama/latest/dev/panorama-end-of-support.html
- Amazon Monitron 文档：https://docs.aws.amazon.com/Monitron/latest/user-guide/what-is-monitron.html
- Amazon Monitron 文档历史：https://docs.aws.amazon.com/Monitron/latest/user-guide/doc-history.html
- AWS HealthLake 文档：https://docs.aws.amazon.com/healthlake/latest/devguide/what-is-amazon-health-lake.html
- Amazon Lookout for Equipment 文档：https://docs.aws.amazon.com/lookout-for-equipment/latest/ug/what-is.html
- Amazon Lookout for Equipment 文档历史：https://docs.aws.amazon.com/lookout-for-equipment/latest/ug/doc-history.html
- Amazon Q Business API 文档：https://docs.aws.amazon.com/amazonq/latest/api-reference/Welcome.html
- Amazon Q Business 说明：https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/rag-fully-managed-q-business.html
- AWS HealthOmics 文档：https://docs.aws.amazon.com/omics/latest/dev/what-is-healthomics.html
- Amazon Nova Act 文档：https://docs.aws.amazon.com/nova-act/latest/userguide/what-is-nova-act.html
- Amazon Bedrock 文档：https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html
- Amazon Bedrock AgentCore 文档：https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html
- Amazon Q Developer 文档：https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/what-is.html
- Amazon Comprehend Medical 文档：https://docs.aws.amazon.com/comprehend-medical/latest/dev/comprehendmedical-welcome.html
- Amazon Lex V2 文档：https://docs.aws.amazon.com/lexv2/latest/dg/what-is.html
- Amazon Bio Discovery 文档：https://aws.amazon.com/documentation-overview/bio-discovery/
- Amazon Bio Discovery 介绍：https://aws.amazon.com/biodiscovery/
- AWS HealthImaging 文档：https://docs.aws.amazon.com/healthimaging/latest/devguide/what-is.html
- Amazon Athena 文档：https://docs.aws.amazon.com/athena/latest/ug/what-is.html
- Amazon Redshift 文档：https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html
- Amazon CloudSearch 文档：https://docs.aws.amazon.com/cloudsearch/latest/developerguide/what-is-cloudsearch.html
- Amazon CloudSearch 新客户访问变更：https://docs.aws.amazon.com/managedservices/latest/onboardingguide/cloud-search.html
- Amazon OpenSearch Service 文档：https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html
- Amazon Kinesis Data Streams 文档：https://docs.aws.amazon.com/streams/latest/dev/introduction.html
- Amazon Quick 文档：https://docs.aws.amazon.com/quicksight/latest/user/using-quicksight-menu-and-landing-page.html
- Amazon Quick 工作原理：https://docs.aws.amazon.com/quick/latest/userguide/how-quicksuite-works.html
- AWS Data Exchange 文档：https://docs.aws.amazon.com/data-exchange/latest/userguide/what-is.html
- AWS Lake Formation 文档：https://docs.aws.amazon.com/lake-formation/latest/dg/what-is-lake-formation.html
- Amazon MSK 文档：https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html
- AWS Glue DataBrew 说明：https://docs.aws.amazon.com/prescriptive-guidance/latest/serverless-etl-aws-glue/databrew.html
- Amazon FinSpace 文档：https://docs.aws.amazon.com/finspace/latest/userguide/finspace-what-is.html
- Amazon FinSpace 停止支持说明：https://docs.aws.amazon.com/finspace/latest/userguide/amazon-finspace-end-of-support.html
- Amazon Managed Service for Apache Flink 文档：https://docs.aws.amazon.com/managed-flink/latest/java/what-is.html
- Amazon EMR 文档：https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-what-is-emr.html
- AWS Clean Rooms 文档：https://docs.aws.amazon.com/clean-rooms/latest/userguide/what-is.html
- Amazon SageMaker 文档：https://docs.aws.amazon.com/next-generation-sagemaker/latest/userguide/what-is-sagemaker.html
- AWS Entity Resolution 文档：https://docs.aws.amazon.com/entityresolution/latest/userguide/what-is-service.html
- AWS Glue 文档：https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html
- AWS Glue 文档历史：https://docs.aws.amazon.com/glue/latest/dg/doc-history.html
- Amazon Data Firehose 文档：https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html
- Amazon DataZone 文档：https://docs.aws.amazon.com/datazone/latest/userguide/what-is-datazone.html
- AWS Resource Access Manager 文档：https://docs.aws.amazon.com/ram/latest/userguide/what-is.html
- Amazon Cognito 文档：https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html
- AWS Secrets Manager 文档：https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html
- Amazon GuardDuty 文档：https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html
- Amazon Inspector 文档：https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html
- Amazon Macie 文档：https://docs.aws.amazon.com/macie/latest/userguide/macie-setting-up.html
- AWS IAM Identity Center 文档：https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html
- AWS Certificate Manager 文档：https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html
- AWS Key Management Service 文档：https://docs.aws.amazon.com/kms/latest/developerguide/overview.html
- AWS CloudHSM 文档：https://docs.aws.amazon.com/cloudhsm/latest/userguide/introduction.html
- AWS Directory Service 文档：https://docs.aws.amazon.com/directoryservice/latest/admin-guide/what_is.html
- AWS WAF、Shield、Firewall Manager 概览：https://docs.aws.amazon.com/console/waf/waf-overview
- AWS Artifact 文档：https://docs.aws.amazon.com/artifact/latest/ug/what-is-aws-artifact.html
- Amazon Detective 文档：https://docs.aws.amazon.com/detective/latest/userguide/what-is-detective.html
- AWS Signer 文档：https://docs.aws.amazon.com/signer/latest/developerguide/Welcome.html
- Amazon Security Lake 文档：https://docs.aws.amazon.com/security-lake/latest/userguide/what-is-security-lake.html
- AWS Security Agent 文档：https://docs.aws.amazon.com/securityagent/latest/userguide/what-is.html
- AWS Security Agent 工作方式：https://docs.aws.amazon.com/securityagent/latest/userguide/how-it-works.html
- Amazon Verified Permissions 文档：https://docs.aws.amazon.com/verifiedpermissions/latest/userguide/what-is-avp.html
- AWS Audit Manager 文档：https://docs.aws.amazon.com/audit-manager/latest/userguide/what-is.html
- AWS Security Hub CSPM 入门：https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-get-started.html
- AWS Security Hub 与 Security Hub CSPM：https://docs.aws.amazon.com/securityhub/latest/userguide/what-are-securityhub-services.html
- AWS IAM 文档：https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html
- AWS Private Certificate Authority 文档：https://docs.aws.amazon.com/privateca/latest/userguide/PcaWelcome.html
- AWS Payment Cryptography 文档：https://docs.aws.amazon.com/payment-cryptography/latest/userguide/what-is.html
- AWS Security Incident Response 文档：https://docs.aws.amazon.com/security-ir/latest/userguide/what-is.html
- AWS Marketplace 买家指南：https://docs.aws.amazon.com/marketplace/latest/buyerguide/what-is-marketplace.html
- AWS Billing Conductor 文档：https://docs.aws.amazon.com/billingconductor/latest/userguide/what-is-billingconductor.html
- AWS Billing and Cost Management 文档：https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-what-is.html
- AWS Amplify Hosting 文档：https://docs.aws.amazon.com/amplify/latest/userguide/welcome.html
- AWS Amplify API 参考说明：https://docs.aws.amazon.com/amplify/latest/APIReference/Welcome.html
- AWS AppSync 文档：https://docs.aws.amazon.com/appsync/latest/devguide/what-is-appsync
- AWS Device Farm 文档：https://docs.aws.amazon.com/devicefarm/latest/developerguide/welcome.html
- Amazon Location Service 文档：https://docs.aws.amazon.com/location/latest/developerguide/what-is.html
- AWS Step Functions 文档：https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html
- Amazon AppFlow 文档：https://docs.aws.amazon.com/appflow/latest/userguide/what-is-appflow.html
- Amazon MQ 文档：https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/welcome.html
- Amazon SNS 文档：https://docs.aws.amazon.com/sns/latest/dg/welcome.html
- Amazon SQS 文档：https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html
- Amazon SWF 文档：https://docs.aws.amazon.com/en_us/amazonswf/latest/developerguide/swf-dg-intro-to-swf.html
- Amazon MWAA 文档：https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html
- Amazon MWAA Serverless 文档：https://docs.aws.amazon.com/zh_cn/mwaa/latest/mwaa-serverless-userguide/what-is-mwaa-serverless.html
- AWS B2B Data Interchange 文档：https://docs.aws.amazon.com/b2bi/latest/userguide/what-is-b2bi.html
- Amazon EventBridge 文档：https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html
- Amazon EventBridge 与 CloudWatch Events 关系：https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-cwe-now-eb.html
- Amazon Connect Customer Profiles 文档：https://docs.aws.amazon.com/connect/latest/adminguide/customer-profiles.html
- Amazon Chime 文档：https://docs.aws.amazon.com/chime/latest/ag/what-is-chime.html
- Amazon Chime 文档历史/停止支持说明：https://docs.aws.amazon.com/chime/latest/ag/doc-history.html
- Amazon SES 文档：https://docs.aws.amazon.com/ses/latest/DeveloperGuide/InitialSetup.Customer.html
- Amazon WorkDocs 文档：https://docs.aws.amazon.com/workdocs/latest/userguide/what_is.html
- AWS full shutdown services 列表：https://docs.aws.amazon.com/general/latest/gr/full_shutdown_services.html
- Amazon WorkMail 文档：https://docs.aws.amazon.com/workmail/latest/adminguide/what_is.html
- Amazon WorkMail 停止支持说明：https://docs.aws.amazon.com/workmail/latest/adminguide/workmail-end-of-support.html
- Amazon Connect Health 文档：https://docs.aws.amazon.com/connecthealth/latest/userguide/what-is-service.html
- Amazon Connect Decisions 文档：https://docs.aws.amazon.com/connect-decisions/latest/userguide/what-is-amazon-connect-decisions-chapter.html
- Amazon Connect Decisions 入门与 Region 说明：https://docs.aws.amazon.com/connect-decisions/latest/adminguide/getting-started.html
- Amazon Pinpoint 文档：https://docs.aws.amazon.com/pinpoint/latest/userguide/welcome.html
- Amazon Pinpoint 停止支持说明：https://docs.aws.amazon.com/pinpoint/latest/userguide/migrate.html
- AWS Wickr 文档：https://docs.aws.amazon.com/wickr/latest/adminguide/what-is-wickr.html
- AWS AppFabric 文档：https://docs.aws.amazon.com/appfabric/latest/adminguide/what-is-appfabric.html
- AWS End User Messaging SMS 文档：https://docs.aws.amazon.com/sms-voice/latest/userguide/what-is-service.html
- AWS End User Messaging Push 文档：https://docs.aws.amazon.com/push-notifications/latest/userguide/what-is-service.html
- AWS End User Messaging Social 文档：https://docs.aws.amazon.com/social-messaging/latest/userguide/what-is-service.html
- Amazon Chime SDK 文档：https://docs.aws.amazon.com/chime-sdk/latest/dg/what-is-chime-sdk.html
- Amazon WorkSpaces 文档：https://docs.aws.amazon.com/workspaces/latest/adminguide/amazon-workspaces.html
- Amazon WorkSpaces Applications 文档：https://docs.aws.amazon.com/appstream2/latest/developerguide/what-is-appstream.html
- Amazon WorkSpaces Thin Client 停止支持说明：https://docs.aws.amazon.com/workspaces-thin-client/latest/ug/workspacesthinclient-end-of-support.html
- Amazon WorkSpaces Secure Browser 文档：https://docs.aws.amazon.com/en_us/workspaces-web/latest/adminguide/what-is-workspaces-secure-browser.html
- AWS IoT Core 文档：https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html
- AWS IoT Device Defender 文档：https://docs.aws.amazon.com/iot-device-defender/latest/devguide/what-is-device-defender.html
- AWS IoT Device Management fleet indexing 文档：https://docs.aws.amazon.com/iot/latest/developerguide/iot-indexing.html
- AWS IoT Jobs 文档：https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html
- AWS IoT Greengrass 文档：https://docs.aws.amazon.com/greengrass/v2/developerguide/what-is-iot-greengrass.html
- AWS IoT SiteWise 文档：https://docs.aws.amazon.com/iot-sitewise/latest/userguide/what-is-sitewise.html
- AWS IoT TwinMaker 文档：https://docs.aws.amazon.com/iot-twinmaker/latest/guide/what-is-twinmaker.html
- AWS IoT Events 文档：https://docs.aws.amazon.com/iotevents/latest/developerguide/what-is-iotevents.html
- AWS IoT FleetWise 文档：https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/what-is-iotfleetwise.html
- AWS IoT FleetWise 可用性变更：https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/iotfleetwise-availability-change.html
- AWS Service Availability Updates：https://aws.amazon.com/about-aws/whats-new/2026/03/aws-service-availability/
- Amazon GameLift Servers 文档：https://docs.aws.amazon.com/gameliftservers/latest/developerguide/gamelift-intro.html
- Amazon GameLift Streams 文档：https://docs.aws.amazon.com/gameliftstreams/latest/developerguide/what-is-service.html
