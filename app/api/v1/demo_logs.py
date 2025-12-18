"""
日志读写演示路由
- 写业务日志
- 读取日志文件最近 N 行
"""
from typing import List
from pathlib import Path
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from app.utils.logger import logger
from app.core.config import settings

router = APIRouter()


class LogRequest(BaseModel):
    level: str = Field(..., description="日志级别: DEBUG/INFO/WARNING/ERROR")
    message: str = Field(..., description="日志内容")


@router.post("/write")
async def write_log(req: LogRequest):
    """写业务日志到系统日志文件"""
    level = req.level.upper()
    if level == "DEBUG":
        logger.debug(req.message)
    elif level == "INFO":
        logger.info(req.message)
    elif level == "WARNING":
        logger.warning(req.message)
    elif level == "ERROR":
        logger.error(req.message)
    else:
        return {"success": False, "error": "不支持的日志级别"}
    return {"success": True}


@router.get("/read")
async def read_logs(lines: int = Query(50, ge=1, le=1000, description="读取最近 N 行日志")) -> List[str]:
    """读取日志文件最近 N 行"""
    log_path = Path(settings.LOG_FILE)
    if not log_path.exists():
        return []

    # 读取文件尾部最近 N 行
    with log_path.open("r", encoding="utf-8") as f:
        content = f.readlines()
    return content[-lines:]