import os
from dotenv import load_dotenv

load_dotenv()

# --- Database Configuration ---
# 请替换成你自己的数据库信息
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 3308)
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "136404838Zz")
DB_NAME = os.getenv("DB_NAME", "tur")
DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- Security Configuration ---
SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key_change_this_in_production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30

# --- SMS Configuration ---
# 需求 1: 每个号码发送限制 (常量)
MAX_SMS_PER_DAY = 5
SMS_CODE_EXPIRE_MINUTES = 5

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@127.0.0.1:5672/%2F?connection_attempts=3&heartbeat=3600")

LLM_API_KEY = os.getenv("LLM_API_KEY", "ollama")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://192.168.0.5:11434/v1")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "qwen2.5")

EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY", "ollama")
EMBEDDING_BASE_URL = os.getenv("EMBEDDING_BASE_URL", "http://192.168.0.5:11434/v1")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "bge-m3")

# 定义集合名称
EMBEDDING_MILVUS_DB_PATH = os.getenv("EMBEDDING_MILVUS_DB_PATH", "./milvus_db/me_knowledge.db")
EMBEDDING_CHROMA_DB_PATH = os.getenv("EMBEDDING_CHROMA_DB_PATH", "./milvus_db/me_knowledge_chroma")
EMBEDDING_COLLECTION_NAME = os.getenv("EMBEDDING_COLLECTION_NAME", "knowledge_base")
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "1024"))

# 使用Chromadb作为faq数据库
USE_CHROMADB = os.getenv("USE_CHROMADB", True)

# 最大查询知识库数量
CHROMADB_MAXIMUM_QUERY_RESULT = int(os.getenv("CHROMADB_MAXIMUM_QUERY_RESULT", "100"))
CHROMADB_QUERY_THRESHOLD = float(os.getenv("CHROMADB_QUERY_THRESHOLD", "1"))

# 相关问题知识库数量
CHROMADB_RELATED_MAXIMUM_QUERY_RESULT = int(os.getenv("CHROMADB_RELATED_MAXIMUM_QUERY_RESULT", "5"))
CHROMADB_RELATED_QUERY_THRESHOLD = float(os.getenv("CHROMADB_RELATED_QUERY_THRESHOLD", "1"))

LLM_SYSTEM_PROMPT = """# 角色与核心任务
你是一位智能AI教师。
你的核心任务是根据我提供的【学习资料】和你的知识库，为用户提供个性化、启发式的教学和辅导。

# 回答内容的规则
1.  **启发式教学**: 优先通过提问、举例和类比来引导用户独立思考，而不仅仅是直接给出答案。
2.  **融合知识**: 将【学习资料】与你自身的知识库相结合，提供更全面、深入的解释。
3.  **自信地教学**: 以清晰、专业的教师口吻进行讲解，避免使用“根据资料显示...”等不确定的前言。
4.  **处理未知问题**: 如果【学习资料】不足或无法回答用户的问题，应尝试引导用户换一种方式提问，或推荐相关的学习主题。如果确实无法解答，可以说：“这个问题很有趣，但可能超出了我目前的知识范围，我们可以一起探索其他相关的主题。” 绝对禁止编造答案。
5.  **保持鼓励与耐心**: 你的语气应始终充满耐心、鼓励性，并对用户的提问表示赞赏。

# 输出格式的绝对指令
你必须严格遵守以下格式化指令，这是最高优先级：
1.  **语言**: 必须使用用户所用语言进行回答，包括[ACTION]、[QUIZ]和[RESOURCE]后续所跟随的标题也需要适配语言。
2.  **结构**: 你的回答由不同类型的行组成。**每种元素必须独占一行**。
    *   **普通文本**: 直接书写，无需任何标签，不准输出方括号 "[" 或者 "]"，会被类型匹配器进行匹配,从而误以为是[ACTION]、[QUIZ]、[RESOURCE]。
    *   **互动操作**: 使用 `[ACTION] 操作标题` 格式，例如 `[ACTION] 给我举个例子` 或 `[ACTION] 深入解释一下`。
    *   **相关问题/测验**: 使用 `[QUIZ] 问题标题` 格式，用于检验学习效果。
    *   **学习资源**: 使用 `[RESOURCE] [资源标题](资源链接URL)` 格式。
3. **互动引导**: 当解释完一个概念后，主动使用 [ACTION] 或 [QUIZ] 引导用户进行下一步学习，增强互动性。
4. **鼓励性互动**: 当用户遇到困难或问题模糊时，使用 [ACTION] 按钮引导他们细化问题，例如 `[ACTION] 换个方式提问`。
5. **保持教育者角色**: 你的所有互动都应以激发好奇心和加深理解为目标。
"""

VISION_QUEUE_NAME = os.getenv("VISION_QUEUE_NAME", "paper_vision_queue")
NLP_QUEUE_NAME = os.getenv("NLP_QUEUE_NAME", "question_nlp_queue")

# SiliconFlow API 配置
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY", "sk-jwcnjpikvwlvkqaodhmtqallesmqoxakvfpigazqdjfqkyxo")
SILICONFLOW_BASE_URL = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")

# 文件存储目录
DATA_DIR = os.getenv("DATA_DIR", "./data")

CROPS_DIR = os.getenv("CROPS_DIR", "./data/crops")

# 大语言模型名称
VISION_MODEL_NAME = os.getenv("VISION_MODEL_NAME", "Qwen/Qwen2.5-VL-32B-Instruct")
LANGUAGE_MODEL_NAME = os.getenv("LANGUAGE_MODEL_NAME", "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B")
