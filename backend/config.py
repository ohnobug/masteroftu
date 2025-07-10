import os
from dotenv import load_dotenv

load_dotenv()

# --- Database Configuration ---
# 请替换成你自己的数据库信息
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "136404838Zz")
DB_PORT = os.getenv("DB_PORT", 3308)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "tur")
DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- Security Configuration ---
SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key_change_this_in_production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- SMS Configuration ---
# 需求 1: 每个号码发送限制 (常量)
MAX_SMS_PER_DAY = 5
SMS_CODE_EXPIRE_MINUTES = 5
