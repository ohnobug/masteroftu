# 文件: ./schemas/base_response.py (修正后的正确版本)

from pydantic import BaseModel
from typing import TypeVar, Generic # <--- 1. 关键导入

# 2. 定义一个类型变量 T，它将作为我们数据类型的占位符
T = TypeVar('T')

# 3. 让 BaseResponse 继承 BaseModel 和 Generic[T]
class BaseResponse(BaseModel, Generic[T]):
    code: int = 200
    message: str = "Success"
    data: T | None = None