# Docker 学习笔记

这份笔记的目标不是背命令，而是把 Docker 当成一套“打包、运行、分发应用”的工程工具来理解。学完后，你应该能看懂一个项目里的 `Dockerfile` 和 `docker-compose.yml`，能在本机跑起服务，能排查常见问题，也能理解它和 AWS ECR / ECS 的关系。

## 先建立心智模型

| 概念 | 可以先这样理解 | 你真正要记住的点 |
| --- | --- | --- |
| Image | 应用的安装包 / 快照 | 只读模板，里面有代码、依赖、运行时和启动命令 |
| Container | 正在运行的应用进程 | 从 image 启动出来，有独立文件系统、网络和进程空间 |
| Dockerfile | 制作 image 的菜谱 | 每一行指令都会构建 image 的一层 |
| Registry | 镜像仓库 | Docker Hub、AWS ECR 都是 registry |
| Volume | 容器外的数据盘 | 用来保存数据库数据、上传文件、缓存等持久数据 |
| Network | 容器之间的内网 | Compose 里的服务名可以当 DNS 名称互相访问 |
| Compose | 多容器本地编排 | 一条命令启动 app、db、redis、worker 等一组服务 |

一句话版本：

> Dockerfile 生成 image，image 启动 container，container 通过 volume 保存数据，通过 network 互相通信，通过 registry 分发到别的机器或云上。

## 学习路线

1. 会跑容器：知道 `docker run`、`docker ps`、`docker logs`、`docker exec`。
2. 会构建镜像：能写基础 `Dockerfile`，理解 `FROM`、`COPY`、`RUN`、`CMD`。
3. 会保存数据：理解 bind mount 和 named volume 的区别。
4. 会连接服务：理解 container port、host port、bridge network。
5. 会用 Compose：用 `docker compose up` 跑 Web + DB。
6. 会排错和清理：知道容器为什么退出、端口为什么冲突、磁盘为什么变大。
7. 会接 AWS：理解本地 image 如何 push 到 ECR，再由 ECS/Fargate 拉起。

## Day 1：安装后先跑起来

先确认 Docker 可用：

```bash
docker version
docker info
docker run hello-world
```

如果 `hello-world` 成功，你已经完成了第一件事：Docker 从 registry 拉取 image，并在本机启动了一个短生命周期 container。

常用观察命令：

```bash
docker ps
docker ps -a
docker images
docker logs <container>
docker inspect <container>
```

`docker ps` 只看正在运行的容器，`docker ps -a` 会把已经退出的容器也列出来。

## Day 2：运行一个真实服务

用 Nginx 快速启动一个 Web 服务：

```bash
docker run --name web-demo -p 8080:80 nginx
```

打开浏览器访问：

```text
http://localhost:8080
```

这里的端口映射要这样读：

```text
-p 8080:80
本机 8080 端口 -> 容器 80 端口
```

停止和删除：

```bash
docker stop web-demo
docker rm web-demo
```

后台运行：

```bash
docker run -d --name web-demo -p 8080:80 nginx
docker logs web-demo
docker stop web-demo
docker rm web-demo
```

进入容器：

```bash
docker exec -it web-demo sh
```

注意：不是所有镜像都有 `bash`。轻量镜像通常只有 `sh`。

## Day 3：Image 和 Container 的区别

最容易混淆的是 image 和 container。

```text
Image: 静态模板，像一个应用安装包
Container: 从 image 启动出来的运行实例
```

同一个 image 可以启动多个 container：

```bash
docker run -d --name web-1 -p 8081:80 nginx
docker run -d --name web-2 -p 8082:80 nginx
```

这两个容器来自同一个 `nginx` image，但它们是两个独立的运行实例。

删除 container 不等于删除 image：

```bash
docker rm web-1
docker rm web-2
docker images
```

删除 image：

```bash
docker rmi nginx
```

如果还有容器依赖这个 image，Docker 会阻止你删除。先删容器，再删 image。

## Day 4：写第一个 Dockerfile

以一个最小 Python Web 服务为例。

项目结构：

```text
hello-docker/
  app.py
  requirements.txt
  Dockerfile
```

`app.py`：

```python
from flask import Flask

app = Flask(__name__)

@app.get("/")
def home():
    return {"message": "hello docker"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

`requirements.txt`：

```text
flask
```

`Dockerfile`：

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000
CMD ["python", "app.py"]
```

构建 image：

```bash
docker build -t hello-docker:local .
```

运行 container：

```bash
docker run --name hello-docker -p 5000:5000 hello-docker:local
```

访问：

