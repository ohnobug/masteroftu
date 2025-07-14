import { getData } from "./request";

export const APIUserInfo = () => getData('/api/userinfo')

export const APILogin = (data) => getData("/api/login", data);

export const APIRegister = (data) => getData("/api/register", data);

export const APIForgotPassword = (data) => getData("/api/forgotpassword", data);

export const APIChatSessions = async () => getData("/api/chat_sessions")

export const APIChatHistory = async (data) => getData("/api/chat_history", data)

export const APIChatNewSession = async (data) => getData("/api/chat_newsession", data)

export const APIChatNewMessage = async (data) => getData("/api/chat_newmessage", data)

export const APIChatDelMessage = async (data) => getData("/api/chat_delsession", data)