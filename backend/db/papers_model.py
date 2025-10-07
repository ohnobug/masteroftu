import enum

from sqlalchemy import JSON, TIMESTAMP, Column, ForeignKey, Integer, String, Text, func, Enum
from db.database import Base
from sqlalchemy.orm import relationship

class PaperStatus(enum.Enum):
    PENDING = "PENDING"
    PROCESSING_VISION = "PROCESSING_VISION"
    PROCESSING_NLP = "PROCESSING_NLP"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TurPapers(Base):
    __tablename__ = "tur_papers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tur_users.id"), nullable=False, index=True)
    file_hash = Column(String(128), unique=True, index=True, nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    status = Column(Enum(PaperStatus), default=PaperStatus.PENDING, nullable=False)
    subject = Column(String(100), nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # 添加与用户的 relationship
    user = relationship("TurUsers", back_populates="papers")

    # relationship 指向正确的类名 'TurQuestion'
    questions = relationship(
        "TurQuestion", back_populates="paper", cascade="all, delete-orphan"
    )


class TurQuestion(Base):
    __tablename__ = "tur_questions"

    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("tur_papers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("tur_users.id"), nullable=False, index=True)

    id_in_paper = Column(String(32), nullable=True)
    question_text = Column(Text, nullable=True)
    type = Column(String(50), nullable=True)
    options = Column(JSON, nullable=True)
    position_info = Column(JSON, nullable=True)
    cropped_image_path = Column(String(512), nullable=True)
    reference_answer = Column(Text, nullable=True)
    analysis = Column(Text, nullable=True)

    paper = relationship("TurPapers", back_populates="questions")
