// src/components/icons/CircularUploadIcon.jsx
import React from 'react';

// 全新的、更简洁的 SVG 实现
export const CircularUploadIcon = ({ className }) => (
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    className={className}
    fill="none" 
    viewBox="0 0 24 24" 
    stroke="currentColor" 
    strokeWidth="1.5"
  >
    {/* Path 1: 里面的向上箭头 */}
    <path 
      strokeLinecap="round" 
      strokeLinejoin="round" 
      d="M12 9v6m3-3l-3-3m0 0l-3 3" 
    />
    
    {/* Path 2: 外面的圆环 */}
    <path 
      strokeLinecap="round" 
      strokeLinejoin="round" 
      // cx="12" cy="12" r="10" 创建一个中心在(12,12)，半径为10的圆
      d="M22 12c0 5.523-4.477 10-10 10S2 17.523 2 12 6.477 2 12 2s10 4.477 10 10z" 
    />
  </svg>
);