```text
http://localhost:5000
```

### Dockerfile 每行在做什么

| 指令 | 作用 |
| --- | --- |
| `FROM` | 选择基础镜像 |
| `WORKDIR` | 设置容器内工作目录 |
| `COPY` | 把本机文件复制进 image |
| `RUN` | 构建 image 时执行命令 |
| `EXPOSE` | 声明容器内部服务端口 |
| `CMD` | 容器启动时默认执行的命令 |

`RUN` 是构建时执行，`CMD` 是容器启动时执行。这个区别很重要。

## Day 5：构建缓存和 .dockerignore

Docker build 会缓存每一层。常见优化思路是：先复制依赖清单并安装依赖，再复制业务代码。

这样写比较好：

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
```

因为你改 `app.py` 时，依赖安装层可以复用。

建议添加 `.dockerignore`：

```gitignore
.git
__pycache__
.venv
node_modules
.env
.DS_Store
```

`.dockerignore` 的作用是减少 build context，避免把无关文件或敏感文件复制进构建过程。

## Day 6：Volume：容器删除后数据还在吗

容器自己的文件系统适合放运行时文件，不适合放重要数据。容器删除后，容器内写入的数据通常也会一起消失。

### Bind mount

把本机目录挂进容器：

```bash
docker run --name web-bind -p 8080:80 -v "$PWD/html:/usr/share/nginx/html" nginx
```

适合开发时把本地代码挂进容器。

### Named volume

让 Docker 管理一个持久数据卷：

```bash
docker volume create pgdata
docker run --name postgres-demo -e POSTGRES_PASSWORD=secret -v pgdata:/var/lib/postgresql/data postgres:16
```

适合数据库数据。

查看 volume：

```bash
docker volume ls
docker volume inspect pgdata
```

## Day 7：Network：容器之间怎么通信

在同一个 Docker network 里，容器可以用容器名或 Compose 服务名访问彼此。

创建网络：

```bash
docker network create app-net
```

启动数据库：

```bash
docker run -d --name db --network app-net -e POSTGRES_PASSWORD=secret postgres:16
```

如果另一个容器也在 `app-net` 里，它可以用 `db:5432` 访问数据库，而不是用 `localhost:5432`。

关键点：

```text
容器里的 localhost = 容器自己
本机的 localhost = 你的电脑
另一个容器 = 用 network 里的服务名或容器名
```

这也是很多连接数据库问题的根源。

## Day 8：Docker Compose 入门

单个容器用 `docker run` 还能接受。多个服务一起跑时，就应该用 Compose。

`docker-compose.yml`：

```yaml
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      DATABASE_URL: postgres://postgres:secret@db:5432/app
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: app
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

启动：

```bash
docker compose up
docker compose up -d
```

查看：

```bash
docker compose ps
docker compose logs
docker compose logs app
```

停止：

```bash
docker compose down
```

停止并删除 volume：

```bash
docker compose down -v
```

小心 `-v`：它会删除 Compose 创建的 named volume，数据库数据会被清掉。

## Day 9：常见命令速查

### 容器

```bash
docker ps
docker ps -a
docker run --name <name> <image>
docker run -d --name <name> <image>
docker stop <container>
docker start <container>
docker restart <container>
docker rm <container>
docker logs <container>
docker logs -f <container>
docker exec -it <container> sh
```

### 镜像

```bash
docker images
docker pull <image>
docker build -t <name>:<tag> .
docker rmi <image>
docker tag <source> <target>
docker push <image>
```

### Volume

```bash
docker volume ls
docker volume inspect <volume>
docker volume rm <volume>
```

### Network

```bash
docker network ls
docker network inspect <network>
docker network create <network>
docker network rm <network>
```

### Compose

```bash
docker compose up
docker compose up -d
docker compose ps
docker compose logs
docker compose logs -f
docker compose down
docker compose down -v
docker compose build
docker compose pull
```

## Day 10：排错套路

### 容器一启动就退出

先看退出原因：

```bash
docker ps -a
docker logs <container>
docker inspect <container>
```

常见原因：

| 现象 | 可能原因 |
| --- | --- |
| `Exited (0)` | 主进程正常结束，比如运行了一个一次性命令 |
| `Exited (1)` | 应用启动报错 |
| 找不到命令 | `CMD` 或 `ENTRYPOINT` 写错，或镜像里没有这个命令 |
| 配置缺失 | 环境变量、配置文件、secret 没传进去 |

### 端口冲突

报错类似：

```text
port is already allocated
```

说明本机端口已经被占用。换一个 host port：

