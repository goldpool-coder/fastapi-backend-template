"""
演示 Redis 缓存的 API 路由
- 详情缓存：优先读取缓存，未命中则回源数据库，并写入缓存
- 列表缓存：演示读取/写入/清理
"""
from typing import Optional, Literal
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.item_service import ItemService
from app.services.cache_service import cache_service
from app.schemas.item import ItemResponse

router = APIRouter()


@router.get("/item/{item_id}", response_model=ItemResponse)
async def get_item_with_cache(item_id: int, db: Session = Depends(get_db)):
    """
    优先读取 Item 详情缓存，未命中则查询数据库并写入缓存
    """
    cached = await cache_service.get_item_cache(item_id)
    if cached:
        return ItemResponse.model_validate(cached)

    item = ItemService.get(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    data = ItemResponse.model_validate(item).model_dump()
    await cache_service.set_item_cache(item_id, data, expire_seconds=300)
    return ItemResponse.model_validate(data)


@router.post("/item/{item_id}/cache")
async def set_item_cache(item_id: int, db: Session = Depends(get_db)):
    """
    主动写入 Item 详情缓存（从数据库读取并写入缓存）
    """
    item = ItemService.get(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    data = ItemResponse.model_validate(item).model_dump()
    await cache_service.set_item_cache(item_id, data, expire_seconds=300)
    return {"success": True, "message": "Item 缓存已写入"}


@router.delete("/item/{item_id}/cache")
async def delete_item_cache(item_id: int):
    """
    删除 Item 详情缓存
    """
    await cache_service.delete_item_cache(item_id)
    return {"success": True}


@router.get("/items")
async def get_items_with_cache(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    is_active: Optional[bool] = None,
    order: Literal["asc", "desc"] = Query("desc", description="排序方式，asc/desc"),
    db: Session = Depends(get_db),
):
    """
    读取 Item 列表缓存，如果未命中则回源数据库，并写入缓存
    注意：为了演示，列表缓存 key 固定为所有列表的一个缓存，实际项目应按查询条件维度拆分 key
    """
    cached_list = await cache_service.get_item_list_cache()
    if cached_list:
        return {"from_cache": True, "data": cached_list}

    items = ItemService.get_multi_filtered(
        db,
        skip=skip,
        limit=limit,
        status=status,
        is_active=is_active,
        order=order,
    )
    data = [ItemResponse.model_validate(item).model_dump() for item in items]
    await cache_service.set_item_list_cache(data, expire_seconds=60)
    return {"from_cache": False, "data": data}


@router.post("/items/cache")
async def set_items_cache(db: Session = Depends(get_db)):
    """
    主动写入一个 Item 列表缓存（示例：读取前 10 条 active=true 的数据）
    """
    items = ItemService.get_multi_filtered(db, skip=0, limit=10, status="active", is_active=True, order="desc")
    data = [ItemResponse.model_validate(item).model_dump() for item in items]
    await cache_service.set_item_list_cache(data, expire_seconds=60)
    return {"success": True, "message": "Item 列表缓存已写入", "count": len(data)}


@router.delete("/items/cache")
async def delete_items_cache():
    """
    删除 Item 列表缓存
    """
    await cache_service.delete_item_list_cache()
    return {"success": True}