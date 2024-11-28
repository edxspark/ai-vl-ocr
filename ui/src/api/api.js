import axios from 'axios'

const api = axios.create({
    baseURL: process.env.VUE_APP_BACKEND_HOST,
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
