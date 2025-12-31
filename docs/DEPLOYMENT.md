# 部署指南

本指南提供了将此 FastAPI 项目部署到生产环境的多种方法，包括本地部署和基于 Docker 的容器化部署。

## 1. 本地部署 (裸机部署)

本地部署适用于快速验证或内部使用场景。生产环境推荐使用 Gunicorn + Uvicorn + Nginx 的组合。

### 1.1. 环境要求

-   一台安装了 Linux (如 Ubuntu 22.04) 的服务器。
-   Python 3.13+ 和 Poetry。
-   Nginx (作为反向代理)。
-   一个可用的数据库 (MySQL 或 MS SQL Server)。
-   **Redis Server** (6.0+)。
-   **MQTT Broker** (如 Mosquitto)。

### 1.2. 部署步骤

1.  **上传项目文件**: 将项目代码上传到服务器，例如 `/var/www/fastapi-app`。

2.  **安装依赖**: 
    ```bash
    cd /var/www/fastapi-app
    poetry install --no-dev
    ```

3.  **配置环境变量**: 创建 `.env` 文件并填入生产环境的配置，特别是数据库、Redis 和 MQTT 的连接信息。

4.  **初始化数据库**: 
    ```bash
    poetry run python scripts/init_db.py
    ```

5.  **启动 Gunicorn**: 
    ```bash
    poetry run gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000
    ```

6.  **配置 Nginx 反向代理**: Nginx 将作为前端服务器，接收公网流量并转发给 Gunicorn。

    创建 `/etc/nginx/sites-available/fastapi-app`:
    ```nginx
    server {
        listen 80;
        server_name your_domain.com;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /static {
            alias /var/www/fastapi-app/static;
        }
    }
    ```

## 2. Docker 容器化部署 (推荐)

容器化是现代应用部署的首选方案，它提供了环境一致性、可移植性和易于扩展的优点。

### 2.1. 使用 Docker Compose

`docker-compose.yml` 文件已更新，现在包含 **应用服务**、**MySQL 数据库**、**Redis 缓存** 和 **Mosquitto MQTT 代理** 四个服务。

1.  **配置 `.env` 文件**: 确保 `.env` 文件中的服务主机名设置为 Docker Compose 服务名：
    ```env
    DATABASE_HOST=mysql
    REDIS_HOST=redis
    MQTT_HOST=mosquitto
    ```

2.  **创建 Mosquitto 配置**: 项目根目录下已创建 `mosquitto/mosquitto.conf` 文件，默认允许匿名访问。生产环境请务必修改此配置以增加安全性。

3.  **启动服务**:
    ```bash
    docker-compose up -d --build
    ```
    此命令会构建应用镜像，并一键启动所有服务。

4.  **查看日志**:
    ```bash
    docker-compose logs -f app
    ```

5.  **停止服务**:
    ```bash
    docker-compose down
    ```

### 2.2. 依赖服务说明

| 服务名 | 镜像 | 端口 | 作用 |
| :--- | :--- | :--- | :--- |
| `mysql` | `mysql:8.0` | 3306 | 关系型数据库 |
| `redis` | `redis:7.2-alpine` | 6379 | 内存缓存服务 |
| `mosquitto` | `eclipse-mosquitto:2.0` | 1883 | MQTT 消息代理 |
| `app` | 自定义 | 8000 | FastAPI 后端应用 |

**注意**: `app` 服务已配置 `depends_on`，确保在应用启动前，MySQL、Redis 和 Mosquitto 服务已经启动。

### 2.3. 切换到 MSSQL

如果希望使用 MS SQL Server，请在 `docker-compose.yml` 文件中：
1.  注释掉 `mysql` 服务。
2.  取消对 `mssql` 服务的注释。
3.  在 `app` 服务的 `environment` 中，将 `DATABASE_HOST` 修改为 `mssql`。
4.  在 `.env` 文件中，将 `DATABASE_TYPE` 设置为 `mssql`，并更新相应的连接信息。

然后重新运行 `docker-compose up -d`。

### 2.4. 推送镜像到服务器（多种方法与区别）

- 使用 Image ID 进行精确标记（推荐）：
  ```bash
  # 使用 IMAGE ID 来标记，这是最准确的方式
  docker tag abade886bae8 harmonynext/fastapi-backend-template:0.1
  # 登录并推送到镜像仓库（如 Docker Hub 或私有仓库）
  docker login
  docker push harmonynext/fastapi-backend-template:0.1
  ```
  说明：`docker tag` 只是为现有镜像添加一个新的名称/标签，不会产生新镜像，适用于你已经通过 Dockerfile 构建好的可复现镜像。

- 从运行中的容器生成镜像（临时变更快照）：
  ```bash
  docker commit --author "飞浪 <goldpool@gmail.com>" --message "修改了环境变量" fastapi-backend-app harmonynext/fastapi-backend-template:0.2
  docker push harmonynext/fastapi-backend-template:0.2
  ```
  说明：`docker commit` 会将当前容器的文件系统快照固化为新镜像，适合快速保存运行时的临时更改，但不可复现（缺少 Dockerfile 构建步骤），不建议用于生产长期维护。

