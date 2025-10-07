# ./routers/papers.py (修正后)

import os
import hashlib
from typing import List, Dict

# 导入 Form 用于接收表单数据，以及 pydantic 的 ValidationError 和 TypeAdapter
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
    BackgroundTasks,
    Form,
    status,
)
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import ValidationError, TypeAdapter
import aiofiles
import config
from utils.utils import get_userInfo_from_token
from routers.oauth2_scheme import oauth2_scheme
from sqlalchemy.orm import selectinload

# --- 【关键修正】导入新的、正确的响应模型 ---
from schemas.papers import (
    PaperResponse, 
    PaperListResponse, # <--- 新增
    PositionInfoCreate, 
    QuestionResponse,
    QuestionListResponse # <--- 新增
)
from db.database import get_db
from db.papers_model import TurPapers, TurQuestion, PaperStatus
from pikaClient import pika_client

# 创建一个 APIRouter 实例
router = APIRouter(prefix='/api')

# 可复用的依赖项，用于获取当前用户信息
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    try:
        user_info = get_userInfo_from_token(token)
        return user_info
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 无效或已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )

# /upload 接口
@router.post(
    "/upload", 
    response_model=PaperResponse, 
    # 当成功创建新资源时，返回 201 更符合 HTTP 规范
    status_code=status.HTTP_201_CREATED,
    # 当文件已存在时，我们也会返回 200
    responses={200: {"description": "File already exists"}}
)
async def upload_paper(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    anchors_json: str = Form("[]"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """上传试卷图片，如果图片已存在则直接返回，否则创建新记录并处理。"""
    
    print(f"PRODUCER: Sending to queue -> '{config.VISION_QUEUE_NAME}'")
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="文件必须是图片格式。")

    contents = await file.read()
    file_hash = hashlib.sha256(contents).hexdigest()

    query = select(TurPapers).where(TurPapers.file_hash == file_hash)
    result = await db.execute(query)
    existing_paper = result.scalars().first()

    # 如果试卷记录已存在，构造完整的响应并返回
    if existing_paper:
        return PaperResponse(code=200, message="File already exists.", data=existing_paper)
    
    # 1. 验证和解析 anchors_json
    try:
        anchor_adapter = TypeAdapter(List[PositionInfoCreate])
        anchors_data = anchor_adapter.validate_json(anchors_json)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"锚框信息 (anchors_json) 格式错误: {e}"
        )

    # 2. 保存上传的原始图片文件
    file_extension = os.path.splitext(file.filename)[1]
    file_path = os.path.join(config.DATA_DIR, f"{file_hash}{file_extension}")

    async with aiofiles.open(file_path, "wb") as out_file:
        await out_file.write(contents)

    user_id = current_user.get('id')

    # 3. 创建新的数据库记录
    db_paper = TurPapers(
        user_id=user_id,
        file_hash=file_hash,
        original_filename=file.filename,
        file_path=file_path,
        status=PaperStatus.PENDING,
    )

    db.add(db_paper)

    if anchors_data:
        questions_to_add = []
        for anchor in anchors_data:
            new_question = TurQuestion(
                user_id=user_id,
                paper=db_paper,
                type=anchor.label,
                position_info=anchor.model_dump(mode="json"),
            )
            questions_to_add.append(new_question)
        db.add_all(questions_to_add)

    await db.commit()
    await db.refresh(db_paper)

    # 4. 构造并发送消息到 RabbitMQ
    message = {
        "paper_id": db_paper.id,
        "user_id": user_id,
        "file_path": file_path,
        "file_hash": file_hash,
        "anchors": [anchor.model_dump(mode="json") for anchor in anchors_data] if anchors_data else [],
    }
    
    background_tasks.add_task(
        pika_client.send_message,
        config.VISION_QUEUE_NAME,
        message
    )

    # 创建成功，构造完整的响应并返回
    return PaperResponse(code=201, message="Upload successful, processing started.", data=db_paper)


# --- 【关键修正】修改 response_model 和 return 语句 ---
@router.get("/papers", response_model=PaperListResponse)
async def get_all_papers(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """查询当前用户的所有已上传试卷列表。"""
    user_id = current_user.get('id')
    
    query = select(TurPapers).where(TurPapers.user_id == user_id).order_by(TurPapers.created_at.desc())
    result = await db.execute(query)
    papers = result.scalars().all()
    
    # 将查询结果包装在 PaperListResponse 中返回
    return PaperListResponse(data=papers)


@router.get("/papers/{paper_id}", response_model=PaperResponse)
async def get_paper_details(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """查询指定试卷的详细信息，确保该试卷属于当前用户。"""
    user_id = current_user.get('id')
    
    query = select(TurPapers).where(TurPapers.id == paper_id, TurPapers.user_id == user_id)
    result = await db.execute(query)
    db_paper = result.scalars().first()
    
    if not db_paper:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="试卷未找到或无权访问")

    # 将查询结果包装在 PaperResponse 中返回
    return PaperResponse(data=db_paper)


# 修改 response_model 和 return 语句 ---
@router.get("/papers/{paper_id}/questions", response_model=QuestionListResponse)
async def get_paper_questions(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """查询指定试卷的所有试题，确保该试卷属于当前用户。"""
    user_id = current_user.get('id')
    
    # 在查询时使用 selectinload 预加载 questions 关系
    query = (
        select(TurPapers)
        .where(TurPapers.id == paper_id, TurPapers.user_id == user_id)
        .options(selectinload(TurPapers.questions))
    )
    result = await db.execute(query)
    db_paper = result.scalars().first()

    if not db_paper:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="试卷未找到或无权访问")

    # 现在访问 db_paper.questions 不会再触发新的数据库查询，因为数据已经被预加载了
    return QuestionListResponse(data=db_paper.questions or [])


@router.get("/questions/{question_id}", response_model=QuestionResponse)
async def get_question_details(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """查询指定题目的详细信息，确保该题目属于当前用户。"""
    user_id = current_user.get('id')
    
    query = select(TurQuestion).where(TurQuestion.id == question_id, TurQuestion.user_id == user_id)
    result = await db.execute(query)
    db_question = result.scalars().first()

    if not db_question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="题目未找到或无权访问")

    # 将查询结果包装在 QuestionResponse 中返回
    return QuestionResponse(data=db_question)

