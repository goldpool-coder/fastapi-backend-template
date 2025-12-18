"""
Item CRUD 服务层
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, asc, desc

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    """Item 服务类"""

    @staticmethod
    def create(db: Session, item_in: ItemCreate) -> Item:
        """
        创建新的 Item
        
        Args:
            db: 数据库会话
            item_in: Item 创建数据
            
        Returns:
            创建的 Item 对象
        """
        item = Item(**item_in.model_dump())
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def get(db: Session, item_id: int) -> Optional[Item]:
        """
        根据 ID 获取 Item
        
        Args:
            db: 数据库会话
            item_id: Item ID
            
        Returns:
            Item 对象或 None
        """
        return db.query(Item).filter(Item.id == item_id).first()

    @staticmethod
    def get_multi(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        """
        获取多个 Item
        
        Args:
            db: 数据库会话
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            Item 列表
        """
        return db.query(Item).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, item_id: int, item_in: ItemUpdate) -> Optional[Item]:
        """
        更新 Item
        
        Args:
            db: 数据库会话
            item_id: Item ID
            item_in: 更新数据
            
        Returns:
            更新后的 Item 对象或 None
        """
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            return None

        update_data = item_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(item, field, value)

        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete(db: Session, item_id: int) -> bool:
        """
        删除 Item
        
        Args:
            db: 数据库会话
            item_id: Item ID
            
        Returns:
            是否删除成功
        """
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            return False

        db.delete(item)
        db.commit()
        return True

    @staticmethod
    def search(db: Session, keyword: str, skip: int = 0, limit: int = 100) -> List[Item]:
        """
        搜索 Item
        
        Args:
            db: 数据库会话
            keyword: 搜索关键词
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            Item 列表
        """
        return (
            db.query(Item)
            .filter(Item.title.contains(keyword))
            .offset(skip)
            .limit(limit)
            .all()
        )

    # --- 新增：过滤与分页支持 ---
    @staticmethod
    def count_filtered(db: Session, status: Optional[str] = None, is_active: Optional[bool] = None) -> int:
        """统计满足条件的 Item 总数"""
        q = db.query(func.count(Item.id))
        if status is not None:
            q = q.filter(Item.status == status)
        if is_active is not None:
            q = q.filter(Item.is_active == is_active)
        return q.scalar() or 0

    @staticmethod
    def get_multi_filtered(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        is_active: Optional[bool] = None,
        order: str = "desc",
    ) -> List[Item]:
        """按条件筛选并分页返回 Item 列表"""
        q = db.query(Item)
        if status is not None:
            q = q.filter(Item.status == status)
        if is_active is not None:
            q = q.filter(Item.is_active == is_active)
        if order == "asc":
            q = q.order_by(asc(Item.created_at))
        else:
            q = q.order_by(desc(Item.created_at))
        return q.offset(skip).limit(limit).all()
