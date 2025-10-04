import React, { useState, useEffect } from 'react';

import { Link } from 'react-router-dom';
import TDSHeader from "./components/TDSHeader";
import TDSFooter from "./components/TDSFooter";
import { getPapersList } from './api/paper'; // 确保 API 函数的导入路径正确

// --- 子组件：单个试卷的列表项 ---
// 将列表项封装成独立组件，使代码更清晰
const PaperListItem = ({ paper }) => (
    // 2. 使用 Link 组件包裹，让整个列表项都可以点击
    //    目标 URL 指向一个未来的详情页，例如 /papers/123
    <Link
        to={`/papers/${paper.id}`}
        className="block bg-white p-4 rounded-lg shadow-md hover:shadow-lg hover:scale-[1.02] transition-all duration-200 ease-in-out cursor-pointer"
    >
        <div className="flex justify-between items-center">
            {/* 左侧：文件名和上传时间 */}
            <div>
                <h3 className="font-semibold text-lg text-gray-800">{paper.original_filename}</h3>
                {/* 3. 格式化并显示日期，对用户更友好 */}
                <p className="text-sm text-gray-500 mt-1">
                    上传于: {new Date(paper.created_at).toLocaleString('zh-CN')}
                </p>
            </div>

            {/* 右侧：处理状态徽章 */}
            <span
                className={`px-3 py-1 text-xs font-bold rounded-full
          ${paper.status === 'SUCCESS' ? 'bg-green-100 text-green-800' : ''}
          ${paper.status === 'PENDING' ? 'bg-yellow-100 text-yellow-800' : ''}
          ${paper.status === 'PROCESSING' ? 'bg-blue-100 text-blue-800' : ''}
          ${paper.status === 'FAILED' ? 'bg-red-100 text-red-800' : ''}
        `}
            >
                {paper.status}
            </span>
        </div>
    </Link>
);


// --- 页面主组件 ---
function PaperListPage() {
    // 4. 使用三个 state 来完整地管理数据获取周期
    const [papers, setPapers] = useState([]);
    const [isLoading, setIsLoading] = useState(true); // 初始为 true，页面加载时自动获取
    const [error, setError] = useState(null);

    // 5. 使用 useEffect 在组件首次渲染时获取数据
    useEffect(() => {
        const fetchPapers = async () => {
            try {
                setIsLoading(true); // 开始获取前，设置加载状态
                const paperData = await getPapersList();
                setPapers(paperData);
                setError(null); // 成功后，清空之前的错误信息
            } catch (err) {
                setError("无法加载试卷列表，请稍后再试。");
                console.error("获取试卷列表失败:", err);
            } finally {
                // 无论成功或失败，最后都结束加载状态
                setIsLoading(false);
            }
        };

        fetchPapers();
    }, []); // 空依赖数组 [] 意味着这个 effect 只会在组件挂载时运行一次

    // --- 渲染逻辑 ---
    const renderContent = () => {
        // a. 正在加载时，显示加载指示器
        if (isLoading) {
            return <p className="text-center text-gray-500 py-10">正在加载中...</p>;
        }

        // b. 出现错误时，显示错误信息
        if (error) {
            return <p className="text-center text-red-500 py-10">{error}</p>;
        }

        // c. 没有数据时，显示空状态提示
        if (papers.length === 0) {
            return <p className="text-center text-gray-500 py-10">您还没有上传任何试卷。</p>;
        }

        // d. 数据加载成功，渲染列表
        return (
            <div className="space-y-4">
                {papers.map(paper => <PaperListItem key={paper.id} paper={paper} />)}
            </div>
        );
    };

    return (
        <div className="flex flex-col min-h-screen bg-gray-50">

            {/* 顶部导航栏 */}
            <TDSHeader />

            <main className="flex-grow container mx-auto max-w-7xl py-10 px-4 flex flex-col">
                <div className="w-full bg-white rounded-2xl shadow-2xl flex flex-col flex-grow overflow-hidden">
                    {/* 页面标题 */}
                    <div className="text-center border-b border-gray-200 pb-6">
                        <h1 className="text-4xl font-bold text-gray-900">我的试卷库</h1>
                        <p className="mt-2 text-md text-gray-600">查看所有已上传和处理的试卷</p>
                    </div>

                    {/* 动态内容区域 */}
                    <div>
                        {renderContent()}
                    </div>
                </div>
            </main>


            {/* 页脚和备案号 */}
            <TDSFooter />
        </div>
    );
}

export default PaperListPage;