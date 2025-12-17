# FastAPI 后端项目模板 - 交付说明

## 项目概述

本次交付的是一个完整的、生产级别的 FastAPI 后端项目模板，专为快速启动新的后端开发项目而设计。该模板特别适用于数据采集、内容管理和 API 服务等场景，并已根据您的需求进行了定制化配置。

## 技术栈确认

本项目严格按照您的要求构建，采用以下技术栈：

| 组件 | 技术选型 | 版本要求 |
|------|---------|---------|
| 编程语言 | Python | 3.13+ |
| Web 框架 | FastAPI | 0.115+ |
| 依赖管理 | Poetry | 1.8+ |
| 数据库支持 | MySQL / MS SQL Server | MySQL 8.0+ / MSSQL 2022+ |
| ORM 框架 | SQLAlchemy | 2.0+ |
| ASGI 服务器 | Uvicorn | 0.32+ |
| 容器化 | Docker & Docker Compose | - |

## 项目结构说明

项目采用模块化的分层架构设计，主要目录结构如下：

```
fastapi-backend-template/
├── app/                        # 应用主目录
│   ├── api/v1/                 # API 路由层（表现层）
│   │   ├── items.py            # Item CRUD API 示例
│   │   └── files.py            # 文件上传下载 API
│   ├── core/                   # 核心配置模块
│   │   └── config.py           # 统一配置管理（支持环境变量）
│   ├── db/                     # 数据库访问层
│   │   └── session.py          # 数据库连接和会话管理
│   ├── models/                 # SQLAlchemy 数据模型
│   │   └── item.py             # Item 数据模型示例
│   ├── schemas/                # Pydantic 数据验证模型
│   │   └── item.py             # Item Schema 定义
│   ├── services/               # 业务逻辑层
│   │   ├── item_service.py     # Item CRUD 服务
│   │   └── file_service.py     # 文件管理服务
│   ├── utils/                  # 工具函数模块
│   │   ├── logger.py           # 日志管理工具
│   │   └── http_client.py      # HTTP 客户端工具
│   └── main.py                 # 应用启动入口
├── scripts/                    # 脚本目录
│   └── init_db.py              # 数据库初始化脚本
├── docs/                       # 文档目录
│   ├── QUICK_START.md          # 快速开始指南
│   ├── DEVELOPMENT.md          # 开发环境配置指南
│   ├── DEPLOYMENT.md           # 部署指南
│   └── PROJECT_OVERVIEW.md     # 项目架构总览
├── tests/                      # 测试目录（预留）
├── uploads/                    # 文件上传目录
├── .env.example                # 环境变量配置示例
├── pyproject.toml              # Poetry 依赖配置
├── requirements.txt            # pip 依赖列表（备选）
├── Dockerfile                  # Docker 镜像构建文件
├── docker-compose.yml          # Docker Compose 配置
└── README.md                   # 项目说明文档
```

## 核心功能实现

本模板已实现以下核心功能，可作为您后续开发的参考和基础：

### 1. 数据库操作模块

**位置**: `app/services/item_service.py`

实现了完整的 CRUD (Create, Read, Update, Delete) 操作示例，包括：

-   创建记录 (`create`)
-   根据 ID 查询单条记录 (`get`)
-   分页查询多条记录 (`get_multi`)
-   更新记录 (`update`)
-   删除记录 (`delete`)
-   关键词搜索 (`search`)

### 2. 文件访问模块

**位置**: `app/services/file_service.py` 和 `app/api/v1/files.py`

提供了完整的文件管理功能：

-   **文件上传**: 支持异步上传，包含文件类型和大小验证。
-   **文件下载**: 通过文件名下载已上传的文件。
-   **文件删除**: 删除指定的上传文件。
-   **文件列表**: 列出所有已上传的文件及其元信息。

### 3. API 接口定义与调用

**位置**: `app/api/v1/`

所有 API 端点遵循 RESTful 设计规范，并通过 FastAPI 的自动文档生成功能提供了交互式 API 文档（Swagger UI 和 ReDoc）。API 路由采用版本化设计（v1），便于未来的版本迭代。

### 4. 网络请求工具

**位置**: `app/utils/http_client.py`

基于 `httpx` 库实现的异步 HTTP 客户端，支持：

-   发起 GET 和 POST 请求
-   下载网络文件到本地
-   自定义请求头和超时时间

此工具可用于调用外部 API（如抖音官方 API）或下载网络资源。

## 数据库配置与切换

项目通过环境变量实现了数据库的灵活配置和切换。

### MySQL 配置

在 `.env` 文件中设置：

```env
DATABASE_TYPE=mysql
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=your_password
DATABASE_NAME=fastapi_db
```

### MS SQL Server 配置

在 `.env` 文件中设置：

```env
DATABASE_TYPE=mssql
DATABASE_HOST=localhost
DATABASE_PORT=1433
DATABASE_USER=sa
DATABASE_PASSWORD=YourPassword123
DATABASE_NAME=fastapi_db
MSSQL_DRIVER=ODBC Driver 17 for SQL Server
```

**注意**: 使用 MSSQL 需要在系统中安装 ODBC Driver。在 Linux 系统上，可以参考 [Microsoft 官方文档](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server) 进行安装。

