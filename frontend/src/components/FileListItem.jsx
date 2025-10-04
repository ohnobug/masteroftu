// src/components/FileListItem.jsx

// import { Counter } from "../store/Counter";
import { formatBytes } from "./utils/formatBytes"; // 1. 导入刚刚创建的工具函数

// 2. 引入一个简单的文档图标，增强视觉表现
const DocumentIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
  </svg>
);

// 3. 引入一个简单的状态图标
const CheckCircleIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" {...props}>
    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clipRule="evenodd" />
  </svg>
);


const FileListItem = ({ file: fileItem, onRemove }) => {
  // 为了避免混淆，将 prop 'file' 重命名为 'fileItem'
  // fileItem 现在是 { id, file, progress, status, ... }

  // 从 fileItem 中解构出原始的 File 对象，方便使用
  const { file } = fileItem;

  return (
    <div className="flex items-center justify-between bg-white px-4 py-3 border-b border-gray-100 hover:bg-gray-50/70 transition-colors duration-200">

      {/* ===== 左侧：文件名 ===== */}
      <div className="flex items-center gap-x-3 flex-1 min-w-0">
        <DocumentIcon className="h-6 w-6 text-gray-400 flex-shrink-0" />
        <span
          className="font-medium text-gray-800 truncate"
          // ✅ 修正: 访问 file.name
          title={file.name}
        >
          {/* ✅ 修正: 访问 file.name */}
          {file.name}
        </span>
      </div>

      {/* ===== 右侧：状态、大小和操作 ===== */}
      <div className="flex items-center gap-x-4 ml-4 flex-shrink-0">

        {/* 状态徽章 */}
        <div className="flex items-center gap-x-1.5 bg-green-100 text-green-700 font-medium text-xs px-2.5 py-1 rounded-full">
          <CheckCircleIcon className="h-4 w-4" />
          {/* ✅ 正确: 直接访问我们自定义的 fileItem.status 和 fileItem.progress */}
          {
            fileItem.status === "uploading" ?
              <span>{fileItem.progress ? `${fileItem.progress}%` : "0%"}</span>
              : <span>{fileItem.status}</span> // 这里可以进一步美化，例如将 'pending' 翻译成 '准备中'
          }
        </div>

        {/* 文件大小 */}
        <span className="text-sm text-gray-500 w-24 text-right font-mono">
          {/* ✅ 修正: 访问 file.size */}
          {formatBytes(file.size)}
        </span>

        {/* 删除按钮 */}
        <button
          // ✅ 正确: 直接访问我们自定义的 fileItem.id
          onClick={() => onRemove(fileItem.id)}
          className="text-gray-400 hover:text-red-500 hover:bg-red-100 rounded-full p-1 transition-all"
          title="移除文件"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default FileListItem;