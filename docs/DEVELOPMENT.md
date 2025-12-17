# 开发环境配置指南

本指南将详细介绍如何配置 PyCharm IDE 以进行本项目的高效开发、测试和调试。

## 1. 前置要求

- **IDE**: [PyCharm Professional](https://www.jetbrains.com/pycharm/download/) 2024.2 或更高版本。专业版提供了对 FastAPI 的原生支持，强烈推荐使用。
- **Python**: 3.13 或更高版本。
- **Poetry**: 一个现代化的 Python 依赖管理工具。如果尚未安装，请参考 [官方文档](https://python-poetry.org/docs/#installation) 进行安装。

## 2. PyCharm 安装与初始配置

1.  **下载并安装 PyCharm**: 从 JetBrains 官网下载并安装 PyCharm Professional。
2.  **安装推荐插件**: 为了提升开发效率，建议安装以下插件：
    *   **Python**: PyCharm 自带的核心插件。
    *   **.env files support**: 支持 `.env` 文件语法高亮和变量补全。
    *   **Docker**: 提供 Docker 镜像和容器的管理界面。
    *   **Markdown**: 提供 Markdown 文件的实时预览和编辑支持。

    安装方法：进入 `File` > `Settings` > `Plugins`，在 Marketplace 中搜索并安装上述插件。

## 3. 在 PyCharm 中配置项目

1.  **打开项目**: 启动 PyCharm，选择 `File` > `Open`，然后选择项目根目录 `fastapi-backend-template`。

2.  **配置 Python 解释器和 Poetry 环境**:
    *   PyCharm 通常会自动检测到 `pyproject.toml` 文件并建议使用 Poetry 环境。如果未自动配置，请手动操作。
    *   进入 `File` > `Settings` > `Project: fastapi-backend-template` > `Python Interpreter`。
    *   点击右上角的 `Add Interpreter`，选择 `Add Local Interpreter`。
    *   在左侧选择 `Poetry Environment`。
    *   PyCharm 会自动检测到 Poetry 可执行文件。如果找不到，请手动指定其路径。
    *   选择 `Install packages from pyproject.toml`。
    *   点击 `OK`，PyCharm 将会创建一个新的 Poetry 虚拟环境并安装所有依赖。

    ![PyCharm Poetry Interpreter](https://i.imgur.com/your-image-link-here.png)  <!-- 占位符，实际应替换为截图 -->

3.  **配置环境变量**: 
    *   复制 `.env.example` 文件并重命名为 `.env`。
    *   根据你的本地环境（特别是数据库连接信息）修改 `.env` 文件。
    *   PyCharm 会自动识别 `.env` 文件，并在运行时加载其中的环境变量。

## 4. 运行与调试

1.  **创建运行/调试配置**:
    *   点击 PyCharm 右上角的 `Add Configuration...`。
    *   点击 `+` 号，选择 `Python`。
    *   **Name**: `Run FastAPI App`
    *   **Script path**: 选择项目中的 `app/main.py` 文件。
    *   **Environment variables**: 确认 `Enable EnvFile` 已勾选，并指向项目根目录的 `.env` 文件。
    *   点击 `OK` 保存配置。

2.  **启动应用**:
    *   选择刚刚创建的 `Run FastAPI App` 配置。
    *   点击绿色的 `Run` 按钮 (▶️) 启动应用。
    *   控制台将显示应用启动信息，包括 API 文档地址。

3.  **调试应用**:
    *   在代码中设置断点（点击行号左侧空白处）。
    *   点击绿色的 `Debug` 按钮 (🐞) 启动调试模式。
    *   当代码执行到断点时，程序将暂停，你可以检查变量、执行表达式等。

## 5. 测试 API 接口

PyCharm Professional 提供了内置的 HTTP Client，可以方便地测试 API。

1.  **使用 OpenAPI (Swagger UI)**:
    *   启动应用后，在浏览器中访问 `http://localhost:8000/api/v1/docs`。
    *   你可以在这个交互式界面中测试所有 API 端点。

2.  **使用 PyCharm HTTP Client**:
    *   在 `api/v1` 目录下，你会看到每个路由文件旁边都有一个绿色的播放按钮。
    *   点击按钮，选择 `Run all requests in...`，PyCharm 会自动生成一个 `.http` 文件，并列出所有可用的端点。
    *   你可以直接点击每个请求旁边的播放按钮来发送请求并查看响应。

    ```http
    ### Create a new item
    POST http://localhost:8000/api/v1/items/
    Content-Type: application/json

    {
      "title": "My New Item",
      "description": "This is a test item."
    }
    ```

## 6. 功能与模块说明

-   **`app/main.py`**: 应用主入口，负责创建 FastAPI 实例、配置中间件、注册路由和启动事件。
-   **`app/core/config.py`**: 使用 Pydantic Settings 管理所有配置。配置项优先从环境变量读取，其次是 `.env` 文件，最后是代码中的默认值。
-   **`app/db/session.py`**: 负责数据库连接和会话管理。`get_db` 是一个标准的 FastAPI 依赖项，用于在请求处理期间提供数据库会话。
-   **`app/models/`**: 存放 SQLAlchemy 的数据模型。每个文件对应一个数据表。
-   **`app/schemas/`**: 存放 Pydantic 的数据校验模型 (Schema)。用于请求体验证和响应数据序列化，确保 API 的类型安全。
-   **`app/services/`**: 业务逻辑层。将数据库操作和业务规则封装在此处，使 API 路由层保持简洁。
    -   `item_service.py`: 演示了标准的 CRUD (Create, Read, Update, Delete) 操作。
    -   `file_service.py`: 演示了文件上传、下载和管理功能。
-   **`app/api/v1/`**: API 路由层。负责处理 HTTP 请求，调用服务层完成业务逻辑，并返回响应。
-   **`scripts/init_db.py`**: 用于在应用首次启动前初始化数据库，创建所有数据表。
