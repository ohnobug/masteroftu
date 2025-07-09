import asyncio
import aiohttp
import json
import ssl # 用于处理可能的SSL证书问题
from multidict import CIMultiDict, MultiDict # aiohttp 使用 multidict

# --- 1. 核心配置 (请根据您的 Moodle 环境修改) ---
MOODLE_URL = 'https://learn.turcar.net.cn'       # 你的 Moodle 网址
TOKEN = 'e37b279206e60c6e48c3fc08437dc631'     # 你的 Web Service 令牌
SERVICE_URL = f'{MOODLE_URL}/webservice/rest/server.php'


# --- Moodle API 响应错误结构 ---
def is_moodle_error(response_data):
    """检查 Moodle API 的响应是否包含错误信息"""
    return (isinstance(response_data, dict) and
            ('exception' in response_data or 'error' in response_data))

def encode_moodle_params(kwargs):
    """
    将 Python 的 kwargs（可能包含列表和字典）编码成 Moodle Web Services
    所期望的 form-urlencoded 格式。
    例如: {'users': [{'username': 'u1', 'email': 'e1'}]}
    会编码成: {'users[0][username]': 'u1', 'users[0][email]': 'e1'}
    """
    encoded_params = {}
    
    def flatten_dict(d, prefix=""):
        if isinstance(d, dict):
            for k, v in d.items():
                new_prefix = f"{prefix}[{k}]" if prefix else k
                flatten_dict(v, new_prefix)
        elif isinstance(d, list):
            for i, item in enumerate(d):
                new_prefix = f"{prefix}[{i}]" if prefix else str(i)
                flatten_dict(item, new_prefix)
        else:
            encoded_params[prefix] = str(d) # 确保所有值都转为字符串

    for key, value in kwargs.items():
        flatten_dict(value, key)
        
    return encoded_params


async def call_moodle_api(session: aiohttp.ClientSession, function_name: str, **kwargs):
    """
    一个通用的、异步的 Moodle API 调用函数。
    """
    # 构建请求参数
    base_params = {
        'wstoken': TOKEN,
        'wsfunction': function_name,
        'moodlewsrestformat': 'json'
    }

    # 使用 encode_moodle_params 来处理嵌套的 kwargs
    # 注意：local_mobile_get_autologin_key 通常不需要其他参数，
    # 它依赖于调用它的用户的会话/令牌。
    encoded_kwargs = encode_moodle_params(kwargs)
    
    # 合并 base_params 和编码后的 kwargs
    final_params = base_params.copy()
    final_params.update(encoded_kwargs)

    try:
        async with session.post(SERVICE_URL, data=final_params) as response:
            response.raise_for_status()

            try:
                result = await response.json(content_type=None)
            except aiohttp.ContentTypeError:
                print(f"Moodle API ({function_name}) 返回了非 JSON 格式的响应 (Content-Type: {response.content_type})。")
                raw_text = await response.text()
                print(f"原始响应:\n{raw_text}")
                return None
            except json.JSONDecodeError:
                print(f"Moodle API ({function_name}) 响应无法解码为 JSON。")
                raw_text = await response.text()
                print(f"原始响应:\n{raw_text}")
                return None

            if is_moodle_error(result):
                error_details = result.get('error', {})
                if 'message' in error_details:
                    print(f"Moodle API ({function_name}) 返回错误:")
                    print(f"  消息: {error_details.get('message')}")
                    if 'debuginfo' in error_details:
                        print(f"  详细信息: {error_details.get('debuginfo')}")
                else: # 兼容旧版本 Moodle 的错误格式
                    print(f"Moodle API ({function_name}) 返回错误:")
                    print(f"  异常: {result.get('exception')}")
                    print(f"  错误码: {result.get('errorcode')}")
                    print(f"  消息: {result.get('message')}")
                return None
            
            return result

    except aiohttp.ClientConnectorError as e:
        print(f"连接到 Moodle ({MOODLE_URL}) 时发生错误: {e}")
        return None
    except aiohttp.ClientResponseError as e:
        print(f"HTTP 响应错误: 状态 {e.status}, 原因 {e.message}")
        print(f"URL: {e.request_info.url}")
        # 在这里我们可以尝试打印响应体，如果响应对象可用
        try:
            # 尝试获取响应文本，但注意此时response可能不是一个有效的对象
            # 如果你想更健壮，可以在 try块中定义 response 对象
            pass 
        except Exception:
            pass 
        return None
    except asyncio.TimeoutError:
        print(f"请求 Moodle API ({function_name}) 超时。")
        return None
    except Exception as e:
        print(f"调用 Moodle API ({function_name}) 时发生未知错误: {e}")
        return None


