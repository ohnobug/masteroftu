// src/components/FileConverterUI.jsx

import React, { useRef } from 'react';
// 1. 导入 useNavigate hook 用于页面跳转
import { useNavigate } from 'react-router-dom';
import FileListItem from './FileListItem';
import { DocumentTextIcon } from './icons/DocumentTextIcon';
// 引入一个新的图标用于新按钮
import { ListBulletIcon } from './icons/ListBulletIcon';

const FileConverterUI = ({ files, onFilesAdded, onRemoveFile, onStartExtraction }) => {
  const fileInputRef = useRef(null);
  // 2. 实例化 navigate 函数
  const navigate = useNavigate();

  const handleFilesChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      onFilesAdded(Array.from(e.target.files));
      e.target.value = null;
    }
  };

  const handleAddMoreClick = () => {
    fileInputRef.current.click();
  };

  // 3. 【新增】“查看进度”按钮的点击处理函数
  const handleViewProgressClick = () => {
    // 跳转到我们创建的试卷列表页面
    navigate('/papers');
  };

  // 4. 【新增】计算是否所有文件都上传完毕
  //    - `files.length > 0` 确保数组不为空
  //    - `files.every(...)` 检查数组中的每一项是否都满足条件
  const allUploadsDone = files.length > 0 && files.every(file => file.progress === 100);

  return (
    <div className="bg-white rounded-2xl shadow-2xl shadow-purple-500/5 overflow-hidden">
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept="image/*"
        className="hidden"
        onChange={handleFilesChange}
      />

      <div className="p-6 text-center border-b border-gray-100">
        <h1 className="text-3xl font-bold text-dark-charcoal">已上传的试卷图片</h1>
        <p className="text-gray-500 mt-2">AI 将自动识别下图中的题目和选项</p>
      </div>

      <div className="bg-gray-50/70 p-4 space-y-2 max-h-96 overflow-y-auto">
        {files.map(file => (
          <FileListItem key={file.id} file={file} onRemove={onRemoveFile} />
        ))}
      </div>

      <div className="bg-white p-4 flex justify-between items-center border-t border-gray-100">

        {/* 5. 【核心改动】使用三元运算符进行条件渲染 */}
        {allUploadsDone ? (
          // a. 如果所有文件都已上传完毕，显示 "查看进度" 按钮
          <button
            onClick={handleViewProgressClick}
            className="
              bg-purple-600 text-white font-bold py-2 px-4 rounded-lg 
              hover:bg-purple-700 transition-all text-sm flex items-center gap-x-2
              shadow-md hover:shadow-lg
            "
          >
            <ListBulletIcon className="w-4 h-4" />
            查看试卷处理进度
          </button>
        ) : (
          // b. 否则，显示原来的 "添加更多图片" 按钮
          <button
            onClick={handleAddMoreClick}
            className="bg-gray-100 text-gray-700 font-bold py-2 px-4 rounded-lg hover:bg-gray-200 transition-all text-sm"
          >
            + 添加更多图片
          </button>
        )}

        {/* 主操作按钮 */}
        <button
          onClick={onStartExtraction}
          className="
            bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold 
            py-3 px-8 rounded-lg text-base transition-all duration-300 ease-in-out
            shadow-lg hover:shadow-xl hover:scale-105 hover:-translate-y-1
            flex items-center gap-x-2
          "
        >
          <DocumentTextIcon className="w-5 h-5" />
          开始提取试题
        </button>
      </div>
    </div>
  );
};



export default FileConverterUI;