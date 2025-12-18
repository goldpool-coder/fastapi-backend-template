"""
Redis 客户端工具模块
"""
import json
from typing import Any, Optional
import redis.asyncio as redis

from app.core.config import settings


class RedisClient:
    """Redis 客户端类"""

    def __init__(self):
        """初始化 Redis 连接"""
        self._redis_client: Optional[redis.Redis] = None

    async def connect(self):
        """建立 Redis 连接"""
        self._redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
        try:
            await self._redis_client.ping()
            print("✅ Redis 连接成功")
        except Exception as e:
            print(f"❌ Redis 连接失败: {e}")
            self._redis_client = None

    async def disconnect(self):
        """断开 Redis 连接"""
        if self._redis_client:
            await self._redis_client.close()
            print("🛑 Redis 连接已断开")

    @property
    def client(self) -> redis.Redis:
        """获取 Redis 客户端实例"""
        if not self._redis_client:
            raise ConnectionError("Redis 客户端未连接")
        return self._redis_client

    # --- 缓存操作 ---

    async def set_cache(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """
        设置缓存
        
        Args:
            key: 键
            value: 值 (会自动序列化为 JSON)
            ex: 过期时间（秒）
            
        Returns:
            是否设置成功
        """
        try:
            serialized_value = json.dumps(value)
            return await self.client.set(key, serialized_value, ex=ex)
        except Exception as e:
            print(f"Redis set_cache 失败: {e}")
            return False

    async def get_cache(self, key: str) -> Optional[Any]:
        """
        获取缓存
        
        Args:
            key: 键
            
        Returns:
            值 (会自动反序列化为 Python 对象) 或 None
        """
        try:
            value = await self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Redis get_cache 失败: {e}")
            return None

    async def delete_cache(self, key: str) -> int:
        """
        删除缓存
        
        Args:
            key: 键
            
        Returns:
            删除的键的数量
        """
        try:
            return await self.client.delete(key)
        except Exception as e:
            print(f"Redis delete_cache 失败: {e}")
            return 0


# 创建全局 Redis 客户端实例
redis_client = RedisClient()
