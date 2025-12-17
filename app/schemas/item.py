"""
Item 相关的 Pydantic Schema
用于请求验证和响应序列化
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """Item 基础 Schema"""

    title: str = Field(..., min_length=1, max_length=200, description="标题")
    description: Optional[str] = Field(None, description="描述")
    status: str = Field(default="active", description="状态")
    is_active: bool = Field(default=True, description="是否激活")


class ItemCreate(ItemBase):
    """创建 Item 的 Schema"""

    pass


class ItemUpdate(BaseModel):
    """更新 Item 的 Schema"""

    title: Optional[str] = Field(None, min_length=1, max_length=200, description="标题")
    description: Optional[str] = Field(None, description="描述")
    status: Optional[str] = Field(None, description="状态")
    is_active: Optional[bool] = Field(None, description="是否激活")


class ItemInDB(ItemBase):
    """数据库中的 Item Schema"""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ItemResponse(ItemInDB):
    """Item 响应 Schema"""

    pass
