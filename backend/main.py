import json
import aiohttp
import schemas
import database
import datetime
from fastapi import Depends, FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse, HTMLResponse
from SimpleCrypto import SimpleCrypto
from moodle_api import api_create_users, api_get_autologin_key, api_get_users_by_username
from database import TurChatSessions, TurChatHistory, TurUsers, TurVerifyCodes
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from utils import get_token, get_userInfo_from_token, password_hash, generate_numeric_code_randint, p
from io import StringIO

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



@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """
    自定义 HTTPException 处理器。
     khusus 针对 401 Unauthorized 错误返回统一的 JSON 格式响应。
    """
    print(f"Caught HTTPException with status code: {exc.status_code} and detail: {exc.detail}") # Optional debug print

    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        # 这会捕获：
        # 1. oauth2_scheme 因为缺少 Header 抛出的默认 401
        # 2. get_current_user 因为令牌无效等原因抛出的 401
        # 您可以根据需要进一步检查 exc.detail 来区分不同的 401 原因，
        # 但通常提供一个通用的“认证失败”消息就足够了，以免泄露过多信息。
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "code": 401,
                "message": exc.detail
            }
        )
    else:
        # 对于其他 HTTPException 状态码 (如 400, 404, 422, 500)，
        # 可以选择：
        # A) 重新抛出异常，让 FastAPI 的默认 HTTPException 处理器处理
        # raise exc
        # B) 返回一个基于原始异常信息的 JSON 响应 (如下所示)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                 "code": exc.status_code,
                 "message": exc.detail
            }
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

# 登录
@app.post("/api/login", response_model=schemas.UserLoginRequestOut)
async def login(request: schemas.UserLoginRequestIn, db: AsyncSession = Depends(database.get_db)):
    """
    用户登录
    """
    query_stmt = select(TurUsers).where(TurUsers.phone_number == request.phone_number)
    result = await db.execute(query_stmt)
    userinfo = result.scalar_one_or_none()

    if userinfo is None:
        raise HTTPException(status_code=401, detail="手机号未注册")

    checkPassword = password_hash(request.password)
    if (checkPassword == userinfo.password_hash):
        token = get_token(userinfo)
        
        return schemas.UserLoginRequestOut(
            code=200,
            message="Success",
            data=schemas.UserLoginToken(token=token)
        )
    else:
        raise HTTPException(status_code=401, detail="用户密码错误")

# 注册
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
        raise HTTPException(status_code=409, detail="手机号已被注册")

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

# 重置密码
@app.post("/api/reset_password", response_model=schemas.UserResetPasswordRequestOut, summary="重置密码")
async def reset_password(request: schemas.UserResetPasswordRequestIn, db: AsyncSession = Depends(database.get_db)):
    """
    重置密码
    """
    # 检测用户是否注册
    user_exists_stmt = select(TurUsers).where(TurUsers.phone_number == request.phone_number)
    result = await db.execute(user_exists_stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="手机号未注册")

    # 检查验证码
    select_stmt = select(
        TurVerifyCodes
    ).where(
        TurVerifyCodes.phone_number == request.phone_number,
        TurVerifyCodes.purpose == schemas.UserGetVerifyCodePurposeEnum.FORGOT_PASSWORD,
        TurVerifyCodes.is_used == False,
        TurVerifyCodes.code == request.verify_code
    ).order_by(
        TurVerifyCodes.id.desc()
    ).limit(1)
    lastVerifyCode = (await db.execute(select_stmt)).scalar_one_or_none()

    if lastVerifyCode is None:
        raise HTTPException(status_code=429, detail="请先获取验证码")

    if lastVerifyCode.created_at < datetime.datetime.now() - datetime.timedelta(seconds=60):
        raise HTTPException(status_code=429, detail="验证码已过期")

    # 更新为已使用
    update_stmt = update(TurVerifyCodes).where(
        TurVerifyCodes.id == lastVerifyCode.id
    ).values(
        is_used=True
    )
    result = await db.execute(update_stmt)
    await db.commit()

    update_stmt = update(TurUsers).where(
        TurUsers.phone_number == request.phone_number
    ).values(
        password_hash=password_hash(request.new_password)
    )

    result = await db.execute(update_stmt)
    await db.commit()

    return schemas.UserResetPasswordRequestOut(
        code=200,
        message="重置密码成功"
    )

