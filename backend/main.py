import json
import aiohttp
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse
import schemas
from SimpleCrypto import SimpleCrypto
from moodle_api import api_create_users, api_get_autologin_key, api_get_users_by_username
from database import TurChatSessions, TurChatHistory, TurUsers
import database
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from utils import get_token, get_userInfo_from_token, password_hash

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动阶段 (在 yield 之前)
    print("Application startup...")

    yield
    
    print("Application shutdown...")

    # 释放数据库 Engine 和连接池
    if database.engine:
        await database.engine.dispose()
    print("Database engine disposed")


# app = FastAPI(title="FastAPI SMS and Auth Demo", lifespan=lifespan)
app = FastAPI(title="FastAPI SMS and Auth Demo", lifespan=lifespan)


class UnicornException(Exception):
    def __init__(self, message: str, code: int = 400):
        self.code = code
        self.message = message


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=400,
        content={"code": exc.code, "message": exc.message},
    )

origins = [
    "https://turcar.net.cn",
    "https://learn.turcar.net.cn",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # 在这里验证 form_data.username 和 form_data.password
    # 如果验证成功，生成一个 token 并返回
    # 如果验证失败，抛出 HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, ...)
    return {"access_token": "your_generated_token", "token_type": "bearer"}


@app.post("/api/login", response_model=schemas.UserLoginRequestOut)
async def login(request: schemas.UserLoginRequestIn, db: AsyncSession = Depends(database.get_db)):
    """
    用户登录
    """
    query_stmt = select(TurUsers).where(TurUsers.phone_number == request.phone_number)
    result = await db.execute(query_stmt)
    userinfo = result.scalar_one_or_none()
    
    if userinfo is None:
        raise HTTPException(status_code=400, detail="该账号尚未注册")

    checkPassword = password_hash(request.password)
    if (checkPassword == userinfo.password_hash):
        token = get_token(userinfo)
        
        return schemas.UserLoginRequestOut(
            code=200,
            message="Success",
            data=schemas.UserLoginToken(token=token)
        )
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")



@app.post("/api/register", response_model=schemas.UserRegisterRequestOut, summary="用户注册")
async def register(request: schemas.UserRegisterRequestIn, db: AsyncSession = Depends(database.get_db)):
    """
    用户注册
    """
    query_stmt = select(TurUsers).where(
        TurUsers.phone_number == request.phone_number
    )
    result = await db.execute(query_stmt)
    if result.fetchone() is not None:
        raise HTTPException(status_code=400, detail="手机号已被注册")

    passwordh = password_hash(request.password)
    insert_stmt = insert(TurUsers).values(
        phone_number=request.phone_number,
        password_hash=passwordh
    )
    
    result = await db.execute(insert_stmt)
    result.inserted_primary_key[0]
    await db.commit()

    return schemas.UserRegisterRequestOut(
        code=200,
        message="注册成功"
    )
    
    # async with aiohttp.ClientSession() as session:
    #     # 检测手机号是否已存在
    #     userinfo = await api_get_users_by_username(session, [user_data.phone_number])
    #     if userinfo:
    #         raise UnicornException(code=400, message="手机号已被注册")
        
    #     # 注册新账号
    #     result = await api_create_users(session, [{
    #         'username': user_data.phone_number,
    #         'password': user_data.password,
    #         'firstname': "姓",
    #         'lastname': "名",
    #         'email': user_data.phone_number + "@turcar.net.cn",
    #     }])

    # if result is None:
    #     raise UnicornException(code=400, message=json.dumps(result))

    # return schemas.BaseResponse(
    #     code=200,
    #     message="注册成功"
    # )


@app.post("/api/user", response_model=schemas.UserInfoRequestOut)
async def read_users_me(request: schemas.UserInfoRequestIn):
    decryptStr = SimpleCrypto.decrypt(request.username)
    decryptStr = decryptStr.replace("\b", "")
    decryptStr = decryptStr.replace("\u000b", "")
    
    # print(await api_get_user_by_username(decryptStr))
    
    return {
        "username": decryptStr
    }






# 获取会话列表
@app.post("/api/chat_sessions", response_model=schemas.ChatSessionOut)
async def chat_sessions(db: AsyncSession = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    try:
        userinfo = get_userInfo_from_token(token)
    except:
        HTTPException(status_code=401, detail="Token is invalid")

    query_stmt = select(
        TurChatSessions.id,
        TurChatSessions.title,
        TurChatSessions.created_at
    ).where(
        TurChatSessions.user_id == userinfo['id']
    ).order_by(
        TurChatSessions.id.desc()
    )
    data = await db.execute(query_stmt)
    
    output = dict()
    for item in data.mappings():
        processed_item = dict(item)
        processed_item['created_at'] = item['created_at'].timestamp()
        output[processed_item['id']] = processed_item
        
    return schemas.ChatSessionOut(
            code=200,
            message="Success",
            data=output
        )

# 获取会话的历史信息
@app.post("/api/chat_history", response_model=schemas.ChatHistoryOut)
async def chat_history(request: schemas.ChatHistoryIn, db: AsyncSession = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    try:
        userinfo = get_userInfo_from_token(token)
    except:
        HTTPException(status_code=401, detail="Token is invalid")

    query_stmt = select(
        TurChatHistory.id, 
        TurChatHistory.sender, 
        TurChatHistory.text, 
        TurChatHistory.created_at
    ).where(
        TurChatHistory.chat_session_id == request.chat_session_id,
        TurChatHistory.user_id == userinfo['id']
    ).order_by(
        TurChatHistory.created_at.desc()
    )

    data = await db.execute(query_stmt)
    
    output = dict()
    for item in data.mappings():
        processed_item = dict(item)
        processed_item['created_at'] = item['created_at'].timestamp()
        output[processed_item['id']] = processed_item

    return schemas.ChatHistoryOut(
            code=200,
            message="Success",
            data=output
        )

# 新建会话
@app.post("/api/chat_newsession", response_model=schemas.ChatNewsessionOut)
async def chat_newsession(request: schemas.ChatNewsessionIn, db: AsyncSession = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    try:
        userinfo = get_userInfo_from_token(token)
    except:
        HTTPException(status_code=401, detail="Token is invalid")

    # 插入会话
    query_stmt = insert(TurChatSessions).values(
        user_id = userinfo['id'],
        title = request.title,
    )

    data = await db.execute(query_stmt)
    chatSessionId = data.inserted_primary_key[0]
    await db.commit()

    return schemas.ChatNewsessionOut(
            code=200,
            message="Success",
            data=schemas.ChatNewsession(chat_session_id=chatSessionId)
        )


@app.post("/api/chat_delsession", response_model=schemas.ChatDelsessionOut)
async def chat_delsession(request: schemas.ChatDelsessionIn, db: AsyncSession = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    try:
        userinfo = get_userInfo_from_token(token)
    except:
        HTTPException(status_code=401, detail="Token is invalid")

    # 删除会话
    query_stmt = delete(TurChatSessions).where(
        TurChatSessions.id == request.chat_session_id,
        TurChatSessions.user_id == userinfo['id'],
    )
    await db.execute(query_stmt)
    await db.commit()

    return schemas.ChatDelsessionOut(
            code=200,
            message="Success",
        )


# 发送消息
@app.post("/api/chat_newmessage", response_model=schemas.ChatNewmessageOut)
async def chat_newmessage(request: schemas.ChatNewmessageIn, db: AsyncSession = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    try:
        userinfo = get_userInfo_from_token(token)
    except:
        HTTPException(status_code=401, detail="Token is invalid")

    # 插入历史记录
    query_stmt = insert(TurChatHistory).values(
        user_id = userinfo['id'],
        chat_session_id = request.chat_session_id,
        sender = "user",
        text = request.text,
    )

    data = await db.execute(query_stmt)
    chatMessageId = data.inserted_primary_key[0]
    
    # 插入空白消息等待AI回复
    query_stmt = insert(TurChatHistory).values(
        user_id = userinfo['id'],
        chat_session_id = request.chat_session_id,
        sender = "ai",
        text = "",
    )

    data = await db.execute(query_stmt)
    aiMessageId = data.inserted_primary_key[0]

    await db.commit()
    
    return schemas.ChatNewmessageOut(
            code=200,
            message="Success",
            data=schemas.ChatNewmessage(
                chat_message_id=chatMessageId,
                ai_message_id=aiMessageId
            )
        )