## 开发环境配置指南

### PyCharm 配置要点

详细的配置步骤请参考 `docs/DEVELOPMENT.md`，以下是关键要点：

1.  **Python 解释器**: 使用 PyCharm 的 Poetry 环境支持，自动创建虚拟环境并安装依赖。
2.  **推荐插件**:
    -   `.env files support`: 环境变量文件支持
    -   `Docker`: Docker 容器管理
    -   `Markdown`: 文档编辑和预览
3.  **运行配置**: 创建 Python 运行配置，指向 `app/main.py`，并启用 `.env` 文件加载。
4.  **调试功能**: 支持断点调试，可以在代码中设置断点并逐步执行。

### 开发工作流

1.  在 PyCharm 中打开项目。
2.  等待 Poetry 环境自动配置完成。
3.  复制 `.env.example` 为 `.env` 并配置数据库连接。
4.  运行 `scripts/init_db.py` 初始化数据库。
5.  启动应用并访问 `http://localhost:8000/api/v1/docs` 查看 API 文档。
6.  在 Swagger UI 中测试 API 端点。

## 部署方案

本项目提供了两种部署方案，详细步骤请参考 `docs/DEPLOYMENT.md`。

### 方案一：本地部署（裸机部署）

适用于快速验证或内部使用场景。推荐使用 Gunicorn + Uvicorn + Nginx 的组合：

-   **Gunicorn**: 作为 WSGI HTTP 服务器，管理多个 worker 进程。
-   **Uvicorn**: 作为 ASGI worker，处理异步请求。
-   **Nginx**: 作为反向代理，处理静态文件和负载均衡。

### 方案二：Docker 容器化部署（推荐）

提供了完整的 `Dockerfile` 和 `docker-compose.yml` 配置：

-   **单容器部署**: 使用 `docker build` 和 `docker run` 快速启动应用。
-   **多服务部署**: 使用 `docker-compose up` 一键启动应用和数据库服务。
-   **数据持久化**: 通过 Docker 卷挂载实现数据库数据和上传文件的持久化。

## 文档清单

本次交付包含以下完整文档：

| 文档名称 | 路径 | 用途 |
|---------|------|------|
| 项目说明 | `README.md` | 项目概览和快速导航 |
| 快速开始指南 | `docs/QUICK_START.md` | 5 分钟快速启动教程 |
| 开发环境配置指南 | `docs/DEVELOPMENT.md` | PyCharm IDE 配置详解 |
| 部署指南 | `docs/DEPLOYMENT.md` | 本地和 Docker 部署步骤 |
| 项目架构总览 | `docs/PROJECT_OVERVIEW.md` | 技术架构和设计理念 |

## 使用建议

### 针对抖音视频采集项目的扩展建议

基于您提到的"从抖音官网抓取热门视频及其评论"的需求，以下是一些扩展建议：

1.  **创建 Video 和 Comment 数据模型**: 参考 `app/models/item.py` 的结构，在 `app/models/` 目录下创建 `video.py` 和 `comment.py`，定义视频和评论的数据表结构。

2.  **实现抖音 API 客户端**: 在 `app/services/` 目录下创建 `douyin_service.py`，使用 `http_client` 工具调用抖音官方 API 或通过爬虫技术获取数据。

3.  **定时任务**: 可以集成 Celery 或 APScheduler 来实现定时抓取任务。将抓取逻辑封装在服务层，通过定时任务调度器定期执行。

4.  **数据存储**: 抓取到的视频和评论数据可以通过已实现的 CRUD 服务保存到数据库中。

5.  **前端集成**: 虽然本次交付的重点是后端模板，但此 FastAPI 应用可以无缝对接任何前端技术栈（Vue、React、ASP.NET、WinForm 等）。前端只需调用本项目提供的 RESTful API 即可。

### 代码质量保障

项目已配置了以下开发工具，建议在开发过程中使用：

-   **Black**: 代码自动格式化工具，确保代码风格一致。
-   **Flake8**: 代码风格检查工具，检测潜在的代码问题。
-   **isort**: 自动排序和组织 import 语句。
-   **MyPy**: 静态类型检查工具，提高代码的类型安全性。

运行方式：

```bash
poetry run black app/
poetry run flake8 app/
poetry run isort app/
poetry run mypy app/
```

## 后续支持

本项目模板已包含所有必要的代码、配置和文档。如果在使用过程中遇到任何问题，建议：

1.  首先查阅相关文档（特别是 `QUICK_START.md` 和 `DEVELOPMENT.md`）。
2.  检查 `.env` 配置文件是否正确。
3.  确认数据库服务是否正常运行。
4.  查看应用日志文件（`logs/app.log`）以获取详细的错误信息。

## 总结

本次交付的 FastAPI 后端项目模板是一个完整的、可直接用于生产的解决方案。它不仅满足了您提出的所有技术要求（Python 3.13、FastAPI、Poetry、MySQL/MSSQL 支持），还提供了丰富的功能示例和详尽的文档。无论您是用于快速原型开发还是构建大型应用，此模板都能为您节省大量的初始化和配置时间，让您可以专注于业务逻辑的实现。

祝您开发顺利！
