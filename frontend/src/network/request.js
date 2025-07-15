import axios from "axios";

// 网络请求实例
const request = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:3000",
    withCredentials: true,
    headers: {
        "Content-Type": "application/json"
    },
    responseType: "json",
});

// 网络请求封装
export const getData = (url, data) => {
    let token = localStorage.getItem("token");

    return request.post(
        url,
        data,
        {
            headers: {
                "Authorization": token ? "bearer " + token : null
            }
        }
    ).then(response => response.data);
};
