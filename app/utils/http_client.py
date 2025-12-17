"""
HTTP 客户端工具模块
用于发起外部 API 请求
"""
import httpx
from typing import Optional, Dict, Any


class HTTPClient:
    """HTTP 客户端类"""

    def __init__(self, base_url: Optional[str] = None, timeout: int = 30):
        """
        初始化 HTTP 客户端
        
        Args:
            base_url: 基础 URL
            timeout: 超时时间（秒）
        """
        self.base_url = base_url
        self.timeout = timeout

    async def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        发起 GET 请求
        
        Args:
            url: 请求 URL
            params: 查询参数
            headers: 请求头
            
        Returns:
            响应 JSON 数据
        """
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()

    async def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        发起 POST 请求
        
        Args:
            url: 请求 URL
            data: 表单数据
            json: JSON 数据
            headers: 请求头
            
        Returns:
            响应 JSON 数据
        """
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            response = await client.post(url, data=data, json=json, headers=headers)
            response.raise_for_status()
            return response.json()

    async def download_file(self, url: str, save_path: str) -> None:
        """
        下载文件
        
        Args:
            url: 文件 URL
            save_path: 保存路径
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            async with client.stream("GET", url) as response:
                response.raise_for_status()
                with open(save_path, "wb") as f:
                    async for chunk in response.aiter_bytes():
                        f.write(chunk)


# 创建全局 HTTP 客户端实例
http_client = HTTPClient()
