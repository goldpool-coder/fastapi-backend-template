"""
文件服务模块
处理文件上传、下载、删除等操作
"""
import os
import shutil
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException
import aiofiles

from app.core.config import settings


class FileService:
    """文件服务类"""

    def __init__(self):
        """初始化文件服务"""
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def _validate_file(self, filename: str) -> None:
        """
        验证文件扩展名
        
        Args:
            filename: 文件名
            
        Raises:
            HTTPException: 文件类型不允许
        """
        ext = filename.split(".")[-1].lower()
        if ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件类型: .{ext}，允许的类型: {', '.join(settings.ALLOWED_EXTENSIONS)}",
            )

    async def save_upload_file(
        self, upload_file: UploadFile, custom_filename: Optional[str] = None
    ) -> dict:
        """
        保存上传的文件
        
        Args:
            upload_file: 上传的文件对象
            custom_filename: 自定义文件名（可选）
            
        Returns:
            包含文件信息的字典
        """
        # 验证文件大小
        content = await upload_file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"文件大小超过限制 ({settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB)",
            )

        # 验证文件类型
        filename = custom_filename or upload_file.filename
        self._validate_file(filename)

        # 保存文件
        file_path = self.upload_dir / filename
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)

        return {
            "filename": filename,
            "path": str(file_path),
            "size": len(content),
            "content_type": upload_file.content_type,
        }

    def get_file_path(self, filename: str) -> Path:
        """
        获取文件路径
        
        Args:
            filename: 文件名
            
        Returns:
            文件路径
            
        Raises:
            HTTPException: 文件不存在
        """
        file_path = self.upload_dir / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="文件不存在")
        return file_path

    def delete_file(self, filename: str) -> bool:
        """
        删除文件
        
        Args:
            filename: 文件名
            
        Returns:
            是否删除成功
        """
        try:
            file_path = self.upload_dir / filename
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"删除文件失败: {str(e)}")

    def list_files(self) -> list:
        """
        列出所有上传的文件
        
        Returns:
            文件列表
        """
        files = []
        for file_path in self.upload_dir.iterdir():
            if file_path.is_file():
                files.append(
                    {
                        "filename": file_path.name,
                        "size": file_path.stat().st_size,
                        "created_at": file_path.stat().st_ctime,
                    }
                )
        return files


# 创建全局文件服务实例
file_service = FileService()
