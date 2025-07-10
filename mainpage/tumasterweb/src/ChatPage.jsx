import React, { useEffect, useState } from "react"; // 引入 useState Hook
import TDSBg from "./components/TDSBg";
import TDSHeader from "./components/TDSHeader";
import {
  APIChatHistory,
  APIChatSessions,
  APIChatNewSession,
  APIChatNewMessage,
} from "./network/api";
import { useDispatch, useSelector } from "react-redux";
import { setChatSessions, setCurrentChatId } from "./store/chatSlice";
import socket from "./network/ws";

function ChatPage() {
  const chatSessions = useSelector((state) => state.chat.chatSessions);
  const currentChatId = useSelector((state) => state.chat.currentChatId);
  const dispatch = useDispatch();

  const [input, setInput] = useState(""); // 输入框内容

  // 处理发送消息
  const handleSendMessage = async () => {
    if (input.trim()) {
      const data = await APIChatNewMessage({
        chat_session_id: currentChatId,
        text: input.trim(),
      });

      if (data.code != 200) {
        alert(data.message);
        return;
      }

      // 获取最新消息列表
      fetchChatHistory(currentChatId);

      socket.emit("get_text", {
        ai_message_id: data.data.ai_message_id,
        chat_session_id: currentChatId,
      });

      setInput("");
    }
  };

  // 切换会话 (这里只是一个占位符，实际切换需要加载对应会话的消息)
  const handleSessionClick = (sessionId) => {
    dispatch(setCurrentChatId(sessionId));
  };

  const fetchSession = async () => {
    const data = await APIChatSessions();

    if (data.code != 200) {
      alert(data.message);
      return;
    }

    dispatch(setChatSessions(data.data));
  };

  const fetchChatHistory = async (id) => {
    const data = await APIChatHistory({
      chat_session_id: id,
    });

    if (data.code != 200) {
      alert(data.message);
      return;
    }

    let newChat = JSON.parse(JSON.stringify(chatSessions));
    newChat[id].messages = data.data;

    dispatch(setChatSessions(newChat));
  };

  const fetchNewSession = async (text) => {
    const data = await APIChatNewSession({
      text: text,
    });

    if (data.code != 200) {
      alert(data.message);
      return;
    }

    await fetchSession();
    dispatch(setCurrentChatId(data.data["chat_session_id"]));
  };

  useEffect(() => {
    fetchSession();
  }, []);

  useEffect(() => {
    if (currentChatId != -1) {
      fetchChatHistory(currentChatId);
    }
  }, [currentChatId]);

  const [inputStr, setInputStr] = useState("");

  return (
    <>
      {/* 背景图片和渐变叠加层 */}
      <TDSBg />

      {/* 顶部导航栏 */}
      <TDSHeader />

      {/* 主要内容区域：AI聊天界面 */}
      {/* 使用 flex 布局将左右两部分排列，h-[calc(100vh - ...)] 计算占据除去Header和Footer的高度 */}
      {/* 假设Header和Footer总高约216px，如果实际高度不同，需要调整此处的计算 */}
      <main
        className="relative flex z-10 p-4"
        style={{
          minHeight: "calc(100vh - 90px)",
          height: "calc(100vh - 90px)",
        }}
      >
        {/* 左侧：会话列表 */}
        <div className="w-64 bg-white/80 rounded-lg p-4 mr-4 flex flex-col shadow-lg overflow-y-auto">
          <button
            className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition-colors mb-3"
            onClick={() => {
              dispatch(setCurrentChatId(-1));
            }}
          >
            新建会话
          </button>

          <h2 className="text-lg font-semibold mb-4 text-black">会话记录</h2>
          <ul>
            {Object.values(chatSessions).map((session) => (
              <li
                key={session.id}
                className={`cursor-pointer p-2 rounded-md mb-2 transition-colors ${
                  currentChatId === session.id
                    ? "bg-blue-500 text-white"
                    : "bg-gray-100 hover:bg-gray-200 text-black"
                }`}
                style={{
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                  wordBreak: "keep-all",
                }}
                onClick={() => handleSessionClick(session.id)}
              >
                {session.title}
              </li>
            ))}
          </ul>
        </div>

        {/* 右侧：聊天区域 */}
        {currentChatId == -1 ? (
          <main className="flex-1 bg-white/90 rounded-lg flex flex-col shadow-lg overflow-hidden justify-center">
            <div className="flex flex-col items-center gap-6 text-center w-full">
              <h1 className="text-black text-6xl md:text-7xl font-bold">
                Learn About
              </h1>

              {/* 搜索输入框 */}
              <div className="relative w-full max-w-xl mt-2">
                <input
                  type="text"
                  placeholder="请输入你的问题"
                  onChange={(v) => {
                    setInputStr(v.target.value);
                  }}
                  onKeyDown={(v) => {
                    if (v.key == "Enter") {
                      fetchNewSession(inputStr);
                    }
                  }}
                  className="blinking-cursor w-full bg-white rounded-full py-4 pl-8 pr-16 text-lg text-black placeholder-gray shadow-lg focus:outline-none focus:ring-2 focus:ring-teal-400 transition-all duration-300"
                />
                {/* 发送图标 */}
                <button
                  className="absolute right-3 top-1/2 -translate-y-1/2 p-2.5 text-gray-400 hover:text-black transition-colors"
                  onClick={() => {
                    fetchNewSession(inputStr);
                  }}
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-6 w-6"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
                  </svg>
                </button>
              </div>

              {/* 描述文本 */}
              <div className="text-black/90 max-w-lg text-lg font-normal mt-2">
                <div>让好奇心，成为你的向导</div>
                <span className="inline-flex items-center">
                  <strong className="font-semibold">你的专属AI学习伙伴</strong>
                </span>
                <div>有什么想知道的？现在就问我吧！</div>
              </div>
            </div>
          </main>
        ) : (
          <div className="flex-1 bg-white/90 rounded-lg flex flex-col shadow-lg overflow-hidden">
            {/* 消息显示区域 */}
            <div className="flex-1 p-4 overflow-y-auto flex flex-col-reverse">
              {/* 使用 flex-col-reverse 让最新的消息在底部，滚动向上 */}
              {chatSessions[currentChatId]?.messages
                ? Object.values(chatSessions[currentChatId].messages)
                    .sort((a, b) => b.id - a.id)
                    .map((message) => (
                      <div
                        key={message.id}
                        className={`flex mb-4 ${
                          message.sender === "user"
                            ? "justify-end"
                            : "justify-start"
                        }`}
                      >
                        <div
                          className={`max-w-[70%] p-3 rounded-lg ${
                            message.sender === "user"
                              ? "bg-blue-500 text-white rounded-br-none"
                              : "bg-gray-200 text-black rounded-bl-none"
                          }`}
                        >
                          {message.text}
                        </div>
                      </div>
                    ))
                : null}
              {/* Spacer to prevent content from hiding under the input bar */}
              <div className="pb-20"></div> {/* Adjust padding as needed */}
            </div>

            {/* 聊天输入区域 */}
            <div className="p-4 border-t border-gray-200 flex items-center bg-white">
              <input
                type="text"
                placeholder="请输入你的问题..."
                className="flex-1 rounded-full py-2 px-4 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") handleSendMessage();
                }} // 按回车发送
              />
              <button
                onClick={handleSendMessage}
                className="ml-2 p-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={!input.trim()} // 输入为空时禁用按钮
              >
                {/* 发送图标 */}
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-6 w-6"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                >
                  <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
                </svg>
              </button>
            </div>
          </div>
        )}
      </main>
    </>
  );
}

export default ChatPage;
