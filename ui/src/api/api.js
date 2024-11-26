// src/api/api.js
import axios from 'axios'

// 创建一个 Axios 实例
const api = axios.create({
    baseURL: 'https://u260419-a935-26f44c0c.bjb1.seetacloud.com:8443',
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
