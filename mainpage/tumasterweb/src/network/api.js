import { getData } from "./request";

export const APIUserInfo = async (data) => {
    const response = await getData("https://learn.turcar.net.cn/fontend_getusername.php");
    // console.log(data.data);
    return response.data;
}

export const APILogin = (data) => getData("/api/login", data);

export const APIRegister = (data) => getData("/api/register", data);

export const APIForgotPassword = (data) => getData("/api/forgotpassword", data);
