const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/api': {
        target: 'https://u260419-a5e7-81a835e7.bjb1.seetacloud.com:8443',
        changeOrigin: true,
        pathRewrite: { '^/api': '' }
      }
    }
  }
})
