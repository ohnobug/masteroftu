from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func, Enum
from db.database import Base
from sqlalchemy.orm import relationship

class TurChatSessions(Base):
    __tablename__ = "tur_chat_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tur_users.id"), index=True, nullable=False)
    title = Column(String(255), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("TurUsers", back_populates="chat_sessions")


class TurChatHistory(Base):
    __tablename__ = "tur_chat_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tur_users.id"), index=True, nullable=False)
    chat_session_id = Column(Integer, ForeignKey("tur_chat_sessions.id"), index=True, nullable=False)
    sender = Column(Enum("ai", "user"), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
