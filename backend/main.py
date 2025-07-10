from datetime import datetime
import json
import aiohttp
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse
import schemas
from SimpleCrypto import SimpleCrypto
from moodle_api import api_create_users, api_get_autologin_key, api_get_users_by_username
from database import TurChatSessions, TurChatHistory
import database
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from utils import get_userInfo_from_token

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
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# # --- 1. 短信发送接口 ---
# @app.post("/api/sms/send", response_model=dict, summary="发送短信验证码 (带频率限制)")
# async def send_sms(request: schemas.SendSMSRequest):
#     """
#     发送短信验证码。
#     - 检查 MAX_SMS_PER_DAY 限制。
#     - purpose: REGISTER 或 RESET_PASSWORD
#     """
#     # 如果是注册，检查手机号是否已存在
#     if request.purpose == "REGISTER":
#         query = select(exists().where(User.phone_number == request.phone_number))
#         user_exists = await database.fetch_val(query)
#         if user_exists:
#             raise HTTPException(status_code=400, detail="Phone number already registered.")

#     # 如果是重置密码，检查手机号是否存在
#     if request.purpose == "RESET_PASSWORD":
#         query = select(exists().where(User.phone_number == request.phone_number))
#         user_exists = await database.fetch_val(query)
#         if not user_exists:
#             raise HTTPException(status_code=404, detail="Phone number not found.")

#     result = await utils.send_sms_code(request.phone_number, request.purpose)
#     return result



# # --- 4. 注册接口 (用短信验证码) ---
# @app.post("/api/register", response_model=schemas.Token, summary="用户注册")
# async def register(user_data: schemas.UserCreate):
#     # 1. 验证短信验证码
#     is_valid = await utils.verify_sms_code(user_data.phone_number, user_data.verification_code, "REGISTER")
#     if not is_valid:
#         raise HTTPException(status_code=400, detail="Invalid or expired verification code.")

#     # 2. 检查用户是否已存在（双重检查）
#     query = select(exists().where(User.phone_number == user_data.phone_number))
#     if await database.fetch_val(query):
#          raise HTTPException(status_code=400, detail="Phone number already registered.")

#     # 3. 创建用户
#     hashed_password = utils.get_password_hash(user_data.password)
#     query = insert(User).values(
#         phone_number=user_data.phone_number,
#         password_hash=hashed_password
#     )
#     user_id = await database.execute(query)

#     # 4. 注册成功后自动登录，返回 Token
#     access_token = utils.create_access_token(data={"sub": str(user_id)})
#     return {"access_token": access_token, "token_type": "bearer"}



# # --- 3. 登录接口 ---
# @app.get("/api/login", summary="用户登录")
# async def login(
#     # form_data: OAuth2PasswordRequestForm = Depends()
#     ):
#     get_login_username = await utils.get_login_username("")
#     print(get_login_username)
#     return get_login_username
    
#     # # OAuth2PasswordRequestForm 需要 phone_number 作为 username
#     # phone_number = form_data.username 
#     # password = form_data.password

#     # query = select(User).where(User.phone_number == phone_number)
#     # user = await database.fetch_one(query)

#     # if not user or not utils.verify_password(password, user.password_hash):
#     #     raise HTTPException(
#     #         status_code=status.HTTP_401_UNAUTHORIZED,
#     #         detail="Incorrect phone number or password",
#     #         headers={"WWW-Authenticate": "Bearer"},
#     #     )
    
#     # access_token = utils.create_access_token(data={"sub": str(user.id)})
#     # return {"access_token": access_token, "token_type": "bearer"}



# # --- 5. 忘记密码接口 (用短信验证码重置) ---
# @app.post("/api/password/reset", response_model=dict, summary="重置密码")
# async def reset_password(request: schemas.ResetPasswordRequest):
#     # 1. 验证短信验证码
#     is_valid = await utils.verify_sms_code(request.phone_number, request.verification_code, "RESET_PASSWORD")
#     if not is_valid:
#         raise HTTPException(status_code=400, detail="Invalid or expired verification code.")

#     # 2. 查找用户
#     query = select(User).where(User.phone_number == request.phone_number)
#     user = await database.fetch_one(query)
#     if not user:
#         # 虽然验证码通过了，但理论上用户应该存在
#         raise HTTPException(status_code=404, detail="User not found.")

#     # 3. 更新密码
#     new_hashed_password = utils.get_password_hash(request.new_password)
#     update_query = update(User).where(User.id == user.id).values(password_hash=new_hashed_password)
#     await database.execute(update_query)

#     return {"message": "Password reset successfully."}



# --- 2. 已发送的短信看板 ---
# @app.get("/api/sms/dashboard", response_model=List[schemas.SMSLogOut], summary="短信发送记录看板 (需要登录)")
# async def sms_dashboard(
#     skip: int = 0, 
#     limit: int = 20, 
#     current_user: schemas.UserOut = Depends(utils.get_current_user)
# ):
#     """
#     获取所有短信发送记录。
#     注意：在生产环境中，你可能需要限制只有管理员才能访问此接口，或者只显示当前用户的记录。
#     这里为了演示，只要登录了就能看所有记录。
#     """
#     query = select(SMSLog).order_by(SMSLog.sent_at.desc()).offset(skip).limit(limit)
#     logs = await database.fetch_all(query)
#     return logs

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # 在这里验证 form_data.username 和 form_data.password
    # 如果验证成功，生成一个 token 并返回
    # 如果验证失败，抛出 HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, ...)
    return {"access_token": "your_generated_token", "token_type": "bearer"}

@app.post("/api/register", response_model=schemas.BaseResponse, summary="用户注册")
async def register(user_data: schemas.UserCreate):
    """
    用户注册
    """
    async with aiohttp.ClientSession() as session:
        # 检测手机号是否已存在
        userinfo = await api_get_users_by_username(session, [user_data.phone_number])
        if userinfo:
            raise UnicornException(code=400, message="手机号已被注册")
        
        # 注册新账号
        result = await api_create_users(session, [{
            'username': user_data.phone_number,
            'password': user_data.password,
            'firstname': "姓",
            'lastname': "名",
            'email': user_data.phone_number + "@turcar.net.cn",
        }])

    if result is None:
        raise UnicornException(code=400, message=json.dumps(result))

    return schemas.BaseResponse(
        code=200,
        message="注册成功"
    )


@app.post("/api/login", response_model=schemas.UserInfoRequestOut)
async def login(request: schemas.UserLoginPrivatetoken):
    async with aiohttp.ClientSession() as session:
        # 使用私有令牌获取自动登录密钥
        if not request.privatetoken:
            raise UnicornException(code=400, message="私有令牌不能为空")
        
        print(f"使用私有令牌: {request.privatetoken}")
        
        # 获取自动登录密钥
        result = await api_get_autologin_key(session=session, privatetoken=request.privatetoken)
        print(result)
    
    return {
        "username": ""
    }


# 示例：获取当前登录用户信息
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
