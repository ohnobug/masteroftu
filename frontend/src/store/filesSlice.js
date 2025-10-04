import { createSlice } from '@reduxjs/toolkit';

// Redux 中最好只存储可序列化的数据。
// File 对象本身不是完全可序列化的，所以我们提取关键信息。
const processFile = (file) => ({
    id: `${file.name}-${file.lastModified}`, // 创建一个相对唯一的 ID
    name: file.name,
    size: file.size,
    type: file.type,
    // 注意：原始的 File 对象在这里丢失了，我们将在上传时再处理它。
    // 这是一个重要的权衡，确保了 Redux state 的健康。
});

const initialState = {
    list: [],
};

export const filesSlice = createSlice({
    name: 'files',
    initialState,
    // `reducers` 字段让我们定义 reducers 并生成相关的 actions
    reducers: {
        // Action: 添加一个或多个文件
        addFiles: (state, action) => {
            // action.payload 应该是原始的 File 对象数组
            const newFiles = action.payload.map(processFile);
            state.list.push(...newFiles);
        },
        // Action: 根据 ID 删除一个文件
        removeFile: (state, action) => {
            // action.payload 应该是文件的 ID
            state.list = state.list.filter(file => file.id !== action.payload);
        },
        // Action: 清空文件列表
        clearFiles: (state) => {
            state.list = [];
        },
    },
});

// 为每个 reducer 函数导出 Action Creators
export const { addFiles, removeFile, clearFiles } = filesSlice.actions;

// 默认导出 reducer
export default filesSlice.reducer;