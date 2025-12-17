"""
示例数据模型 - Item
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean

from app.db.session import Base


class Item(Base):
    """物品模型"""

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    title = Column(String(200), nullable=False, index=True, comment="标题")
    description = Column(Text, nullable=True, comment="描述")
    status = Column(String(50), default="active", comment="状态")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间"
    )

    def __repr__(self):
        return f"<Item(id={self.id}, title={self.title})>"
