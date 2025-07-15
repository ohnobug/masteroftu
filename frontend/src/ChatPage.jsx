import { useEffect, useState, useRef } from "react"; // 引入 useState Hook
import TDSBg from "./components/TDSBg";
import TDSHeader from "./components/TDSHeader";
import {
  APIChatHistory,
  APIChatSessions,
  APIChatNewSession,
  APIChatNewMessage,
  APIChatDelMessage
} from "./network/api";
import { useDispatch, useSelector } from "react-redux";
import {
  setChatSessions,
  setCurrentChatId,
  setChatMessage,
  setTokenToMessage,
} from "./store/chatSlice";
import { checkIsLogin } from "./utils";
import markdownit from "markdown-it";
import MarkdownItHightlightJS from "markdown-it-highlightjs";
import "highlight.js/styles/github-dark.css";
import { useLocation, useNavigate } from "react-router-dom";
import io from "socket.io-client";
import { TDTextLoading } from "./components/TDTextLoading";


function ChatPage() {
  const navigate = useNavigate();
  const chatSessions = useSelector((state) => state.chat.chatSessions);
  const currentChatId = useSelector((state) => state.chat.currentChatId);
  const dispatch = useDispatch();

  const [input, setInput] = useState(""); // 输入框内容
  const [inputStr, setInputStr] = useState(""); // 大界面输入框
  const md = useRef(null); // markdownit实例
  const chataeraRef = useRef(null); // 对话记录界面
  const socket = useRef(null); // socket实例
  const inputRef = useRef(null);
  const bigInputRef = useRef(null);


  const newChatSession = async (input, chatId) => {
    if (input.trim()) {
      const data = await APIChatNewMessage({
        chat_session_id: chatId,
        text: input.trim(),
      });

      if (data.code != 200) {
        alert(data.message);
        return;
      }

      // 获取最新消息列表
      await fetchChatHistory(chatId);

      socket.current.emit("get_text", {
        ai_message_id: data.data.ai_message_id,
        chat_session_id: chatId,
      });

      setInput("");

      // 如果控件在，则按下回车滚动到最底部
      if (chataeraRef.current) {
        chataeraRef.current.scrollTop = chataeraRef.current.scrollHeight;
      }
    }
  };

  // 处理发送消息
  const handleSendMessage = async () => {
    newChatSession(input, currentChatId);
  };

  // 切换会话 (这里只是一个占位符，实际切换需要加载对应会话的消息)
  const handleSessionClick = async (sessionId) => {
    dispatch(setCurrentChatId(sessionId));
    await fetchChatHistory(sessionId);
  };

  // 获取会话列表
  const fetchSession = async () => {
    const data = await APIChatSessions();

    if (data.code != 200) {
      alert(data.message);
      return;
    }

    dispatch(setChatSessions(data.data));
    if (Object.keys(data.data).length == 0) {
      dispatch(setCurrentChatId(-1));
    }

    return data.data;
  };

  // 获取会话历史聊天
  const fetchChatHistory = async (id) => {
    const data = await APIChatHistory({
      chat_session_id: id,
    });

    if (data.code != 200) {
      alert(data.message);
      return;
    }

    dispatch(
      setChatMessage({
        chat_session_id: id,
        messages: data.data,
      })
    );

    return data.data;
  };

  // 删除会话
  const fetchDelSession = async (id) => {
    const data = await APIChatDelMessage({
      chat_session_id: id,
    });

    if (data.code != 200) {
      alert(data.message);
      return;
    }

    // 删除会话
    const entries = Object.entries(chatSessions);
    const filteredEntries = entries.filter(([key, value]) => {
      return key != id;
    })
    const finishedFilteredEntries = Object.fromEntries(filteredEntries)
    dispatch(setChatSessions(finishedFilteredEntries));

    let sortSession = Object.keys(finishedFilteredEntries).sort((a, b) => b - a);
    const chatLen = sortSession.length;

    // 如果剩下一个，那么这一个就是被选
    if (chatLen == 1) {
      await fetchChatHistory(sortSession[0]);
      dispatch(setCurrentChatId(sortSession[0]));
      return;
    } else if (chatLen == 0) {
      // 如果不剩会话，就切换到大屏
      dispatch(setCurrentChatId(-1));
      return;
    }

    // 如果删除的是当前会话，那么切换到下一个会话
    if (id == currentChatId) {
      let currentIndex = sortSession.findIndex((item) => item == id);
      let nextId = sortSession[currentIndex + 1];

      if (nextId) {
        dispatch(setCurrentChatId(nextId));
        await fetchChatHistory(nextId);
      } else {
        dispatch(setCurrentChatId(sortSession[0]));
        await fetchChatHistory(sortSession[0]);
      }
    }
  }

  // 创建新会话
  const fetchNewSession = async (text) => {
    // 新建会话
    const data1 = await APIChatNewSession({
      title: text,
    });

    if (data1.code != 200) {
      alert(data1.message);
      return;
    }

    dispatch(setCurrentChatId(data1.data.chat_session_id));

    // 更新会话列表
    await fetchSession();

    // 插入新消息
    const data2 = await APIChatNewMessage({
      chat_session_id: data1.data.chat_session_id,
      text: text.trim(),
    });

    if (data2.code != 200) {
      alert(data2.message);
      return;
    }

    // 获取会话的最新消息列表
    await fetchChatHistory(data1.data.chat_session_id);

    // 让AI生成回答
    socket.current.emit("get_text", {
      ai_message_id: data2.data.ai_message_id,
      chat_session_id: data1.data.chat_session_id,
    });

    setInput("");
  };

  // 连接websocket
  const connectWs = () => {
    socket.current = io(import.meta.env.VITE_WS_BASE_URL, {
      reconnectionDelayMax: 10000,
      // path: '/wschat/',
      extraHeaders: {
        authorization: `bearer ` + localStorage.getItem("token"),
      },
    });

    socket.current.on("connect", () => {
      console.log("链接成功");
    });

    socket.current.on("disconnect", () => {
      console.log("链接断开");
    });

    socket.current.on("token_output", (data) => {
      const jdata = JSON.parse(data);
      dispatch(
        setTokenToMessage({
          chat_session_id: jdata.chat_session_id,
          ai_message_id: jdata.ai_message_id,
          token: jdata.token,
        })
      );
    });
  };

  // 得到用户信息
  useEffect(() => {
    // 未登录跳到登录页
    if (!checkIsLogin()) {
      navigate("/login");
      return;
    }

    // 获取会话
    fetchSession();

    // 连接socketio
    connectWs();

    // 初始化markdownit实例
    md.current = markdownit({
      html: true,
      linkify: true,
      typographer: true,
      langPrefix: 'language-',
    }).use(MarkdownItHightlightJS);

    md.current.renderer.rules.table_open = () =>
      '<table style="border-collapse: collapse; width: 100%;">';
    md.current.renderer.rules.table_close = () => "</table>";

    // 修改表头单元格样式
    md.current.renderer.rules.th_open = () =>
      '<th style="border: 1px solid #ddd; padding: 8px; background: #f5f5f5;">';
    md.current.renderer.rules.td_open = () =>
      '<td style="border: 1px solid #ddd; padding: 8px;">';
  }, []);

  // 会话内容有变化的时候，比如输出状态就要不断切换到底部
  useEffect(() => {
    if (chataeraRef.current) {
      console.log("滚动条垂直位置:", chataeraRef.current.scrollTop);

      if (chataeraRef.current.scrollTop > -60) {
        chataeraRef.current.scrollTop = chataeraRef.current.scrollHeight;
      }
    } else {
      console.log("chataeraRef.current 还没有指向 DOM 元素");
    }
  }, [chatSessions]);

  // 有传参过来的时候
  const location = useLocation();
  useEffect(() => {
    if (location.state?.input) {
      fetchNewSession(location.state.input);
    }
  }, [location]);

  useEffect(() => {
    if (currentChatId == -1) {
      bigInputRef.current?.focus()
    } else {
      inputRef.current?.focus();
    }
  }, [currentChatId])

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
            className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition-colors mb-3 cursor-pointer"
            onClick={() => {
              dispatch(setCurrentChatId(-1));
            }}
          >
            新建会话
          </button>

          <h2 className="text-lg font-semibold mb-4 text-black">会话记录</h2>
          {Object.keys(chatSessions).length === 0 ? (
            <div>无会话</div>
          ) : (
            <ul>
              {Object.values(chatSessions)
                .sort((a, b) => b.id - a.id)
                .map((session) => (
                  <li
                    key={session.id}
                    className={`cursor-pointer p-2 rounded-md mb-2 transition-colors flex justify-between ${currentChatId == session.id
                      ? "bg-blue-500 text-white"
                      : "bg-gray-100 hover:bg-gray-200 text-black"
                      }`}
                    onClick={() => handleSessionClick(session.id)}
                  >
                    <div
                      style={{
                        textOverflow: "ellipsis",
                        wordBreak: "keep-all",
                        width: "180px",
                        overflow: "hidden",
                        whiteSpace: "nowrap",
                      }}
                      title={session.title}
                    >
                      {session.title}
                    </div>
                    <button
                      className="w-5 h-5 rounded-full flex items-center justify-center text-white hover:bg-red-600 transition-colors"
                      style={{
                        background: "oklch(0.84 0 0)",
                        minWidth: "20px",
                        cursor: "pointer",
                      }}
                      onClick={(e) => {
                        e.stopPropagation();
                        // 删除会话
                        fetchDelSession(session.id);
                      }}
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-3 w-3"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                      >
                        <path
                          fillRule="evenodd"
                          d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                          clipRule="evenodd"
                        />
                      </svg>
                    </button>
                  </li>
                ))}
            </ul>
          )}
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
                  ref={bigInputRef}
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
            <div
              className="flex-1 p-4 overflow-y-auto flex flex-col-reverse markdown-body"
              ref={chataeraRef}
            >
              {/* 使用 flex-col-reverse 让最新的消息在底部，滚动向上 */}
              {chatSessions[currentChatId]?.messages
                ? Object.values(chatSessions[currentChatId].messages)
                  .sort((a, b) => b.id - a.id)
                  .map((message) => (
                    <div
                      key={message.id}
                      className={`flex mb-4 ${message.sender === "user"
                        ? "justify-end"
                        : "justify-start"
                        }`}
                    >
                      {message?.text ? (
                        <div
                          className={`max-w-[70%] p-3 rounded-lg ${message?.sender === "user"
                            ? "bg-blue-500 text-white rounded-br-none"
                            : "bg-gray-200 text-black rounded-bl-none"
                            }`}
                          dangerouslySetInnerHTML={{
                            __html: message?.text
                              ? md.current.render(message?.text)
                              : "",
                          }}
                        ></div>
                      ) : (
                        <div
                          className={`max-w-[70%] p-3 rounded-lg ${message?.sender === "user"
                            ? "bg-blue-500 text-white rounded-br-none"
                            : "bg-gray-200 text-black rounded-bl-none"
                            }`}
                        >
                          <TDTextLoading text="思考中" />
                        </div>
                      )}
                    </div>
                  ))
                : null}

              <div className="pb-20"></div>
            </div>

            {/* 聊天输入区域 */}
            <div className="p-4 border-t border-gray-200 flex items-center bg-white">
              <input
                type="text"
                placeholder="请输入你的问题..."
                className="flex-1 rounded-full py-2 px-4 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                ref={inputRef}
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