```bash
docker run -p 8081:80 nginx
```

### 容器里连不上数据库

先问三个问题：

1. app 和 db 在同一个 Docker network 吗？
2. app 用的是 `db:5432`，还是错误地用了 `localhost:5432`？
3. db 是否已经启动完成，并且用户名、密码、数据库名正确？

### 镜像太大

常见优化：

1. 使用 slim / alpine 等较小基础镜像。
2. 加 `.dockerignore`。
3. 不把 `.git`、`node_modules`、虚拟环境复制进 image。
4. 构建依赖和运行依赖分开，必要时使用 multi-stage build。

## Day 11：开发环境和生产环境的区别

开发环境通常关注方便：

```text
本地代码 bind mount 进容器
热更新
详细日志
本地数据库
```

生产环境通常关注稳定：

```text
image 是不可变产物
配置通过环境变量或 secret 注入
日志输出到 stdout / stderr
数据放在托管数据库或持久存储
容器可以随时被销毁和重建
```

一个重要原则：

> 不要把生产数据只放在容器自己的文件系统里。

生产中的容器应该是可替换的。容器没了，服务可以重建；数据没了，就是真的事故。

## Day 12：Docker 和 AWS 的关系

如果你把 Docker 接到 AWS，常见链路是：

```text
本机 Dockerfile
  -> docker build 生成 image
  -> docker tag 标记成 ECR 地址
  -> docker push 推到 Amazon ECR
  -> ECS/Fargate 从 ECR 拉 image
  -> Task 启动 container
  -> ALB 把外部请求转发到 container
```

对应概念：

| Docker 本地 | AWS 上 |
| --- | --- |
| Image | ECR 里的 image |
| Container | ECS task 里的 container |
| `docker run` | ECS service / task 启动 |
| `docker logs` | CloudWatch Logs |
| `.env` / `-e` | ECS task definition environment / secrets |
| 本机端口映射 | ALB listener + target group + security group |
| named volume | EFS、RDS、S3 等持久化服务 |

在你的 AWS 学习主线里，Docker 最重要的落点是 ECS/Fargate：你把应用打成 image，ECS 负责在云上运行它。

## 最小实践项目

做一个 `hello-docker` 小项目，目标是把下面几件事串起来：

1. 写一个返回 JSON 的 Python Flask API。
2. 写 `Dockerfile`。
3. `docker build -t hello-docker:local .`。
4. `docker run -p 5000:5000 hello-docker:local`。
5. 改代码后重新 build。
6. 加 `.dockerignore`。
7. 写 `docker-compose.yml`，加一个 Postgres 服务。
8. app 用 `db` 这个服务名连接数据库。
9. 用 `docker compose logs` 排查一次错误。
10. 用 `docker compose down -v` 清理环境，并确认数据会被删。

## 自测问题

1. Image 和 container 有什么区别？
2. `RUN` 和 `CMD` 的区别是什么？
3. `-p 8080:80` 左边和右边分别是谁的端口？
4. 容器里的 `localhost` 指谁？
5. 什么时候用 bind mount，什么时候用 named volume？
6. 为什么数据库数据不应该只放在 container 文件系统里？
7. Compose 里 app 为什么可以用 `db` 访问数据库？
8. `.dockerignore` 解决什么问题？
9. 本地 Docker image 要上 AWS ECS，中间为什么通常要经过 ECR？
10. 容器启动失败时，你第一时间看哪三个命令？

## 常见误区

| 误区 | 正确理解 |
| --- | --- |
| Docker 是虚拟机 | Docker 更像进程级隔离，通常比虚拟机轻 |
| 容器里能跑就代表生产没问题 | 还要考虑配置、日志、数据、网络、安全、资源限制 |
| `latest` 最方便 | 生产环境应该固定 tag，避免不可控升级 |
| 删除容器就是删除镜像 | 容器和镜像是两层东西 |
| 容器内用 `localhost` 连接另一个容器 | 应该用同一 network 下的服务名 |
| 把 `.env` COPY 进 image | 敏感配置应该在运行时注入，不要烤进镜像 |

## 你应该形成的判断力

学 Docker 最关键的是这几个问题：

1. 这个东西是在 build 阶段发生，还是 run 阶段发生？
2. 这个文件是在本机、image 里，还是 container 里？
3. 这个数据删除容器后还在不在？
4. 这个地址是从本机访问容器，还是容器访问另一个容器？
5. 这个 image 将来是只在本机跑，还是要 push 到 registry 给云服务拉取？

只要这五个问题能分清，大多数 Docker 问题都会变得可拆解。
