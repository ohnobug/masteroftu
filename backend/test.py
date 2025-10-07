# test_combined.py (最终增强版：修复URL + 增加超时)

import pika
import json
import uuid
import time

# ============================ 必填配置 ============================

# 【关键修正】在 URL 末尾加上斜杠 "/" 来明确指定默认的虚拟主机
RABBITMQ_URL = "amqp://guest:guest@127.0.0.1:5672/" 
VISION_QUEUE_NAME = "paper_vision_queue"

# =================================================================

def producer_send_one_message():
    """【生产者角色】"""
    print("\n--- [PRODUCER] an's mission: Send one message. ---")
    try:
        with pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL)) as connection:
            channel = connection.channel()
            channel.queue_declare(queue=VISION_QUEUE_NAME, durable=True)
            
            message_body = {
                "paper_id": int(time.time()), "user_id": 999,
                "file_path": f"./data/test_file_{uuid.uuid4()}.jpg",
                "file_hash": str(uuid.uuid4()), "source": "test_combined.py"
            }
            channel.basic_publish(
                exchange='', routing_key=VISION_QUEUE_NAME, body=json.dumps(message_body),
                properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
            )
            print(f"✅ [PRODUCER] Message successfully sent to queue '{VISION_QUEUE_NAME}'.")
            print(json.dumps(message_body, indent=2))
            return True
    except Exception as e:
        print(f"❌ [PRODUCER] Failed to send message. Error: {e}")
        return False

def consumer_with_timeout(timeout_seconds=5):
    """
    【消费者角色 - 增强版】: 监听队列，如果超时则自动退出。
    """
    print("\n--- [CONSUMER] mission: Receive one message (with a 5-second timeout). ---")
    connection = None
    try:
        connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
        channel = connection.channel()
        print(f"  - [CONSUMER] Connection established. Waiting for a message for up to {timeout_seconds} seconds...")

        # 使用 get 方法一次性获取一条消息，而不是持续消费
        # 这是进行快速测试的理想方法
        method_frame, header_frame, body = channel.basic_get(queue=VISION_QUEUE_NAME)

        if method_frame:
            # 如果成功获取到消息
            print("\n" + "*"*20 + " MESSAGE RECEIVED! " + "*"*20)
            print("✅ [CONSUMER] Successfully received a message from the queue.")
            message_data = json.loads(body.decode('utf-8'))
            print("[CONSUMER] Message content:")
            print(json.dumps(message_data, indent=2))
            
            # 确认消息已被处理
            channel.basic_ack(method_frame.delivery_tag)
            print("[CONSUMER] Message acknowledged (ACK).")
        else:
            # 如果超时后仍然没有消息
            print("\n" + "!"*20 + " TIMEOUT! " + "!"*20)
            print(f"❌ [CONSUMER] No message received in the queue '{VISION_QUEUE_NAME}' within {timeout_seconds} seconds.")

    except pika.exceptions.AMQPConnectionError as e:
        print(f"❌ [CONSUMER] Could not connect to RabbitMQ. Please check the URL. Error: {e}")
    except Exception as e:
        print(f"❌ [CONSUMER] An error occurred. Error: {e}")
    finally:
        if connection and connection.is_open:
            connection.close()
            print("  - [CONSUMER] Connection closed.")

if __name__ == "__main__":
    print("=" * 60)
    print("      RabbitMQ Combined Producer-Consumer Test (Enhanced)")
    print("=" * 60)
    input("Press Enter to begin the test...")

    # 第一步：扮演生产者
    if producer_send_one_message():
        # 第二步：如果发送成功，就扮演消费者
        # 短暂等待，确保消息有时间到达队列
        print("\nWaiting for 1 second for message to propagate...")
        time.sleep(1)
        consumer_with_timeout()
    
    print("\n" + "=" * 60)
    print("                      Test Complete.")
    print("=" * 60)