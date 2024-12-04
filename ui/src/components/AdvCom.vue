<template>
  <div style="background-color:#ffffff;height: 600px">
    <div class="verification-page">
      <div class="steps-section">
        <div class="upload-section-title">对比流程</div>
        <el-steps :active="activeStep" align-center>
          <el-step title="上传广告设计图"></el-step>
          <el-step title="上传实际效果图"></el-step>
          <el-step title="执行对比处理"></el-step>
        </el-steps>
      </div>

      <div class="upload-section" style="height: 600px;">
        <el-row>
          <el-col :span="12" style="text-align: right;padding-right: 10px;padding-top: 30px">
            <el-upload class="upload-demo" drag ref="upload" :action="uploadHost" :data="uploadData"
                       :on-remove="handleFileRemove" accept=".jpg,.png,.jpeg"
                       :on-success="handleUploadSuccess" :file-list="fileList1"
                       :on-error="handleUploadError" multiple>
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">将【广告设计图】拖到此处或<em>点击上传</em></div>
              <div style="font-size:11px">(仅支持上传图片)</div>
            </el-upload>
          </el-col>
          <el-col :span="12" style="text-align: left; padding-left: 10px;padding-top: 30px">
            <el-upload class="upload-demo" drag ref="upload" :action="uploadHost" :data="uploadData"
                       :on-remove="handleFileRemove" accept=".jpg,.png,.jpeg"
                       :on-success="handleUploadSuccess" :file-list="fileList2"
                       :on-error="handleUploadError" multiple>
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">将实际【广告实际效果图】拖到此处或<em>点击上传</em></div>
              <div style="font-size:11px">(仅支持上传图片)</div>
            </el-upload>
          </el-col>
        </el-row>
      </div>
      <el-row style="padding-top: 30px">
        <el-col :span="24">
              <el-button type="primary" @click="adv_clean">清空对比文件</el-button>
              <el-button type="warning" @click="adv_compare" :loading="downloadLoading">执行对比处理</el-button>
        </el-col>
      </el-row>
      <el-divider></el-divider>
      <el-row style="padding-top: 2px;padding-bottom: 30px;">
        <el-col :span="24">
          <pre style="text-align: left;white-space: pre-wrap;">{{result}}</pre>
        </el-col>
      </el-row>

    </div>
  </div>
</template>

<script>
import api from '@/api/api';
export default {
  data() {
    return {
      apiHost: '',
      uploadHost: '',
      uploadData: {},
      currentSelectIndex:1,
      file_id1:'',
      file_id2:'',
      result:'',
      downloadLoading: false,
      activeStep: 4,
      fileList1: [],
      fileList2: [],
      tableList: [],
      loading: false,
      totalFiles: 0,
      formData: {
        clientId: "",
        key: '',
      },
      serverName: "",
      waitingProcessing: "0",
      refreshInterval: null,
      refreshText: "定时刷新",
      refreshSeconds: 10,
      submitLoading: false,
      dialogVisible: false,
      rules: {
        key: [
          { required: true, message: 'Please input Key', trigger: 'blur' }
        ]
      }

    };
  },
  methods: {

    adv_clean(){
      this.file_id1 = ''
      this.file_id2 = ''
      this.fileList1 = []
      this.fileList2 = []
      this.result=''
    },
    adv_compare(){
      console.log("file_id1="+this.file_id1);
      console.log("file_id2="+this.file_id2);
      this.result = 'Compare...'
      this.downloadLoading = true
      const compare_url = `${this.apiHost}?img_url_1=${this.file_id1}&img_url_2=${this.file_id2}`;
      api.post(compare_url, { responseType: 'text' })
          .then((response) => {
            this.result = response
            this.downloadLoading = false
            this.file_id1 = ''
            this.file_id2 = ''
          })
          .catch(error => {
            this.downloadLoading = false
            this.$message.error('Compare Failure');
            console.error('Compare Failure:', error);
          });
    },
    handleUploadSuccess(response, file) {
      if (response.status !== '') {
        this.$message.success(`${file.name} Upload successful.`);
        if(this.file_id1 === ''){
          console.log("index1");
          this.file_id1 = response.file_id
          this.fileList1 = [file];
        }else{
          console.log("index2");
          this.file_id2 = response.file_id
          this.fileList2 = [file];
        }
      } else {
        this.$message.error(`Upload failure`);
      }
    },
    handleUploadError(err, file) {
      this.$message.error(`${file.name} Upload failure`);
    },
    handleFileRemove() {
      this.fileList1 = [];
      this.fileList2 = [];
    },
  },

  mounted() {
    const mode = process.env.VUE_APP_MODE
    const baseURL = process.env.VUE_APP_BACKEND_HOST
    console.log("mode="+mode)
    if(mode === 'pro'){
      this.uploadHost = api.defaults.baseURL+"/ai/adv/agent/upload";
      this.apiHost = baseURL+"/ai/vl/compare";
    }else{
      this.uploadHost = "/api/ai/adv/agent/upload";
      this.apiHost = "/api/ai/vl/compare";
      api.defaults.baseURL = ""
    }
  },
};
</script>


