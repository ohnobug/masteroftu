import TDSBg from "./components/TDSBg";
import TDSHeader from "./components/TDSHeader";
import TDSFooter from "./components/TDSFooter";
import { Link } from "react-router";

const Card = ({ image, title, description, teacher, date }) => {
  return (
    <Link
      to="/"
      class="group block bg-white/80 backdrop-blur-md rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-2xl hover:-translate-y-2"
    >
      <div class="relative">
        <img
          src={image}
          alt="课程封面"
          class="w-full h-40 object-cover transition-transform duration-300 group-hover:scale-105"
        />
      </div>
      <div class="p-5 flex flex-col h-40">
        <h3 class="text-lg font-bold text-black mb-2 group-hover:text-cyan-600 transition-colors">
          {title}
        </h3>
        <p class="text-sm text-gray-600 mb-4 flex-grow">{description}</p>
        <div class="mt-auto border-t border-gray-200 pt-3 flex justify-between items-center text-xs text-gray-500">
          <span>
            <strong class="font-medium">主讲:</strong> {teacher}
          </span>
          <span>{date}</span>
        </div>
      </div>
    </Link>
  );
};

function CoursePage() {
  return (
    <>
      {/* 背景图片和渐变叠加层 */}
      <TDSBg />

      {/* 顶部导航栏 */}
      <TDSHeader />

      {/* 主要内容 */}
      <main class="relative z-10 py-16 px-6">
        <div class="max-w-screen-xl mx-auto space-y-16">
          {/* ========= 小学阶段 ========= */}
          <section>
            <h2 class="text-3xl font-bold text-black mb-6 border-l-4 border-cyan-500 pl-4">
              小学阶段
            </h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
              <Card
                image="/images/5.webp"
                title="趣味编程：Scratch动画与游戏"
                description="通过拖拽积木，激发孩子创造力，轻松步入编程世界。"
                teacher="李老师"
                date="2024-05-10"
              />
              <Card
                image="/images/2.webp"
                title="奥数思维拓展"
                description="培养逻辑推理能力，用巧妙方法解决数学难题。"
                teacher="王老师"
                date="2024-04-22"
              />
              <Card
                image="/images/3.webp"
                title="创意看图写话"
                description="提升观察力和想象力，让孩子爱上写作。"
                teacher="赵老师"
                date="2024-03-15"
              />
              <Card
                image="/images/4.webp"
                title="自然拼读法英语启蒙"
                description="掌握字母发音规律，见词能读，听音能写。"
                teacher="Mary"
                date="2024-05-01"
              />
            </div>
          </section>

          {/* ========= 初中阶段 ========= */}
          <section>
            <h2 class="text-3xl font-bold text-black mb-6 border-l-4 border-teal-500 pl-4">
              初中阶段
            </h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
              <Card
                image="/images/1.webp"
                title="物理世界探秘：力与运动"
                description="结合实验与动画，生动解析牛顿定律，攻克力学难点。"
                teacher="陈老师"
                date="2024-04-18"
              />
              <Card
                image="/images/6.webp"
                title="函数与几何综合精讲"
                description="梳理代数与几何的内在联系，掌握中考核心考点。"
                teacher="张老师"
                date="2024-03-20"
              />
              <Card
                image="/images/7.webp"
                title="文言文阅读与鉴赏"
                description="逐字逐句精读经典篇目，轻松掌握实词虚词用法。"
                teacher="刘老师"
                date="2024-02-28"
              />
              <Card
                image="/images/8.webp"
                title="中考英语语法冲刺"
                description="系统复习时态、语态、从句等核心语法，决胜中考。"
                teacher="David"
                date="2024-05-05"
              />
            </div>
          </section>

          {/* ========= 高中阶段 ========= */}
          <section>
            <h2 class="text-3xl font-bold text-black mb-6 border-l-4 border-sky-500 pl-4">
              高中阶段
            </h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
              <Card
                image="/images/9.webp"
                title="高考数学：导数与圆锥曲线"
                description="专题突破高考两大压轴题型，掌握核心解题技巧。"
                teacher="黄老师"
                date="2024-04-01"
              />
              <Card
                image="/images/10.webp"
                title="有机化学基础与进阶"
                description="从官能团到有机合成，构建完整的有机化学知识体系。"
                teacher="孙老师"
                date="2024-03-10"
              />
              <Card
                image="/images/11.webp"
                title="Python编程入门与算法竞赛"
                description="掌握Python语法，学习基础算法，为信息学竞赛做准备。"
                teacher="李俊杰"
                date="2024-05-20"
              />
              <Card
                image="/images/12.webp"
                title="大学自主招生面试指导"
                description="提升综合素养与表达能力，在自主招生中脱颖而出。"
                teacher="周老师"
                date="2024-02-15"
              />
            </div>
          </section>

          {/* ========= 大学阶段 ========= */}
          <section>
            <h2 class="text-3xl font-bold text-black mb-6 border-l-4 border-indigo-500 pl-4">
              大学阶段
            </h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
              <Card
                image="/images/13.webp"
                title="数据结构与算法 (C++)"
                description="计算机专业核心课程，手把手带你实现链表、树、图等结构。"
                teacher="林教授"
                date="2024-03-01"
              />
              <Card
                image="/images/14.webp"
                title="线性代数及其应用"
                description="矩阵、向量空间、特征值，理解机器学习的数学基础。"
                teacher="郑教授"
                date="2024-04-10"
              />
              <Card
                image="/images/15.webp"
                title="学术论文写作与规范"
                description="从选题、文献综述到格式排版，助你顺利完成学术写作。"
                teacher="钱博士"
                date="2024-02-20"
              />
              <Card
                image="/images/16.webp"
                title="操作系统原理 (Linux)"
                description="深入理解进程、内存管理、文件系统等核心概念。"
                teacher="吴教授"
                date="2024-05-12"
              />
              <Card
                image="/images/17.webp"
                title="数据结构与算法 (C++)"
                description="计算机专业核心课程，手把手带你实现链表、树、图等结构。"
                teacher="林教授"
                date="2024-03-01"
              />
              <Card
                image="/images/18.webp"
                title="线性代数及其应用"
                description="矩阵、向量空间、特征值，理解机器学习的数学基础。"
                teacher="郑教授"
                date="2024-04-10"
              />
              <Card
                image="/images/19.webp"
                title="学术论文写作与规范"
                description="从选题、文献综述到格式排版，助你顺利完成学术写作。"
                teacher="钱博士"
                date="2024-02-20"
              />
              <Card
                image="/images/20.webp"
                title="操作系统原理 (Linux)"
                description="深入理解进程、内存管理、文件系统等核心概念。"
                teacher="吴教授"
                date="2024-05-12"
              />
            </div>
          </section>

          {/* ========= 职业技能 ========= */}
          <section>
            <h2 class="text-3xl font-bold text-black mb-6 border-l-4 border-purple-500 pl-4">
              职业技能
            </h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
              <Card
                image="/images/21.webp"
                title="React全家桶与企业级项目实战"
                description="深入React、Redux、Router，构建现代化、高性能的前端应用。"
                teacher="李俊杰"
                date="2024-04-15"
              />
              <Card
                image="/images/22.webp"
                title="AI大模型应用开发实战"
                description="基于LangChain和API，快速构建自己的AI智能助手和应用。"
                teacher="李俊杰"
                date="2024-02-22"
              />
              <Card
                image="/images/23.webp"
                title="UI/UX产品设计全流程"
                description="从用户研究、原型设计到可用性测试，成为合格的产品设计师。"
                teacher="Eva"
                date="2024-03-01"
              />
              <Card
                image="/images/24.webp"
                title="AWS云计算架构师认证"
                description="系统学习AWS核心服务，备考Solutions Architect Associate认证。"
                teacher="Frank"
                date="2024-05-18"
              />
            </div>
          </section>
        </div>
      </main>

      {/* 页脚和备案号 */}
      <TDSFooter />
    </>
  );
}

export default CoursePage;
