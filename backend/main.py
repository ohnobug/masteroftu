from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.concurrency import asynccontextmanager
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, insert, update, exists
from typing import List

from database import database, User, SMSLog
import schemas
import utils


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield    
    await database.disconnect()


app = FastAPI(title="FastAPI SMS and Auth Demo", lifespan=lifespan)

# --- 1. 短信发送接口 ---
@app.post("/sms/send", response_model=dict, summary="发送短信验证码 (带频率限制)")
async def send_sms(request: schemas.SendSMSRequest):
    """
    发送短信验证码。
    - 检查 MAX_SMS_PER_DAY 限制。
    - purpose: REGISTER 或 RESET_PASSWORD
    """
    # 如果是注册，检查手机号是否已存在
    if request.purpose == "REGISTER":
        query = select(exists().where(User.phone_number == request.phone_number))
        user_exists = await database.fetch_val(query)
        if user_exists:
            raise HTTPException(status_code=400, detail="Phone number already registered.")

    # 如果是重置密码，检查手机号是否存在
    if request.purpose == "RESET_PASSWORD":
        query = select(exists().where(User.phone_number == request.phone_number))
        user_exists = await database.fetch_val(query)
        if not user_exists:
            raise HTTPException(status_code=404, detail="Phone number not found.")

    result = await utils.send_sms_code(request.phone_number, request.purpose)
    return result

# --- 4. 注册接口 (用短信验证码) ---
@app.post("/register", response_model=schemas.Token, summary="用户注册")
async def register(user_data: schemas.UserCreate):
    # 1. 验证短信验证码
    is_valid = await utils.verify_sms_code(user_data.phone_number, user_data.verification_code, "REGISTER")
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code.")

    # 2. 检查用户是否已存在（双重检查）
    query = select(exists().where(User.phone_number == user_data.phone_number))
    if await database.fetch_val(query):
         raise HTTPException(status_code=400, detail="Phone number already registered.")

    # 3. 创建用户
    hashed_password = utils.get_password_hash(user_data.password)
    query = insert(User).values(
        phone_number=user_data.phone_number,
        password_hash=hashed_password
    )
    user_id = await database.execute(query)

    # 4. 注册成功后自动登录，返回 Token
    access_token = utils.create_access_token(data={"sub": str(user_id)})
    return {"access_token": access_token, "token_type": "bearer"}

# --- 3. 登录接口 ---
@app.post("/login", response_model=schemas.Token, summary="用户登录")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # OAuth2PasswordRequestForm 需要 phone_number 作为 username
    phone_number = form_data.username 
    password = form_data.password

    query = select(User).where(User.phone_number == phone_number)
    user = await database.fetch_one(query)

    if not user or not utils.verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone number or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = utils.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


# --- 5. 忘记密码接口 (用短信验证码重置) ---
@app.post("/password/reset", response_model=dict, summary="重置密码")
async def reset_password(request: schemas.ResetPasswordRequest):
    # 1. 验证短信验证码
    is_valid = await utils.verify_sms_code(request.phone_number, request.verification_code, "RESET_PASSWORD")
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code.")

    # 2. 查找用户
    query = select(User).where(User.phone_number == request.phone_number)
    user = await database.fetch_one(query)
    if not user:
        # 虽然验证码通过了，但理论上用户应该存在
        raise HTTPException(status_code=404, detail="User not found.")

    # 3. 更新密码
    new_hashed_password = utils.get_password_hash(request.new_password)
    update_query = update(User).where(User.id == user.id).values(password_hash=new_hashed_password)
    await database.execute(update_query)

    return {"message": "Password reset successfully."}


# --- 2. 已发送的短信看板 ---
@app.get("/sms/dashboard", response_model=List[schemas.SMSLogOut], summary="短信发送记录看板 (需要登录)")
async def sms_dashboard(
    skip: int = 0, 
    limit: int = 20, 
    current_user: schemas.UserOut = Depends(utils.get_current_user)
):
    """
    获取所有短信发送记录。
    注意：在生产环境中，你可能需要限制只有管理员才能访问此接口，或者只显示当前用户的记录。
    这里为了演示，只要登录了就能看所有记录。
    """
    query = select(SMSLog).order_by(SMSLog.sent_at.desc()).offset(skip).limit(limit)
    logs = await database.fetch_all(query)
    return logs

# 示例：获取当前登录用户信息
@app.get("/users/me", response_model=schemas.UserOut)
async def read_users_me(current_user: schemas.UserOut = Depends(utils.get_current_user)):
    return current_user
