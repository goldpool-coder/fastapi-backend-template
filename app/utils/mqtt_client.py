"""
MQTT 客户端工具模块
使用 paho-mqtt 实现消息发布和订阅
"""
import paho.mqtt.client as mqtt
from typing import Callable, Dict, Any, List

from app.core.config import settings
from app.utils.logger import logger


class MQTTClient:
    """MQTT 客户端类"""

    def __init__(self):
        """初始化 MQTT 客户端"""
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        self.is_connected = False
        self.message_handlers: Dict[str, List[Callable[[str, Any], None]]] = {}

    def _on_connect(self, client, userdata, flags, rc):
        """连接成功回调"""
        if rc == 0:
            logger.info("✅ MQTT 连接成功")
            self.is_connected = True
            # 重新订阅所有主题
            for topic in self.message_handlers.keys():
                client.subscribe(topic)
        else:
            logger.error(f"❌ MQTT 连接失败，返回码: {rc}")
            self.is_connected = False

    def _on_disconnect(self, client, userdata, rc):
        """断开连接回调"""
        self.is_connected = False
        logger.warning(f"🛑 MQTT 连接已断开，返回码: {rc}")

    def _on_message(self, client, userdata, msg):
        """接收消息回调"""
        topic = msg.topic
        payload = msg.payload.decode()
        logger.info(f"📥 接收到 MQTT 消息: Topic='{topic}', Payload='{payload}'")

        if topic in self.message_handlers:
            try:
                for handler in list(self.message_handlers.get(topic, [])):
                    handler(topic, payload)
            except Exception as e:
                logger.error(f"处理 MQTT 消息失败: {e}")

    def connect_async(self):
        """异步连接到 MQTT 代理"""
        try:
            self.client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
            self.client.connect_async(settings.MQTT_HOST, settings.MQTT_PORT, 60)
            self.client.loop_start()  # 启动一个后台线程来处理网络流量
            logger.info(f"🚀 尝试连接到 MQTT 代理: {settings.MQTT_HOST}:{settings.MQTT_PORT}")
        except Exception as e:
            logger.error(f"❌ 启动 MQTT 连接失败: {e}")

    def disconnect(self):
        """断开 MQTT 连接"""
        # 无论当前连接状态如何，都尝试停止循环和断开连接，保证后台线程不会残留
        try:
            self.client.loop_stop()
        except Exception:
            pass
        try:
            self.client.disconnect()
        except Exception:
            pass
        logger.info("🛑 MQTT 客户端已停止")
        self.is_connected = False

    def publish(self, topic: str, payload: str, qos: int = 0, retain: bool = False) -> bool:
        """发布消息"""
        if not self.is_connected:
            logger.warning("⚠️ MQTT 客户端未连接，无法发布消息")
            return False

        result = self.client.publish(topic, payload, qos, retain)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            logger.info(f"📤 成功发布 MQTT 消息: Topic='{topic}', Payload='{payload}'")
            return True
        else:
            logger.error(f"❌ 发布 MQTT 消息失败: {result.rc}")
            return False

    def subscribe(self, topic: str, handler: Callable[[str, Any], None], qos: int = 0):
        """订阅主题并注册处理函数"""
        self.message_handlers.setdefault(topic, []).append(handler)
        if self.is_connected:
            self.client.subscribe(topic, qos)
            logger.info(f"🔔 成功订阅 MQTT 主题: '{topic}'")


# 创建全局 MQTT 客户端实例
mqtt_client = MQTTClient()
