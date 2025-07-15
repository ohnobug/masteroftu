import { APIUserInfo } from "./network/api.js";
import { useDispatch } from "react-redux";
import { setUserinfo } from "./store/userSlice";

export const useFetchUserInfo = () => {
  if (localStorage.getItem("token") === null) return () => {};

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

