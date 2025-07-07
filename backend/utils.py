import random
from datetime import datetime, timedelta, timezone
import aiohttp
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select, insert, update, func, and_
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, MAX_SMS_PER_DAY, SMS_CODE_EXPIRE_MINUTES
from database import database, User, VerificationCode, SMSLog

# --- Authentication Utils ---

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    query = select(User).where(User.id == int(user_id))
    user = await database.fetch_one(query)
    if user is None:
        raise credentials_exception
    return user

# --- SMS Service Utils ---

async def check_sms_rate_limit(phone_number: str):
    """检查短信发送频率限制"""
    one_day_ago = datetime.now(timezone.utc) - timedelta(days=1)
    query = select(func.count(SMSLog.id)).where(
        SMSLog.phone_number == phone_number,
        SMSLog.sent_at >= one_day_ago,
        SMSLog.status == 'SUCCESS'
    )
    count = await database.execute(query)
    if count >= MAX_SMS_PER_DAY:
        # 记录超限日志
        log_query = insert(SMSLog).values(
            phone_number=phone_number, content="Rate limit exceeded", status="RATE_LIMITED"
        )
        await database.execute(log_query)
        return False
    return True

async def send_sms_code(phone_number: str, purpose: str):
    """模拟发送短信验证码并保存到数据库"""
    
    # 1. 检查频率限制
    if not await check_sms_rate_limit(phone_number):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"SMS limit exceeded. Max {MAX_SMS_PER_DAY} per day."
        )

    # 2. 生成验证码
    code = "".join([str(random.randint(0, 9)) for _ in range(6)])
    content = f"【MyApp】您的验证码是: {code}。用于{purpose}，{SMS_CODE_EXPIRE_MINUTES}分钟内有效。"
    
    # 3. 模拟发送 (这里可以对接真实的短信服务商 API)
    print(f"--- SIMULATING SMS SENDING TO {phone_number} ---")
    print(content)
    print("------------------------------------------------")

    # 4. 记录发送日志
    log_query = insert(SMSLog).values(
        phone_number=phone_number, content=content, status="SUCCESS"
    )
    await database.execute(log_query)

    # 5. 存储验证码到 verification_codes 表
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=SMS_CODE_EXPIRE_MINUTES)
    code_query = insert(VerificationCode).values(
        phone_number=phone_number, code=code, purpose=purpose, expires_at=expires_at
    )
    await database.execute(code_query)
    
    return {"message": "SMS sent successfully", "phone_number": phone_number}

async def verify_sms_code(phone_number: str, code: str, purpose: str):
    """校验验证码"""
    now = datetime.now(timezone.utc)
    query = select(VerificationCode).where(
        VerificationCode.phone_number == phone_number,
        VerificationCode.code == code,
        VerificationCode.purpose == purpose,
        VerificationCode.is_used == False,
        VerificationCode.expires_at > now
    ).order_by(VerificationCode.id.desc())
    
    record = await database.fetch_one(query)
    
    if not record:
        return False
    
    # 标记验证码为已使用
    update_query = update(VerificationCode).where(VerificationCode.id == record.id).values(is_used=True)
    await database.execute(update_query)
    return True


# 得到登录用户名
async def get_login_username(cookie: str = None):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://learn.turcar.net.cn/getusername.php?cookie=' + cookie) as response:            
            html = await response.text()
            return html

