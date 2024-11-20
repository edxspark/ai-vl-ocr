// src/api/api.js
import axios from 'axios'

// 创建一个 Axios 实例
const api = axios.create({
    baseURL: 'https://127.0.0.1:6606',
    timeout: 10000
})

// 请求拦截器
api.interceptors.request.use(
    config => {
        return config
    },
    error => {
        return Promise.reject(error)
    }
)

// 响应拦截器
api.interceptors.response.use(
    response => {
        return response.data // 只返回数据部分
    },
    error => {
        return Promise.reject(error)
    }
)

export default api
