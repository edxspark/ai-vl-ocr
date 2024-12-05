const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    // proxy: {
    //   '/api': {
    //     target: process.env.VUE_APP_BACKEND_HOST,
    //     changeOrigin: true,
    //     pathRewrite: { '^/api': '' }
    //   }
    // }
  }
})
