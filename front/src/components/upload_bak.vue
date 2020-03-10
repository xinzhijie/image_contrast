<template>
  <el-upload
    class="upload-demo"
    action="/index"
    ref="upload"
    :http-request="httpRequest"
    :on-preview="handlePreview"
    :on-remove="handleRemove"
    :on-change="onChange"
    multiple
    :on-exceed="handleExceed"
    :file-list="fileList"
    :auto-upload="false"
    accept="image/jpeg,image/jpg,image/png"
  >
    <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
    <el-button
      style="margin-left: 10px;"
      size="small"
      type="success"
      @click="submitUpload"
    >上传到服务器</el-button>
     <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
  </el-upload>
</template>
<script>
export default {
  data () {
    return {
      fileList: []
    };
  },
  methods: {
    httpRequest (file) {
      console.log(file);
    },
    submitUpload (file) {
      this.$refs.upload.submit()
      let param = new FormData()
      this.fileList.forEach(file => {
        const isIMAGE = file.name.split('.')[file.name.split('.').length - 1] === 'jpeg' || 'jpg' || 'png'
        if (isIMAGE) {
          param.append('photo', file.raw)
          param.append('fileNames', file.name)
        }
      })
      this.$http
        .post('/index', param)
        .then(res => {
          this.fileList = []
          this.$message({
            message: "上传成功",
            type: "success"
          })
        })
        .catch(error => {
          // console.log(error);
        })

    },
    onChange (file, fileList) {
      this.fileList = fileList;
    },
    handleRemove (file, fileList) {
      console.log(file, fileList);
    },
    handlePreview (file) {
      console.log(file);
    },
    handleExceed (files, fileList) {
      this.$message.warning(
        `当前限制选择 5 个文件，本次选择了 ${
          files.length
        } 个文件，共选择了 ${files.length + fileList.length} 个文件`
      )
    }
  }
}
</script>
