"""
应用核心配置模块
使用 Pydantic Settings 管理环境变量和配置
"""
from typing import List, Optional, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置类"""

    # 基础配置
    PROJECT_NAME: str = "FastAPI Backend Template"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "通用 FastAPI 后端项目模板，支持 MySQL/MSSQL/PostgreSQL 数据库"
    API_V1_STR: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # CORS 配置
    BACKEND_CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """解析 CORS 配置"""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # 数据库配置
    # 可选类型: mysql, mssql, postgres, postgresql
    DATABASE_TYPE: str = "mysql"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 3306
    DATABASE_USER: str = "root"
    DATABASE_PASSWORD: str = "password"
    DATABASE_NAME: str = "fastapi_db"
    DATABASE_ECHO: bool = False  # 是否打印 SQL 语句

    # MSSQL 特定配置
    MSSQL_DRIVER: str = "ODBC Driver 17 for SQL Server"

    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "gif", "pdf", "txt", "zip"]

    # Redis 配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = ""

    @property
    def REDIS_URL(self) -> str:
        """生成 Redis 连接字符串"""
        # 如提供密码，则使用带密码的连接字符串（不记录/不打印密码）
        if self.REDIS_PASSWORD:
            return (
                f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
            )
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # MQTT 配置
    MQTT_HOST: str = "localhost"
    MQTT_PORT: int = 1883
    MQTT_USER: str = ""
    MQTT_PASSWORD: str = ""

    # JWT 配置 (可选)
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    @property
    def database_url(self) -> str:
        """根据数据库类型生成连接字符串"""
        if self.DATABASE_TYPE == "mysql":
            return (
                f"mysql+pymysql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
                f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
            )
        elif self.DATABASE_TYPE == "mssql":
            return (
                f"mssql+pyodbc://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
                f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
                f"?driver={self.MSSQL_DRIVER.replace(' ', '+')}"
            )
        elif self.DATABASE_TYPE in ("postgres", "postgresql"):
            # 使用 SQLAlchemy 官方推荐的 psycopg 驱动
            return (
                f"postgresql+psycopg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
                f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
            )
        else:
            raise ValueError(f"不支持的数据库类型: {self.DATABASE_TYPE}")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )


# 创建全局配置实例
settings = Settings()
