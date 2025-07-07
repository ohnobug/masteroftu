import asyncio
import aiohttp

# --- 1. 核心配置 (请根据您的 Moodle 环境修改) ---
MOODLE_URL = 'https://learn.turcar.net.cn'       # 你的 Moodle 网址
TOKEN = 'e37b279206e60c6e48c3fc08437dc631'     # 你的 Web Service 令牌
SERVICE_URL = f'{MOODLE_URL}/webservice/rest/server.php'


async def call_moodle_api(function_name, **kwargs):
    """
    一个通用的、异步的 Moodle API 调用函数。

    :param session: aiohttp.ClientSession 对象，用于管理连接。
    :param function_name: 要调用的 Moodle Web Service 函数名。
    :param kwargs: 函数所需的参数，以关键字参数形式传入。
    :return: 解码后的 Moodle API 响应 (通常是字典或列表)，如果出错则返回 None。
    """
    print(f"--- 正在调用 API: {function_name} ---")

    # 构建请求参数
    params = {
        'wstoken': TOKEN,
        'wsfunction': function_name,
        'moodlewsrestformat': 'json'
    }

    # Moodle API 对列表和字典有特殊的编码要求 (如 list[0], list[1]...)
    # 这部分处理逻辑与同步版本相同
    processed_kwargs = {}
    for key, value in kwargs.items():
        if isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    for sub_key, sub_value in item.items():
                        processed_kwargs[f'{key}[{i}][{sub_key}]'] = sub_value
                else:
                    processed_kwargs[f'{key}[{i}]'] = item
        else:
            processed_kwargs[key] = value
            
    params.update(processed_kwargs)

    try:
        async with aiohttp.ClientSession() as session:
            # 使用传入的 session 发送异步 POST 请求
            async with session.post(SERVICE_URL, data=params) as response:
                response.raise_for_status()  # 如果HTTP状态码是 4xx/5xx, 抛出 ClientResponseError

                # 异步地读取和解析 JSON 响应
                # aiohttp 可能会抛出 aiohttp.ContentTypeError 而不是 ValueError
                result = await response.json(content_type=None) 

                # 检查 Moodle 返回的特定错误
                if isinstance(result, dict) and 'exception' in result:
                    print("Moodle API 返回错误:")
                    print(f"  异常: {result.get('exception')}")
                    print(f"  错误码: {result.get('errorcode')}")
                    print(f"  消息: {result.get('message')}")
                    return None
                return result
    except aiohttp.ClientError as e:
        print(f"网络或协议错误: {e}")
        return None
    except asyncio.TimeoutError:
        print("请求超时。")
        return None
    except Exception as e:
        # 捕获可能的 JSON 解析错误或其他未知错误
        print(f"发生未知错误: {e}")
        # 尝试打印原始文本以供调试
        try:
            print("原始响应文本:", await response.text())
        except:
            pass
        return None


async def api_get_user_by_username(username):
    """
    步骤：通过用户名异步获取 Moodle 用户信息。

    :param session: aiohttp.ClientSession 对象。
    :param username: 要查询的用户的用户名。
    :return: 包含用户信息的字典，如果找不到或失败则返回 None。
    """
    print(f"\n--- 目标操作: 正在通过用户名 '{username}' 获取账号信息 ---\n")
    
    users_data = await call_moodle_api(
        'core_user_get_users_by_field',
        field='username',
        values=[username]
    )

    if not users_data:
        print(f"!!! 错误: 获取用户信息失败或找不到用户 '{username}'。\n")
        return None

    user_info = users_data[0]
    print(f"✅ 成功获取到用户 '{username}' 的信息，用户ID为: {user_info['id']}\n")
    return user_info



# async def main():
#     """主执行协程函数"""

#     async with aiohttp.ClientSession() as session:
#         # --- 任务: 通过用户名获取账号信息 (单个、顺序执行) ---
#         target_username = 'lijunjie'
        
#         user_details = await api_get_user_by_username(session, target_username)


#         if user_details:
#             print("===== 用户详细信息 =====")
#             print(user_details)
#             # print(f"  ID: {user_details.get('id')}")
#             # print(f"  姓名: {user_details.get('fullname')}")
#             # print(f"  邮箱: {user_details.get('email')}")
#             print("========================\n")
#         else:
#             print(f"未能获取到用户 '{target_username}' 的信息。")


# if __name__ == '__main__':
#     asyncio.run(main())
