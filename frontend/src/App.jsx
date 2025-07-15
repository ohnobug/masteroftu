import { Outlet } from "react-router";
import { useEffect } from "react";
import { useFetchUserInfo } from "./utils"

const App = () => {
  const fetchu = useFetchUserInfo();

  useEffect(() => {
    fetchu();
  }, []);

  return (
    <>
      <Outlet />
    </>
  );
};

export default App;
