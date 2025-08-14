from fastapi import APIRouter, Depends, HTTPException
import schemas
from routers.oauth2_scheme import oauth2_scheme
from utils.utils import get_userInfo_from_token
from utils.milvus_helpers import COLLECTION_NAME, client, get_embedding

router = APIRouter()

# 针对向量数据库的验证
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        userinfo = get_userInfo_from_token(token)
        if userinfo['id'] != 1:
            raise
    except:
        raise HTTPException(status_code=401, detail="Token parsing error")

@router.post("/api/embedding/insert", response_model=schemas.EmbeddingInsertOut)
async def insert_data(request: schemas.EmbeddingInsertIn, _: dict = Depends(verify_token)):
    """
    向 Milvus 集合中插入数据。
    """
    try:
        question=request['question']
        answer=request['answer']
        category=request['category']
        vector = get_embedding(question)

        data_to_insert = [
            {
                "question": question,
                "answer": answer,
                "category": category,
                "embedding": vector
            }
        ]

        res = client.insert(
            collection_name=COLLECTION_NAME,
            data=data_to_insert
        )

        return schemas.EmbeddingInsertOut(data={"inserted_ids": res['ids']})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting data into Milvus: {e}")


@router.post("/api/embedding/search", response_model=schemas.ApiResponse)
async def search_data(request: schemas.EmbeddingSearchIn, _: dict = Depends(verify_token)):
    """
    在 Milvus 中进行向量相似性搜索。
    """
    try:
        res = client.search(
            collection_name=request.collection_name,
            data=request.data,
            filter=request.filter,
            limit=request.limit,
            output_fields=request.output_fields,
        )
        return schemas.ApiResponse(data=res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching in Milvus: {e}")


@router.post("/api/embedding/query", response_model=schemas.ApiResponse)
async def query_data(request: schemas.EmbeddingQueryIn, _: dict = Depends(verify_token)):
    """
    根据过滤条件查询 Milvus 中的数据。
    """
    try:
        res = client.query(
            collection_name=request.collection_name,
            filter=request.filter,
            output_fields=request.output_fields,
        )
        return schemas.ApiResponse(data=res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying from Milvus: {e}")


@router.post("/api/embedding/delete", response_model=schemas.ApiResponse)
async def delete_data(request: schemas.EmbeddingDeleteIn, _: dict = Depends(verify_token)):
    """
    根据过滤条件删除 Milvus 中的数据。
    """
    try:
        res = client.delete(
            collection_name=request.collection_name,
            filter=request.filter,
        )
        return schemas.ApiResponse(data={"deleted_count": res['delete_count']})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting data from Milvus: {e}")
