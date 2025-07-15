import { getData } from "./request";

// 获取用户信息
export const APIUserInfo = () => getData('/api/userinfo')

// 用户登录
export const APILogin = (data) => getData("/api/login", data);

// 用户注册
export const APIRegister = (data) => getData("/api/register", data);

// 重置密码
export const APIResetPassword = (data) => getData("/api/reset_password", data);

// 获取验证码
export const APIGetVerifyCode = (data) => getData("/api/get_verify_code", data);

// 获取聊天会话列表
export const APIChatSessions = async () => getData("/api/chat_sessions")

// 获取聊天历史记录
export const APIChatHistory = async (data) => getData("/api/chat_history", data)

// 创建新的聊天会话
export const APIChatNewSession = async (data) => getData("/api/chat_newsession", data)

// 发送新消息
export const APIChatNewMessage = async (data) => getData("/api/chat_newmessage", data)

// 删除消息
export const APIChatDelMessage = async (data) => getData("/api/chat_delsession", data)

