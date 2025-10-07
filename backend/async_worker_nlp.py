# async_worker_nlp.py (纯异步最终版)

import json
import asyncio

import aio_pika
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import config
# 【修改】从您的 db 包中导入异步会话管理器和模型
from db.database import get_session
from db.user_model import TurUsers
from db.chat_model import TurChatSessions, TurChatHistory
from db.papers_model import TurPapers, TurQuestion, PaperStatus

# 【修改】导入您的 AI 模型函数
from ai_models import get_question_analysis_from_nlp


async def check_and_complete_paper(db: AsyncSession, paper_id: int):
    """【异步】检查试卷的所有题目是否都已处理完毕"""
    # 【修改】使用异步语法进行查询
    stmt = (
        select(func.count(TurQuestion.id))
        .where(TurQuestion.paper_id == paper_id)
        .where(TurQuestion.analysis == None)
    )
    result = await db.execute(stmt)
    unprocessed_count = result.scalar_one()

    if unprocessed_count == 0:
        # 使用 await db.get() 来通过主键高效获取对象
        paper = await db.get(TurPapers, paper_id)
        if paper and paper.status != PaperStatus.COMPLETED:
            print(f"NLPWorker: 试卷 ID {paper_id} 的所有题目均已完成，更新最终状态。")
            paper.status = PaperStatus.COMPLETED
            await db.commit()


async def async_process_question_nlp(db: AsyncSession, question_id: int, user_id: int):
    """
    【异步】负责处理单个题目的NLP分析。
    """
    # 【修改】使用 selectinload 预加载 paper 关系，避免额外的查询
    stmt = (
        select(TurQuestion)
        .where(TurQuestion.id == question_id, TurQuestion.user_id == user_id)
        .options(selectinload(TurQuestion.paper))
    )
    result = await db.execute(stmt)
    question = result.scalars().first()

    if not question:
        print(f"[错误] NLPWorker: 找不到 question_id={question_id} 且 user_id={user_id} 的记录。")
        return

    paper = question.paper
    if not paper:
        print(f"[严重错误] NLPWorker: 题目 {question_id} 没有关联的试卷。")
        return

    try:
        print(f"NLPWorker: > 正在分析题目 ID: {question.id} (属于用户 {user_id}, 试卷 {paper.id})")
        loop = asyncio.get_running_loop()

        # 【关键】将同步阻塞的 AI 调用放入线程池中执行
        analysis_data = await loop.run_in_executor(
            None, get_question_analysis_from_nlp, paper.subject, question
        )

        if analysis_data:
            question.reference_answer = analysis_data.get("reference_answer")
            question.analysis = analysis_data.get("analysis")
            await db.commit() # 提交对单个 question 的修改
            print(f"NLPWorker: > 题目 ID: {question.id} 分析并保存成功。")

            # 检查是否可以完成整个试卷
            await check_and_complete_paper(db, paper.id)
        else:
            print(f"NLPWorker: > [警告] 题目 ID: {question.id} 分析失败，模型未返回有效数据。")

    except Exception as e:
        print(f"[严重错误] NLPWorker: 分析题目 ID {question.id} 时失败: {e}")
        await db.rollback()
        # 【可选】更新单个题目的错误状态
        question_to_update = await db.get(TurQuestion, question_id)
        if question_to_update:
            # 假设 Question 模型有 error_message 字段
            # question_to_update.error_message = str(e)
            await db.commit()
        raise


async def on_message(message: aio_pika.IncomingMessage):
    """【异步】RabbitMQ 消息回调函数"""
    async with message.process():
        try:
            data = json.loads(message.body)
            print(f"NLPWorker: 收到新消息: {data}")

            question_id = data.get("question_id")
            user_id = data.get("user_id")

            if not (question_id and user_id):
                print("[错误] NLPWorker: 收到的消息不完整，缺少 'question_id' 或 'user_id'。")
                return

            # 使用异步上下文管理器获取数据库会话
            async with get_session() as db:
                await async_process_question_nlp(db, question_id, user_id)

        except Exception as e:
            print(f"[严重错误] 在回调函数 on_message 中发生未知错误: {type(e).__name__}: {e}")


async def main():
    """【异步】主函数，设置并运行 aio-pika 消费者"""
    connection = await aio_pika.connect_robust(config.RABBITMQ_URL)
    print("成功连接到 RabbitMQ。")
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)
        
        # 【修改】使用 config 中定义的 NLP 队列名称
        queue = await channel.declare_queue(config.NLP_QUEUE_NAME, durable=True)
        
        print(f"[*] NLP Worker 等待消息中，队列: {config.NLP_QUEUE_NAME}")
        await queue.consume(on_message)

        try:
            await asyncio.Future()
        finally:
            await connection.close()


if __name__ == "__main__":
    print(f"CONSUMER: Listening on queue -> '{config.NLP_QUEUE_NAME}'")
    from ai_models import init_client

    if not init_client():
        print("无法启动 NLP Worker，AI 客户端初始化失败。")
    else:
        print("OpenAI 客户端初始化成功。")
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("程序被用户中断。")