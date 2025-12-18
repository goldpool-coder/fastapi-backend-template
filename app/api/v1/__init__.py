from fastapi import APIRouter

from .items import router as items_router
from .files import router as files_router
from .demo_cache import router as cache_demo_router
from .demo_mqtt import router as mqtt_demo_router
from .demo_http import router as http_demo_router
from .demo_logs import router as logs_demo_router

api_router = APIRouter()
api_router.include_router(items_router, prefix="/items", tags=["Items"])
api_router.include_router(files_router, prefix="/files", tags=["Files"])
api_router.include_router(cache_demo_router, prefix="/demo/cache", tags=["Demo-Cache"])
api_router.include_router(mqtt_demo_router, prefix="/demo/mqtt", tags=["Demo-MQTT"])
api_router.include_router(http_demo_router, prefix="/demo/http", tags=["Demo-HTTP"])
api_router.include_router(logs_demo_router, prefix="/demo/logs", tags=["Demo-Logs"])
