import api from './index';

// 上传单个文件
export const uploadSingleFile = (file) => {
    const formData = new FormData();
    formData.append('file', file); // 'file' 是后端定义的字段名

    return api.post('/upload', formData, {
    });
};

// 上传文件并显示进度
export const uploadFileWithProgress = (file, onProgress) => {
    const formData = new FormData();
    formData.append('file', file);

    return api.post('/upload', formData, {
        onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            if (onProgress) {
                onProgress(percentCompleted);
            }
        }
    });
};