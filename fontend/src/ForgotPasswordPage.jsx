import { useState, useEffect, useRef } from "react";
import axios from "axios";

// 假设这些是你的共享组件，我们继续使用它们保持风格统一
import TDSBg from "./components/TDSBg";
import TDSHeader from "./components/TDSHeader";
import TDSFooter from "./components/TDSFooter";

function ForgotPasswordPage() {
  // 使用 state 来管理表单输入、错误信息和各种加载状态
  const [phoneNumber, setPhoneNumber] = useState("");
  const [verificationCode, setVerificationCode] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [error, setError] = useState(null);

  // 主提交按钮的加载状态
  const [isLoading, setIsLoading] = useState(false);
  // 获取验证码按钮的加载状态
  const [isSendingCode, setIsSendingCode] = useState(false);
  // 倒计时状态
  const [countdown, setCountdown] = useState(0);
  const timerRef = useRef(null);

  // 组件卸载时清除定时器，防止内存泄漏
  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  // --- 获取验证码的处理函数 ---
  const handleGetCode = async () => {
    // 简单的前端手机号校验
    if (!phoneNumber || !/^1[3-9]\d{9}$/.test(phoneNumber)) {
      setError("请输入有效的11位手机号码。");
      return;
    }

    setError(null);
    setIsSendingCode(true);

    try {
      // --- 使用 Axios 发送获取验证码的请求 ---
      // 请将 '/api/v1/send-verification-code' 替换成你真实的API接口
      await axios.post("/api/v1/send-verification-code", {
        phoneNumber: phoneNumber,
      });

      // 发送成功后开始倒计时
      setIsSendingCode(false);
      setCountdown(60);
      timerRef.current = setInterval(() => {
        setCountdown((prev) => {
          if (prev <= 1) {
            clearInterval(timerRef.current);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    } catch (err) {
      setIsSendingCode(false);
      console.error("验证码发送失败:", err);
      setError(err.response?.data?.message || "验证码发送失败，请稍后再试。");
    }
  };

  // --- 表单提交处理函数 ---
  const handleResetSubmit = async (event) => {
    event.preventDefault(); // 阻止表单默认的刷新页面的行为
    setError(null); // 重置错误信息
    setIsLoading(true); // 开始加载

    try {
      // --- 使用 Axios 发送重置密码的请求 ---
      // 请将 '/api/v1/reset-password' 替换成你真实的API接口
      const response = await axios.post("/api/v1/reset-password", {
        phoneNumber: phoneNumber,
        code: verificationCode,
        newPassword: newPassword,
      });

      // 重置成功
      console.log("密码重置成功:", response.data);
      setIsLoading(false);

      // 密码重置成功后的操作，例如提示用户并跳转到登录页
      alert("密码重置成功！请使用新密码登录。");
      window.location.href = "/login"; // 跳转到登录页
    } catch (err) {
      // 重置失败
      console.error("密码重置失败:", err);
      setIsLoading(false);

      // 根据后端返回的错误信息设置友好的提示
      if (err.response) {
        setError(err.response.data.message || "信息填写有误，请检查后重试。");
      } else if (err.request) {
        setError("无法连接到服务器，请检查你的网络。");
      } else {
        setError("发生未知错误，请稍后再试。");
      }
    }
  };

  return (
    <>
      <TDSBg />
      <TDSHeader />
      <main
        className="relative flex items-center justify-center px-4 z-10"
        style={{ minHeight: "calc(100vh - 216px)" }}
      >
        <div className="container mx-auto grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
          {/* 左侧内容 - 欢迎语 */}
          <div className="text-left text-black hidden md:block">
            <h1 className="text-5xl lg:text-6xl font-bold leading-tight">
              忘记密码？
            </h1>
            <p className="mt-4 text-xl text-black/80">
              别担心，我们来帮你找回账户。
            </p>
          </div>

          {/* 右侧内容 - 重置密码表单 */}
          <div className="w-full max-w-md mx-auto md:mx-0 md:justify-self-end">
            <form
              onSubmit={handleResetSubmit}
              className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-2xl p-8 space-y-6"
            >
              <h2 className="text-3xl font-bold text-center text-gray-800">
                重置密码
              </h2>

              {/* 手机号输入 */}
              <div>
                <label
                  htmlFor="phoneNumber"
                  className="text-sm font-medium text-gray-700"
                >
                  手机号码
                </label>
                <input
                  id="phoneNumber"
                  type="tel"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                  required
                  className="mt-1 block w-full px-4 py-3 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  placeholder="请输入注册时使用的手机号"
                />
              </div>

              {/* 验证码输入 */}
              <div>
                <label
                  htmlFor="verificationCode"
                  className="text-sm font-medium text-gray-700"
                >
                  验证码
                </label>
                <div className="mt-1 flex items-center space-x-2">
                  <input
                    id="verificationCode"
                    type="text"
                    value={verificationCode}
                    onChange={(e) => setVerificationCode(e.target.value)}
                    required
                    className="block w-full px-4 py-3 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                    placeholder="请输入6位验证码"
                  />
                  <button
                    type="button"
                    onClick={handleGetCode}
                    disabled={isSendingCode || countdown > 0}
                    className="flex-shrink-0 px-4 py-3 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition-all duration-300"
                  >
                    {isSendingCode
                      ? "发送中..."
                      : countdown > 0
                      ? `${countdown}s 后重试`
                      : "获取验证码"}
                  </button>
                </div>
              </div>

              {/* 新密码输入 */}
              <div>
                <label
                  htmlFor="newPassword"
                  className="text-sm font-medium text-gray-700"
                >
                  新密码
                </label>
                <input
                  id="newPassword"
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  required
                  className="mt-1 block w-full px-4 py-3 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  placeholder="请输入您的新密码"
                />
              </div>

              {/* 错误信息提示 */}
              {error && (
                <div className="text-sm text-red-600 bg-red-100 p-3 rounded-md">
                  {error}
                </div>
              )}

              {/* 确认重置按钮 */}
              <div>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full flex justify-center py-3 px-4 border border-transparent rounded-full shadow-lg text-lg font-medium text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition-all duration-300"
                >
                  {isLoading ? "正在重置..." : "确认重置"}
                </button>
              </div>

              {/* 其他链接 */}
              <div className="text-center text-sm text-gray-600">
                <a
                  href="/login"
                  className="font-medium text-teal-600 hover:text-teal-500"
                >
                  返回登录
                </a>
              </div>
            </form>
          </div>
        </div>
      </main>
      <TDSFooter />
    </>
  );
}

export default ForgotPasswordPage;
