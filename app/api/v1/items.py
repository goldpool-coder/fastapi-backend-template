"""Item 相关 API 路由"""
from typing import List, Optional, Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.item import (
    ItemCreate,
    ItemUpdate,
    ItemResponse,
    ItemListResponse,
)
from app.services.item_service import ItemService

router = APIRouter()


@router.post("/", response_model=ItemResponse)
async def create_item(item_in: ItemCreate, db: Session = Depends(get_db)):
    """创建 Item"""
    item = ItemService.create(db, item_in)
    return ItemResponse.model_validate(item)


@router.get("/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    """根据 ID 获取单个 Item"""
    item = ItemService.get(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse.model_validate(item)


@router.get("/", response_model=List[ItemResponse])
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取多个 Item（基础列表接口）"""
    items = ItemService.get_multi(db, skip=skip, limit=limit)
    return [ItemResponse.model_validate(item) for item in items]


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int, item_in: ItemUpdate, db: Session = Depends(get_db)
):
    """更新 Item"""
    item = ItemService.update(db, item_id, item_in)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse.model_validate(item)


@router.delete("/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """删除 Item"""
    success = ItemService.delete(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"success": True}


@router.get("/search/", response_model=List[ItemResponse])
async def search_items(
    keyword: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """根据关键词搜索 Item"""
    items = ItemService.search(db, keyword, skip=skip, limit=limit)
    return [ItemResponse.model_validate(item) for item in items]


# --- 新增：标准分页 + 条件过滤示例 ---
@router.get("/page/", response_model=ItemListResponse)
async def read_items_paged(
    skip: int = Query(0, ge=0, description="起始偏移量"),
    limit: int = Query(10, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query(None, description="按状态过滤，例如: pending/done"),
    is_active: Optional[bool] = Query(None, description="按是否启用过滤"),
    order: Literal["asc", "desc"] = Query("desc", description="排序方式，asc/desc"),
    db: Session = Depends(get_db),
):
    """分页 + 条件过滤获取 Item 列表（CRUD 示例）"""
    total = ItemService.count_filtered(db, status=status, is_active=is_active)
    items = ItemService.get_multi_filtered(
        db,
        skip=skip,
        limit=limit,
        status=status,
        is_active=is_active,
        order=order,
    )
    return ItemListResponse(
        total=total,
        items=[ItemResponse.model_validate(item) for item in items],
        skip=skip,
        limit=limit,
    )
