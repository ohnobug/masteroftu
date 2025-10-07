# async_worker_vision.py

import base64
import json
import os
import asyncio
from io import BytesIO

import aio_pika
from PIL import Image

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import config
from db.database import get_session
from db.user_model import TurUsers
from db.chat_model import TurChatSessions, TurChatHistory
from db.papers_model import TurPapers, TurQuestion, PaperStatus
from ai_models import extract_question_data_from_image
from pikaClient import pika_client # 假设 pika_client 在这个 worker 中也需要

async def async_process_paper_vision(
    db: AsyncSession,
    paper_id: int,
    user_id: int,
    file_path: str,
    file_hash: str,
    anchors: list,
):
    loop = asyncio.get_running_loop()
    
    stmt = select(TurPapers).where(TurPapers.id == paper_id)
    result = await db.execute(stmt)
    paper = result.scalars().first()

    if not paper:
        print(f"[错误] VisionWorker: 找不到 paper_id={paper_id} 的记录。")
        return

    try:
        # 【关键修正】: 使用正确的关键字参数 exist_ok=True
        if not os.path.exists(config.CROPS_DIR):
            os.makedirs(config.CROPS_DIR, exist_ok=True)

        print(f"VisionWorker: 开始处理试卷 ID: {paper_id}, 用户 ID: {user_id}")
        paper.status = PaperStatus.PROCESSING_VISION
        await db.flush()

        questions_for_nlp = []

        if anchors:
            print(f"VisionWorker: 检测到 {len(anchors)} 个锚框，开始切割处理。")
            original_image = await loop.run_in_executor(None, Image.open, file_path)
            stmt_q = select(TurQuestion).where(TurQuestion.paper_id == paper_id)
            result_q = await db.execute(stmt_q)
            all_questions = result_q.scalars().all()
            questions_map = {
                str(q.position_info["id"]): q
                for q in all_questions if q.position_info and "id" in q.position_info
            }
            for anchor in anchors:
                anchor_uuid = anchor.get("id")
                question_to_update = questions_map.get(anchor_uuid)
                if not question_to_update: continue
                box = (anchor["x"], anchor["y"], anchor["x"] + anchor["width"], anchor["y"] + anchor["height"])
                cropped_image = await loop.run_in_executor(None, original_image.crop, box)
                crop_filename = f"{file_hash}_{anchor_uuid}.png"
                crop_path = os.path.join(config.CROPS_DIR, crop_filename)
                await loop.run_in_executor(None, cropped_image.save, crop_path, "PNG")
                buffered = BytesIO()
                await loop.run_in_executor(None, cropped_image.save, buffered, "PNG")
                encoded_bytes = await loop.run_in_executor(None, base64.b64encode, buffered.getvalue())
                base64_crop = encoded_bytes.decode('utf-8')
                extracted_data = extract_question_data_from_image(base64_crop)
                if not extracted_data: continue
                question_to_update.question_text, question_to_update.options = extracted_data.get("question_text"), extracted_data.get("options")
                if extracted_data.get("type"): question_to_update.type = extracted_data.get("type")
                question_to_update.cropped_image_path = crop_path
                questions_for_nlp.append(question_to_update)
            print("VisionWorker: 已完成所有锚框的处理。")
        else:
            print("VisionWorker: 未提供锚框，进行整页识别。")
            def read_and_encode(path):
                with open(path, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode("utf-8")
            base64_image = await loop.run_in_executor(None, read_and_encode, file_path)
            extracted_data = extract_question_data_from_image(base64_image)
            if not extracted_data or "questions" not in extracted_data:
                raise ValueError("视觉模型未能返回有效的题目数据。")
            paper.subject = extracted_data.get("subject", "未知学科")
            for q_data in extracted_data["questions"]:
                new_question = TurQuestion(
                    paper_id=paper.id, user_id=user_id, id_in_paper=q_data.get("id_in_paper"),
                    question_text=q_data.get("question_text"), options=q_data.get("options"),
                    type=q_data.get("type", "未知类型"),
                )
                db.add(new_question)
                questions_for_nlp.append(new_question)
            print(f"VisionWorker: 成功提取并创建了 {len(questions_for_nlp)} 道新题目。")
        
        await db.flush()
        paper.status = PaperStatus.PROCESSING_NLP
        
        for question in questions_for_nlp:
            nlp_message = {"question_id": question.id, "user_id": user_id}
            await loop.run_in_executor(None, pika_client.send_message, config.NLP_QUEUE_NAME, nlp_message)
        print(f"VisionWorker: 已将 {len(questions_for_nlp)} 个任务发送到 NLP 队列。")
        
        await db.commit()
    except Exception as e:
        print(f"[严重错误] VisionWorker: 处理试卷 ID {paper_id} 时失败: {e}")
        await db.rollback()
        paper_to_update = await db.get(TurPapers, paper_id) # 重新获取对象以更新
        if paper_to_update:
            paper_to_update.status = PaperStatus.FAILED
            paper_to_update.error_message = str(e)
            await db.commit()
        raise

async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            data = json.loads(message.body)
            print(f"VisionWorker: 收到新消息: {data}")
            paper_id, user_id = data.get("paper_id"), data.get("user_id")
            file_path, file_hash = data.get("file_path"), data.get("file_hash")
            anchors = data.get("anchors", [])
            if not all([paper_id, user_id, file_path, file_hash]): return

            async with get_session() as db:
                await async_process_paper_vision(
                    db, paper_id, user_id, file_path, file_hash, anchors
                )
        except Exception as e:
            print(f"[严重错误] 在回调函数 on_message 中发生未知错误: {type(e).__name__}: {e}")

async def main():
    connection = await aio_pika.connect_robust(config.RABBITMQ_URL)
    print("成功连接到 RabbitMQ。")
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)
        queue = await channel.declare_queue(config.VISION_QUEUE_NAME, durable=True)
        print(f"[*] Vision Worker 等待消息中，队列: {config.VISION_QUEUE_NAME}")
        await queue.consume(on_message)
        try:
            await asyncio.Future()
        finally:
            await connection.close()

if __name__ == "__main__":
    print(f"CONSUMER: Listening on queue -> '{config.VISION_QUEUE_NAME}'")
    if not hasattr(config, "CROPS_DIR"):
        print("[错误] 请在 config.py 中配置 config.CROPS_DIR")
    else:
        from ai_models import init_client
        if not init_client():
            print("无法启动 Vision Worker，AI 客户端初始化失败。")
        else:
            print("OpenAI 客户端初始化成功。")
            try:
                asyncio.run(main())
            except KeyboardInterrupt:
                print("程序被用户中断。")
