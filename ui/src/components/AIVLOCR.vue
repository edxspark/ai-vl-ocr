<template>
  <div>
    <div class="verification-page">
      <div class="upload-section">
        <el-row>
           <el-col :span="16" style="overflow-y: auto;border-radius:8px 0px 0px 8px;text-align: left; padding-left: 10px;padding-top: 10px; background-color: #2c3e50;height: 600px">
               <div>
                 <vue-markdown :source="markdownContent" style="color: #ffffff;font-size: 14px"></vue-markdown>
               </div>
           </el-col>
          <el-col :span="8" style="border-radius:0px 8px 8px 0px;text-align: center;padding-right: 10px;padding-top: 50px;background-color: #2c3e50;border-left: 1px solid gray;height: 600px">
            <el-form ref="form" :model="form" label-width="0px" label-position="right">
<!--                <el-form-item label="DocType" >-->
<!--                  <el-select v-model="form.docType" placeholder="" style="width: 300px">-->
<!--                    <el-option label="IMG" value="IMG"></el-option>-->
<!--                    <el-option label="PDF" value="PDF"></el-option>-->
<!--                  </el-select>-->
<!--                </el-form-item>-->
                <el-form-item label="ReturnType">
                  <el-select v-model="form.returnType" placeholder="" style="width: 300px">
                    <el-option label="MARKDOWN" value="MARKDOWN"></el-option>
                    <el-option label="JSON" value="JSON"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="Prompt">
                  <el-input type="textarea" v-model="form.prompt" rows="5" style="width: 300px"></el-input>
                </el-form-item>
              </el-form>
            <el-upload class="upload-demo" drag ref="upload" :action="uploadHost" :data="uploadData"
                       :before-upload="beforeUpload"
                       :on-remove="handleFileRemove" accept=".jpg,.png,.jpeg,.pdf"
                       :on-success="handleUploadSuccess" :file-list="fileList1"
                       :on-error="handleUploadError" multiple>
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">Click upload <em>pdf/img</em></div>
            </el-upload>
          </el-col>

        </el-row>
      </div>
    </div>
    <div style="padding-top: 10px">
    <span>Power By @EdxSpark</span>
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
        returnType:'MARKDOWN',
        prompt:'Help me accurately identify the content of the file'
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
        console.log(result)
        this.markdownContent = result;
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

    this.markdownContent = "" +
        "        A very simple way of OCR-ing a document of AI vision.\n" +
        "        Documents are meant to be a visual representation after all.\n" +
        "        With weird layouts, tables, charts, etc.\n" +
        "        The vision models just make sense!\n" +
        "\n" +
        "        The general logic:\n" +
        "        - Pass in a file (pdf, image, etc.)\n" +
        "        - Convert that file into a series of images\n" +
        "        - Pass each image to AI vision LLM and ask nicely for Markdown\n" +
        "        - Aggregate the responses and return Markdown or JSON";
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
  min-height: 700px;
  background-color: white;
  margin: 10px 20px;

}

.upload-section {
  margin: 20px 0px;
  display: inline;
}

.upload-demo {
  margin-bottom: 10px;
  margin-top: 20px;
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
