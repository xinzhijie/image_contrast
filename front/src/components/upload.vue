<template>
  <el-scrollbar :style="{'height':min+'px'}" wrap-class="scrollbar-wrapper">
    <div style="margin: 20px">
      <el-row>
        <el-button @click="add()">新增</el-button>
      </el-row>
      <el-row :gutter="10" style="margin-top: 10px">
        <div v-for="(item, index) in tableList">
          <el-col :span="8">
            <el-card class="box-card">
              <el-row>
                <el-col :span="14">
                  <el-upload
                    :disabled="parseInt(item.status) > 0"
                    :show-file-list="false"
                    class="upload-demo"
                    action="/index"
                    :ref='"upload" + index'
                    :file-list="item.fileList"
                    :http-request="httpRequest"
                    :on-preview="handlePreview"
                    :on-remove="handleRemove"
                    :on-change="(file, fileList) => {onChange(file, fileList, index)}"
                    multiple
                    :auto-upload="false"
                    accept="image/jpeg,image/jpg,image/png"
                  >
                    <el-button :disabled="parseInt(item.status) > 0" slot="trigger" size="mini" type="primary">选取图片
                    </el-button>
                    <el-button
                      :disabled="parseInt(item.status) > 0"
                      style="margin-left: 10px;"
                      size="mini"
                      type="success"
                      @click="submitUpload(index, item.folder_name)"
                    >上传
                    </el-button>
                    <div slot="tip" class="el-upload__tip">当前选取{{ item.fileList.length }}张图片</div>
                    <div slot="tip" class="el-upload__tip">当前已经上传{{ parseInt(item.size) }}张图片</div>
                    <div slot="tip" class="el-upload__tip">只能上传jpg/png文件</div>
                    <el-button style="margin-top: 8px" slot="tip" :disabled="parseInt(item.status) > 0"
                               class="el-upload__tip" size="mini" @click="over(item)">结束上传
                    </el-button>
                    <el-button style="margin-top: 8px" slot="tip" :disabled="!(parseInt(item.status) < 2)"
                               class="el-upload__tip" size="mini" @click="deleteTask(item)">删除
                    </el-button>
                  </el-upload>
                </el-col>
                <el-col :span="10">
                  <div style="margin-top: 10px;height: 50px" v-if="parseInt(item.status) > 1">
                    <span style="font-size:13px" v-for="u in tableList[index].users">
                      <span v-if="u.id === item.user_id">指定用户:{{u.username}}</span>
                    </span>
                    <div  v-if="parseInt(item.status) === 3" style="margin-top: 10px;font-size:13px">
                      已经完成
                    </div>
                    <div v-else style="margin-top: 10px; font-size:13px;">未完成</div>
                    <div v-if="parseInt(item.status) === 3" style="margin-top: 50px">
                      <el-button size="mini" slot="tip" class="el-upload__tip" @click="download(item.folder_name)">标注下载
                      </el-button>
                      <el-button size="mini" slot="tip" class="el-upload__tip" @click="downloadResult(item.folder_name)">结果下载
                      </el-button>
                    </div>
                  </div>
                  <div style="height: 50px" v-else>
                    <div style="font-size:13px">指定人:</div>
                    <div>
                      <el-select :disabled="!(parseInt(item.status) === 1)" v-model="item.user_id" placeholder="请选择">
                        <el-option
                          v-for="u in users"
                          :key="u.id"
                          :label="u.username"
                          :value="u.id">
                        </el-option>
                      </el-select>
                    </div>
                    <div style="text-align: right;margin-top: 10px">
                      <el-button size="mini" :disabled="!(parseInt(item.status) === 1)" @click="complete(item)">确定
                      </el-button>
                    </div>
                  </div>
                </el-col>
              </el-row>
            </el-card>
          </el-col>
        </div>

      </el-row>

    </div>
  </el-scrollbar>
</template>
<script>
import Vue from 'vue'
import uuidv1 from 'uuid/v1'

export default {
  data () {
    return {
      value: '',
      tableList: [],
      users: [],
      min: ''
    }
  },
  methods: {
    deleteTask (item) {
      this.axios.get('deleteTask/' + item.id).then(res => {
        this.getTask()
        this.$message({
          message: '更新成功',
          type: 'success'
        })
      })
    },
    downloadResult (value) {
      window.location.href = 'download/' + value + '/result.xlsx'
    },
    download (value) {
      window.location.href = 'download/' + value + '/data.xlsx'
    },
    over (item) {
      if (item.size > 1) {
        item.status = 1
        this.axios.post('updateTask', item).then(res => {
          this.getTask()
          this.$message({
            message: '更新成功',
            type: 'success'
          })
        })
      } else {
        this.$message({
          message: '至少两张图片',
          type: 'success'
        })
      }

    },
    complete (item) {
      if (item.user_id === null || item.user_id === '') {
        this.$message({
          message: '清选择正确的人',
          type: 'success'
        })
      } else {
        item.status = 2
        this.axios.post('updateTask', item).then(res => {
          this.getTask()
          this.$message({
            message: '更新成功',
            type: 'success'
          })
        })
      }
    },
    add () {
      const temp = {
        'folder_name': uuidv1(),
        'size': 0,
        'fileList': [],
        'users': this.users,
        'user_id': '',
        'id': -1
      }
      this.tableList.unshift(temp)
    },
    httpRequest (file) {
      console.log(file)
    },
    submitUpload (index, folderName) {
      this.$refs['upload' + index][0].submit()
      let param = new FormData()
      this.tableList[index].fileList.forEach(file => {
        const isIMAGE = file.name.split('.')[file.name.split('.').length - 1] === 'jpeg' || 'jpg' || 'png'
        if (isIMAGE) {
          param.append('photo', file.raw)
          param.append('fileNames', file.name)
        }
      })
      param.append('folderName', folderName)
      this.$http
        .post('/index', param)
        .then(res => {
          this.tableList[index].id = res.data.id
          this.tableList[index].size = parseInt(this.tableList[index].size) + this.tableList[index].fileList.length
          this.tableList[index].fileList = []
          this.$message({
            message: '上传成功',
            type: 'success'
          })
        })
    },
    onChange (file, fileList, index) {
      this.tableList[index].fileList = fileList
    },
    handleRemove (file, fileList) {
      console.log(file, fileList)
    },
    handlePreview (file) {
      console.log(file)
    },
    getTask () {
      this.axios.get('getUsers').then(data => {

        this.axios
          .get('/getTask')
          .then(res => {
            const userList = []
            const tableList = res.data
            tableList.forEach(item => {
              Vue.set(item, 'fileList', [])
              Vue.set(item, 'users', JSON.parse(JSON.stringify(data.data)))
              item.user_id = parseInt(JSON.parse(JSON.stringify(item.user_id)))
              if (parseInt(item.status) === 2) {
                userList.push(item.user_id)
              }
            })
            this.tableList = JSON.parse(JSON.stringify(tableList))
            this.users = data.data.filter(i => {
              let num = 0
              userList.forEach(item => {

                if (parseInt(i.id) === item) {
                  num++
                }
              })
              if (num > 0) {
                return false
              } else {
                return true
              }
            })
          })
      })
    },
  },
  created () {
    this.min = (window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight) - 90
    this.getTask()
  }
}
</script>
<style>
  .el-scrollbar__wrap {
    overflow-x: hidden;
  }
</style>
