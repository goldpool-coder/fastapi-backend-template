# 快速开始指南

本指南将帮助您在 5 分钟内快速启动并运行此 FastAPI 后端项目模板。

## 前置条件检查

在开始之前，请确保您的系统已安装以下软件：

-   **Python 3.13 或更高版本**: 运行 `python --version` 检查版本。
-   **Poetry**: 运行 `poetry --version` 检查是否已安装。
-   **数据库**: MySQL 8.0+ 或 MS SQL Server 2022+。
-   **Redis**: 缓存服务（可选，推荐使用 Docker 启动）。
-   **MQTT Broker**: 消息代理服务（可选，推荐使用 Docker 启动）。

## 步骤 1: 获取项目代码

如果您已经下载了项目压缩包，请解压到您的工作目录：

```bash
tar -xzf fastapi-backend-template.tar.gz
cd fastapi-backend-template
```

如果项目托管在 Git 仓库中，可以通过克隆获取：

```bash
git clone <repository-url>
cd fastapi-backend-template
```

## 步骤 2: 安装项目依赖

使用 Poetry 安装所有必需的 Python 包：

```bash
poetry install
```

## 步骤 3: 配置环境变量

复制示例环境变量文件并根据您的本地环境进行修改：

```bash
cp .env.example .env
```

使用文本编辑器打开 `.env` 文件，配置数据库、Redis 和 MQTT 连接信息。

**注意**: 如果您使用 Docker Compose 启动服务，请将 `.env` 中的 `DATABASE_HOST` 设置为 `mysql`，`REDIS_HOST` 设置为 `redis`，`MQTT_HOST` 设置为 `mosquitto`。如果是在本地裸机运行，则都设置为 `localhost`。

## 步骤 4: 初始化数据库

在首次运行应用之前，需要创建数据库表：

```bash
poetry run python scripts/init_db.py
```

如果一切正常，您将看到 "✅ 数据库表创建成功" 的提示信息。

## 步骤 5: 启动应用

### 选项 A: 本地启动 (需要本地安装并运行 MySQL/Redis/MQTT)

```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 选项 B: Docker Compose 启动 (推荐)

如果您想一键启动所有服务（应用、MySQL、Redis、Mosquitto），请使用 Docker Compose：

```bash
docker-compose up -d
```

## 步骤 6: 验证安装

应用启动后，您将在控制台看到 Redis 和 MQTT 的连接信息。

打开浏览器，访问以下地址来验证安装：

-   **健康检查**: [http://localhost:8000/health](http://localhost:8000/health)
-   **API 文档 (Swagger UI)**: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)

## 步骤 7: 测试新功能

-   **测试缓存**: 可以在 `app/services/cache_service.py` 中查看 Redis 缓存的设置和获取逻辑。
-   **测试消息**: 可以在 `app/services/message_service.py` 中查看 MQTT 消息的发布和订阅逻辑。您可以使用任何 MQTT 客户端工具连接到 `localhost:1883`，向 `command/video_crawler` 主题发送消息，观察应用日志的响应。

## 下一步

恭喜！您已经成功启动了扩展后的 FastAPI 后端项目模板。接下来您可以：

-   阅读 [项目总览文档](PROJECT_OVERVIEW.md) 了解项目架构和设计理念。
-   查看 [开发环境配置指南](DEVELOPMENT.md) 学习如何在 PyCharm 中进行高效开发。
-   参考 [部署指南](DEPLOYMENT.md) 将应用部署到生产环境。
-   根据您的业务需求，开始添加新的数据模型和 API 端点。
