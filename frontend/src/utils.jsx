import { APIUserInfo } from "./network/api.js";
import { useDispatch } from "react-redux";
import { setUserinfo } from "./store/userSlice";

// 获取用户信息
export const useFetchUserInfo = () => {
  if (localStorage.getItem("token") === null) return () => { };

  const dispatch = useDispatch();

  return async () => {
    try {
      const data = await APIUserInfo();
      dispatch(setUserinfo(data.data));
    } catch (error) {
      console.info(error?.response?.data?.message || '用户尚未登录');
    }
  };
}

// 检测用户是否登录
export const checkIsLogin = () => {
  return localStorage.getItem("token") !== null;
}