<style>
.my-custom-prompt .el-button {
  background-color: #5866f2;
  border-color: #5866f2;
}

.my-custom-prompt .el-button:hover {
  background-color: #5866f2;
  border-color: #5866f2;
}

.my-custom-input .el-input__inner {
  border: 1px solid #5866f2;
  color: #333;
}

.my-custom-input .el-input__inner::placeholder {
  color: #5866f2;
}
</style>
<style scoped>
.nav-bar {
  padding: 2px;
  background-color: white;
}

.left-content {
  display: flex;
  align-items: center;
}

.logo {
  width: 32px;
  height: 32px;
  margin-right: 10px;
}

.title {
  font-size: 18px;
  font-weight: bold;
}

.right-content {
  display: flex;
  font-size: 13px;
  align-items: center;
  justify-content: flex-end;
}

.uuid-btn {
  background-color: #FAC070;
  color: white;
  font-size: 15px;
  padding: 10px;
  margin-right: 15px;
}

.client-info {
  display: flex;
  align-items: center;
}

.copy-link,
.settings-link {
  margin-left: 10px;
}

.verification-page {
  width: 90%;
  background-color: white;
  margin: 10px auto;
  padding: 10px 20px;

}

.steps-section {
  background-color: #F7F8FA;
  padding: 5px 0px;
}

.upload-section {
  margin: 20px 0px;
  display: inline;
}

.upload-btn {
  margin-top: -50px;
  text-align: right;
}


.upload-section-title {
  font-weight: bold;
  margin-left: 5%;
  text-align: left;
  font-size: 14px;
}

.upload-demo {
  margin-bottom: 10px;
}

.el-upload-text {
  font-size: 16px;
}

.file-list-section {}

.el-pagination {
  margin-top: 20px;
  text-align: right;
}


/deep/.el-step__title {
  font-size: 14px;
}

/deep/.el-upload-dragger {
  background-color: #F7F8FA !important;
  height: 120px;
}

/deep/.el-upload-dragger .el-icon-upload {
  line-height: 10px;
}

.el-table__header-wrapper th {
  background-color: #409EFF;
  color: #fff;
}

.upload__tip {
  display: flex;
  justify-content: flex-end;
}

.el-table .el-table__row {
  line-height: 30px;
}

/deep/.el-step__head.is-process .el-step__icon {
  background-color: #5866f2;
  border-color: #5866f2;
}

/deep/.el-step__head.is-finish {
  color: #5866f2;
  border-color: #5866f2;
}

/deep/.el-step__head.is-wait {
  border-color: #5866f2;
  background-color: #5866f2;
  color: #5866f2;
}

.el-step__icon {
  border-color: #5866f2;
}

/deep/.el-step__line {
  background-color: #5866f2;
}

/deep/.el-step__title.is-process {
  color: #5866f2;
}

.footer-btn {
  color: white;
  background-color: #5866f2;
}

/deep/.el-step__title.is-finish {
  color: #5866f2;
}

/deep/ .el-upload-dragger:hover {
  border-color: #5866f2;
}

/deep/ .el-upload-dragger .el-upload__text em {
  color: #5866f2;
}

/deep/ .el-table .descending .sort-caret.descending {
  border-top-color: #5866f2;
}

/deep/ .el-table .ascending .sort-caret.ascending {
  border-bottom-color: #5866f2;
}

.client-info button {
  color: #5866f2;
}

.el-pagination>>>.el-pager li.active {
  background-color: #5866f2 !important;
  border-color: #5866f2 !important;
  color: white !important;
}

.el-pagination>>>.el-pagination__btn {
  color: #5866f2 !important;
}

.el-pagination>>>.el-pagination__jump button {
  background-color: #5866f2 !important;
  color: white !important;
}

.el-pagination>>>.el-pager li:hover {
  color: #5866f2 !important;
  border-color: #5866f2 !important;
}
</style>