# --- 新增函数来调用 local_mobile_get_autologin_key ---
async def api_get_autologin_key(session: aiohttp.ClientSession, privatetoken: str = None):
    """
    异步获取 Moodle 移动应用的自动登录密钥。
    这个函数不接收额外参数，它依赖于调用时使用的 TOKEN 进行身份验证。
    """
    print("\n--- 目标操作: 正在获取 Moodle 自动登录密钥 (autologin_key) ---")
    
    # local_mobile_get_autologin_key 是 Moodle 的一个核心 Web 服务函数
    # 它不需要额外的参数，因为它依赖于传入的 wstoken 来识别用户
    autologin_key_data = await call_moodle_api(
        session,
        'tool_mobile_get_autologin_key',
        privatetoken=privatetoken
    )

    if autologin_key_data is None:
        print("!!! 错误: 获取自动登录密钥时发生未知错误。\n")
        return None
    
    # autologin_key_data 的结构通常是 {'key': 'your_autologin_key'}
    if 'key' in autologin_key_data:
        print(f"✅ 成功获取自动登录密钥: {autologin_key_data['key'][:10]}... (长度: {len(autologin_key_data['key'])})")
        return autologin_key_data['key']
    else:
        print("❌ 响应格式不包含 'key' 字段，无法提取自动登录密钥。")
        print(f"原始响应: {autologin_key_data}\n")
        return None


# --- 以下函数保持不变，只是确保它们调用了修改后的 call_moodle_api ---
async def api_get_users_by_username(session: aiohttp.ClientSession, usernames: list):
    """
    异步通过用户名列表获取 Moodle 用户信息。
    """
    if not usernames:
        print("未提供要查询的用户名列表。")
        return []

    print(f"\n--- 目标操作: 正在通过用户名列表 {usernames} 获取账号信息 ---\n")

    users_data = await call_moodle_api(
        session,
        'core_user_get_users_by_field',
        field='username',
        values=usernames
    )

    if users_data is None:
        print(f"!!! 错误: 在查询用户名列表 {usernames} 时发生未知错误。\n")
        return None

    if not users_data:
        print(f"未找到任何用户名在 {usernames} 中的用户。\n")
        return []

    print(f"✅ 成功获取到 {len(users_data)} 个用户的部分信息。")
    for user_info in users_data:
        print(f"  找到用户: '{user_info.get('username')}' (ID: {user_info.get('id')})")
    print("")
    return users_data

async def api_create_users(session: aiohttp.ClientSession, users_to_create: list):
    """
    异步批量创建 Moodle 用户。
    """
    if not users_to_create:
        return []

    print(f"\n--- 目标操作: 正在批量创建用户 ---")
    # 将 users_to_create 列表直接作为 'users' 参数的值传递
    # call_moodle_api 中的 encode_moodle_params 会处理好嵌套结构
    creation_results = await call_moodle_api(
        session,
        'core_user_create_users',
        users=users_to_create
    )

    if creation_results is None:
        # call_moodle_api 内部已经打印了错误信息
        return None

    successful_creations = 0
    failed_creations = 0
    if isinstance(creation_results, list):
        for user_info in creation_results:
            if 'id' in user_info and 'username' in user_info:
                print(f"  ✅ 成功创建: 用户名 '{user_info['username']}' (ID: {user_info['id']})")
                successful_creations += 1
            else:
                # 即使在列表中，也可能存在错误条目
                print(f"  ❌ 创建失败或响应格式异常: {user_info}")
                failed_creations += 1
        print(f"\n✅ 用户创建完成。成功: {successful_creations}, 失败: {failed_creations}")
    else:
        print(f"  ❌ 批量创建返回了非预期的格式: {creation_results}")
        failed_creations = len(users_to_create)
        print(f"\n❌ 用户创建失败。总计: {failed_creations}")
    print("")
    return creation_results

# --- 主执行函数 ---
async def main():
    # 忽略 SSL 证书验证警告 (如果 Moodle 的 SSL 证书有问题，可以加上这行)
    # 注意：在生产环境中，建议正确配置 SSL 证书，而不是禁用验证。
    # ssl_context = ssl.create_default_context()
    # ssl_context.check_hostname = False
    # ssl_context.verify_mode = ssl.CERT_NONE

    # async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
    
    async with aiohttp.ClientSession() as session: # 默认情况下使用系统 SSL 上下文
        
        # --- 示例 1: 获取自动登录密钥 ---
        autologin_key = await api_get_autologin_key(session)
        # 可以在这里存储 autologin_key 以备后续使用

        # --- 示例 2: 批量创建用户 (保持原样) ---
        # users_to_create_data = [
        #     {
        #         "username": "asyncuser001",
        #         "password": "ComplexPassword123!",
        #         "firstname": "Async",
        #         "lastname": "UserOne",
        #         "email": "asyncuser001@example.com",
        #         "auth": "manual", # 手动认证
        #         "idnumber": "ASYNC-001",
        #         "city": "Nanjing",
        #         "country": "CN",
        #         "lang": "zh_cn",
        #         "timezone": "Asia/Shanghai",
        #         "mailformat": 1 # 1 for HTML
        #     }
        # ]
        # await api_create_users(session, users_to_create_data)

        # --- 示例 3: 获取用户信息 (原样，可取消注释测试) ---
        # usernames_to_fetch = ["admin", "testuser1"] # 请替换为 Moodle 中存在的用户名
        # await api_get_users_by_username(session, usernames_to_fetch)


if __name__ == "__main__":
    asyncio.run(main())
