# 文件: ./schemas/papers.py

import datetime
import uuid
from pydantic import BaseModel
from typing import List
from db.papers_model import PaperStatus
from .base_response import BaseResponse

# 用于验证请求体中的锚框数据
class PositionInfoCreate(BaseModel):
    x: float
    y: float
    width: float
    height: float
    label: str
    # 注意：ID 通常由后端生成，在 "Create" 模型中最好是可选或不存在
    id: uuid.UUID | None = None 

# 描述 "试卷" 的核心数据
class PaperInfo(BaseModel):
    id: int
    user_id: int
    original_filename: str
    status: PaperStatus
    subject: str | None
    created_at: datetime.datetime
    error_message: str | None

    class Config:
        from_attributes = True

# 描述 "问题" 的核心数据
class QuestionInfo(BaseModel):
    id: int
    user_id: int
    paper_id: int
    id_in_paper: str | None
    question_text: str | None
    options: dict | None
    type: str | None
    position_info: dict | None
    cropped_image_path: str | None
    reference_answer: str | None
    analysis: str | None

    class Config:
        from_attributes = True

# 返回单个试卷的响应
class PaperResponse(BaseResponse[PaperInfo]):
    pass

# 返回试卷列表的响应
class PaperListResponse(BaseResponse[List[PaperInfo]]):
    pass

# 返回单个问题的响应
class QuestionResponse(BaseResponse[QuestionInfo]):
    pass

# 返回问题列表的响应
class QuestionListResponse(BaseResponse[List[QuestionInfo]]):
    pass