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
