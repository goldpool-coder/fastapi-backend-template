"""
API v1 路由聚合
"""
from fastapi import APIRouter

from app.api.v1 import items, files

api_router = APIRouter()

# 注册各个模块的路由
api_router.include_router(items.router, prefix="/items", tags=["Items"])
api_router.include_router(files.router, prefix="/files", tags=["Files"])
