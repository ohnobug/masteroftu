// src/components/FileDropzone.jsx
import React, { useState, useRef } from 'react';

// 1. 导入新的图标，删除旧的
import { CircularUploadIcon } from './icons/CircularUploadIcon';

const FileDropzone = ({ onFilesAdded }) => {
  const [isDragActive, setIsDragActive] = useState(false);
  const fileInputRef = useRef(null);

  // --- 事件处理 (这部分逻辑保持不变) ---
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setIsDragActive(true);
    } else if (e.type === "dragleave") {
      setIsDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      onFilesAdded(Array.from(e.dataTransfer.files));
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files.length > 0) {
      onFilesAdded(Array.from(e.target.files));
    }
  };

  const onButtonClick = () => {
    fileInputRef.current.click();
  };

  return (
    <div
      className="bg-white rounded-2xl shadow-2xl shadow-purple-500/5 overflow-hidden"
      onDragEnter={handleDrag}
      onDragOver={handleDrag}
      onDragLeave={handleDrag}
      onDrop={handleDrop}
    >
      <div class="text-center py-12 px-6">
        <h1 class="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          AI 智能提取试题
        </h1>
        <p class="text-gray-500 mt-3 text-lg">轻松上传试卷图片，让 AI 为您完成题目整理</p>
      </div>

      <div className="px-8 pb-10">
        <div
          className={`
            border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300
            ${isDragActive ? 'border-purple-500 bg-purple-50' : 'border-gray-300'}
          `}
        >
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept="image/*"
            className="hidden"
            onChange={handleChange}
          />

          {/* 2. 在这里使用新的 CircularUploadIcon 组件 */}
          <CircularUploadIcon
            className={`
              mx-auto h-16 w-16 transition-all duration-300
              ${isDragActive ? 'text-purple-600' : 'text-gray-400'}
            `}
          />

          <p className="mt-4 text-gray-600">
            将试卷图片拖拽到这里, 或
          </p>

          <button
            onClick={onButtonClick}
            className="
              mt-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold 
              py-3 px-12 rounded-lg text-lg transition-all duration-300 ease-in-out
              shadow-lg hover:shadow-xl hover:scale-105 hover:-translate-y-1
            "
          >
            上传试卷图片
          </button>

          <p className="text-xs text-gray-400 mt-5">
            支持 JPG, PNG, WEBP 等格式
          </p>
        </div>
      </div>
    </div>
  );
};

export default FileDropzone;