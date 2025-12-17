"""
文件上传下载相关的 API 路由
"""
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from app.services.file_service import file_service

router = APIRouter()


@router.post("/upload", status_code=201)
async def upload_file(
    file: UploadFile = File(..., description="要上传的文件"),
):
    """
    上传文件
    """
    result = await file_service.save_upload_file(file)
    return {
        "message": "文件上传成功",
        "data": result,
    }


@router.get("/download/{filename}")
async def download_file(filename: str):
    """
    下载文件
    """
    file_path = file_service.get_file_path(filename)
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream",
    )


@router.delete("/{filename}", status_code=204)
def delete_file(filename: str):
    """
    删除文件
    """
    success = file_service.delete_file(filename)
    if not success:
        raise HTTPException(status_code=404, detail="文件不存在")
    return None


@router.get("/", response_model=List[dict])
def list_files():
    """
    列出所有文件
    """
    files = file_service.list_files()
    return files
