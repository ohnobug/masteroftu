import { Outlet } from "react-router";
import { useEffect } from "react";
import { APIUserInfo } from "./network/api.js";
import { useDispatch } from "react-redux";
import { setUserinfo } from "./store/userSlice";

const App = () => {
  const dispatch = useDispatch();

  const fetchUserInfo = async () => {
    const data = await APIUserInfo();
    dispatch(setUserinfo(data.data));
  };

  useEffect(() => {
    fetchUserInfo();
  }, []);

  return (
    <>
      <Outlet />
    </>
  );
};

export default App;
