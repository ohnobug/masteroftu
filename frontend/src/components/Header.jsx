// src/components/Header.jsx
import React from 'react';

// 1. Logo 组件已修改为文字，并应用了渐变色样式
const Logo = () => (
  <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
    图克教育
  </span>
);

const NavLink = ({ children, hasArrow = false }) => (
  <a href="#" className="text-gray-600 hover:text-purple-600 px-4 py-2 text-sm font-medium flex items-center transition-colors duration-200">
    {children}
    {hasArrow && (
      <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
    )}
  </a>
);

const Header = () => {
  return (
    // 头部容器，增加了更柔和的阴影
    <header className="bg-white/80 backdrop-blur-md sticky top-0 z-50 border-b border-gray-200">
      <div className="container mx-auto max-w-7xl flex justify-between items-center px-4 h-16">
        <div className="flex items-center space-x-8">
          <a href="#">
            <Logo />
          </a>
          <nav className="hidden md:flex items-center">
            <NavLink hasArrow>转换</NavLink>
            <NavLink>OCR</NavLink>
            <NavLink>API</NavLink>
            <NavLink>定价</NavLink>
            <NavLink>Help</NavLink>
          </nav>
        </div>
        <div className="flex items-center space-x-4">
          <a href="#" className="text-gray-600 hover:text-purple-600 text-sm font-medium transition-colors duration-200">
            登录
          </a>
          {/* 2. "注册" 按钮已修改为与主题一致的渐变色按钮 */}
          <a 
            href="#" 
            className="
              bg-gradient-to-r from-blue-500 to-purple-600 text-white 
              px-4 py-1.5 rounded-md text-sm font-semibold transition-all duration-300
              hover:scale-105 hover:shadow-lg
            "
          >
            注册
          </a>
        </div>
      </div>
    </header>
  );
};

export default Header;