# FastAPI Backend Template

通用 FastAPI 后端项目模板，支持 MySQL/MSSQL 数据库，适用于快速启动新的后端项目开发。

## 项目特性

- **现代技术栈**：基于 Python 3.13+ 和 FastAPI 框架
- **依赖管理**：使用 Poetry 进行依赖管理
- **数据库支持**：支持 MySQL 和 MS SQL Server，可灵活切换
- **缓存管理**：集成 **Redis** 缓存服务
- **消息队列**：集成 **MQTT** 消息代理服务
- **模块化设计**：清晰的项目结构，易于扩展和维护
- **完整功能**：包含 CRUD 操作、文件上传下载、HTTP 客户端、缓存和消息发布/订阅功能
- **容器化部署**：提供 Docker 和 Docker Compose 配置
- **开发友好**：详细的开发环境配置指南和 API 文档

## 项目结构

```
fastapi-backend-template/
├── app/                        # 应用主目录
│   ├── api/                    # API 路由
│   │   └── v1/                 # API v1 版本
│   │       ├── __init__.py     # 路由聚合
│   │       ├── items.py        # Item CRUD API
│   │       └── files.py        # 文件上传下载 API
│   ├── core/                   # 核心配置
│   │   ├── __init__.py
│   │   └── config.py           # 应用配置
│   ├── db/                     # 数据库
│   │   ├── __init__.py
│   │   └── session.py          # 数据库会话管理
│   ├── models/                 # 数据模型
│   │   ├── __init__.py
│   │   └── item.py             # Item 模型
│   ├── schemas/                # Pydantic Schemas
│   │   ├── __init__.py
│   │   └── item.py             # Item Schema
│   ├── services/               # 业务逻辑层
│   │   ├── item_service.py     # Item 服务
│   │   ├── file_service.py     # 文件服务
│   │   ├── cache_service.py    # Redis 缓存服务
│   │   └── message_service.py  # MQTT 消息服务
│   ├── utils/                  # 工具函数
│   │   ├── logger.py           # 日志工具
│   │   ├── http_client.py      # HTTP 客户端
│   │   ├── redis_client.py     # Redis 客户端
│   │   └── mqtt_client.py      # MQTT 客户端
│   ├── __init__.py
│   └── main.py                 # 应用入口
├── scripts/                    # 脚本目录
│   └── init_db.py              # 数据库初始化脚本
├── tests/                      # 测试目录
├── docs/                       # 文档目录
├── mosquitto/                  # MQTT 代理配置
│   └── mosquitto.conf          # 匿名访问配置
├── .env.example                # 环境变量示例
├── .gitignore                  # Git 忽略文件
├── pyproject.toml              # Poetry 配置
├── Dockerfile                  # Docker 配置
├── docker-compose.yml          # Docker Compose 配置
└── README.md                   # 项目说明
```

## 快速开始

### 前置要求

- Python 3.13+
- Poetry
- MySQL 或 MS SQL Server
- Redis Server (可选，Docker Compose 会启动)
- MQTT Broker (可选，Docker Compose 会启动)
- PyCharm 2024.2+ (推荐)

### 安装步骤

1. **克隆项目**

```bash
git clone <repository-url>
cd fastapi-backend-template
```

2. **安装依赖**

```bash
poetry install
```
python 安装命令
```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```
安装的时候可能要设置代理：
```bash
set HTTP_PROXY=http://192.168.65.99:7766
set HTTPS_PROXY=http://192.168.65.99:7766
poetry install
```

3. **配置环境变量**

```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库、Redis、MQTT 连接等信息
```
注意：拷贝后须修改数据库账号和密码。

4. **初始化数据库（在已有数据库或容器场景）**

- 先在数据库服务器创建数据库（MySQL 示例）：
  ```sql
  CREATE DATABASE fastapi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  ```

- 不要在“数据库容器”里运行 Poetry 命令。初始化脚本应在“应用环境”执行，任选其一：
  1) 本机开发环境：
  ```bash
  poetry run python scripts/init_db.py
  ```
  2) Docker Compose：
  ```bash
  docker-compose exec app poetry run python scripts/init_db.py
  ```
  3) 直接使用镜像运行一次性初始化（无需本机装 Poetry）：
  ```bash
  docker run --rm --env-file ./.env harmonynext/fastapi-backend-template:last python scripts/init_db.py
  ```
  或者挂载 `.env` 文件：
  ```bash
  docker run --rm -v "./.env:/app/.env" harmonynext/fastapi-backend-template:last python scripts/init_db.py
  ```

- 如果无法使用上述脚本，你也可以用 MySQL 客户端手动创建/迁移：
  ```bash
  docker exec -it <mysql_container> mysql -u<user> -p -e "CREATE DATABASE IF NOT EXISTS fastapi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
  ```

### MQTT 初始化（容器默认无账号与密码）

1. 进入 mosquitto 容器并创建密码文件与用户：
```bash
docker exec -it mqtt sh
mosquitto_passwd -c /mosquitto/config/pwfile myuser
# 再添加其它用户（非首次用 -b）
# mosquitto_passwd -b /mosquitto/config/pwfile another_user strong_password
```

2. 编辑配置文件 `/mosquitto/config/mosquitto.conf`：
```
persistence true
persistence_location /mosquitto/data/
log_dest file /mosquitto/log/mosquitto.log
listener 1883
allow_anonymous false
password_file /mosquitto/config/pwfile
```

