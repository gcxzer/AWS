# EC2 Instance 类型命名与 GPU 选型

这篇放在 AWS 主线笔记里，因为 instance type 是 EC2、ECS、SageMaker、Batch Job 等很多服务都会遇到的基础概念，不只属于 AI。

## 最小心智模型

在 AWS 上“租一台 GPU 机器”，本质上通常是启动一台带 GPU 的 EC2 instance。

| 概念 | 人话解释 |
| --- | --- |
| EC2 instance | 你真正租的云服务器 |
| Instance type | 这台服务器的硬件套餐，例如 `g5.xlarge`、`p4d.24xlarge` |
| AMI | 操作系统镜像，例如 Ubuntu、Deep Learning AMI |
| EBS | 云硬盘 |
| VPC | 服务器所在的网络空间 |
| Subnet | VPC 里的一个小网络区域 |
| Security Group | 防火墙规则，例如只允许自己的 IP 走 SSH |
| Key Pair | 登录 EC2 的 SSH 钥匙 |

所以流程不是“先租 VPC，再租 EC2”。更准确是：

```text
启动 EC2
  -> 选择 AMI
  -> 选择 instance type
  -> 选择/默认使用 VPC 和 subnet
  -> 配 security group 和 key pair
```

学习阶段如果账号里有 default VPC，通常先用默认 VPC 即可。

## 命名规则

AWS instance 名字一般这样读：

```text
系列 + 世代 + 后缀 . 大小
```

例子：

```text
g5.xlarge
```

| 部分 | 例子 | 怎么理解 |
| --- | --- | --- |
| `g` | `g5.xlarge` | 系列/用途：GPU 图形或 AI 推理类 |
| `5` | `g5.xlarge` | 第 5 代，数字越大通常越新 |
| 无/后缀 | `g5n`、`m7i`、`c7gn` | CPU、网络、磁盘、显存等特殊版本 |
| `.xlarge` | `g5.xlarge` | 机器大小：CPU、内存、GPU 数量的档位 |

再看一个更大的：

```text
p4d.24xlarge
```

可以读成：

```text
P = 高端 GPU 计算
4 = 第 4 代
d = 带本地磁盘/特殊增强
24xlarge = 很大的规格，常见为多 GPU 训练机器
```

## 主系列代号

| 代号 | 大意 | 适合什么 |
| --- | --- | --- |
| `T` | 突发型通用机器 | 便宜开发机、小网站、轻负载 |
| `M` | 通用型 | 普通服务器、后端、数据库、小服务 |
| `C` | 计算优化 | CPU 密集任务、编译、批处理 |
| `R` | 内存优化 | 大内存应用、数据库、缓存 |
| `X` | 超大内存 | SAP、内存数据库、大数据 |
| `U` | 高内存裸金属类 | 超大内存企业应用 |
| `I` | 存储优化 | 本地 NVMe、高 I/O 数据库 |
| `D` | 密集存储 | 大容量本地硬盘、日志、数据仓库 |
| `Hpc` | 高性能计算 | 科学计算、仿真、HPC |
| `G` | GPU/图形密集 | 图形、视频、AI 推理、小中型模型 |
| `P` | 高端 GPU 计算 | 深度学习训练、A100/H100 级别 |
| `Inf` | AWS Inferentia | AI 推理，AWS 自研芯片 |
| `Trn` | AWS Trainium | AI 训练，AWS 自研芯片 |
| `F` | FPGA | FPGA 加速，比较少见 |
| `VT` | 视频转码 | 视频编码/转码 |
| `Mac` | macOS 机器 | iOS/macOS 构建、测试 |

## 常见后缀

| 后缀 | 例子 | 含义 |
| --- | --- | --- |
| `a` | `m7a`、`c7a` | AMD CPU |
| `i` | `m7i`、`c7i` | Intel CPU |
| `g` | `m7g`、`c7g` | AWS Graviton / ARM CPU |
| `d` | `m6id`、`g5d` | 带本地 instance store 磁盘 |
| `n` | `c7gn`、`m6in` | 网络/EBS 性能增强 |
| `e` | `r7ie`、`p4de` | 更多内存、存储或显存，取决于系列 |
| `flex` | `m7i-flex` | 便宜均衡版，适合普通负载 |
| `zn` | `m5zn` | 高频 CPU + 网络增强 |
| `metal` | `i4i.metal` | 裸金属整机 |

## 大小后缀

