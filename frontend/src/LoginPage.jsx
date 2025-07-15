import { useState } from "react";
import TDSBg from "./components/TDSBg";
import TDSHeader from "./components/TDSHeader";
import TDSFooter from "./components/TDSFooter";
import { APILogin } from "./network/api";
import { useNavigate } from "react-router";
import { useFetchUserInfo } from "./utils"

function LoginPage() {
  // 使用 state 来管理表单输入、错误信息和加载状态
  const [phoneNumber, setPhoneNumber] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const fetchu = useFetchUserInfo();

  // 表单提交处理函数
  const handleSubmit = async (event) => {
    event.preventDefault(); // 阻止表单默认的刷新页面的行为
    setError(null); // 重置错误信息
    setIsLoading(true); // 开始加载

    try {
      const data = await APILogin({
        phone_number: phoneNumber,
        password: password,
      });

      localStorage.setItem("token", data.data.token);

      await fetchu().then(() => navigate("/chat"));
    } catch (error) {
      console.error(error);
      if (error?.response?.data) {
        setError(error?.response?.data?.message);
        setIsLoading(false);
      } else {
        setError("网络错误");
        setIsLoading(false);
      }
    }
  };

  return (
    <>
      {/* 背景图片和渐变叠加层 */}
      <TDSBg />

      {/* 顶部导航栏 */}
      <TDSHeader />

      {/* 主要内容 - 采用左右布局 */}
      <main
        className="relative flex items-center justify-center px-4 z-10"
        style={{ minHeight: "calc(100vh - 216px)" }}
      >
        <div className="container mx-auto grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
          {/* 左侧内容 - 欢迎语 */}
          <div className="text-left text-black hidden md:block">
            <h1 className="text-5xl lg:text-6xl font-bold leading-tight">
              欢迎回来
            </h1>
            <p className="mt-4 text-xl text-black/80">
              登录以继续你的 AI 学习之旅。
            </p>
          </div>

          {/* 右侧内容 - 登录表单 */}
          <div className="w-full max-w-md mx-auto md:mx-0 md:justify-self-end">
            <form
              onSubmit={handleSubmit}
              className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-2xl p-8 space-y-6"
            >
              <h2 className="text-3xl font-bold text-center text-gray-800">
                用户登录
              </h2>

              {/* 用户名输入 */}
              <div>
                <label
                  htmlFor="username"
                  className="text-sm font-medium text-gray-700"
                >
                  用户名
                </label>
                <input
                  id="username"
                  type="text"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                  required
                  className="mt-1 block w-full px-4 py-3 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  placeholder="请输入用户名或邮箱"
                />
              </div>

              {/* 密码输入 */}
              <div>
                <label
                  htmlFor="password"
                  className="text-sm font-medium text-gray-700"
                >
                  密码
                </label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="mt-1 block w-full px-4 py-3 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  placeholder="请输入密码"
                />
              </div>

              {/* 错误信息提示 */}
              {error && (
                <div className="text-sm text-red-600 bg-red-100 p-3 rounded-md">
                  {error}
                </div>
              )}

              {/* 登录按钮 */}
              <div>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full flex justify-center py-3 px-4 border border-transparent rounded-full shadow-lg text-lg font-medium text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition-all duration-300"
                >
                  {isLoading ? "正在登录..." : "立即登录"}
                </button>
              </div>

              {/* 其他链接 */}
              <div className="text-center text-sm text-gray-600">
                <a
                  href="/forgot_password"
                  className="font-medium text-teal-600 hover:text-teal-500"
                >
                  忘记密码?
                </a>
                <span className="mx-2">|</span>
                <a
                  href="/register"
                  className="font-medium text-teal-600 hover:text-teal-500"
                >
                  注册新账户
                </a>
              </div>
            </form>
          </div>
        </div>
      </main>

      {/* 页脚和备案号 */}
      <TDSFooter />
    </>
  );
}

export default LoginPage;
