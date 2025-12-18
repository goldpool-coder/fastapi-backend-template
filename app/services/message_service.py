"""
消息服务模块
封装基于 MQTT 的业务消息逻辑
"""
from typing import Any
from app.utils.mqtt_client import mqtt_client
from app.utils.logger import logger


class MessageService:
    """消息服务类"""

    def __init__(self):
        """初始化并注册消息处理函数"""
        # 示例：订阅一个用于接收命令的主题
        self.subscribe_command_topic()

    def subscribe_command_topic(self):
        """订阅命令主题"""
        topic = "command/video_crawler"
        mqtt_client.subscribe(topic, self._handle_command_message)
        logger.info(f"已注册 MQTT 消息处理函数到主题: {topic}")

    def _handle_command_message(self, topic: str, payload: str):
        """
        处理接收到的命令消息
        
        Args:
            topic: 消息主题
            payload: 消息内容
        """
        logger.info(f"--- 业务逻辑处理开始 ---")
        logger.info(f"接收到命令消息: Topic={topic}, Payload={payload}")
        
        # 实际业务逻辑：例如，解析 payload，触发视频抓取任务
        if "start_crawl" in payload:
            logger.info("触发视频抓取任务...")
            # 这里可以调用您的抓取服务
        elif "stop_crawl" in payload:
            logger.info("停止视频抓取任务...")
        else:
            logger.warning("未知命令")
            
        logger.info(f"--- 业务逻辑处理结束 ---")

    @staticmethod
    def publish_crawl_status(status: str, details: Any):
        """
        发布抓取状态消息
        
        Args:
            status: 状态（如: 'started', 'progress', 'completed', 'error'）
            details: 详细信息
        """
        topic = "status/video_crawler"
        payload = f"{status}: {details}"
        mqtt_client.publish(topic, payload)
        logger.info(f"发布抓取状态: {payload}")


# 创建全局消息服务实例
message_service = MessageService()
