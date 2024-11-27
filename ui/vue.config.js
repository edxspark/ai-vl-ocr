const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/api': {
        target: 'https://u260419-b6e5-4f370630.bjb1.seetacloud.com:8443', // 目标服务器地址
        changeOrigin: true, // 改变请求的origin
        pathRewrite: { '^/api': '' } // 重写请求路径
      }
    }
  }
})
