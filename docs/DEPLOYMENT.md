# 部署指南

本指南提供了将此 FastAPI 项目部署到生产环境的多种方法，包括本地部署和基于 Docker 的容器化部署。

## 1. 本地部署 (裸机部署)

本地部署适用于快速验证或内部使用场景。生产环境推荐使用 Gunicorn + Uvicorn + Nginx 的组合。

### 1.1. 环境要求

-   一台安装了 Linux (如 Ubuntu 22.04) 的服务器。
-   Python 3.13+ 和 Poetry。
-   Nginx (作为反向代理)。
-   一个可用的数据库 (MySQL 或 MS SQL Server)。

### 1.2. 部署步骤

1.  **上传项目文件**: 将项目代码上传到服务器，例如 `/var/www/fastapi-app`。

2.  **安装依赖**: 
    ```bash
    cd /var/www/fastapi-app
    poetry install --no-dev
    ```

3.  **配置环境变量**: 创建 `.env` 文件并填入生产环境的配置，特别是数据库连接信息和 `DEBUG=False`。

4.  **初始化数据库**: 
    ```bash
    poetry run python scripts/init_db.py
    ```

5.  **使用 Gunicorn 运行应用**: Gunicorn 是一个成熟的 WSGI HTTP 服务器，通常用于在生产环境中运行 Python Web 应用。我们将它与 Uvicorn 的 worker 类结合使用来运行 FastAPI。

    安装 Gunicorn:
    ```bash
    poetry add gunicorn
    ```

    通过 Gunicorn 启动:
    ```bash
    poetry run gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000
    ```
    *   `-w 4`: 启动 4 个 worker 进程。通常建议的数量是 `(2 * CPU核心数) + 1`。
    *   `-k uvicorn.workers.UvicornWorker`: 使用 Uvicorn 的 worker 类来处理请求。
    *   `-b 127.0.0.1:8000`: 绑定到本地地址和端口，准备接收来自 Nginx 的流量。

6.  **配置 Systemd 服务 (推荐)**: 为了让应用在后台持续运行并能开机自启，可以创建一个 Systemd 服务文件。

    创建 `/etc/systemd/system/fastapi-app.service`:
    ```ini
    [Unit]
    Description=Gunicorn instance to serve FastAPI app
    After=network.target

    [Service]
    User=ubuntu
    Group=www-data
    WorkingDirectory=/var/www/fastapi-app
    ExecStart=/home/ubuntu/.local/bin/poetry run gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```
    *注意：请将 `User` 和 `ExecStart` 中的 Poetry 路径修改为你的实际用户和路径。*

    启动并启用服务:
    ```bash
    sudo systemctl start fastapi-app
    sudo systemctl enable fastapi-app
    ```

7.  **配置 Nginx 反向代理**: Nginx 将作为前端服务器，接收公网流量并转发给 Gunicorn。

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

    启用配置:
    ```bash
    sudo ln -s /etc/nginx/sites-available/fastapi-app /etc/nginx/sites-enabled
    sudo nginx -t  # 测试配置是否正确
    sudo systemctl restart nginx
    ```

## 2. Docker 容器化部署

容器化是现代应用部署的首选方案，它提供了环境一致性、可移植性和易于扩展的优点。

### 2.1. 使用 Dockerfile

`Dockerfile` 已经包含在项目根目录中，它定义了如何构建应用的镜像。

1.  **构建镜像**:
    ```bash
    docker build -t fastapi-backend-template:latest .
    ```

2.  **运行容器**:
    ```bash
    docker run -d \
      --name fastapi-app-container \
      -p 8000:8000 \
      --env-file .env \
      fastapi-backend-template:latest
    ```
    *   `-d`: 后台运行容器。
    *   `--name`: 为容器指定一个名称。
    *   `-p`: 将主机的 8000 端口映射到容器的 8000 端口。
    *   `--env-file`: 从 `.env` 文件加载环境变量。

### 2.2. 使用 Docker Compose

`docker-compose.yml` 文件定义了应用服务和其依赖（如数据库）的完整堆栈，是多服务应用部署的理想选择。

1.  **配置 `.env` 文件**: 确保 `.env` 文件中的数据库主机设置为 Docker Compose 服务名，例如 `DATABASE_HOST=mysql`。

2.  **启动服务**:
    ```bash
    docker-compose up -d
    ```
    此命令会根据 `docker-compose.yml` 的配置，自动完成以下操作：
    *   构建 `app` 服务的镜像 (如果尚未构建)。
    *   拉取 `mysql` 服务的镜像。
    *   创建并启动 `app` 和 `mysql` 两个容器。
    *   设置容器间的网络，使 `app` 容器可以通过服务名 `mysql` 访问数据库。
    *   挂载数据卷以持久化数据库数据和上传的文件。

3.  **查看日志**:
    ```bash
    docker-compose logs -f app
    ```

4.  **停止服务**:
    ```bash
    docker-compose down
    ```
    此命令会停止并移除由 `docker-compose up` 创建的容器和网络。

### 2.3. 切换到 MSSQL

如果希望使用 MS SQL Server，请在 `docker-compose.yml` 文件中：
1.  注释掉 `mysql` 服务。
2.  取消对 `mssql` 服务的注释。
3.  在 `app` 服务的 `environment` 中，将 `DATABASE_HOST` 修改为 `mssql`。
4.  在 `.env` 文件中，将 `DATABASE_TYPE` 设置为 `mssql`，并更新相应的连接信息。

然后重新运行 `docker-compose up -d`。
