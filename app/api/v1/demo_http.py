"""
外部 API 调用演示路由
- 通过 utils.http_client 进行 GET/POST 请求
- 支持下载文件到本地 uploads/downloads 目录
"""
from typing import Any, Dict, Optional
from pathlib import Path
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from app.utils.http_client import http_client
from app.core.config import settings

router = APIRouter()


class GetRequest(BaseModel):
    url: str = Field(..., description="目标 URL")
    params: Optional[Dict[str, Any]] = Field(None, description="查询参数")
    headers: Optional[Dict[str, str]] = Field(None, description="请求头")


class PostRequest(BaseModel):
    url: str = Field(..., description="目标 URL")
    data: Optional[Dict[str, Any]] = Field(None, description="表单数据")
    body: Optional[Dict[str, Any]] = Field(None, description="JSON 请求体")
    headers: Optional[Dict[str, str]] = Field(None, description="请求头")


@router.post("/get")
async def demo_get(req: GetRequest):
    """演示 GET 请求调用外部 API"""
    result = await http_client.get(req.url, params=req.params, headers=req.headers)
    return {"success": True, "data": result}


@router.post("/post")
async def demo_post(req: PostRequest):
    """演示 POST 请求调用外部 API"""
    result = await http_client.post(req.url, data=req.data, json=req.body, headers=req.headers)
    return {"success": True, "data": result}


@router.get("/download")
async def demo_download(url: str = Query(..., description="文件 URL")):
    """演示下载外部文件到本地"""
    downloads_dir = Path(settings.UPLOAD_DIR) / "downloads"
    downloads_dir.mkdir(parents=True, exist_ok=True)

    # 根据 URL 推断文件名
    filename = url.split("?")[0].rstrip("/").split("/")[-1] or "download.bin"
    save_path = downloads_dir / filename

    await http_client.download_file(url, str(save_path))
    return {"success": True, "saved_path": str(save_path)}