# 获取手机验证码
@app.post("/api/get_verify_code", response_model=schemas.UserGetVerifyCodeRequestOut, summary="获取验证码")
async def get_verify_code(request: schemas.UserGetVerifyCodeRequestIn, db: AsyncSession = Depends(database.get_db)):
    # ------------------------------------------------------------------------
    # 不管用没用60秒内不能重复获取验证码
    select_stmt = select(
        TurVerifyCodes
    ).where(
        TurVerifyCodes.phone_number == request.phone_number,
        TurVerifyCodes.purpose == schemas.UserGetVerifyCodePurposeEnum.FORGOT_PASSWORD,
    ).order_by(
        TurVerifyCodes.id.desc()
    ).limit(1)
    lastVerifyCode = (await db.execute(select_stmt)).scalar()

    if lastVerifyCode is not None:
        p(lastVerifyCode.created_at)
        p(datetime.datetime.now() - datetime.timedelta(seconds=60))

        if lastVerifyCode.created_at > datetime.datetime.now() - datetime.timedelta(seconds=60):
            raise HTTPException(status_code=429, detail="60秒内不允许重复获取验证码")
    # ------------------------------------------------------------------------

    code = generate_numeric_code_randint()
    insert_stmt = insert(TurVerifyCodes).values(
        phone_number=request.phone_number,
        code=code,
        purpose=request.purpose,
        is_used=False
    )
    result = await db.execute(insert_stmt)
    await db.commit()

    return schemas.UserGetVerifyCodeRequestOut(
        code=200,
        message="获取验证码成功"
    )

# 获取手机验证码列表(测试用)
@app.get("/api/get_verify_code_list", response_class=HTMLResponse, summary="获取验证码列表")
async def get_verify_code_list(db: AsyncSession = Depends(database.get_db)):
    # ------------------------------------------------------------------------
    select_stmt = select(TurVerifyCodes).order_by(TurVerifyCodes.id.desc())
    data = (await db.scalars(select_stmt)).all()
    # ------------------------------------------------------------------------

    s = StringIO()

    script = """
<script>
function clearVerifyCodeList() {
    fetch("/api/clear_verify_code_list", {
        method: "POST"
    }).then(res => {
        if (res.status == 200) {
            location.reload();
        }
    })
}
</script>
"""

    s.write(script)

    s.write('<table style="border-collapse: collapse; width: 600px;">')
    s.write('<thead><tr>')

    s.write('<th style="border: 1px solid black; padding: 4px; text-align: left;">电话</th>')
    s.write('<th style="border: 1px solid black; padding: 4px; text-align: left;">验证码</th>')
    s.write('<th style="border: 1px solid black; padding: 4px; text-align: left;">是否已使用</th>')
    s.write('<th style="border: 1px solid black; padding: 4px; text-align: left;">日期</th>')
    s.write('</tr></thead>')
    s.write('<tbody>')

    if len(data) > 0:
        for item in data:
            s.write('<tr>')
            s.write(f'<td style="border: 1px solid black; padding: 4px;">{item.phone_number}</td>')
            s.write(f'<td style="border: 1px solid black; padding: 4px;">{item.code}</td>')
            if item.is_used:
                s.write(f'<td style="border: 1px solid black; padding: 4px;">是</td>')
            else:
                s.write(f'<td style="border: 1px solid black; padding: 4px;">否</td>')
            s.write(f'<td style="border: 1px solid black; padding: 4px;">{item.created_at}</td>')
            s.write('</tr>')
    else:
        s.write("<tr><td style=\"border: 1px solid black; padding: 4px; text-align: center;\" colspan=\"4\">无数据</td></tr>")

    s.write("</tbody>")
    s.write("</table>")
    s.write("<br />")
    s.write(f"<button onclick=\"clearVerifyCodeList()\">清空</button>")
    content = s.getvalue()
    s.close()

    return content


# 清空手机验证码列表(测试用)
@app.post("/api/clear_verify_code_list", response_model=schemas.BaseResponse, summary="清空验证码列表")
async def clear_verify_code_list(db: AsyncSession = Depends(database.get_db)):
    delete_stmt = delete(TurVerifyCodes)
    data = await db.execute(delete_stmt)

    await db.commit()

    return schemas.BaseResponse(code=200, message="清空成功")

# 获取用户信息
@app.post("/api/userinfo", response_model=schemas.UserInfoRequestOut)
async def userinfo(db: AsyncSession = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    try:
        userinfo = get_userInfo_from_token(token)
    except:
        HTTPException(status_code=401, detail="用户尚未登录")
    
    return schemas.UserInfoRequestOut(
        code=200,
        message="success",
        data=schemas.UserInfo(
            phone_number=userinfo['phone_number']
        )
    )


# 获取会话列表
@app.post("/api/chat_sessions", response_model=schemas.ChatSessionOut)
async def chat_sessions(db: AsyncSession = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    try:
        userinfo = get_userInfo_from_token(token)
    except:
        HTTPException(status_code=401, detail="用户尚未登录")

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
        HTTPException(status_code=401, detail="用户尚未登录")

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
        HTTPException(status_code=401, detail="用户尚未登录")

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


# 删除会话
@app.post("/api/chat_delsession", response_model=schemas.ChatDelsessionOut)
async def chat_delsession(request: schemas.ChatDelsessionIn, db: AsyncSession = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    try:
        userinfo = get_userInfo_from_token(token)
    except:
        HTTPException(status_code=401, detail="用户尚未登录")

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
        HTTPException(status_code=401, detail="用户尚未登录")

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
