"""
FastAPI 应用主入口文件
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import api_router
from app.core.config import settings

# 创建 FastAPI 应用实例
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# 配置 CORS 中间件
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
async def startup_event():
    """应用启动时的事件处理"""
    print(f"🚀 {settings.PROJECT_NAME} 正在启动...")
    print(f"📝 API 文档地址: http://{settings.HOST}:{settings.PORT}{settings.API_V1_STR}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的事件处理"""
    print(f"🛑 {settings.PROJECT_NAME} 正在关闭...")


@app.get("/")
async def root():
    """根路径健康检查"""
    return JSONResponse(
        content={
            "message": f"欢迎使用 {settings.PROJECT_NAME}",
            "version": settings.VERSION,
            "docs": f"{settings.API_V1_STR}/docs",
        }
    )


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return JSONResponse(content={"status": "healthy"})


# 注册 API 路由
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
