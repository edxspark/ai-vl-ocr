<template>
  <div id="app">
    <el-row type="flex" justify="space-between" class="nav-bar">
      <el-col :span="8" class="left-content">
        <img src="@/assets/logo.jpg" alt="logo" class="logo" />
        <span class="title">superforu-ai-ocr</span>
      </el-col>
      <el-col :span="8" style="vertical-align: middle">
        <span style="font-weight: bold;">AI vision document OCR</span>
      </el-col>
    </el-row>

  <el-tabs tab-position="left" style="height: 100%">
    <el-tab-pane label="AIOCR">
       <AIVLOCR msg="Welcome to Superforu AI OCR" />
    </el-tab-pane>
    <el-tab-pane label="图对比" style="height: 100%">
      <AdvCom msg="Adv Compare" />
    </el-tab-pane>
  </el-tabs>


  </div>
</template>

<script>
import AIVLOCR from './components/AIVLOCR.vue'
import AdvCom from './components/AdvCom.vue'

export default {
  components:{AIVLOCR,AdvCom}
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
  padding-bottom: 10px;
  background-color: white;
  border-bottom: #E4E7ED solid 1px;
}

.title {
  font-size: 32px;
  font-weight: bold;
  color:#5866f2;
}

/deep/ .el-tabs__item.is-active{
  color:#5866f2;
}

/deep/ .el-tabs__active-bar{
  background-color:#5866f2;
}

/deep/ .el-tabs--left .el-tabs__header.is-left{
  height: 600px;
}

/deep/ .el-tabs__item:hover{
  color: #5866f2;
}
</style>
