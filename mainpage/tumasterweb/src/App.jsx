import { Outlet } from "react-router";
import { useEffect } from "react";
import { APIUserInfo } from "./network/api.js";
import { useDispatch } from "react-redux";
import { setUserinfo } from "./store/userSlice";
import "./network/ws.js"

const App = () => {
  const dispatch = useDispatch();

  const fetchData = async () => {
    const data = await APIUserInfo();
    console.log("User Info:", data);
    if (data.userinfo) {
      dispatch(setUserinfo(data.userinfo));
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <>
      <Outlet />
    </>
  );
};

export default App;
