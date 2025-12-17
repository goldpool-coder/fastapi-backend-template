"""
Item 相关的 API 路由
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.services.item_service import ItemService

router = APIRouter()


@router.post("/", response_model=ItemResponse, status_code=201)
def create_item(
    item_in: ItemCreate,
    db: Session = Depends(get_db),
):
    """
    创建新的 Item
    """
    item = ItemService.create(db=db, item_in=item_in)
    return item


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    """
    根据 ID 获取 Item
    """
    item = ItemService.get(db=db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item 不存在")
    return item


@router.get("/", response_model=List[ItemResponse])
def list_items(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的最大记录数"),
    db: Session = Depends(get_db),
):
    """
    获取 Item 列表
    """
    items = ItemService.get_multi(db=db, skip=skip, limit=limit)
    return items


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item_in: ItemUpdate,
    db: Session = Depends(get_db),
):
    """
    更新 Item
    """
    item = ItemService.update(db=db, item_id=item_id, item_in=item_in)
    if not item:
        raise HTTPException(status_code=404, detail="Item 不存在")
    return item


@router.delete("/{item_id}", status_code=204)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    """
    删除 Item
    """
    success = ItemService.delete(db=db, item_id=item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item 不存在")
    return None


@router.get("/search/", response_model=List[ItemResponse])
def search_items(
    keyword: str = Query(..., min_length=1, description="搜索关键词"),
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的最大记录数"),
    db: Session = Depends(get_db),
):
    """
    搜索 Item
    """
    items = ItemService.search(db=db, keyword=keyword, skip=skip, limit=limit)
    return items
