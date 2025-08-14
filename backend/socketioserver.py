import sys
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import asyncio
from datetime import datetime
import io
import json
import re
from typing import AsyncGenerator, List
from pydantic import BaseModel, Field
import socketio
from sqlalchemy import select, update
import config
from database import AsyncSessionLocal, TurChatHistory, TurChatSessions
from sqlalchemy.ext.asyncio.session import AsyncSession
from openai import AsyncOpenAI
from enum import Enum
import database
from utils.utils import get_userInfo_from_token, p
from utils.chromadb_helpers import chroma_format_knowledge


class RoleEnum(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"

class Message(BaseModel):
    role: RoleEnum
    content: str


class GetTextIn(BaseModel):
    ai_message_id: int = Field(...)
    chat_session_id: int = Field(...)
    question: str = Field(...)

print(f"TIHS IS LLM_API_KEY: {config.LLM_API_KEY}")
print(f"TIHS IS LLM_BASE_URL: {config.LLM_BASE_URL}")
print(f"TIHS IS LLM_MODEL_NAME: {config.LLM_MODEL_NAME}")


async def llmchat(messages: List[Message]) -> AsyncGenerator[str, None]:
    client = AsyncOpenAI(
        api_key=config.LLM_API_KEY,
        base_url=config.LLM_BASE_URL
    )
    
    stream = await client.chat.completions.create(
        model=config.LLM_MODEL_NAME,
        stream=True,
        messages=messages
    )

    async for event in stream:
        content = event.choices[0].delta.content if event.choices and event.choices[0].delta else None

        if content:
            yield content


static_files = {
    '/static': './public',
}

# 使用 AsyncServer 和 ASGIApp 以支持 async/await 语法
sio = socketio.AsyncServer(
    logger=True,
    engineio_logger=True,
    async_mode='asgi',
    cors_allowed_origins='*',
    transports=['websocket']
)

app = socketio.ASGIApp(sio, static_files=static_files)


@sio.on('startup')
async def handle_startup():
     print("ASGI startup signal received.")
     pass


@sio.on('shutdown')
async def handle_shutdown():
    print("ASGI shutdown signal received. Disposing database engine...")
    if  database.engine:
        await database.engine.dispose()
        print("Database engine disposed successfully.")
    else:
        print("Database engine not found or not initialized.")

@sio.on('connect')
async def connect(sid, environ, auth):
    if not auth or 'token' not in auth:
            print(f"Connection rejected for {sid}: No auth token provided.")
            # 拒绝连接
            raise socketio.exceptions.ConnectionRefusedError('Authentication failed: token missing')

    try:
        bearer = auth['token']
        p(bearer)
        userinfo = get_userInfo_from_token(bearer)
        async with sio.session(sid) as session:
            session['id'] = userinfo['id']
            session['phone_number'] = userinfo['phone_number']
    except socketio.exceptions.ConnectionRefusedError as e:
        print(f"Connection refused for sid {sid}: {e}")
        raise e # 重新抛出异常，拒绝连接
    except Exception as e:
        print(f"Authentication process error for sid {sid}: {e}")
        raise socketio.exceptions.ConnectionRefusedError(f'认证过程中发生错误: {e}')

@sio.on('disconnect')
async def disconnect(sid):
    # 'reason' 参数在标准的 disconnect 事件处理器中不可用
    print(f'disconnect {sid}')


# 辅助函数，用于处理和发送缓冲区内容
async def process_buffer(buffer: str, chat_session_id: str, ai_message_id: str):
    content_to_process = buffer.strip()
    if not content_to_process:
        return

    payload = {}

    # 联系人工客服按钮
    if content_to_process.startswith("[BUTTON]"):
        payload.update({
            "chat_session_id": chat_session_id,
            "ai_message_id": ai_message_id,
            "type": "button",
            "token": content_to_process.replace("[BUTTON]", "").strip(),
        })
    # 动作
    elif content_to_process.startswith("[ACTION]"):
        payload.update({
            "chat_session_id": chat_session_id,
            "ai_message_id": ai_message_id,
            "type": "action",
            "token": content_to_process.replace("[ACTION]", "").strip()
        })
    # 小测试
    elif content_to_process.startswith("[QUIZ]"):
        payload.update({
            "chat_session_id": chat_session_id,
            "ai_message_id": ai_message_id,
            "type": "quiz",
            "token": content_to_process.replace("[QUIZ]", "").strip()
        })
    # 参考链接
    elif content_to_process.startswith("[REFERENCE]"):
        pattern = r'\[(.*?)\]\s+?\[(.*?)\]\((.*)'
        match = re.search(pattern, content_to_process)
        if match:
            token_text = match.group(2)
            url = match.group(3)
            payload.update({
                "chat_session_id": chat_session_id,
                "ai_message_id": ai_message_id,
                "type": "reference",
                "token": token_text,
                "url": f"{url}"
            })
    # 打开资源
    elif content_to_process.startswith("[RESOURCE]"):
        pattern = r'\[(.*?)\]\s+?\[(.*?)\]\((.*)'
        match = re.search(pattern, content_to_process)
        if match:
            token_text = match.group(2)
            url = match.group(3)
            payload.update({
                "chat_session_id": chat_session_id,
                "ai_message_id": ai_message_id,
                "type": "resource",
                "token": token_text,
                "url": f"{url}"
            })
    else:
        payload.update({
            "chat_session_id": chat_session_id,
            "ai_message_id": ai_message_id,
            "type": "text",
            "token": content_to_process
        })

    yield json.dumps(payload, ensure_ascii=False)
    await asyncio.sleep(0.01)

# 知识库插入到上下文
async def knowledge_insert(chat_context: list, knowledge_list: list = []):
    """
    少样本提示
    """
    for item in knowledge_list:
        question = item['related']
        urls = item['urls']

        chat_context.append(Message(role=RoleEnum.user, content=f"【参考资料】{item['answer']}\n\n【用户问题】{item['question']}"))
        chat_context.append(Message(role=RoleEnum.assistant, content=f"{item['answer']}\n{urls}\n{question}"))

    chat_context.append(Message(role=RoleEnum.user, content=f"可以讲个笑话吗？"))
    chat_context.append(Message(role=RoleEnum.assistant, content=f"对不起，不可以哦。"))

@sio.on('get_text')
async def get_text(sid, data):
    textin = GetTextIn.model_validate(obj=data)

    async with sio.session(sid) as session:
        userid = session['id']
        async with AsyncSessionLocal() as db:
            try:
                db: AsyncSession = db

                # 查找会话记录
                query_stmt = select(
                    TurChatSessions.id, 
                    TurChatSessions.user_id, 
                    TurChatSessions.title, 
                    TurChatSessions.created_at
                ).where(
                    TurChatSessions.id == textin.chat_session_id,
                    TurChatSessions.user_id == userid
                )
                result = await db.execute(query_stmt)
                if result.fetchone() is None:
                    await sio.emit('response_text', {'data': '没找到会话记录'}, to=sid)
                    return


                # 查找该会话的所有历史记录
                query_stmt = select(
                    TurChatHistory.id, 
                    TurChatHistory.user_id,
                    TurChatHistory.chat_session_id,
                    TurChatHistory.sender,
                    TurChatHistory.text,
                    TurChatHistory.created_at
                ).where(
                    TurChatHistory.chat_session_id == textin.chat_session_id,
                    TurChatHistory.user_id == userid
                ).order_by(
                    TurChatHistory.id.asc()
                )
                result = await db.execute(query_stmt)
                
                history: List[TurChatHistory] = result.mappings().all()            
                historyLength = len(history)

                # 在历史中取出问题
                user_question = textin.question.strip()

                # 整理成上下文提交给大模型
                chat_context = []
                
                system_prompt = config.LLM_SYSTEM_PROMPT

                # 系统提示词
                chat_context.append(Message(role=RoleEnum.system, content=system_prompt))

                # 从知识库中查询出来的知识
                knowledge_list = await chroma_format_knowledge(
                    question=user_question,
                    n_results=config.CHROMADB_MAXIMUM_QUERY_RESULT,
                    threshold=config.CHROMADB_QUERY_THRESHOLD
                )

                if knowledge_list:
                    await knowledge_insert(chat_context, knowledge_list)

                for key, chat in enumerate(history):
                    # 判断用户提供的id与数据库的id是否对应
                    if chat.text == "" and chat.sender == 'ai' and key == historyLength - 1:
                        if chat.id != textin.ai_message_id:
                            await sio.emit('response_text', {'data': '没找到新建的AI对话记录'}, to=sid)
                            return
                        continue

                    if chat.sender == 'user':
                        chat_context.append(Message(role=RoleEnum.user, content=chat.text))
                    else:
                        chat_context.append(Message(role=RoleEnum.assistant, content=chat.text))

                print("❤️" * 50)
                print(chat_context)
                print("❤️" * 50)
                print("\n\n")

                # 流式输出到浏览器
                buffer = ""
                full_response_buffer = io.StringIO()
                async for eachtoken in llmchat(chat_context):
                    print(eachtoken)
                    full_response_buffer.write(eachtoken)

                    # ===========================================
                    # 特殊输出

                    # 如果是[开头就开始累计
                    if eachtoken.strip().startswith('['):
                        buffer += eachtoken
                        continue

                    # 一直累计到换行
                    if len(buffer) > 0:
                        if "\n" in eachtoken:
                            async for item in process_buffer(buffer=buffer, chat_session_id=textin.chat_session_id, ai_message_id=textin.ai_message_id):
                                await sio.emit("token_output", item, to=sid)
                            buffer = ""
                        else:
                            buffer += eachtoken
                        continue
                    # ===========================================
                    
                    # 正常eachtoken输出
                    payload = {
                        "chat_session_id": textin.chat_session_id,
                        "ai_message_id": textin.ai_message_id,
                        "type": "text",
                        "token": eachtoken
                    }
                    await sio.emit("token_output", json.dumps(payload, ensure_ascii=False), to=sid)

                # 最后一个buffer的处理
                if len(buffer) > 0:
                    async for item in process_buffer(buffer=buffer, chat_session_id=textin.chat_session_id, ai_message_id=textin.ai_message_id):
                        await sio.emit("token_output", item, to=sid)

                text = full_response_buffer.getvalue()
                print(f"总的是：{text}")
                if text == "":
                    text = '-'

                # 更新AI回答到数据库
                query_stmt = update(TurChatHistory).values(
                    text=text,
                    created_at=datetime.now()
                ).where(
                    TurChatHistory.id == textin.ai_message_id,
                    TurChatHistory.sender == "ai",
                    TurChatHistory.user_id == userid
                )

                result = await db.execute(query_stmt)
                await db.commit()
            except Exception:
                await db.rollback()
                raise
            finally:
                await db.close()

@sio.on('test')
async def test(sid, data):
    await sio.emit("test_response", "hello now is" + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), to=sid)
