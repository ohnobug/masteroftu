import TDSBg from "./components/TDSBg";
import TDSHeader from "./components/TDSHeader";
import TDSFooter from "./components/TDSFooter";

function IndexPage() {
  return (
    <>
      {/* 背景图片和渐变叠加层 */}
      <TDSBg />

      {/* 顶部导航栏 */}
      <TDSHeader />

      {/* 主要内容 */}
      <main className="relative flex flex-col items-center justify-center px-4 z-10 pb-20" style={{ minHeight: "calc(100vh - 216px)" }}>
        <div className="flex flex-col items-center gap-6 text-center w-full">
          <h1 className="text-black text-6xl md:text-7xl font-bold">
            Learn About
          </h1>

          {/* 搜索输入框 */}
          <div className="relative w-full max-w-xl mt-2">
            <input
              type="text"
              placeholder="请输入你的问题"
              className="blinking-cursor w-full bg-white rounded-full py-4 pl-8 pr-16 text-lg text-black placeholder-gray shadow-lg focus:outline-none focus:ring-2 focus:ring-teal-400 transition-all duration-300"
            />
            {/* 发送图标 */}
            <button className="absolute right-3 top-1/2 -translate-y-1/2 p-2.5 text-gray-400 hover:text-black transition-colors">
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

          {/* Go to Learn About按钮 */}
          <button
            className="mt-4 bg-white text-black rounded-full px-10 py-4 text-lg font-medium shadow-lg hover:bg-gray-100 transition-colors"
            onClick={() => {
              window.location.href = "https://learn.turcar.net.cn";
            }}
          >
            立即前往
          </button>
        </div>
      </main>

      {/* 页脚和备案号 */}
      <TDSFooter />
    </>
  );
}

export default IndexPage;
