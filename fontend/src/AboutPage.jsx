import TDSBg from "./components/TDSBg";
import TDSHeader from "./components/TDSHeader";
import TDSFooter from "./components/TDSFooter";

function AboutPage() {
  return (
    <>
      {/* 背景图片和渐变叠加层 */}
      <TDSBg />

      {/* 顶部导航栏 */}
      <TDSHeader />

      {/* 主要内容 */}
      <main className="relative z-10 py-16 px-6">
        <div className="max-w-screen-xl mx-auto space-y-24">
          {/* ========= Hero Section ========= */}
          <section className="text-center py-12">
            <h1 className="text-5xl md:text-6xl font-extrabold text-black tracking-tight">
              连接知识与未来
            </h1>
            <p className="mt-6 max-w-3xl mx-auto text-lg text-gray-700">
              我们是智能客服，一个充满激情与创意的团队。我们致力于打破传统教育的壁垒，通过科技与创新的力量，让每一位学习者都能享受到高质量、个性化、且触手可及的在线学习体验。
            </p>
          </section>

          {/* ========= 我们的使命与价值观 ========= */}
          <section>
            <h2 className="text-3xl font-bold text-black mb-10 border-l-4 border-cyan-500 pl-4">
              我们的使命与价值观
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-10 text-center">
              {/* 价值卡片 1 */}
              <div className="bg-white/60 backdrop-blur-md p-8 rounded-xl shadow-lg">
                <div className="flex justify-center items-center h-16 w-16 mx-auto bg-cyan-100 rounded-full">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-8 w-8 text-cyan-600"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth="2"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M12 6.253v11.494m-9-5.747h18"
                    />
                  </svg>
                </div>
                <h3 className="mt-6 text-xl font-bold text-black">知识共享</h3>
                <p className="mt-2 text-gray-600">
                  我们相信知识的力量，致力于构建一个开放、共享的学习社区，让优质教育资源无界流动。
                </p>
              </div>
              {/* 价值卡片 2 */}
              <div className="bg-white/60 backdrop-blur-md p-8 rounded-xl shadow-lg">
                <div className="flex justify-center items-center h-16 w-16 mx-auto bg-teal-100 rounded-full">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-8 w-8 text-teal-600"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth="2"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                    />
                  </svg>
                </div>
                <h3 className="mt-6 text-xl font-bold text-black">持续创新</h3>
                <p className="mt-2 text-gray-600">
                  在教学方法、技术平台和课程内容上不断探索，用前沿科技赋能教育，提升学习效率和乐趣。
                </p>
              </div>
              {/* 价值卡片 3 */}
              <div className="bg-white/60 backdrop-blur-md p-8 rounded-xl shadow-lg">
                <div className="flex justify-center items-center h-16 w-16 mx-auto bg-sky-100 rounded-full">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-8 w-8 text-sky-600"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth="2"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                    />
                  </svg>
                </div>
                <h3 className="mt-6 text-xl font-bold text-black">成就学员</h3>
                <p className="mt-2 text-gray-600">
                  将学员的成长与成功视为我们最大的价值。我们提供全方位的支持，陪伴学员走好每一步。
                </p>
              </div>
            </div>
          </section>

          {/* ========= 发展历程 (时间线) ========= */}
          <section>
            <h2 className="text-3xl font-bold text-black mb-12 border-l-4 border-teal-500 pl-4">
              发展历程
            </h2>
            <div className="relative wrap overflow-hidden p-10 h-full">
              <div
                className="border-2-2 absolute border-opacity-20 border-gray-700 h-full border"
                style={{ left: "50%" }}
              ></div>
              {/* Right Timeline */}
              <div className="mb-8 flex justify-between items-center w-full right-timeline">
                <div className="order-1 w-5/12"></div>
                <div className="z-20 flex items-center order-1 bg-teal-500 shadow-xl w-8 h-8 rounded-full">
                  <h1 className="mx-auto font-semibold text-lg text-white">
                    1
                  </h1>
                </div>
                <div className="order-1 bg-white/80 backdrop-blur-md rounded-lg shadow-xl w-5/12 px-6 py-4">
                  <h3 className="mb-3 font-bold text-gray-800 text-xl">
                    2023年 - 梦想起航
                  </h3>
                  <p className="text-sm leading-snug tracking-wide text-gray-600">
                    几位对教育充满热忱的伙伴一拍即合，智能客服的雏形诞生，致力于为K12阶段提供有趣的编程启蒙课程。
                  </p>
                </div>
              </div>
              {/* Left Timeline */}
              <div className="mb-8 flex justify-between flex-row-reverse items-center w-full left-timeline">
                <div className="order-1 w-5/12"></div>
                <div className="z-20 flex items-center order-1 bg-teal-500 shadow-xl w-8 h-8 rounded-full">
                  <h1 className="mx-auto text-white font-semibold text-lg">
                    2
                  </h1>
                </div>
                <div className="order-1 bg-white/80 backdrop-blur-md rounded-lg shadow-xl w-5/12 px-6 py-4">
                  <h3 className="mb-3 font-bold text-gray-800 text-xl">
                    2024年 - 平台上线
                  </h3>
                  <p className="text-sm leading-snug tracking-wide text-gray-600">
                    智能客服平台 (learn.turcar.net.cn)
                    正式上线，整合了从小学到大学的多元化课程，注册用户突破1万。
                  </p>
                </div>
              </div>
              {/* Right Timeline */}
              <div className="mb-8 flex justify-between items-center w-full right-timeline">
                <div className="order-1 w-5/12"></div>
                <div className="z-20 flex items-center order-1 bg-teal-500 shadow-xl w-8 h-8 rounded-full">
                  <h1 className="mx-auto font-semibold text-lg text-white">
                    3
                  </h1>
                </div>
                <div className="order-1 bg-white/80 backdrop-blur-md rounded-lg shadow-xl w-5/12 px-6 py-4">
                  <h3 className="mb-3 font-bold text-gray-800 text-xl">
                    2025年 - AI赋能
                  </h3>
                  <p className="text-sm leading-snug tracking-wide text-gray-600">
                    引入AI助教与个性化学习路径功能，推出“AI大模型应用开发”等前沿职业技能课程，深受好评。
                  </p>
                </div>
              </div>
              {/* Left Timeline */}
              <div className="mb-8 flex justify-between flex-row-reverse items-center w-full left-timeline">
                <div className="order-1 w-5/12"></div>
                <div className="z-20 flex items-center order-1 bg-teal-500 shadow-xl w-8 h-8 rounded-full">
                  <h1 className="mx-auto text-white font-semibold text-lg">
                    4
                  </h1>
                </div>
                <div className="order-1 bg-white/80 backdrop-blur-md rounded-lg shadow-xl w-5/12 px-6 py-4">
                  <h3 className="mb-3 font-bold text-gray-800 text-xl">
                    未来 - 无限可能
                  </h3>
                  <p className="text-sm leading-snug tracking-wide text-gray-600">
                    我们将继续探索教育的边界，连接全球优质资源，致力于成为终身学习者最信赖的伙伴。敬请期待！
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* ===== 核心团队 (复用课程卡片样式) ========= */}
          <section>
            <h2 className="text-3xl font-bold text-black mb-6 border-l-4 border-sky-500 pl-4">
              核心团队
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
              <div className="group block bg-white/80 backdrop-blur-md rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-2xl hover:-translate-y-2">
                <div className="relative">
                  <img
                    src="https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=1974&auto=format&fit=crop"
                    alt="团队成员照片"
                    className="w-full h-80 object-cover object-top transition-transform duration-300 group-hover:scale-105"
                  />
                </div>
                <div className="p-5">
                  <h3 className="text-lg font-bold text-black mb-1 group-hover:text-sky-600 transition-colors">
                    郭教授
                  </h3>
                  <p className="text-sm font-medium text-sky-700 mb-3">
                    学术顾问
                  </p>
                  <p className="text-sm text-gray-600">
                    知名高校计算机系教授，博士生导师。为平台提供高等教育课程的学术指导与前沿方向建议。
                  </p>
                </div>
              </div>
              <div className="group block bg-white/80 backdrop-blur-md rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-2xl hover:-translate-y-2">
                <div className="relative">
                  <img
                    src="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?q=80&w=2070&auto=format&fit=crop"
                    alt="团队成员照片"
                    className="w-full h-80 object-cover object-top transition-transform duration-300 group-hover:scale-105"
                  />
                </div>
                <div className="p-5">
                  <h3 className="text-lg font-bold text-black mb-1 group-hover:text-sky-600 transition-colors">
                    张老师
                  </h3>
                  <p className="text-sm font-medium text-sky-700 mb-3">
                    K12教学总监
                  </p>
                  <p className="text-sm text-gray-600">
                    10年一线教学经验，深谙青少年心理与认知规律，负责中小学课程体系的设计与质量把控。
                  </p>
                </div>
              </div>

              <div className="group block bg-white/80 backdrop-blur-md rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-2xl hover:-translate-y-2">
                <div className="relative">
                  <img
                    src="https://images.unsplash.com/photo-1580489944761-15a19d654956?q=80&w=1961&auto=format&fit=crop"
                    alt="团队成员照片"
                    className="w-full h-80 object-cover object-top transition-transform duration-300 group-hover:scale-105"
                  />
                </div>
                <div className="p-5">
                  <h3 className="text-lg font-bold text-black mb-1 group-hover:text-sky-600 transition-colors">
                    李老师
                  </h3>
                  <p className="text-sm font-medium text-sky-700 mb-3">
                    产品与用户体验设计师
                  </p>
                  <p className="text-sm text-gray-600">
                    追求像素级完美和极致的用户体验，负责将复杂的学习流程设计得简单、直观、有趣。
                  </p>
                </div>
              </div>
              <div className="group block bg-white/80 backdrop-blur-md rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-2xl hover:-translate-y-2">
                <div className="relative">
                  <img
                    src="https://images.unsplash.com/photo-1560250097-0b93528c311a?q=80&w=1974&auto=format&fit=crop"
                    alt="团队成员照片"
                    className="w-full h-80 object-cover object-top transition-transform duration-300 group-hover:scale-105"
                  />
                </div>
                <div className="p-5">
                  <h3 className="text-lg font-bold text-black mb-1 group-hover:text-sky-600 transition-colors">
                    李俊杰
                  </h3>
                  <p className="text-sm font-medium text-sky-700 mb-3">
                    软件工程师
                  </p>
                  <p className="text-sm text-gray-600">
                    全栈工程师，对前沿技术和教育事业充满热情。负责平台技术架构与核心课程研发。
                  </p>
                </div>
              </div>
            </div>
          </section>
        </div>
      </main>

      {/* 页脚和备案号 */}
      <TDSFooter />
    </>
  );
}

export default AboutPage;
