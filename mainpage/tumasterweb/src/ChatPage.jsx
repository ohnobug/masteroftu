import React, { useState } from "react"; // 引入 useState Hook
import TDSBg from "./components/TDSBg";
import TDSHeader from "./components/TDSHeader";
import TDSFooter from "./components/TDSFooter";

// 示例会话数据
const initialSessions = [
  { id: "1", title: "关于React组件的问题" },
  { id: "2", title: "解释机器学习概念" },
  { id: "3", title: "推荐一部科幻电影" },
];

// 示例聊天消息数据
const initialMessages = [
  { id: 1, text: "你好，有什么可以帮助你的吗？", sender: "ai" },
  { id: 2, text: "我想了解一下React Hooks。", sender: "user" },
  { id: 3, text: "好的，React Hooks 是什么... [AI的回答]", sender: "ai" },
  { id: 4, text: "谢谢！", sender: "user" },
];

function ChatPage() {
  const [sessions, setSessions] = useState(initialSessions);
  const [messages, setMessages] = useState(initialMessages); // 当前会话的消息
  const [input, setInput] = useState(""); // 输入框内容
  const [currentSessionId, setCurrentSessionId] = useState(
    initialSessions[0]?.id || null
  ); // 当前选中的会话ID

  // 处理输入框变化
  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  // 处理发送消息
  const handleSendMessage = () => {
    if (input.trim()) {
      const newMessage = {
        id: messages.length + 1, // 简单的ID生成
        text: input,
        sender: "user",
      };
      // 模拟发送后AI回复
      const aiResponse = {
        id: messages.length + 2,
        text: `（模拟AI回复）你问的是：“${input}”`,
        sender: "ai",
      };
      setMessages([...messages, newMessage, aiResponse]); // 添加用户消息和模拟AI回复
      setInput(""); // 清空输入框
      // TODO: 在实际应用中，这里需要调用API发送消息到后端AI服务，并处理AI的真实回复
    }
  };

  // 切换会话 (这里只是一个占位符，实际切换需要加载对应会话的消息)
  const handleSessionClick = (sessionId) => {
    setCurrentSessionId(sessionId);
    // TODO: 在实际应用中，根据sessionId加载对应的消息数据
    console.log(`切换到会话: ${sessionId}`);
    // 为了演示，这里可以清空或加载特定会话的消息
    // setMessages(loadMessagesForSession(sessionId));
  };

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
          <h2 className="text-lg font-semibold mb-4 text-black">会话记录</h2>
          <ul>
            {sessions.map((session) => (
              <li
                key={session.id}
                className={`cursor-pointer p-2 rounded-md mb-2 transition-colors ${
                  currentSessionId === session.id
                    ? "bg-blue-500 text-white"
                    : "bg-gray-100 hover:bg-gray-200 text-black"
                }`}
                onClick={() => handleSessionClick(session.id)}
              >
                {session.title}
              </li>
            ))}
          </ul>
          {/* 可以添加新建会话按钮等 */}
          {/* <button className="mt-auto w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition-colors">新建会话</button> */}
        </div>

        {/* 右侧：聊天区域 */}
        <div className="flex-1 bg-white/90 rounded-lg flex flex-col shadow-lg overflow-hidden">
          {/* 消息显示区域 */}
          <div className="flex-1 p-4 overflow-y-auto flex flex-col-reverse">
            {/* 使用 flex-col-reverse 让最新的消息在底部，滚动向上 */}
            {messages
              .slice()
              .reverse()
              .map(
                (
                  message // reverse() 用于配合 flex-col-reverse
                ) => (
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
                )
              )}
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
              onChange={handleInputChange}
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
      </main>
    </>
  );
}

export default ChatPage;
