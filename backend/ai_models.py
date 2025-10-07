import json
import re
from typing import Dict, Optional, Any
from openai import APIStatusError, OpenAI
import config
from db.papers_model import TurQuestion

# 全局 AI 客户端变量
client: Optional[OpenAI] = None

def init_client() -> bool:
    """
    初始化全局 OpenAI 客户端。
    这是启动任何 worker 之前必须调用的函数。
    返回 True 表示成功，False 表示失败。
    """
    global client
    if client:
        print("OpenAI 客户端已经初始化。")
        return True
    
    try:
        client = OpenAI(
            api_key=config.SILICONFLOW_API_KEY,
            base_url=config.SILICONFLOW_BASE_URL,
            timeout=600.0,
            max_retries=2,
        )
        print("OpenAI 客户端初始化成功。")
        return True
    except Exception as e:
        print(f"[严重错误] OpenAI 客户端初始化失败: {e}")
        client = None
        return False

def fix_and_parse_json(raw_text: str) -> Optional[Dict[str, Any]]:
    """
    健壮的函数，用于清理、修复并解析可能无效的JSON字符串。
    - 移除 Markdown 的 JSON 代码块标记。
    - 尝试解析清理后的字符串。
    """
    # 使用正则表达式移除 ```json ... ``` 标记
    cleaned_text = re.sub(r'```json\s*(.*?)\s*```', r'\1', raw_text, flags=re.DOTALL).strip()
    cleaned_text = re.sub(r'^```json', "", cleaned_text, flags=re.DOTALL).strip()
    cleaned_text = re.sub(r'```$', "", cleaned_text, flags=re.DOTALL).strip()
    # cleaned_text = re.sub(r'\(', "(", cleaned_text, flags=re.DOTALL).strip()
    # cleaned_text = re.sub(r'\)', ")", cleaned_text, flags=re.DOTALL).strip()
    if not cleaned_text:
        # return None
        raise
        
    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        print(f"\n[错误] JSON解析失败: {e}")
        print(f"---------- 导致解析失败的原始内容 BEGIN ----------\n{cleaned_text}\n----------- 导致解析失败的原始内容 END -----------")
        # return None
        raise

def extract_question_data_from_image(base64_image: str) -> Optional[Dict[str, Any]]:
    """
    调用视觉模型从图片中提取题目信息。
    """
    if not client:
        raise ConnectionError("AI 客户端未初始化。请先调用 init_client()")

    # 使用 r"""...""" 原始字符串来避免不必要的转义警告
    prompt = r"""你是一个专业的试卷分析引擎，你的唯一任务是提取信息并以JSON格式输出。
    分析提供的试卷图片，并严格按照以下JSON结构和示例返回结果。
    
    **输出JSON结构:**
    {
      "subject": "学科名称",
      "questions": [
        {
          "id_in_paper": "题号",
          "question_text": "完整的题目文本",
          "options": { "A": "选项A", "B": "选项B", ... },
          "type": "选择题" or "主观题"
        }
      ]
    }
    
    **绝对规则**:
    1. 你的回答必须是且仅是一个完整的、可以被直接解析的JSON对象。禁止任何解释性文字或代码块标记。
    2. 如果题目没有选项（例如主观题），"options"字段的值应为 `null`。
    3. JSON字符串值中的任何单个反斜杠 `\` 必须被转义为 `\\`。
    """

    try:
        response = client.chat.completions.create(
            model=config.VISION_MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            max_tokens=4096,
            temperature=0.0,
        )
        full_response_content = response.choices[0].message.content
        return fix_and_parse_json(full_response_content)
    except Exception as e:
        print(f"调用视觉模型API时发生错误: {e}")
        raise


def get_question_analysis_from_nlp(subject: str, question: TurQuestion) -> Optional[Dict[str, Any]]:
    """
    调用语言模型分析题目并给出答案和解析。(已优化)
    """
    if not client:
        raise ConnectionError("AI 客户端未初始化。请先调用 init_client()")

    question_str = f"题目内容: {question.question_text}\n类型: {question.type}\n"
    if question.options:
        options_text = "\n".join([f"  {key}: {value}" for key, value in question.options.items()])
        question_str += f"选项:\n{options_text}"

    # 【优化 1: 改进 Prompt】
    # - 提供更精确的角色 (例如 "高中数学")
    # - 明确指出文本中可能包含 LaTeX 公式
    analysis_prompt = f"""你是一位资深的**高中{subject}**学科教研专家。
请分析以下题目，并严格按照JSON格式输出答案和解析。

**题目信息 (可能包含 LaTeX 数学公式):**
{question_str}

**输出要求 (JSON格式):**
{{
  "reference_answer": "...",
  "analysis": "..."
}}

**绝对规则**:
1. 你的回答必须是且仅是一个符合上述结构的、可以被直接解析的JSON对象。
2. 禁止在JSON之外添加任何解释性文字或Markdown标记。
3. "reference_answer" 应为题目的最终答案。对于选择题，请直接给出选项字母，例如 "A"。
4. "analysis" 应为详细的解题步骤、思路和涉及的知识点分析。
"""
    try:
        response = client.chat.completions.create(
            model=config.LANGUAGE_MODEL_NAME,
            messages=[{"role": "user", "content": analysis_prompt}],
            max_tokens=4096,
            temperature=0.2,
            # 【优化 2: 重新启用 JSON 模式】
            # 这是获取稳定 JSON 输出的最佳实践
            response_format={"type": "json_object"},
        )
        response_content = response.choices[0].message.content
        return fix_and_parse_json(response_content)
    except APIStatusError as e:
        print(f"调用语言模型API时发生状态错误: Status Code={e.status_code}, Response={e.response}")
        # raise e
        return {
            "reference_answer": "",
            "analysis": ""
        }
    except Exception as e:
        # 其他类型的错误（例如网络问题）
        print(f"调用语言模型API时发生未知错误: {e}")
        return {
            "reference_answer": "",
            "analysis": ""
        }