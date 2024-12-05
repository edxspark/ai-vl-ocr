<template>
  <div>
    <div class="verification-page">
      <div class="upload-section">
        <el-row>
           <el-col :span="16" style="overflow-y: auto;text-align: left; padding-left: 10px;padding-top: 10px; background-color: #202222;height: 650px">
               <div>
                 <vue-markdown :source="markdownContent" style="color: #ffffff;font-size: 14px"></vue-markdown>
               </div>
           </el-col>
          <el-col :span="8" style="text-align: center;padding-right: 20px;padding-top: 50px;background-color: #202222;border-left: 1px solid gray;height: 650px">
            <el-form ref="form" :model="form" label-width="80px" label-position="right">
                <el-form-item label="返回类型">
                  <el-select v-model="form.returnType" placeholder="" style="width: 300px">
                    <el-option label="JSON" value="JSON"></el-option>
                    <el-option label="MARKDOWN" value="MARKDOWN"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="提取描述">
                  <el-input type="textarea" v-model="form.prompt" rows="5" style="width: 300px"></el-input>
                </el-form-item>
              </el-form>

            <el-upload class="upload-demo" drag ref="upload" :action="uploadHost" :data="uploadData"
                       :before-upload="beforeUpload"
                       :on-remove="handleFileRemove" accept=".jpg,.png,.jpeg,.pdf"
                       :on-success="handleUploadSuccess" :file-list="fileList1"
                       :on-error="handleUploadError" multiple>
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">上传 <em>pdf/img</em></div>
            </el-upload>
            <div style="color: #ffffff;font-size: 14px;margin-left: 120px">上传完文件，自动触发识别</div>
          </el-col>

        </el-row>
      </div>
    </div>
    <div style="padding-top: 10px">
    <span></span>
    </div>
  </div>

</template>


<script>
import VueMarkdown from 'vue-markdown';
import api from "@/api/api";
export default {
  components: {
      'vue-markdown': VueMarkdown
    },
  data() {
    return {
      uploadHost: '',
      uploadData: {docType:'',returnType:'',prompt:''},
      file_id1:'',
      markdownContent:'',
      form:{
        docType:'IMG',
        returnType:'JSON',
        prompt:'帮我提取文件中：姓名、车牌号、金额'
      },
      result:'',
      downloadLoading: false,
      activeStep: 4,
      fileList1: [],
      tableList: [],
      loading: false,
      formData: {
        clientId: "",
        key: '',
      },
      submitLoading: false,
      dialogVisible: false,
      rules: {
      }
    }
  },
  methods: {
    handleUploadSuccess(response,file) {
        let result = response
        this.fileList1=[file]
        console.log("result="+result)
        if(this.form.returnType === "JSON"){
          this.markdownContent = JSON.stringify(result);
        }else{
          this.markdownContent = result;
        }
    },
    handleUploadError(err, file) {
      this.$message.error(`${file.name} Failure`);
    },
    handleFileRemove() {
    },
    beforeUpload(file){
      this.markdownContent = "# OCR-ing, please wait...."
      console.log("fileType:"+file.type)
      this.fileList1=[file]
      const fileType = file.type
      if(fileType==="image/png" || fileType==="image/jpg" || fileType==="image/jpeg"){
          this.uploadData.docType="IMG";
      }else{
        this.uploadData.docType="PDF";
      }
      this.uploadData.returnType=this.form.returnType;
      this.uploadData.prompt=this.form.prompt;
    }
  },

  mounted() {
    const mode = process.env.VUE_APP_MODE
    console.log("mode="+mode)
    if(mode === 'pro'){
      this.uploadHost = api.defaults.baseURL+"/ai/vl/ocr";
    }else{
      this.uploadHost = "/api/ai/vl/ocr";
    }

    this.markdownContent = "## 一种非常简单的OCR AI视觉识别\n" +
        "\n" +
        "- 把文档转成图片进行视觉识别，\n" +
        "\n" +
        "- 识别文档的布局、表格、图表等。\n" +
        "\n" +
        "## 处理逻辑\n" +
        "\n" +
        "- 传入文件（pdf、图像等）\n" +
        "\n" +
        "- 将该文件转换为一系列图像\n" +
        "\n" +
        "- 将每张图片传递给AIVL LLM\n" +
        "\n" +
        "- 聚合响应并返回Markdown或JSON";
  },
  beforeDestroy() {
  }
};
</script>


<style scoped>


.left-content {
  display: flex;
  align-items: center;
}

.logo {
  width: 48px;
  height: 36px;
  margin-right: 2px;
}

.title {
  font-family: 'circular,sans-serif';
  font-size: 32px;
  font-weight: bold;
  color:#5866f2;
}


.verification-page {
  width: 95%;
  height: 100%;
  background-color: #371F6D;
  margin-top: 10px;
}

.upload-section {
  margin: 20px 0px;
  display: inline;
}

.upload-demo {
  margin-bottom: 10px;
  margin-top: 20px;
  margin-left: 110px;
}

/deep/ .el-form-item__label{
  color: #ffffff;
  margin-left: 20px;
}

/deep/.el-divider--horizontal {
  font-size: 14px;
  margin-top: 2px;
  margin-bottom: 2px;
}

</style>
