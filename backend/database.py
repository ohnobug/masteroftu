from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, Boolean, func, MetaData
from sqlalchemy.ext.declarative import declarative_base
from databases import Database
from config import DATABASE_URL

# 使用 databases 库进行异步连接管理
database = Database(DATABASE_URL)
metadata = MetaData()
Base = declarative_base(metadata=metadata)

# SQLAlchemy Models (对应 SQL 表结构)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

class VerificationCode(Base):
    __tablename__ = "verification_codes"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), nullable=False, index=True)
    code = Column(String(10), nullable=False)
    purpose = Column(String(50), nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    expires_at = Column(TIMESTAMP, nullable=False)

class SMSLog(Base):
    __tablename__ = "sms_logs"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), nullable=False, index=True)
    content = Column(Text, nullable=False)
    status = Column(String(20), nullable=False)
    sent_at = Column(TIMESTAMP, server_default=func.now())