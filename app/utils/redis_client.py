"""
Redis 客户端工具模块
支持受保护（需密码/用户名）的 Redis 连接
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

    async def connect(
        self,
        url: Optional[str] = None,
        *,
        password: Optional[str] = None,
        username: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        db: Optional[int] = None,
    ):
        """
        建立 Redis 连接
        
        Args:
            url: 连接字符串（如 redis://:password@host:port/db），不提供则使用配置 settings.REDIS_URL
            password: 密码（优先级高于 url，用于受保护的 Redis）
            username: 用户名（Redis 6+ ACL，可选）
            host: 主机（不提供则使用 settings.REDIS_HOST）
            port: 端口（不提供则使用 settings.REDIS_PORT）
            db: 数据库编号（不提供则使用 settings.REDIS_DB）
        """
        try:
            if password is not None or username is not None:
                # 显式使用用户名/密码连接（避免在 URL 中曝光密码）
                self._redis_client = redis.Redis(
                    host=host or settings.REDIS_HOST,
                    port=port or settings.REDIS_PORT,
                    db=db or settings.REDIS_DB,
                    password=password if password is not None else (settings.REDIS_PASSWORD or None),
                    username=username,
                    encoding="utf-8",
                    decode_responses=True,
                )
            else:
                # 优先使用显式传入的 URL；否则使用配置中的 REDIS_URL（已包含密码时自动认证）
                final_url = url or settings.REDIS_URL
                self._redis_client = redis.from_url(
                    final_url,
                    encoding="utf-8",
                    decode_responses=True,
                )

            # 测试连接
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
