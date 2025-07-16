from datetime import datetime
import io
import json
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
from utils import get_userInfo_from_token, p


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

mgr = socketio.AsyncAioPikaManager(config.RABBITMQ_URL)
sio = socketio.AsyncServer(
    logger=True,
    engineio_logger=True,
    async_mode='asgi',
    cors_allowed_origins='*',
    client_manager=mgr,
    transports=['websocket']
    # cors_allowed_origins=[
    #     'http://localhost:5000',
    #     'http://localhost:5173',
    #     'https://admin.socket.io',
    # ]
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

class WschatNamespace(socketio.AsyncNamespace):
    async def on_connect(self, sid, environ, auth):
        if not auth or 'token' not in auth:
                print(f"Connection rejected for {sid}: No auth token provided.")
                # 拒绝连接
                raise socketio.exceptions.ConnectionRefusedError('Authentication failed: token missing')

        try:
            # bearer = environ.get('HTTP_AUTHORIZATION').split(' ')[1]
            bearer = auth['token']
            p(bearer)
            userinfo = get_userInfo_from_token(bearer)
            async with self.session(sid) as session:
                session['id'] = userinfo['id']
                session['phone_number'] = userinfo['phone_number']
        except socketio.exceptions.ConnectionRefusedError as e:
            # 捕获 ConnectionRefusedError 并重新抛出
            # 这样做可以让你在抛出前打印或记录特定信息，或者根据不同原因抛出不同异常
            print(f"Connection refused for sid {sid}: {e}")
            raise e # 重新抛出异常，拒绝连接
        except Exception as e:
            # 捕获其他潜在错误（如 split() 错误、get() 返回 None 等）
            print(f"Authentication process error for sid {sid}: {e}")
            # 对于意外错误，同样拒绝连接
            raise socketio.exceptions.ConnectionRefusedError(f'认证过程中发生错误: {e}')

    async def on_disconnect(self, sid, reason):
        print('disconnect ', sid, reason)

    async def on_get_text(self, sid, data):
        textin = GetTextIn.model_validate(obj=data)

        async with self.session(sid) as session:
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
                        await self.emit('response_text', {'data': '没找到会话记录'}, to=sid)
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

                    # 整理成上下文提交给大模型
                    context = []
                    for key, chat in enumerate(history):
                        # 判断用户提供的id与数据库的id是否对应
                        if chat.text == "" and chat.sender == 'ai' and key == historyLength - 1:
                            if chat.id != textin.ai_message_id:
                                await self.emit('response_text', {'data': '没找到新建的AI对话记录'}, to=sid)
                                return
                            continue

                        if chat.sender == 'user':
                            context.append(Message(role=RoleEnum.user, content=chat.text))
                        else:
                            context.append(Message(role=RoleEnum.assistant, content=chat.text))

                    text_buffer = io.StringIO()

                    # 流式输出到浏览器
                    async for eachtoken in llmchat(context):
                        text_buffer.write(eachtoken)
                        await self.emit("token_output", json.dumps({
                            "chat_session_id": textin.chat_session_id,
                            "ai_message_id": textin.ai_message_id,
                            "token": eachtoken
                        }), to=sid)

                    # 更新AI回答到数据库
                    query_stmt = update(TurChatHistory).values(
                        text=text_buffer.getvalue(),
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

    async def on_test(self, sid, data):
        await self.emit("test_response", "hello now is" + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), to=sid)

sio.register_namespace(WschatNamespace('/'))
