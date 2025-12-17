# FastAPI Backend Template

通用 FastAPI 后端项目模板，支持 MySQL/MSSQL 数据库，适用于快速启动新的后端项目开发。

## 项目特性

- **现代技术栈**：基于 Python 3.13+ 和 FastAPI 框架
- **依赖管理**：使用 Poetry 进行依赖管理
- **数据库支持**：支持 MySQL 和 MS SQL Server，可灵活切换
- **模块化设计**：清晰的项目结构，易于扩展和维护
- **完整功能**：包含 CRUD 操作、文件上传下载、HTTP 客户端等基础功能
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
│   │   └── file_service.py     # 文件服务
│   ├── utils/                  # 工具函数
│   │   ├── logger.py           # 日志工具
│   │   └── http_client.py      # HTTP 客户端
│   ├── __init__.py
│   └── main.py                 # 应用入口
├── scripts/                    # 脚本目录
│   └── init_db.py              # 数据库初始化脚本
├── tests/                      # 测试目录
├── docs/                       # 文档目录
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

3. **配置环境变量**

```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库连接等信息
```
注意：拷贝后须修改数据库账号和密码。

4. **初始化数据库**

```bash
poetry run python scripts/init_db.py
```
注意：运行前需先创建数据库：CREATE DATABASE fastapi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

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

## Docker 部署

### 构建镜像

```bash
docker build -t fastapi-backend-template .
```

### 运行容器

```bash
docker run -d -p 8000:8000 --env-file .env fastapi-backend-template
```

### 使用 Docker Compose

```bash
docker-compose up -d
```

## 开发指南

详细的开发环境配置和使用指南请参考 [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)

## 部署指南

详细的部署步骤和最佳实践请参考 [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

## 许可证

MIT License
