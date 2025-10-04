// src/api/index.js

import axios from 'axios';

// 假设你有一个消息提示组件，例如 antd 的 message
// import { message } from 'antd'; 
// 如果没有，可以用 alert 或者自定义的提示组件
const showMessage = (msg) => alert(msg);


// 1. 创建 Axios 实例
const service = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api', // 使用 /api 前缀，方便本地开发时配置代理
    timeout: 15000,
});

// 2. 请求拦截器 (Request Interceptor)
service.interceptors.request.use(
    (config) => {
        // a. 在发送请求前做什么
        //    比如，从 localStorage 获取 token
        const token = localStorage.getItem('authToken');
        if (token) {
            // b. 让每个请求都携带自定义 token
            //    请根据实际情况修改 'Authorization' 的格式，例如 'Bearer ' + token
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        // 对请求错误做些什么
        console.error('Request Error:', error); // for debug
        return Promise.reject(error);
    }
);

// 3. 响应拦截器 (Response Interceptor)
service.interceptors.response.use(
    (response) => {
        // a. 对响应数据做点什么
        //    后端通常会把数据包裹在一个 data 字段里，例如 { code: 200, message: 'success', data: { ... } }
        //    这里我们直接返回 `response.data`，简化后续操作
        const res = response.data;

        // b. 根据自定义 code 判断请求是否成功
        //    如果 code 不是 200 (或你和后端约定的成功码)，就抛出错误
        if (res.code !== 200) {
            // 可以在这里根据不同的 code 做不同的全局提示
            showMessage(res.message || 'Error');

            // 例如：50008: 非法的token; 50012: 其他客户端登录了; 50014: Token 过期了;
            if (res.code === 50008 || res.code === 50012 || res.code === 50014) {
                // 可以做一些登出操作，比如清除 token，跳转到登录页
                console.log('Token 无效或已过期，请重新登录');
                localStorage.removeItem('authToken');
                // window.location.href = '/login';
            }

            return Promise.reject(new Error(res.message || 'Error'));
        } else {
            // c. 如果成功，直接返回后端数据中的 `data` 部分
            return res.data;
        }
    },
    (error) => {
        // d. 处理 HTTP 网络错误
        console.error('Response Error:', error.message); // for debug

        let errorMessage = '网络请求发生错误，请稍后再试';
        if (error.response) {
            // 请求已发出，但服务器返回了状态码
            switch (error.response.status) {
                case 401:
                    errorMessage = '未授权，请登录';
                    // 执行登出操作
                    break;
                case 403:
                    errorMessage = '禁止访问';
                    break;
                case 404:
                    errorMessage = '请求的资源未找到';
                    break;
                case 500:
                    errorMessage = '服务器内部错误';
                    break;
                default:
                    errorMessage = `连接错误 ${error.response.status}`;
            }
        } else if (error.request) {
            // 请求已发出，但没有收到响应 (例如网络断开)
            errorMessage = '无法连接到服务器，请检查您的网络';
        }

        showMessage(errorMessage);
        return Promise.reject(error);
    }
);

export default service;