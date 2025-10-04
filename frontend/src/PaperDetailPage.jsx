import { useState, useEffect } from 'react';
// 1. 导入 useParams hook 来获取 URL 中的参数 (paperId)
import { useParams, Link } from 'react-router-dom';
import { getPaperStatus, getPaperQuestions } from './api/paper'; // 导入 API 函数

// --- 子组件：单个问题的展示卡片 ---
const QuestionCard = ({ question }) => (
    <div className="bg-white p-4 rounded-lg border border-gray-200">
        <p className="text-gray-800 mb-2">{question.question_text}</p>
        {question.options && (
            <pre className="bg-gray-100 p-2 rounded text-sm text-gray-600">
                {JSON.stringify(question.options, null, 2)}
            </pre>
        )}
        <div className="mt-3 pt-3 border-t">
            <p className="text-sm text-green-700"><strong>参考答案:</strong> {question.reference_answer || '暂无'}</p>
        </div>
    </div>
);

// --- 页面主组件 ---
function PaperDetailPage() {
    // 2. 从 URL 中获取 paperId
    const { paperId } = useParams();

    const [paper, setPaper] = useState(null);
    const [questions, setQuestions] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    // 3. 封装一个获取数据的函数，方便复用
    const fetchData = async () => {
        try {
            // 使用 Promise.all 并行获取试卷详情和问题列表，速度更快
            const [paperData, questionsData] = await Promise.all([
                getPaperStatus(paperId),
                getPaperQuestions(paperId)
            ]);
            setPaper(paperData);
            setQuestions(questionsData);
            setError(null);
        } catch (err) {
            setError("无法加载试卷详情，请稍后重试。");
            console.error("获取数据失败:", err);
        } finally {
            setIsLoading(false);
        }
    };

    // 4. 初次加载时获取数据
    useEffect(() => {
        fetchData();
    }, [paperId]); // 依赖 paperId，如果 URL 变化了会重新获取

    // 5. 【核心】设置轮询，自动刷新状态
    useEffect(() => {
        // 只有当试卷状态是 PENDING 或 PROCESSING 时才需要轮询
        if (paper && (paper.status === 'PENDING' || paper.status === 'PROCESSING')) {
            // 每 5 秒钟刷新一次数据
            const intervalId = setInterval(fetchData, 5000);

            // 关键！组件卸载时清除定时器，防止内存泄漏
            return () => clearInterval(intervalId);
        }
    }, [paper]); // 依赖 paper 对象，当 paper 状态更新后会重新判断是否需要继续轮询

    // --- 渲染逻辑 ---
    if (isLoading) return <p className="text-center text-gray-500 py-10">正在加载试卷详情...</p>;
    if (error) return <p className="text-center text-red-500 py-10">{error}</p>;
    if (!paper) return <p className="text-center text-gray-500 py-10">未找到该试卷。</p>;

    return (
        <div className="space-y-8">
            {/* 页面头部：返回链接和试卷信息 */}
            <div>
                <Link to="/papers" className="text-purple-600 hover:underline mb-4 inline-block">&larr; 返回试卷列表</Link>
                <div className="bg-white p-6 rounded-lg shadow-md">
                    <h1 className="text-3xl font-bold text-gray-900">{paper.original_filename}</h1>
                    <p className="mt-2 text-md text-gray-600">
                        状态:
                        <span className="font-bold ml-2">{paper.status}</span>
                        {/* 如果正在处理，显示一个加载中的动画 */}
                        {(paper.status === 'PENDING' || paper.status === 'PROCESSING') && (
                            <span className="animate-pulse ml-2">(正在处理中...)</span>
                        )}
                    </p>
                </div>
            </div>

            {/* 问题列表 */}
            <div>
                <h2 className="text-2xl font-semibold text-gray-800 mb-4">提取的试题</h2>
                {questions.length > 0 ? (
                    <div className="space-y-4">
                        {questions.map(q => <QuestionCard key={q.id} question={q} />)}
                    </div>
                ) : (
                    <p className="text-center text-gray-500 bg-white p-6 rounded-lg shadow-sm">
                        {paper.status === 'SUCCESS' ? '该试卷没有提取出任何试题。' : '正在等待处理结果...'}
                    </p>
                )}
            </div>
        </div>
    );
}

export default PaperDetailPage;