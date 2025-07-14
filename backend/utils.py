import hashlib
import json
import random
from datetime import datetime, timedelta, timezone
import aiohttp
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select, insert, update, func
from SimpleCrypto import SimpleCrypto
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import database
from database import TurUsers
import random

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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
    
    query = select(TurUsers).where(TurUsers.id == int(user_id))
    user = await database.fetch_one(query)
    if user is None:
        raise credentials_exception
    return user

# 得到登录用户名
async def get_login_username(cookie: str = None):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://learn.turcar.net.cn/getusername.php?cookie=' + cookie) as response:            
            html = await response.text()
            return html


# 得到token
def get_token(userInfo: TurUsers):
    return SimpleCrypto.encrypt(json.dumps({
        "id": userInfo.id,
        "phone_number": userInfo.phone_number
        # "expire": int((datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
    }))



def get_userInfo_from_token(token: str):
    return json.loads(SimpleCrypto.decrypt(token))


# 生成密码哈希
def password_hash(password: str):
    m = hashlib.sha256()
    m.update(password.encode('utf-8'))
    return m.hexdigest()


def generate_numeric_code_randint():
    # 生成一个介于 100000 和 999999 之间的随机整数
    code = random.randint(100000, 999999)
    return code
