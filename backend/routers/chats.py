from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
import schemas
from routers.oauth2_scheme import oauth2_scheme
from utils import get_userInfo_from_token
from database import TurChatHistory, TurChatSessions, get_db

router = APIRouter()

# 获取会话列表
@router.post("/api/chat_sessions", response_model=schemas.ChatSessionOut)
async def chat_sessions(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        userinfo = get_userInfo_from_token(token)
    except:
        raise HTTPException(status_code=401, detail="token解析错误")

    query_stmt = select(
        TurChatSessions.id,
        TurChatSessions.title,
        TurChatSessions.created_at
    ).where(
        TurChatSessions.user_id == userinfo['id']
    ).order_by(
        TurChatSessions.id.desc()
    )
    data = await db.execute(query_stmt)
    
    output = dict()
    for item in data.mappings():
        processed_item = dict(item)
        processed_item['created_at'] = item['created_at'].timestamp()
        output[processed_item['id']] = processed_item
        
    return schemas.ChatSessionOut(
            code=200,
            message="success",
            data=output
        )


# 获取会话的历史信息
@router.post("/api/chat_history", response_model=schemas.ChatHistoryOut)
async def chat_history(request: schemas.ChatHistoryIn, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        userinfo = get_userInfo_from_token(token)
    except:
        raise HTTPException(status_code=401, detail="token解析错误")

    query_stmt = select(
        TurChatHistory.id, 
        TurChatHistory.sender, 
        TurChatHistory.text, 
        TurChatHistory.created_at
    ).where(
        TurChatHistory.chat_session_id == request.chat_session_id,
        TurChatHistory.user_id == userinfo['id']
    ).order_by(
        TurChatHistory.created_at.desc()
    )

    data = await db.execute(query_stmt)
    
    output = dict()
    for item in data.mappings():
        processed_item = dict(item)
        processed_item['created_at'] = item['created_at'].timestamp()
        output[processed_item['id']] = processed_item

    return schemas.ChatHistoryOut(
            code=200,
            message="success",
            data=output
        )


# 新建会话
@router.post("/api/chat_newsession", response_model=schemas.ChatNewsessionOut)
async def chat_newsession(request: schemas.ChatNewsessionIn, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        userinfo = get_userInfo_from_token(token)
    except:
        raise HTTPException(status_code=401, detail="token解析错误")

    savetitle = request.title
    if len(request.title) > 200:
        savetitle = request.title[:200]

    # 插入会话
    query_stmt = insert(TurChatSessions).values(
        user_id = userinfo['id'],
        title = savetitle,
    )

    data = await db.execute(query_stmt)
    chatSessionId = data.inserted_primary_key[0]
    await db.commit()

    return schemas.ChatNewsessionOut(
            code=200,
            message="success",
            data=schemas.ChatNewsession(chat_session_id=chatSessionId)
        )


# 删除会话
@router.post("/api/chat_delsession", response_model=schemas.ChatDelsessionOut)
async def chat_delsession(request: schemas.ChatDelsessionIn, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        userinfo = get_userInfo_from_token(token)
    except:
        raise HTTPException(status_code=401, detail="token解析错误")

    # 删除会话
    query_stmt = delete(TurChatSessions).where(
        TurChatSessions.id == request.chat_session_id,
        TurChatSessions.user_id == userinfo['id'],
    )
    await db.execute(query_stmt)
    await db.commit()

    return schemas.ChatDelsessionOut(
            code=200,
            message="success",
        )


# 发送消息
@router.post("/api/chat_newmessage", response_model=schemas.ChatNewmessageOut)
async def chat_newmessage(request: schemas.ChatNewmessageIn, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        userinfo = get_userInfo_from_token(token)
    except:
        raise HTTPException(status_code=401, detail="token解析错误")

    # 插入历史记录
    query_stmt = insert(TurChatHistory).values(
        user_id = userinfo['id'],
        chat_session_id = request.chat_session_id,
        sender = "user",
        text = request.text,
    )

    data = await db.execute(query_stmt)
    chatMessageId = data.inserted_primary_key[0]
    
    # 插入空白消息等待AI回复
    query_stmt = insert(TurChatHistory).values(
        user_id = userinfo['id'],
        chat_session_id = request.chat_session_id,
        sender = "ai",
        text = "",
    )

    data = await db.execute(query_stmt)
    aiMessageId = data.inserted_primary_key[0]

    await db.commit()
    
    return schemas.ChatNewmessageOut(
            code=200,
            message="success",
            data=schemas.ChatNewmessage(
                chat_message_id=chatMessageId,
                ai_message_id=aiMessageId
            )
        )
