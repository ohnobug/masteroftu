// src/api/paper.js

import api from './index'; // 导入我们封装好的 Axios 实例

/**
 * 获取所有试卷的列表。
 * 后端接口: GET /papers
 * @returns {Promise<any>} 返回一个包含试卷列表的 Promise 对象。
 */
export const getPapersList = () => {
    // 直接调用 api.get 方法，并指定后端的 endpoint
    return api.get('/papers');
};

/**
 * 根据试卷 ID 获取该试卷下所有已提取的问题。
 * 后端接口: GET /papers/{paper_id}/questions
 * @param {number | string} paperId - 要查询的试卷的 ID。
 * @returns {Promise<any>} 返回一个包含问题列表的 Promise 对象。
 */
export const getPaperQuestions = (paperId) => {
    // 使用模板字符串动态构建请求 URL
    return api.get(`/papers/${paperId}/questions`);
};

/**
 * 根据试卷 ID 查询试卷的最新处理状态。
 * (这个接口您在后端已经有了：get_paper_details)
 * 后端接口: GET /papers/{paper_id}
 * @param {number | string} paperId - 要查询的试卷的 ID。
 * @returns {Promise<any>} 返回一个包含单个试卷详细信息的 Promise 对象。
 */
export const getPaperStatus = (paperId) => {
    return api.get(`/papers/${paperId}`);
};