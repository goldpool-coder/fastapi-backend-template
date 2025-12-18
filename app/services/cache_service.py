"""
缓存服务模块
封装基于 Redis 的业务缓存逻辑
"""
from typing import Any, Optional

from app.utils.redis_client import redis_client


class CacheService:
    """缓存服务类"""

    @staticmethod
    async def set_item_cache(item_id: int, item_data: Any, expire_seconds: int = 300):
        """
        设置 Item 详情缓存
        
        Args:
            item_id: Item ID
            item_data: Item 数据
            expire_seconds: 过期时间
        """
        key = f"item:{item_id}"
        await redis_client.set_cache(key, item_data, ex=expire_seconds)

    @staticmethod
    async def get_item_cache(item_id: int) -> Optional[Any]:
        """
        获取 Item 详情缓存
        
        Args:
            item_id: Item ID
            
        Returns:
            Item 数据或 None
        """
        key = f"item:{item_id}"
        return await redis_client.get_cache(key)

    @staticmethod
    async def delete_item_cache(item_id: int):
        """
        删除 Item 详情缓存
        
        Args:
            item_id: Item ID
        """
        key = f"item:{item_id}"
        await redis_client.delete_cache(key)

    # --- 示例：缓存列表 ---

    @staticmethod
    async def set_item_list_cache(list_data: Any, expire_seconds: int = 60):
        """
        设置 Item 列表缓存
        """
        key = "item:list:all"
        await redis_client.set_cache(key, list_data, ex=expire_seconds)

    @staticmethod
    async def get_item_list_cache() -> Optional[Any]:
        """
        获取 Item 列表缓存
        """
        key = "item:list:all"
        return await redis_client.get_cache(key)


# 创建全局缓存服务实例
cache_service = CacheService()