| 大小 | 怎么理解 |
| --- | --- |
| `nano` / `micro` / `small` | 很小，适合轻量服务 |
| `medium` / `large` | 小型生产或开发 |
| `xlarge` | 常见起步档 |
| `2xlarge` / `4xlarge` / `8xlarge` | 越大 CPU、内存、网络越多 |
| `12xlarge` / `24xlarge` / `48xlarge` | 大机器，常用于 GPU、HPC、数据库 |
| `metal` | 裸金属整机 |

## GPU Instance 对照

AWS 控制台里显示的是 instance type，不是显卡零售型号。A100、H100 这种 GPU 名字通常藏在 `P` 系列 instance 后面。

| AWS 名字 | 里面常见 GPU | 怎么理解 |
| --- | --- | --- |
| `g4dn` | NVIDIA T4 | 便宜入门 GPU |
| `g5` | NVIDIA A10G | 24GB 显存，适合个人 AI、推理、小中型模型 |
| `g6` | NVIDIA L4 | 新一点的推理、视频、AI GPU |
| `p3` | NVIDIA V100 | 老一代训练卡 |
| `p4d` / `p4de` | NVIDIA A100 | 真 A100，但通常规格很大、价格很高 |
| `p5` | NVIDIA H100 | H100 级训练和大模型 |
| `p5e` / `p5en` | NVIDIA H200 | H200，更贵更强 |
| `p6` | NVIDIA B200 | Blackwell 新一代，通常非常贵 |

为什么不是 RTX 4090：

```text
4090 = 消费级/桌面显卡
AWS GPU = 数据中心 GPU，例如 A10G、L4、A100、H100、H200
```

云厂商更常用数据中心卡，因为它们更适合 24/7 运行、远程虚拟化、企业驱动、散热供电、ECC/HBM 显存、多卡互联和数据中心管理。

## 从需求反推

| 需求 | 优先看什么 |
| --- | --- |
| 免费/低成本 Linux 小实验 | `t3.micro`、`t4g.micro`，注意 CPU 架构 |
| 普通 Web 服务或后端 | `t3`、`t4g`、`m7i`、`m7g` |
| CPU 密集任务 | `c7i`、`c7g`、`c7a` |
| 大内存服务或数据库 | `r7i`、`r7g` |
| 高速本地 NVMe | `i4i`、`i7i` |
| 入门 GPU/AI 推理 | `g4dn.xlarge`、`g5.xlarge`、`g6.xlarge` |
| 24GB 显存级别个人 GPU 实验 | `g5.xlarge` 或 `g6.xlarge` |
| A100 级训练 | `p4d` / `p4de` |
| H100/H200 级训练 | `p5` / `p5e` / `p5en` |

学习阶段如果只是想跑模型 demo、Stable Diffusion、小模型推理，先看 `g5.xlarge` 或 `g6.xlarge`，不要一上来找 `p4d` / `p5`。

## 租 GPU EC2 的入口

控制台路径：

```text
EC2 Console
  -> Instances
  -> Launch instance
```

关键选择：

| 步骤 | 建议 |
| --- | --- |
| AMI | Ubuntu 或 Deep Learning AMI |
| Instance type | `g5.xlarge`、`g6.xlarge`，需要 A100 才看 `p4d` |
| Network settings | 学习阶段先用 default VPC / default subnet |
| Auto-assign public IP | 需要 SSH 直连时开启 |
| Security Group | SSH `22` 只允许 `My IP` |
| Key Pair | 创建或选择自己的 SSH key |

如果找不到 GPU instance 或启动失败，常见原因是 quota 为 0。去 Service Quotas 里查：

```text
EC2
  -> Running On-Demand G and VT instances
  -> Running On-Demand P instances
```

需要 GPU 时申请对应 quota increase。

## 成本提醒

GPU 不属于普通免费套餐。EC2 只要处于 `running` 状态，即使什么都不跑，也会按实例收费。

用完以后：

```text
短暂停用：Stop instance
确定不要：Terminate instance
同时检查：EBS volume、Elastic IP、snapshot、CloudWatch Logs
```

## 参考

- AWS EC2 instance type naming conventions: https://docs.aws.amazon.com/ec2/latest/instancetypes/instance-type-names.html
- AWS EC2 instance types: https://aws.amazon.com/ec2/instance-types/
- AWS G5 instances: https://aws.amazon.com/ec2/instance-types/g5/
- AWS G6 instances: https://aws.amazon.com/ec2/instance-types/g6/
- AWS P4 instances: https://aws.amazon.com/ec2/instance-types/p4/
- AWS accelerated computing instances: https://aws.amazon.com/ec2/instance-types/accelerated-computing/
