from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, func
from db.database import Base
from sqlalchemy.orm import relationship

class TurUsers(Base):
    __tablename__ = "tur_users"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    chat_sessions = relationship("TurChatSessions", back_populates="user")
    papers = relationship("TurPapers", back_populates="user")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
6

class TurVerifyCodes(Base):
    __tablename__ = "tur_verify_codes"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), nullable=False, index=True)
    code = Column(String(10), nullable=False)
    purpose = Column(String(50), nullable=False)
    is_used = Column(Boolean, default=False)
    used_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