- 无仓库直传到服务器（离线/内网场景）：
  ```bash
  # 在本地导出镜像为 tar
  docker save -o fastapi-backend-template.tar harmonynext/fastapi-backend-template:0.1
  # 传到服务器后导入
  docker load -i fastapi-backend-template.tar
  ```
  说明：适用于无法访问公共/私有镜像仓库的环境，通过文件传输实现镜像分发。

对比与最佳实践：
- 优先使用 Dockerfile 构建 + `docker tag` + `docker push`，可复现、易版本化。
- `docker commit` 适合临时保存现场，但不利于团队协作与长期维护。
- 离线传输（`save/load`）适合受限网络环境。

### 2.5. 启动运行容器（两种方式的差异）

- 使用 `--env-file` 注入环境变量（变量进入进程环境）：
  ```bash
  docker run -d --network=host --name my-fastapi-app --env-file ./.env harmonynext/fastapi-backend-template:last
  ```
  特点：不需要容器内存在 `.env` 文件，变量作为环境变量提供给应用。BaseSettings 会从环境变量读取配置。

- 通过挂载 `.env` 文件（应用按文件读取）：
  ```bash
  docker run -d --network=host --name my-fastapi-app -v "./.env:/app/.env" harmonynext/fastapi-backend-template:last
  ```
  特点：将主机上的 `.env` 文件映射到容器内 `/app/.env`，应用按文件读取配置。适合你依赖 `.env` 文件内容的场景。

- 选择建议：两种方式都可用。若你在 CI/CD 中管理环境变量，推荐 `--env-file`；若你希望与开发环境保持一致（读取 `.env` 文件），推荐挂载文件。注意在 Windows 上路径与引号的使用（PowerShell 需使用双引号）。

#### 通过 Dockerfile 构建镜像并推送（推荐）

1) 在项目根目录（包含 Dockerfile）构建镜像：
```bash
docker build -t harmonynext/fastapi-backend-template:0.1 .
```

2) 登录并推送：
```bash
docker login
docker push harmonynext/fastapi-backend-template:0.1
```

提示：需要修改版本时，重新 `docker build` 并推送新 tag，如 `:0.2`。生产建议使用 CI/CD 自动化构建与推送。

#### 通过 Docker Compose 构建镜像并推送（适合多服务场景）

方式 A（直接构建 app 服务镜像，再手动推送）：
```bash
# 仅构建 app 服务的镜像
docker-compose build app
# 构建完成后为镜像添加标准标签并推送（建议在 compose 中给 app 配置 image 字段以固定名称）
docker tag <LOCAL_IMAGE_ID> harmonynext/fastapi-backend-template:0.1
docker push harmonynext/fastapi-backend-template:0.1
```

方式 B（在 docker-compose.yml 中为 app 服务设置 image 字段）：
- 在 `services.app` 下添加：
```
image: harmonynext/fastapi-backend-template:0.1
```
- 然后构建与推送：
```bash
docker-compose build app
# 使用 Compose v2 时也可以：docker compose push app（需设置了 image 字段）
docker push harmonynext/fastapi-backend-template:0.1
```

说明：Compose 构建的镜像名称若未设置 `image` 字段，通常会生成本地名称（含目录和服务名），不便于统一推送；建议为 app 服务显式设置 `image` 字段以统一镜像命名与推送。

#### 依赖服务安装策略（共享 vs 非共享）

- 共享依赖（服务器已运行的服务）：如 MQTT、Redis、MySQL 等并非本项目专用，服务器可能已经提供这些服务。此时无需在当前项目的 docker-compose 中重复安装与启动，只需在 `.env` 将连接信息指向既有服务：
  ```env
  # 指向服务器现有服务的主机/IP
  DATABASE_HOST=192.168.1.10
  REDIS_HOST=192.168.1.10
  MQTT_HOST=192.168.1.10
  ```
  - 若你使用外部 Docker 网络（如本项目的 `shared-services-net`），也可直接使用网络内的服务名。

- 非共享依赖（仅随本项目提供）：如果目标服务器没有现成的 Redis/MQTT/MySQL，或你希望隔离部署，则在 docker-compose 中包含并启动这些服务。
  - 可通过注释/取消注释来控制是否启动依赖服务；当依赖已由服务器提供时，仅保留 `app` 服务即可。

- 混合策略：根据实际情况，仅在 compose 中保留需要随项目一起部署的服务，其余服务通过 `.env` 指向外部地址或共享网络。

- 仅启动应用并连接既有服务的示例命令：
  ```bash
  # 使用外部已存在服务：只启动 app，加载 .env 指向外部服务
  docker-compose up -d --build app
  # 或者只构建镜像并单独运行：
  docker-compose build app
  docker run -d --name my-fastapi-app --env-file ./.env harmonynext/fastapi-backend-template:0.1
  ```
