# 快速开始指南

本指南将帮助您在 5 分钟内快速启动并运行此 FastAPI 后端项目模板。

## 前置条件检查

在开始之前，请确保您的系统已安装以下软件：

-   **Python 3.13 或更高版本**: 运行 `python --version` 检查版本。
-   **Poetry**: 运行 `poetry --version` 检查是否已安装。如果未安装，请访问 [Poetry 官方文档](https://python-poetry.org/docs/#installation) 进行安装。
-   **数据库**: MySQL 8.0+ 或 MS SQL Server 2022+。

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

此命令会自动创建一个虚拟环境并安装 `pyproject.toml` 中定义的所有依赖。安装过程可能需要几分钟时间，具体取决于您的网络速度。

## 步骤 3: 配置环境变量

复制示例环境变量文件并根据您的本地环境进行修改：

```bash
cp .env.example .env
```

使用文本编辑器打开 `.env` 文件，至少需要修改以下配置：

```env
# 数据库配置 - MySQL 示例
DATABASE_TYPE=mysql
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=your_mysql_password
DATABASE_NAME=fastapi_db
```

如果您使用的是 MS SQL Server，请将 `DATABASE_TYPE` 改为 `mssql` 并填写相应的连接信息。

## 步骤 4: 初始化数据库

在首次运行应用之前，需要创建数据库表：

```bash
poetry run python scripts/init_db.py
```

如果一切正常，您将看到 "✅ 数据库表创建成功" 的提示信息。

## 步骤 5: 启动应用

使用以下命令启动 FastAPI 应用：

```bash
poetry run python app/main.py
```

或者使用 Uvicorn 直接启动（推荐用于开发环境）：

```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

`--reload` 参数会在代码发生变化时自动重启服务器，非常适合开发调试。

## 步骤 6: 验证安装

应用启动后，您将在控制台看到类似以下的输出：

```
🚀 FastAPI Backend Template 正在启动...
📝 API 文档地址: http://0.0.0.0:8000/api/v1/docs
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

打开浏览器，访问以下地址来验证安装：

-   **健康检查**: [http://localhost:8000/health](http://localhost:8000/health)
-   **API 文档 (Swagger UI)**: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
-   **API 文档 (ReDoc)**: [http://localhost:8000/api/v1/redoc](http://localhost:8000/api/v1/redoc)

## 步骤 7: 测试 API

在 Swagger UI 界面中，您可以直接测试所有的 API 端点。例如，创建一个新的 Item：

1.  展开 `POST /api/v1/items/` 端点。
2.  点击 "Try it out" 按钮。
3.  在请求体中输入以下 JSON 数据：
    ```json
    {
      "title": "我的第一个 Item",
      "description": "这是一个测试项目",
      "status": "active",
      "is_active": true
    }
    ```
4.  点击 "Execute" 按钮发送请求。
5.  您将在响应区域看到创建成功的 Item 数据，包括自动生成的 ID 和时间戳。

## 下一步

恭喜！您已经成功启动了 FastAPI 后端项目模板。接下来您可以：

-   阅读 [项目总览文档](PROJECT_OVERVIEW.md) 了解项目架构和设计理念。
-   查看 [开发环境配置指南](DEVELOPMENT.md) 学习如何在 PyCharm 中进行高效开发。
-   参考 [部署指南](DEPLOYMENT.md) 将应用部署到生产环境。
-   根据您的业务需求，开始添加新的数据模型和 API 端点。

如果在启动过程中遇到任何问题，请检查：

-   数据库服务是否正在运行。
-   `.env` 文件中的数据库连接信息是否正确。
-   Python 和 Poetry 的版本是否满足要求。
