"""
MQTT 收发演示路由
- 通过 command 主题发布命令（start_crawl/stop_crawl），由 MessageService 订阅处理
- 通过 status 主题发布状态消息
- 健康检查查看 MQTT 连接状态
- 通用发布到任意主题
- WebSocket 订阅指定主题，实时接收 MQTT 消息
"""
from typing import Any, Literal, List, Tuple, Dict
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from pydantic import BaseModel, Field

from app.utils.mqtt_client import mqtt_client
from app.services.message_service import message_service  # 导入以确保订阅注册

router = APIRouter()


class CommandRequest(BaseModel):
    action: Literal["start_crawl", "stop_crawl"]


class StatusRequest(BaseModel):
    status: str = Field(..., description="状态，如: started/progress/completed/error")
    details: Any = Field(..., description="详细信息")


class PublishRequest(BaseModel):
    topic: str = Field(..., description="要发布的主题")
    payload: str = Field(..., description="消息内容")
    qos: int = Field(0, ge=0, le=2, description="服务质量等级 0/1/2")
    retain: bool = Field(False, description="是否保留消息")


@router.get("/health")
async def mqtt_health():
    """查看 MQTT 客户端连接状态"""
    return {"is_connected": mqtt_client.is_connected}


@router.post("/command")
async def publish_command(req: CommandRequest):
    """向 command/video_crawler 主题发布命令"""
    ok = mqtt_client.publish("command/video_crawler", req.action)
    return {"success": ok, "topic": "command/video_crawler", "payload": req.action}


@router.post("/status")
async def publish_status(req: StatusRequest):
    """向 status/video_crawler 主题发布状态消息（由 MessageService 封装）"""
    message_service.publish_crawl_status(req.status, req.details)
    return {"success": True, "topic": "status/video_crawler"}


@router.post("/publish")
async def publish_generic(req: PublishRequest):
    """通用发布接口：向任意主题发布消息"""
    ok = mqtt_client.publish(req.topic, req.payload, qos=req.qos, retain=req.retain)
    return {"success": ok, "topic": req.topic, "payload": req.payload, "qos": req.qos, "retain": req.retain}


# WebSocket 订阅管理器
class MQTTWebSocketManager:
    def __init__(self):
        # topic -> list[(websocket, loop)]
        self.subscribers: Dict[str, List[Tuple[WebSocket, asyncio.AbstractEventLoop]]] = {}

    def _ensure_topic_subscription(self, topic: str):
        # 若该主题尚未注册处理器，则注册一个处理器，将消息转发给所有订阅该主题的 WebSocket 客户端
        if topic not in mqtt_client.message_handlers:
            def handler(tp: str, payload: Any):
                for ws, loop in list(self.subscribers.get(tp, [])):
                    try:
                        asyncio.run_coroutine_threadsafe(ws.send_text(payload), loop)
                    except Exception:
                        # 忽略发送失败的客户端（可能断开），由 disconnect 进行清理
                        pass
            mqtt_client.subscribe(topic, handler)

    async def connect(self, topic: str, websocket: WebSocket):
        await websocket.accept()
        loop = asyncio.get_running_loop()
        self.subscribers.setdefault(topic, []).append((websocket, loop))
        self._ensure_topic_subscription(topic)

    def disconnect(self, topic: str, websocket: WebSocket):
        clients = self.subscribers.get(topic, [])
        self.subscribers[topic] = [(ws, lp) for (ws, lp) in clients if ws is not websocket]
        if not self.subscribers[topic]:
            # 无订阅者时移除空列表
            self.subscribers.pop(topic, None)


ws_manager = MQTTWebSocketManager()


@router.websocket("/ws/subscribe")
async def ws_subscribe(websocket: WebSocket, topic: str = Query(..., description="要订阅的 MQTT 主题")):
    """WebSocket 订阅指定 MQTT 主题，接收实时消息"""
    await ws_manager.connect(topic, websocket)
    try:
        # 保持连接，客户端如需发送心跳消息可以向该 WS 发送任意文本
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(topic, websocket)