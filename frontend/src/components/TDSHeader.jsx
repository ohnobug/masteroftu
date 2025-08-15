import { useEffect, useRef } from "react";
import { useSelector, useDispatch } from "react-redux";
import { NavLink, useLocation, useNavigate } from "react-router-dom";
import { setUserinfo } from "../store/userSlice";

const TDSHeader = () => {
  const location = useLocation();
  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
  }, [location]);


  const logout = () => {
    dispatch(setUserinfo(null));
    localStorage.removeItem("token");

    if (['/chat'].includes(location.pathname)) {
      navigate('/');
    }
  };

  const inactive = useRef(
    [
      "text-black/80",
      "hover:text-black",
      "font-medium",
      "transition-colors",
    ].join(" ")
  );

  const active = useRef(
    ["text-black", "font-semibold", "transition-colors"].join(" ")
  );

  const userinfo = useSelector((state) => {
    return state.user.userinfo;
  });

  return (
    <header className="sticky top-0 left-0 right-0 p-6 z-40 bg-white/50 backdrop-blur-lg shadow-sm">
      <nav className="flex justify-between items-center max-w-screen-xl mx-auto">
        <div className="flex items-center">
          <div className="flex items-center gap-3">
            <span className="text-black text-lg font-medium">图克教育</span>
            <span className="text-black/70 text-xs font-medium border border-black/30 rounded-full px-3 py-1">
              实验性
            </span>
          </div>
          <div className="hidden md:flex items-center gap-8 ml-10">
            <NavLink
              to="/"
              className={({ isActive, isPending }) =>
                isActive ? active.current : inactive.current
              }
            >
              首页
            </NavLink>

            <NavLink
              to="/chat"
              className={({ isActive, isPending }) =>
                isActive ? active.current : inactive.current
              }
            >
              对话
            </NavLink>

            <NavLink
              to="/course"
              className={({ isActive, isPending }) =>
                isActive ? active.current : inactive.current
              }
            >
              课程分类
            </NavLink>

            <NavLink
              to="/learning_paths"
              className={({ isActive, isPending }) =>
                isActive ? active.current : inactive.current
              }
            >
              学习路径
            </NavLink>

            <NavLink
              to="/about"
              className={({ isActive, isPending }) =>
                isActive ? active.current : inactive.current
              }
            >
              关于我们
            </NavLink>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div
            onClick={() => {
              // window.location.href = "https://learn.turcar.net.cn";
            }}
            style={{ cursor: "pointer" }}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6 text-black/80"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth="1.5"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"
              />
            </svg>
          </div>

          {userinfo ? (
            <div
              // to="/login"
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "10px",
              }}
            >
              <img
                src={
                  "https://img2.baidu.com/it/u=3149121010,3733367959&fm=253&app=138&f=JPEG?w=500&h=500"
                }
                alt="User profile"
                className="w-9 h-9 rounded-full"
              />
              <span>{userinfo?.phone_number}</span>
              <span className="cursor-pointer" onClick={() => logout()}>
                退出
              </span>
            </div>
          ) : (
            <NavLink
              to="/login"
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "10px",
              }}
            >
              <img
                src="/images/user.png"
                alt="User profile"
                className="w-9 h-9 rounded-full"
              />
            </NavLink>
          )}
        </div>
      </nav>
    </header>
  );
};

export default TDSHeader;
