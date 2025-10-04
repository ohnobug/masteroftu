// src/components/AutomatedOcrSection.jsx
import React from 'react';
import { SparklesIcon } from './icons/SparklesIcon'; // 导入我们刚创建的新图标

const AutomatedOcrSection = () => (
  // 使用一个醒目的渐变背景，使其成为页面的视觉焦点
  <div className="my-24">
    <div className="relative bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl shadow-2xl shadow-purple-500/20 text-center py-10 overflow-hidden">
      {/* 添加一些背景装饰元素，增加设计感 */}
      <div className="absolute top-0 left-0 -translate-x-1/4 -translate-y-1/4 w-96 h-96 bg-white/5 rounded-full" />
      <div className="absolute bottom-0 right-0 translate-x-1/4 translate-y-1/4 w-96 h-96 bg-white/5 rounded-full" />

      <div className="relative">
        <SparklesIcon className="mx-auto h-16 w-16 text-white" />
        
        {/* 核心文案，直接点明功能和优势 */}
        <h2 className="text-4xl font-bold text-white mt-6">
          让试卷数字化变得前所未有的简单
        </h2>
        <p className="text-indigo-200 mt-4 max-w-2xl mx-auto text-lg">
          我们先进的 AI 技术能精准识别题目与选项，自动完成结构化提取，彻底告别繁琐的手动录入工作。
        </p>

        {/* 行为召唤按钮，一个主要，一个次要 */}
        <div className="mt-10 flex justify-center items-center gap-x-4">
          <a 
            href="#" 
            className="
              bg-white text-purple-700 font-bold text-lg
              py-3 px-10 rounded-lg transition-all duration-300 ease-in-out
              shadow-lg hover:shadow-xl hover:scale-105 hover:-translate-y-1
            "
          >
            立即体验
          </a>
          <a 
            href="#" 
            className="
              bg-transparent border-2 border-white/80 text-white font-semibold
              py-3 px-8 rounded-lg transition-all duration-300
              hover:bg-white/10
            "
          >
            查看原理
          </a>
        </div>
      </div>
    </div>
  </div>
);

export default AutomatedOcrSection;