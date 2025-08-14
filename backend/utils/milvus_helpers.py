import openai
from pymilvus import MilvusClient

# 定义集合名称
COLLECTION_NAME = "knowledge_base"

# 连接Milvus
client = MilvusClient("../milvus_db/milvus_demo.db")

# 创建集合
if not client.has_collection(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        dimension=1024
    )

client_openai = openai.OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

def get_embedding(text: str):
    """得到词嵌入

    Args:
        text: 文本
    """
    response_embedding = client_openai.embeddings.create(
        model="bge-m3",
        input=[text]
    )

    return response_embedding.data[0].embedding

