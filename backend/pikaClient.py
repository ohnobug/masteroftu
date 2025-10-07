# pika_client.py
import pika
import json
import config

class PikaClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(config.RABBITMQ_URL)
        )
        self.channel = self.connection.channel()

    def send_message(self, queue_name: str, message: dict):
        """发送消息到队列"""
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # 使消息持久化
            )
        )
        print(f" [x] Sent message: {message}")

    def close(self):
        """关闭连接"""
        self.connection.close()

# 创建一个全局实例，可在 FastAPI 中复用
pika_client = PikaClient()