# =========================================================================
# 第一阶段：构建器 (Builder)
# 这个阶段负责编译和安装所有依赖，包括开发依赖。
# =========================================================================
FROM python:3.13-slim as builder

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.8.0 \
    POETRY_HOME="/opt/poetry" \
    # 核心修改：告诉 Poetry 在项目目录中创建 .venv 文件夹
    POETRY_VIRTUALENVS_IN_PROJECT=true

# 将 Poetry 安装到系统路径中
ENV PATH="$POETRY_HOME/bin:$PATH"

# 安装构建所需的系统依赖和 Poetry
RUN pip install poetry==1.8.0

# 设置工作目录
WORKDIR /app

# 复制依赖定义文件
# 这样可以利用 Docker 缓存  ，只有当这些文件变化时才重新安装依赖
COPY pyproject.toml poetry.lock* ./

# 安装项目依赖
# --no-dev 确保只安装生产环境需要的包
RUN poetry install --no-interaction --no-ansi --no-root --only main


# =========================================================================
# 第二阶段：最终镜像 (Final Image)
# 这个阶段只包含运行应用所必需的文件，非常轻量。
# =========================================================================
FROM python:3.13-slim as final

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 设置工作目录
WORKDIR /app

# [安全优化] 创建一个非 root 用户来运行应用
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 安装仅在运行时需要的系统依赖
# 注意：如果你的应用运行时需要 odbc，则保留 unixodbc-dev。如果只是编译时需要，可以去掉。
# 我们假设运行时也需要它。
RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev \
    curl \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 从构建器阶段复制已安装的 Python 依赖
COPY --from=builder /app/.venv /app/.venv

# 将虚拟环境的路径加入 PATH，这样可以直接执行包里的命令
ENV PATH="/app/.venv/bin:$PATH"

# 复制项目代码
# 注意：这里的 . . 会复制你项目根目录下的所有文件，包括 venv 和 app 文件夹
# 这意味着容器内的 /app 目录下会有一个 app 子目录，即 /app/app/
# 你的启动命令 CMD ["uvicorn", "app.main:app", ...] 是正确的，因为它会寻找 /app/app/main.py
COPY --chown=appuser:appuser . .

# 创建并赋予新用户目录权限
RUN mkdir -p uploads logs \
    && chown -R appuser:appuser uploads logs /app

# 切换到非 root 用户
USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
