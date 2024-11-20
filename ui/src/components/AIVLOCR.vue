<template>
  <div style="background-color:#F7F8FA;">
    <el-row type="flex" justify="space-between" class="nav-bar">
      <el-col :span="8" class="left-content">
        <img src="@/assets/logo.jpg" alt="logo" class="logo" />
        <span class="title">AI-VL-OCR</span>
      </el-col>
    </el-row>
    <div class="verification-page">
      <div class="upload-section">
        <el-row>
          <el-col :span="8" style="text-align: center;padding-right: 10px;padding-top: 50px;background-color: #2c3e50;height: 700px">
                        <el-upload class="upload-demo" drag ref="upload" :action="uploadHost" :data="uploadData"
                       :on-remove="handleFileRemove" accept=".jpg,.png,.jpeg,.pdf"
                       :on-success="handleUploadSuccess" :file-list="fileList1"
                       :on-error="handleUploadError" multiple>
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">Click upload <em>pdf/img</em></div>
            </el-upload>
            <el-button type="success" @click="adv_compare" :loading="downloadLoading">Run</el-button>
          </el-col>
           <el-col :span="16" style="text-align: left; padding-left: 10px;padding-top: 20px;background-color: #057748;height: 700px">
             right
           </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
import Clipboard from 'clipboard';
import api from '@/api/api';
export default {
  data() {
    return {
      apiHost: 'https://u260419-a935-26f44c0c.bjb1.seetacloud.com:8443',
      uploadHost: 'https://u260419-a935-26f44c0c.bjb1.seetacloud.com:8443/ai/adv/agent/upload',
      uploadData: {},
      currentSelectIndex:1,
      file_id1:'',
      file_id2:'',
      result:'',
      downloadLoading: false,
      activeStep: 4, // 当前核验步骤
      fileList1: [], // 文件列表
      fileList2: [], // 文件列表
      tableList: [],
      currentPage: 1, // 当前页数
      pageSize: 10, // 每页显示条数
      loading: false,
      totalFiles: 0, // 总文件数
      formData: {
        clientId: "",
        key: '',
      },
      serverName: "",
      waitingProcessing: "0",
      refreshInterval: null, // 列表刷新定时器
      refreshText: "定时刷新",
      refreshSeconds: 10,
      submitLoading: false, // 提交时的加载状态
      dialogVisible: false,
      rules: {
        clientId: [
          { required: true, message: '请输入客户端ID', trigger: 'blur' },
          { pattern: /^\d{10}$/, message: '客户端ID不正确（10位数字）', trigger: 'blur' }
        ],
        key: [
          { required: true, message: '请输入Key', trigger: 'blur' }
        ]
      }

    };
  },
  methods: {
    initClipboard() {
      const clipboard = new Clipboard('#copyButton', {
        text: () => this.formData.clientId,
      });
      clipboard.on('success', () => {
        this.$message.success('客户端ID复制成功！');
        clipboard.destroy()
      });
      clipboard.on('error', () => {
        this.$message.error('复制失败，请重试！');
        clipboard.destroy()
      });
    },
    open_set_user() {
      this.dialogVisible = true;
    }
    ,
    onChangeFile1(index) {
      console.log("index="+index);
      this.currentSelectIndex = index
    },
    onChangeFile2(index) {
      console.log("index="+index);
      this.currentSelectIndex = index
    },
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
      this.result = '对比处理中...'
      this.downloadLoading = true
      const compare_url = `/ai/adv/agent/compare?img_file_name1=${this.file_id1}&img_file_name2=${this.file_id2}`;
      api.post(compare_url, { responseType: 'text' })
          .then((response) => {
            this.result = response
            this.downloadLoading = false
            this.file_id1 = ''
            this.file_id2 = ''
          })
          .catch(error => {
            this.downloadLoading = false
            this.$message.error('对比失败');
            console.error('对比失败:', error);
          });


    },
    // 文件上传成功
    handleUploadSuccess(response, file) {
      if (response.status !== '') {
        this.$message.success(`${file.name} 上传成功`);
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
        this.$message.error(`上传失败`);
      }
    },
    handleFileChange(file, fileList) {
      // 每次上传新文件时清空列表，只保留新文件
      if (fileList.length > 1) {
        fileList.splice(0, fileList.length - 1); // 保留最后一个文件
      }
      this.fileList = fileList;
    },
    // 文件上传失败
    handleUploadError(err, file) {
      this.$message.error(`${file.name} 上传失败`);
    },
    handleFileRemove() {
      this.fileList = [];
    }
  },

  mounted() {
  },
  beforeDestroy() {
  }
};
</script>


<style>
.my-custom-prompt .el-button {
  background-color: #057748;
  border-color: #057748;
}
.my-custom-prompt .el-button:hover {
  background-color: #057748;
  border-color: #057748;
}
.my-custom-input .el-input__inner {
  border: 1px solid #057748;
  color: #333;
}
.my-custom-input .el-input__inner::placeholder {
  color: #057748;
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


.verification-page {
  width: 95%;
  min-height: 700px;
  background-color: white;
  margin: 10px 20px;
  padding: 10px 20px;

}

.upload-section {
  margin: 20px 0px;
  display: inline;
}

.upload-demo {
  margin-bottom: 10px;
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
  /* Background color */
  color: #fff;
  /* Text color */
}


.el-table .el-table__row {
  line-height: 30px;
}

/deep/.el-step__head.is-process .el-step__icon {
  background-color: #057748;
  border-color: #057748;
}

/deep/.el-step__head.is-finish {
  color: #057748;
  border-color: #057748;
}

/deep/.el-step__head.is-wait {
  border-color: #057748;
  background-color: #057748;
  color: #057748;
}

.el-step__icon {
  border-color: #057748;
}

/deep/.el-step__line {
  background-color: #057748;
}

/deep/.el-step__title.is-process {
  color: #057748;
}

.footer-btn {
  color: white;
  background-color: #057748;
}

/deep/.el-step__title.is-finish {
  color: #057748;
}

/deep/ .el-upload-dragger:hover {
  border-color: #057748;
}

/deep/ .el-upload-dragger .el-upload__text em {
  color: #057748;
}

/deep/ .el-table .descending .sort-caret.descending {
  border-top-color: #057748;
}

/deep/ .el-table .ascending .sort-caret.ascending {
  border-bottom-color: #057748;
}

.client-info button {
  color: #057748;
}


.el-pagination>>>.el-pager li.active {
  background-color: #057748 !important;
  border-color: #057748 !important;
  color: white !important;
}

.el-pagination>>>.el-pagination__btn {
  color: #057748 !important;
}

.el-pagination>>>.el-pagination__jump button {
  background-color: #057748 !important;
  color: white !important;
}

.el-pagination>>>.el-pager li:hover {
  color: #057748 !important;
  border-color: #057748 !important;
}
</style>
