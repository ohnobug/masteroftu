// src/components/Footer.jsx
import React from 'react';
import { GlobeIcon } from './icons/GlobeIcon';

const Footer = () => {
  return (
    // 使用更深的灰色，并移除内联样式，以保持 Tailwind 的一致性
    <footer className="bg-gray-900 text-gray-400">
      
      {/* 1. Stats Bar -> 改造为与试卷提取相关的、建立信任感的数据 */}
      <div className="border-b border-gray-700">
        <div className="container mx-auto max-w-7xl flex flex-col md:flex-row justify-around items-center gap-y-6 py-8 px-4 text-center">
          <div>
            <p className="text-4xl font-light tracking-wider text-white">125,849,102</p>
            <p className="text-sm text-gray-500 mt-1">已精准提取题目</p>
          </div>
          <div>
            <p className="text-4xl font-light tracking-wider text-white">3,450,980</p>
            <p className="text-sm text-gray-500 mt-1">已处理试卷</p>
          </div>
        </div>
      </div>

      {/* 2. Main Footer Links -> 改造为与产品、解决方案、资源相关的链接 */}
      <div className="container mx-auto max-w-7xl py-12 px-4">
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-8 text-sm">
          {/* Column 1: 关于我们 */}
          <div className="space-y-3">
            <h4 className="font-semibold text-white mb-4">图克教育</h4>
            <a href="#" className="block hover:text-white transition-colors">关于我们</a>
            <a href="#" className="block hover:text-white transition-colors">联系我们</a>
            <a href="#" className="block hover:text-white transition-colors">隐私政策</a>
            <a href="#" className="block hover:text-white transition-colors">服务条款</a>
          </div>
          {/* Column 2: 核心功能 */}
          <div className="space-y-3">
            <h4 className="font-semibold text-white mb-4">核心功能</h4>
            <a href="#" className="block hover:text-white transition-colors">题目提取</a>
            <a href="#" className="block hover:text-white transition-colors">选项识别</a>
            <a href="#" className="block hover:text-white transition-colors">公式识别</a>
            <a href="#" className="block hover:text-white transition-colors">格式化导出</a>
          </div>
          {/* Column 3: 资源与支持 */}
          <div className="space-y-3">
            <h4 className="font-semibold text-white mb-4">资源与支持</h4>
            <a href="#" className="block hover:text-white transition-colors">帮助中心</a>
            <a href="#" className="block hover:text-white transition-colors">常见问题</a>
            <a href="#" className="block hover:text-white transition-colors">API 文档</a>
            <a href="#" className="block hover:text-white transition-colors">技术博客</a>
          </div>
        </div>
      </div>

      {/* 3. Bottom Bar -> 更新版权信息 */}
      <div className="bg-black py-4">
        <div className="container mx-auto max-w-7xl flex flex-col sm:flex-row justify-between items-center px-4 text-xs text-gray-500 gap-y-2">
          <div>
            <span>© 2024–2025 图克教育. 版权所有.</span>
            <a href="#" className="ml-4 hover:text-gray-300">Terms of Use</a>
            <a href="#" className="ml-4 hover:text-gray-300">Privacy Policy</a>
          </div>
          <button className="flex items-center hover:text-gray-300">
            <GlobeIcon />
            简体中文
          </button>
        </div>
      </div>
    </footer>
  );
};

export default Footer;