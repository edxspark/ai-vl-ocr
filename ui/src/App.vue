<template>
  <div id="app">
    <el-row type="flex" justify="space-between" class="nav-bar">
      <el-col :span="8" class="left-content">
        <img src="@/assets/logo.png" alt="logo" class="logo" />
        <span class="title">superforu-ai-ocr</span>
      </el-col>
      <el-col :span="8" style="margin-top: 10px" >
        <span style="font-weight: bold;color:#ffffff">AI vision document OCR</span>
      </el-col>
    </el-row>

  <el-tabs tab-position="left" style="height: 100%;border-bottom: 1px solid gray;margin-right:20px">
    <el-tab-pane label="AIOCR识别" style="background-color: #202222">
       <AIVLOCR msg="Welcome to Superforu AI OCR" />
    </el-tab-pane>
    <el-tab-pane label="AIVL广告比对" style="height: 100%;background-color: #202222">
      <AIVLImg msg="Adv Compare" />
    </el-tab-pane>
  </el-tabs>
     <div style="margin-top: 20px">Copyright@2024</div>
  </div>

</template>

<script>
import AIVLOCR from './components/AIVLOCR.vue'
import AIVLImg from './components/AIVLImg.vue'

export default {
  components:{AIVLOCR,AIVLImg}
}

</script>

<style scoped>


#app {
  font-family: "微软雅黑", Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.left-content {
  display: flex;
  align-items: center;
}

.logo {
  width: 48px;
  height: 36px;
  margin-right: 2px;
}

.nav-bar {
  padding-top: 10px;
  padding-bottom: 10px;
  background-color: #191a1a;
  border-bottom: 1px solid gray;
}

.title {
  font-size: 32px;
  font-weight: bold;
  color:#ffffff;
}


/deep/ .el-tabs__item{
  color: #ffffff;
}

/deep/ .el-tabs__nav-wrap::after{
  background-color: gray;
  width: 1px !important;
}


/deep/ .el-tabs__item.is-active{
  color:#5866f2;
}

/deep/ .el-tabs__active-bar{
  background-color:#5866f2;
}

/deep/ .el-tabs--left .el-tabs__header.is-left{
  height: 700px;
}

/deep/ .el-tabs__item:hover{
  color: #5866f2;
}

/deep/ .el-tabs--left .el-tabs__active-bar.is-left, .el-tabs--left .el-tabs__active-bar.is-right, .el-tabs--right .el-tabs__active-bar.is-left, .el-tabs--right .el-tabs__active-bar.is-right {
  width: 1px !important;
}
</style>
