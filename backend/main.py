import database
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from routers import chats, users

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动阶段 (在 yield 之前)
    print("Application startup...")
    yield    
    print("Application shutdown...")
    # 释放数据库 Engine 和连接池
    if database.engine:
        await database.engine.dispose()
    print("Database engine disposed")


app = FastAPI(title="FastAPI新接口", lifespan=lifespan)

class UnicornException(Exception):
    def __init__(self, message: str, code: int = 400):
        self.code = code
        self.message = message

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=400,
        content={"code": exc.code, "message": exc.message},
    )

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """
    自定义 HTTPException 处理器。
     khusus 针对 401 Unauthorized 错误返回统一的 JSON 格式响应。
    """
    print(f"Caught HTTPException with status code: {exc.status_code} and detail: {exc.detail}")


    if exc.detail == "Not authenticated":
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": 401,
                "message": "用户尚未登录"
            }
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={
                "code": exc.status_code,
                "message": exc.detail
        }
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://turcar.net.cn",
        "https://learn.turcar.net.cn",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 对话路由
app.include_router(chats.router)

# 用户路由
app.include_router(users.router)
