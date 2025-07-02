import TDSBg from "./components/TDSBg";
import TDSHeader from "./components/TDSHeader";
import TDSFooter from "./components/TDSFooter";

function LearningPaths() {
  return (
    <>
      {/* 背景图片和渐变叠加层 */}
      <TDSBg />

      {/* 顶部导航栏 */}
      <TDSHeader />

      {/* 主要内容 */}
      <main className="relative flex flex-col items-center justify-center min-h-screen px-4 z-10 pb-20">
        <div className="flex flex-col items-center gap-6 text-center w-full">
          <h1 className="text-black text-6xl md:text-7xl font-bold">
            Learn About
          </h1>

          {/* 搜索输入框 */}
          <div className="relative w-full max-w-xl mt-2">
            <input
              type="text"
              placeholder="请输入你的问题"
              className="blinking-cursor w-full bg-white rounded-full py-4 pl-8 pr-16 text-lg text-black placeholder-gray-500 shadow-lg focus:outline-none focus:ring-2 focus:ring-teal-400 transition-all duration-300"
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

          {/* "Go to Learn About" 按钮 */}
          <button
            className="mt-4 bg-white text-black rounded-full px-10 py-4 text-lg font-medium shadow-lg hover:bg-gray-100 transition-colors"
            onclick="window.location.href='https://learn.turcar.net.cn'"
          >
            立即前往
          </button>
        </div>
      </main>

      <section
        id="learning-paths"
        className="relative bg-[#0c0c2c] py-20 md:py-28 z-0"
      >
        <div className="max-w-screen-xl mx-auto px-6">
          {/* <!-- 标题和描述 --> */}
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white">
              探索我们的学习路径
            </h2>
            <p className="mt-4 text-lg text-white/70 max-w-2xl mx-auto">
              我们为你精心设计了从入门到精通的专业学习路线图，助你系统地掌握知识，高效达成学习目标。
            </p>
          </div>

          {/* <!-- 学习路径卡片网格 --> */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* <!-- 卡片 1: 前端开发 --> */}
            <div className="bg-gray-800/50 backdrop-blur-sm border border-white/10 rounded-xl overflow-hidden shadow-lg flex flex-col transition-all duration-300 hover:border-teal-400/50 hover:-translate-y-2">
              <img
                src="https://images.unsplash.com/photo-1542831371-29b0f74f9713?q=80&w=2070&auto=format&fit=crop"
                alt="Web Development"
                className="w-full h-48 object-cover"
              />
              <div className="p-6 flex flex-col flex-grow">
                <span className="inline-block bg-teal-500/20 text-teal-300 text-xs font-semibold px-3 py-1 rounded-full mb-4 self-start">
                  热门
                </span>
                <h3 className="text-2xl font-bold text-white mb-2">
                  前端开发专家路径
                </h3>
                <p className="text-white/70 text-base mb-6 flex-grow">
                  从 HTML, CSS 和 JavaScript 基础开始，深入学习 React 和
                  Vue.js，最终成为一名全栈前端工程师。
                </p>
                <div className="space-y-3 mt-auto border-t border-white/10 pt-4">
                  <div className="flex items-center text-white/80">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-5 w-5 mr-3 text-teal-400"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 005.5 16c1.255 0 2.443-.29 3.5-.804V4.804zM14.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 0014.5 16c1.255 0 2.443-.29 3.5-.804v-10A7.968 7.968 0 0014.5 4z" />
                    </svg>
                    <span>包含 12 门课程</span>
                  </div>
                  <div className="flex items-center text-white/80">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-5 w-5 mr-3 text-teal-400"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.414-1.415L11 9.586V6z"
                        clip-rule="evenodd"
                      />
                    </svg>
                    <span>预计 90 小时</span>
                  </div>
                  <div className="flex items-center text-white/80">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-5 w-5 mr-3 text-teal-400"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path d="M2 11h14a1 1 0 011 1v2a1 1 0 01-1 1H2a1 1 0 01-1-1v-2a1 1 0 011-1zM2 3h14a1 1 0 011 1v2a1 1 0 01-1 1H2a1 1 0 01-1-1V4a1 1 0 011-1z" />
                    </svg>
                    <span>难度: 中级</span>
                  </div>
                </div>
              </div>
              <div className="p-6 pt-0">
                <a
                  href="#"
                  className="block w-full text-center bg-teal-500 hover:bg-teal-600 text-white font-semibold py-3 rounded-lg transition-colors"
                >
                  开始学习
                </a>
              </div>
            </div>

            {/* <!-- 卡片 2: 人工智能 --> */}
            <div className="bg-gray-800/50 backdrop-blur-sm border border-white/10 rounded-xl overflow-hidden shadow-lg flex flex-col transition-all duration-300 hover:border-cyan-400/50 hover:-translate-y-2">
              <img
                src="https://images.unsplash.com/photo-1599058917212-d750089bc07e?q=80&w=2069&auto=format&fit=crop"
                alt="Artificial Intelligence"
                className="w-full h-48 object-cover"
              />
              <div className="p-6 flex flex-col flex-grow">
                <span className="inline-block bg-cyan-500/20 text-cyan-300 text-xs font-semibold px-3 py-1 rounded-full mb-4 self-start">
                  前沿
                </span>
                <h3 className="text-2xl font-bold text-white mb-2">
                  人工智能与机器学习
                </h3>
                <p className="text-white/70 text-base mb-6 flex-grow">
                  掌握 Python, TensorFlow 和
                  PyTorch，深入理解深度学习和自然语言处理，开启你的AI工程师生涯。
                </p>
                <div className="space-y-3 mt-auto border-t border-white/10 pt-4">
                  <div className="flex items-center text-white/80">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-5 w-5 mr-3 text-cyan-400"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 005.5 16c1.255 0 2.443-.29 3.5-.804V4.804zM14.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 0014.5 16c1.255 0 2.443-.29 3.5-.804v-10A7.968 7.968 0 0014.5 4z" />
                    </svg>
                    <span>包含 15 门课程</span>
                  </div>
                  <div className="flex items-center text-white/80">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-5 w-5 mr-3 text-cyan-400"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.414-1.415L11 9.586V6z"
                        clip-rule="evenodd"
                      />
                    </svg>
                    <span>预计 150 小时</span>
                  </div>
                  <div className="flex items-center text-white/80">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-5 w-5 mr-3 text-cyan-400"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path d="M2 11h16a1 1 0 011 1v2a1 1 0 01-1 1H2a1 1 0 01-1-1v-2a1 1 0 011-1zM2 3h16a1 1 0 011 1v2a1 1 0 01-1 1H2a1 1 0 01-1-1V4a1 1 0 011-1z" />
                    </svg>
                    <span>难度: 高级</span>
                  </div>
                </div>
              </div>
              <div className="p-6 pt-0">
                <a
                  href="#"
                  className="block w-full text-center bg-cyan-500 hover:bg-cyan-600 text-white font-semibold py-3 rounded-lg transition-colors"
                >
                  开始学习
                </a>
              </div>
            </div>

            {/* <!-- 卡片 3: UI/UX 设计 --> */}
            <div className="bg-gray-800/50 backdrop-blur-sm border border-white/10 rounded-xl overflow-hidden shadow-lg flex flex-col transition-all duration-300 hover:border-purple-400/50 hover:-translate-y-2">
              <img
                src="https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?q=80&w=2070&auto=format&fit=crop"
                alt="UI/UX Design"
                className="w-full h-48 object-cover"
              />
              <div className="p-6 flex flex-col flex-grow">
                <span className="inline-block bg-purple-500/20 text-purple-300 text-xs font-semibold px-3 py-1 rounded-full mb-4 self-start">
                  设计
                </span>
                <h3 className="text-2xl font-bold text-white mb-2">
                  UI/UX 设计全流程
                </h3>
                <p className="text-white/70 text-base mb-6 flex-grow">
                  学习用户研究、线框图、原型制作和可用性测试，使用 Figma
                  等现代工具创造出用户喜爱的产品。
                </p>
                <div className="space-y-3 mt-auto border-t border-white/10 pt-4">
                  <div className="flex items-center text-white/80">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-5 w-5 mr-3 text-purple-400"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 005.5 16c1.255 0 2.443-.29 3.5-.804V4.804zM14.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 0014.5 16c1.255 0 2.443-.29 3.5-.804v-10A7.968 7.968 0 0014.5 4z" />
                    </svg>
                    <span>包含 8 门课程</span>
                  </div>
                  <div className="flex items-center text-white/80">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-5 w-5 mr-3 text-purple-400"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.414-1.415L11 9.586V6z"
                        clip-rule="evenodd"
                      />
                    </svg>
                    <span>预计 60 小时</span>
                  </div>
                  <div className="flex items-center text-white/80">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-5 w-5 mr-3 text-purple-400"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path d="M2 11h10a1 1 0 011 1v2a1 1 0 01-1 1H2a1 1 0 01-1-1v-2a1 1 0 011-1zM2 3h10a1 1 0 011 1v2a1 1 0 01-1 1H2a1 1 0 01-1-1V4a1 1 0 011-1z" />
                    </svg>
                    <span>难度: 入门</span>
                  </div>
                </div>
              </div>
              <div className="p-6 pt-0">
                <a
                  href="#"
                  className="block w-full text-center bg-purple-500 hover:bg-purple-600 text-white font-semibold py-3 rounded-lg transition-colors"
                >
                  开始学习
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 页脚和备案号 */}
      <TDSFooter />
    </>
  );
}

export default LearningPaths;
