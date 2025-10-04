import React, { useState, useRef, useEffect } from 'react';
import TDSHeader from "./components/TDSHeader";
import TDSFooter from "./components/TDSFooter";

// 定义标签常量
const LABELS = {
    QUESTION: '试题',
    FIGURE: '题目中的图形',
};

// 定义标签颜色
const LABEL_COLORS = {
    [LABELS.QUESTION]: 'rgba(255, 102, 102, 1)',
    [LABELS.FIGURE]: 'rgba(102, 178, 255, 1)',
};

function ImageAnnotator() {
    // 状态管理
    const [image, setImage] = useState(null);
    const [annotations, setAnnotations] = useState([]);
    const [currentLabel, setCurrentLabel] = useState(LABELS.QUESTION);
    const [isDrawing, setIsDrawing] = useState(false);
    const [startPoint, setStartPoint] = useState({ x: 0, y: 0 });
    const [endPoint, setEndPoint] = useState({ x: 0, y: 0 });
    const [isDraggingOver, setIsDraggingOver] = useState(false);
    const [imageDimensions, setImageDimensions] = useState({ width: 0, height: 0 });

    // Refs
    const canvasRef = useRef(null);
    const imageRef = useRef(null);
    const fileInputRef = useRef(null);
    const dragCounter = useRef(0);
    // 【关键修复】Ref 现在指向您指定的新滚动容器 div
    const scrollContainerRef = useRef(null);

    // 效果钩子 1 & 2 (逻辑无变动)
    useEffect(() => {
        const handleResize = () => { if (image && imageRef.current && canvasRef.current) { const canvas = canvasRef.current; const imageElement = imageRef.current; const ctx = canvas.getContext('2d'); const displayWidth = imageElement.clientWidth; const displayHeight = imageElement.clientHeight; const dpr = window.devicePixelRatio || 1; canvas.width = displayWidth * dpr; canvas.height = displayHeight * dpr; canvas.style.width = `${displayWidth}px`; canvas.style.height = `${displayHeight}px`; ctx.scale(dpr, dpr); } };
        handleResize(); window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, [image]);

    useEffect(() => {
        if (image && canvasRef.current && imageDimensions.width > 0) {
            const canvas = canvasRef.current; const ctx = canvas.getContext('2d'); const displayWidth = canvas.clientWidth; const displayHeight = canvas.clientHeight; const scaleX = displayWidth / imageDimensions.width; const scaleY = displayHeight / imageDimensions.height; ctx.clearRect(0, 0, displayWidth, displayHeight);
            const drawAnnotation = (anno) => { ctx.strokeStyle = LABEL_COLORS[anno.label]; ctx.lineWidth = 2; ctx.strokeRect(anno.x * scaleX, anno.y * scaleY, anno.width * scaleX, anno.height * scaleY); ctx.fillStyle = LABEL_COLORS[anno.label].replace('1)', '0.2)'); ctx.fillRect(anno.x * scaleX, anno.y * scaleY, anno.width * scaleX, anno.height * scaleY); ctx.font = `14px Arial`; ctx.fillStyle = LABEL_COLORS[anno.label]; ctx.fillText(anno.label, (anno.x * scaleX) + 5, (anno.y * scaleY) + 15); };
            annotations.forEach(drawAnnotation);
            if (isDrawing) { const rect = getRect(startPoint, endPoint); drawAnnotation({ ...rect, label: currentLabel }); }
        }
    }, [annotations, isDrawing, startPoint, endPoint, currentLabel, image, imageDimensions]);

    // 效果钩子 3: 自动滚动
    useEffect(() => {
        // 【关键修复】现在操作的是您指定的新滚动容器 div
        if (scrollContainerRef.current) {
            const scrollContainer = scrollContainerRef.current;
            scrollContainer.scrollTop = scrollContainer.scrollHeight;
        }

        console.log(annotations)
    }, [annotations]);

    // 所有函数逻辑 (无变动)
    const processFile = (file) => { if (file && file.type.startsWith('image/')) { const reader = new FileReader(); reader.onload = (event) => { const img = new Image(); img.onload = () => { setImageDimensions({ width: img.width, height: img.height }); setImage(event.target.result); }; img.src = event.target.result; }; reader.readAsDataURL(file); setAnnotations([]); } else { alert('请上传图片文件 (e.g., png, jpg)'); } };
    const getMousePos = (e) => { const rect = canvasRef.current.getBoundingClientRect(); const scaleX = imageDimensions.width / rect.width; const scaleY = imageDimensions.height / rect.height; return { x: (e.clientX - rect.left) * scaleX, y: (e.clientY - rect.top) * scaleY }; };
    const handleFileChange = (e) => { const file = e.target.files[0]; if (file) { processFile(file); } };
    const handleSelectFileClick = () => { fileInputRef.current.click(); };
    const handleDragEnter = (e) => { e.preventDefault(); e.stopPropagation(); dragCounter.current++; if (e.dataTransfer.items && e.dataTransfer.items.length > 0) { setIsDraggingOver(true); } };
    const handleDragLeave = (e) => { e.preventDefault(); e.stopPropagation(); dragCounter.current--; if (dragCounter.current === 0) { setIsDraggingOver(false); } };
    const handleDragOver = (e) => { e.preventDefault(); e.stopPropagation(); };
    const handleFileDrop = (e) => { e.preventDefault(); e.stopPropagation(); setIsDraggingOver(false); dragCounter.current = 0; const file = e.dataTransfer.files[0]; if (file) { processFile(file); } };
    const handleMouseDown = (e) => { if (image) { setIsDrawing(true); const pos = getMousePos(e); setStartPoint(pos); setEndPoint(pos); } };
    const handleMouseMove = (e) => { if (isDrawing) { setEndPoint(getMousePos(e)); } };
    const handleMouseUp = () => { if (isDrawing) { setIsDrawing(false); const rect = getRect(startPoint, endPoint); if (rect.width > 5 && rect.height > 5) { setAnnotations(prev => [...prev, { ...rect, label: currentLabel, id: crypto.randomUUID() }]); } } };
    const getRect = (start, end) => ({ x: Math.min(start.x, end.x), y: Math.min(start.y, end.y), width: Math.abs(start.x - end.x), height: Math.abs(start.y - end.y) });
    const removeAnnotation = (id) => { setAnnotations(prev => prev.filter(a => a.id !== id)); };

    return (
        <div className="flex flex-col min-h-screen bg-gray-50">
            <TDSHeader />
            <main className="flex-grow container mx-auto max-w-7xl py-10 px-4 flex flex-col">
                <div className="w-full bg-white rounded-2xl shadow-2xl flex flex-col flex-grow overflow-hidden">
                    <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6 p-6 overflow-hidden">
                        {/* 图片标注区 */}
                        <div
                            className={`lg:col-span-2 relative flex justify-center items-center bg-gray-100 rounded-lg border-2 transition-colors overflow-auto ${isDraggingOver ? 'border-blue-500 bg-blue-50' : 'border-dashed border-transparent'}`}
                            onDrop={handleFileDrop} onDragOver={handleDragOver} onDragEnter={handleDragEnter} onDragLeave={handleDragLeave}
                        >
                            {image ? (
                                <div className="relative flex justify-center items-center p-4">
                                    <img ref={imageRef} src={image} alt=" " draggable="false" className="max-w-full max-h-full object-contain select-none" />
                                    <canvas ref={canvasRef} className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 cursor-crosshair" onMouseDown={handleMouseDown} onMouseMove={handleMouseMove} onMouseUp={handleMouseUp} onMouseLeave={handleMouseUp} />
                                </div>
                            ) : (
                                <div className="w-full h-full flex flex-col justify-center items-center p-4 border-2 border-dashed border-gray-300 rounded-lg text-center">
                                    <input type="file" ref={fileInputRef} onChange={handleFileChange} accept="image/*" className="hidden" />
                                    <button className="bg-blue-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-blue-700 transition-all mb-4" onClick={handleSelectFileClick}>选择图片</button>
                                    <p className="text-gray-500">或将图片拖拽到这里</p>
                                </div>
                            )}
                        </div>

                        {/* 侧边栏 */}
                        <div className="lg:col-span-1 bg-white border border-gray-200 rounded-lg p-4 flex flex-col overflow-hidden">
                            {/* 选择标签 (固定部分) */}
                            <div className="pb-4 border-b border-gray-100 flex-shrink-0">
                                <h3 className="text-base font-semibold mb-3">选择标签</h3>
                                <div className="flex items-center gap-x-2">
                                    <button className={`w-full py-2 px-4 rounded-lg text-sm font-semibold transition-colors ${currentLabel === LABELS.QUESTION ? 'bg-blue-600 text-white shadow' : 'bg-gray-100 hover:bg-gray-200'}`} onClick={() => setCurrentLabel(LABELS.QUESTION)}>{LABELS.QUESTION}</button>
                                    <button className={`w-full py-2 px-4 rounded-lg text-sm font-semibold transition-colors ${currentLabel === LABELS.FIGURE ? 'bg-blue-600 text-white shadow' : 'bg-gray-100 hover:bg-gray-200'}`} onClick={() => setCurrentLabel(LABELS.FIGURE)}>{LABELS.FIGURE}</button>
                                </div>
                            </div>

                            {/* 标注列表标题 (固定部分) */}
                            <div className="mt-4 flex-shrink-0">
                                <h3 className="text-base font-bold pb-2 border-b border-gray-100">标注列表 ({annotations.length})</h3>
                            </div>

                            {/* ======================= 【严格按照您的要求修改】 ======================= */}
                            {/* 1. 在 ul 外面包裹一层 div。这个 div 负责占据剩余空间并滚动。 */}
                            <div ref={scrollContainerRef} className="flex-grow mt-2 overflow-y-auto" style={{
                                height: "400px",
                            }}>
                                {/* 2. ul 只负责展示列表内容，不再有任何布局相关的类。 */}
                                <ul className="space-y-1">
                                    {annotations.map((anno, index) => (
                                        <li key={anno.id} className="flex justify-between items-center p-2 rounded hover:bg-gray-50">
                                            <span className="text-sm text-gray-700">{index + 1}. {anno.label}</span>
                                            <button className="bg-red-500 text-white text-xs font-bold py-1 px-2 rounded hover:bg-red-600 transition-opacity" onClick={() => removeAnnotation(anno.id)}>删除</button>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                            {/* =================================================================== */}
                        </div>
                    </div>
                </div>
            </main>
            <TDSFooter />
        </div>
    );
}

export default ImageAnnotator;
