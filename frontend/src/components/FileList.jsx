// src/components/FileList.jsx
import React, { useMemo } from 'react';
import FileListItem from './FileListItem';

const FileList = ({ files, onRemove, onConvert, onAddFiles }) => {
  const fileInputRef = React.useRef(null);

  // 决定转换按钮是否可用
  const isReadyToConvert = useMemo(() => {
    if (files.length === 0) return false;
    return files.every(file => file.status === 'uploaded');
  }, [files]);

  const handleAddClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e) => {
    if (e.target.files) {
      onAddFiles(Array.from(e.target.files));
    }
  };

  return (
    <div>
      <div className="space-y-3">
        {files.map(file => (
          <FileListItem key={file.id} file={file} onRemove={onRemove} />
        ))}
      </div>
      <div className="mt-6 flex flex-col sm:flex-row justify-between items-center space-y-3 sm:space-y-0">
        <input
          type="file"
          multiple
          ref={fileInputRef}
          className="hidden"
          onChange={handleFileChange}
        />
        <button
          onClick={handleAddClick}
          className="w-full sm:w-auto bg-gray-200 text-gray-700 font-bold py-2 px-4 rounded-lg hover:bg-gray-300 transition-all"
        >
          + 添加更多文件
        </button>
        <button
          onClick={onConvert}
          disabled={!isReadyToConvert}
          className="w-full sm:w-auto bg-red-500 text-white font-bold py-3 px-8 rounded-lg hover:bg-red-600 transition-all disabled:bg-red-300 disabled:cursor-not-allowed"
        >
          转换
        </button>
      </div>
    </div>
  );
};

export default FileList;