3. 重启容器使配置生效：
```bash
docker restart mqtt
```

4. 在 `.env` 设置：
```env
MQTT_HOST=localhost
MQTT_PORT=1883
MQTT_USER=myuser
MQTT_PASSWORD=strong_password
```

如果你是首次启动并希望直接启用账号密码，可使用挂载配置和数据目录的方式：
```bash
docker run -d --name mqtt -p 1883:1883 \
  -v ./mosquitto/config:/mosquitto/config \
  -v ./mosquitto/data:/mosquitto/data \
  -v ./mosquitto/log:/mosquitto/log \
  eclipse-mosquitto:2.0
```

5. **启动应用**

```bash
poetry run python app/main.py
```

或使用 uvicorn：

```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. **访问 API 文档**

打开浏览器访问：http://localhost:8000/api/v1/docs

## 数据库配置

### MySQL 配置

在 `.env` 文件中配置：

```env
DATABASE_TYPE=mysql
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=password
DATABASE_NAME=fastapi_db
```

### MSSQL 配置

在 `.env` 文件中配置：

```env
DATABASE_TYPE=mssql
DATABASE_HOST=localhost
DATABASE_PORT=1433
DATABASE_USER=sa
DATABASE_PASSWORD=YourPassword123
DATABASE_NAME=fastapi_db
MSSQL_DRIVER=ODBC Driver 17 for SQL Server
```

注意：使用 MSSQL 需要安装 ODBC 驱动。

## 缓存与消息配置

### Redis 配置（无密码与有密码两种方式）

在 `.env` 文件中配置（根据你的实际情况选择）：

- 无密码（默认）：
  ```env
  REDIS_HOST=localhost
  REDIS_PORT=6379
  REDIS_DB=0
  # REDIS_PASSWORD 不设置或留空
  ```

- 有密码：
  ```env
  REDIS_HOST=localhost
  REDIS_PORT=6379
  REDIS_DB=0
  REDIS_PASSWORD=your-strong-password
  ```

如何设置 Redis 访问密码与绑定 IP：
- 本机 `redis-cli` 临时设置密码并持久化：
  ```bash
  redis-cli CONFIG SET requirepass "your-strong-password"
  redis-cli CONFIG REWRITE
  ```
- 使用配置文件持久化（`redis.conf`）：
  ```
  requirepass your-strong-password
  bind 127.0.0.1
  protected-mode yes
  ```
  提示：
  - 仅本机访问：`bind 127.0.0.1`
  - 对外访问：`bind 0.0.0.0` 并确保已开启防火墙/安全组规则，建议同时设置 `requirepass`。
- Docker 启动带密码并绑定 IP：
  ```bash
  docker run -d --name redis -p 6379:6379 redis:7.2-alpine \
    redis-server --requirepass "your-strong-password" --bind 0.0.0.0 --protected-mode yes
  ```

注意：
- 当 Redis 没有设置密码时，保持 `REDIS_PASSWORD` 留空或不填；启用密码后将其填写到 `.env`。
- 应用已支持通过 `.env` 的 `REDIS_PASSWORD` 安全连接，无需手动拼接 Redis URL。

### MQTT 配置

在 `.env` 文件中配置：

```env
MQTT_HOST=localhost
MQTT_PORT=1883
MQTT_USER=
MQTT_PASSWORD=
```

## API 接口

### Item CRUD

- `POST /api/v1/items/` - 创建 Item
- `GET /api/v1/items/{item_id}` - 获取单个 Item
- `GET /api/v1/items/` - 获取 Item 列表
- `PUT /api/v1/items/{item_id}` - 更新 Item
- `DELETE /api/v1/items/{item_id}` - 删除 Item
- `GET /api/v1/items/search/` - 搜索 Item

### 文件管理

- `POST /api/v1/files/upload` - 上传文件
- `GET /api/v1/files/download/{filename}` - 下载文件
- `DELETE /api/v1/files/{filename}` - 删除文件
- `GET /api/v1/files/` - 列出所有文件

## Docker 容器化部署 (推荐)

项目已配置好 `docker-compose.yml`，可以一键启动应用、MySQL、Redis 和 Mosquitto (MQTT Broker) 服务。

1. **配置 `.env` 文件**: 确保 `.env` 文件中的服务主机名设置为 Docker Compose 服务名：
    ```env
    DATABASE_HOST=mysql
    REDIS_HOST=redis
    MQTT_HOST=mosquitto
    ```

2. **启动服务**:

```bash
docker-compose up -d
```

3. **停止服务**:

```bash
docker-compose down
```

## 开发指南

详细的开发环境配置和使用指南请参考 [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)

## 部署指南

详细的部署步骤和最佳实践请参考 [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

## 许可证

MIT License

本项目是本人学习 Python 的练习项目，目的只是为了构建一个项目框架，也是作为日后开发企业应用系统后端接口的模板，因为企业业务系统通常都会用到数据库、消息、缓存、文件操作、接口访问等功能，所以模板直接集成了这几个功能。值得一提的是，本项目所有文件（包括文档）全程都是使用AI生成的，我没有写一行代码。
欢迎大家使用，也可以与本人联系交流：
飞浪 gold.pool@gmail.com 
http://ai.urok.cn
