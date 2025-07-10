import { getData } from "./request";

export const APIUserInfo = async (data) => {
    const response = await getData("https://learn.turcar.net.cn/fontend_getusername.php");
    // console.log(data.data);
    return response.data;
}

export const APILogin = (data) => getData("/api/login", data);

export const APIRegister = (data) => getData("/api/register", data);

export const APIForgotPassword = (data) => getData("/api/forgotpassword", data);

export const APIChatSessions = async () => getData("/api/chat_sessions")

export const APIChatHistory = async (data) => getData("/api/chat_history", data)

export const APIChatNewSession = async (data) => getData("/api/chat_newsession", data)

export const APIChatNewMessage = async (data) => getData("/api/chat_newmessage", data)