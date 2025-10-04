// pages/HomePage.jsx

import React, { useState } from 'react';
import TDSHeader from "./components/TDSHeader";
import TDSFooter from "./components/TDSFooter";
import FileDropzone from './components/FileDropzone';
import FileConverterUI from './components/FileConverterUI';
import { uploadFileWithProgress } from "./api/upload";

function Homework() {
    // state 现在存储的是我们自定义的、包含更多信息的文件对象数组
    const [rawFiles, setRawFiles] = useState([]);

    // 1. 重构 handleAddFiles，将原始 File 对象包装成我们自定义的结构
    const handleAddFiles = (newFilesArray) => {
        const newFilesWithStatus = newFilesArray.map(file => ({
            // 使用 crypto.randomUUID() 创建一个真正唯一的 ID (现代浏览器支持)
            id: crypto.randomUUID(),
            file: file, // 原始的 File 对象
            progress: 0, // 初始进度
            status: 'pending', // 初始状态
            response: null, // 用于存储服务器响应
            error: null, // 用于存储错误信息
        }));

        setRawFiles(prevFiles => [...prevFiles, ...newFilesWithStatus]);
    };

    // 2. 重构 handleRemoveFile，现在通过我们自定义的 id 来过滤
    const handleRemoveFile = (fileIdToRemove) => {
        setRawFiles(prevFiles => prevFiles.filter(
            item => item.id !== fileIdToRemove
        ));
    };

    // 3. 重构 handleStartExtraction，这是改动最大的部分
    const handleStartExtraction = () => {
        console.log('准备上传以下文件:', rawFiles);

        if (rawFiles.length === 0) {
            alert("没有文件可上传！");
            return;
        }

        // 遍历我们自定义的对象数组
        rawFiles.forEach(fileItem => {
            // 如果文件不是待处理状态，则跳过（防止重复上传）
            if (fileItem.status !== 'pending') {
                return;
            }

            // 更新状态为 'uploading'
            setRawFiles(prevFiles => prevFiles.map(item =>
                item.id === fileItem.id ? { ...item, status: 'uploading', progress: 0 } : item
            ));

            // 传入原始的 File 对象进行上传
            uploadFileWithProgress(
                fileItem.file,
                // a. 进度回调
                (progress) => {
                    // 更新特定文件的进度
                    setRawFiles(prevFiles => prevFiles.map(item =>
                        item.id === fileItem.id ? { ...item, progress: progress } : item
                    ));
                }
            )
                .then(response => {
                    // b. 成功回调
                    console.log(`文件 ${fileItem.file.name} 上传成功:`, response);
                    // 更新特定文件的状态和服务器响应
                    setRawFiles(prevFiles => prevFiles.map(item =>
                        item.id === fileItem.id ? { ...item, status: 'success', progress: 100, response: response } : item
                    ));
                })
                .catch(error => {
                    // c. 失败回调
                    console.error(`文件 ${fileItem.file.name} 上传失败:`, error);
                    // 更新特定文件的状态和错误信息
                    setRawFiles(prevFiles => prevFiles.map(item =>
                        item.id === fileItem.id ? { ...item, status: 'error', error: error.message } : item
                    ));
                });
        });
    };

    return (
        <div className="flex flex-col min-h-screen bg-gray-50">

            {/* 顶部导航栏 */}
            <TDSHeader />

            <main className="flex-grow container mx-auto max-w-7xl py-10 px-4 flex flex-col">
                <div className="w-full bg-white rounded-2xl shadow-2xl flex flex-col flex-grow overflow-hidden">
                    {/* <Link to="/image_annotator">Dashboard</Link> */}

                    {rawFiles.length === 0 ? (
                        <FileDropzone onFilesAdded={handleAddFiles} />
                    ) : (
                        <FileConverterUI
                            // 4. 将新的、包含更多信息的文件对象数组传递给子组件
                            files={rawFiles}
                            onFilesAdded={handleAddFiles}
                            onRemoveFile={handleRemoveFile}
                            onStartExtraction={handleStartExtraction}
                        />
                    )}

                    {/* <Features /> */}
                    {/* <AutomatedOcrSection /> */}

                </div>
            </main>

            {/* 页脚和备案号 */}
            <TDSFooter />
        </div>
    );
}

export default Homework;