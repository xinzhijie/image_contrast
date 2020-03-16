<template>
  <div>
    <div v-show="info.length > 0" style="margin-left: 50px" class="container">
      <el-row>
        <el-col style="text-align: center">
          切换位置:
          <el-select v-model="value1" placeholder="请选择">
            <el-option
              v-for="item in options1"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
          <el-select v-model="value2" placeholder="请选择">
            <el-option
              v-for="item in options2"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
          <el-button type="primary" @click="jump()">确定</el-button>
        </el-col>
      </el-row>
      <el-row style="margin-top: 80px">
        <el-col :span="10">
          <div style="text-align:center">
            <div>第{{arr[0]}}张</div>
            <div style="margin-top: 10px"><img class="exam" style="width: 300px;height: 300px" :src="image1"/></div>
          </div>
        </el-col>
        <el-col style="text-align:center" :span="4">
          <div style="margin-top: 10px">
            <el-button :type="bt1" @click="check(5)" round>明显强于</el-button>
          </div>
          <div style="margin-top: 10px">
            <el-button :type="bt2" @click="check(3)" round>略微强于</el-button>
          </div>
          <div style="margin-top: 10px">
            <el-button :type="bt3" @click="check(1)" round>&nbsp;&nbsp;相&nbsp;&nbsp;&nbsp;等&nbsp;&nbsp;</el-button>
          </div>
          <div style="margin-top: 10px">
            <el-button :type="bt4" @click="check(-3)" round>略微弱于</el-button>
          </div>
          <div style="margin-top: 10px">
            <el-button :type="bt5" @click="check(-5)" round>明显弱于</el-button>
          </div>
        </el-col>
        <el-col :span="10">
          <div style="text-align:center">
            <div>第{{arr[1]}}张</div>
            <div style="margin-top: 10px">
              <img class="exam" style="width: 300px;height: 300px" :src="image2"/>
            </div>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <div style="margin-top: 10px;text-align: center">
          <el-button @click="previous()">上一个</el-button>
          <el-button v-if="parseInt(size) - 1 === arr[0] && parseInt(size) === arr[1]" @click="submit()">提交</el-button>
          <el-button v-else @click="next()">下一个</el-button>
        </div>
      </el-row>
    </div>
    <div v-show="info.length === 0" style="text-align: center">
      <h3>当前未分配数据</h3>
    </div>
  </div>

</template>
<script>
export default {
  data () {
    return {
      min: '',
      verify: 0,
      arr: [1, 2],
      size: 0,
      image1: '',
      image2: '',
      bt1: 'primary',
      bt2: 'primary',
      bt3: 'primary',
      bt4: 'primary',
      bt5: 'primary',
      disableValue: false,
      nextName: '下一个',
      options1: [],
      value1: '',
      options2: [],
      value2: '',
      excelValue: '',
      info: []
    }
  },
  methods: {
    getTask () {
      this.axios
        .get('/getTask')
        .then(res => {
          this.axios
            .get('/getTaskBean')
            .then(res => {
              this.arr[0] = parseInt(res.data.place.split('-')[0])
              this.arr[1] = parseInt(res.data.place.split('-')[1])
              this.getValue(this.arr)
              this.getImage(this.arr[0], '1')
              this.getImage(this.arr[1], '2')
            })
          this.info = res.data.filter(item => {
            if (item.user_id === sessionStorage.getItem('accessToken') && parseInt(item.status) === 2) {
              return true
            }
          })
        })
    },
    primary (value) {
      this.bt1 = 'primary'
      this.bt2 = 'primary'
      this.bt3 = 'primary'
      this.bt4 = 'primary'
      this.bt5 = 'primary'
      if (value === 5) {
        this.bt1 = ''
        this.verify = 1
      } else if (value === 3) {
        this.bt2 = ''
        this.verify = 1
      } else if (value === 1) {
        this.bt3 = ''
        this.verify = 1
      } else if (value === -3) {
        this.bt4 = ''
        this.verify = 1
      } else if (value === -5) {
        this.bt5 = ''
        this.verify = 1
      }
    },
    getV (arr) {
      const that = this
      return new Promise(function (resolve, reject) {
        that.axios
          .post('getValue/' + arr[0] + '/' + arr[1])
          .then(res => {
            that.excelValue = res.data
            resolve()
          })
          .catch(error => {
            console.log(error)
          })
      })
    },
    jump () {
      const arr = [this.size - 1, this.size]

      this.getV(arr).then(res => {
        if (this.excelValue !== 0 && this.excelValue !== '') {
          if (this.value1 === '' || this.value2 === '') {
            this.$message({
              showClose: true,
              message: '请选择位置'
            })
          } else if (this.value1 === this.value2) {
            this.$message({
              showClose: true,
              message: '不能选择相同的位置'
            })
          } else {
            this.arr[0] = this.value1 > this.value2 ? this.value2 : this.value1
            this.arr[1] = this.value1 < this.value2 ? this.value2 : this.value1
            this.getValue(this.arr)
            this.getImage(this.arr[0], '1')
            this.getImage(this.arr[1], '2')
            this.nextName = '下一个'
          }
        } else {
          this.$message({
            showClose: true,
            message: '请标记完全部在进行切换'
          })
        }
      })
    },
    check (value) {
      this.primary(value)
      this.axios
        .post('update_excel/' + this.arr[0] + '/' + this.arr[1] + '/' + value)
        .then(res => {
          let message = '左侧图片'
          if (parseInt(value) === 5) {
            message += '明显强于'
          } else if (parseInt(value) === 3) {
            message += '略微强于'
          } else if (parseInt(value) === 1) {
            message += '相等'
          } else if (parseInt(value) === -3) {
            message += '略微弱于'
          } else if (parseInt(value) === -5) {
            message += '略微明显'
          }
          message = message + '右侧图片'
          this.$message('标注成功: ' + message)
          this.verify = 1
        })
        .catch(error => {
          console.log(error)
        })
    },
    previous () {
      this.nextName = '下一个'
      if (this.arr[1] - 1 !== 1) {
        this.arr[1] = this.arr[1] - 1
        if (this.arr[1] <= this.arr[0]) {
          this.arr[0] = this.arr[0] - 1
          this.arr[1] = this.size
        }
        this.getValue(this.arr)
        this.getImage(this.arr[0], '1')
        this.getImage(this.arr[1], '2')
      }
    },
    next () {
      if (this.verify > 0) {
        if ((this.arr[0] === this.size - 2 && this.arr[1] === this.size) ||
          (this.arr[0] === this.size - 1 && this.arr[1] === this.size)) {
          this.nextName = '提交'
        } else {
          this.verify = 0
          this.primary(6)
          this.nextName = '下一个'
        }

        if (!(this.arr[0] === this.size - 1 && this.arr[1] === this.size)) {
          this.arr[1] = this.arr[1] + 1
          if (this.arr[1] > this.size) {
            this.arr[0] = this.arr[0] + 1
            this.arr[1] = this.arr[0] + 1
          }
          this.getValue(this.arr)
          this.getImage(this.arr[0], '1')
          this.getImage(this.arr[1], '2')
        } else {
          this.$message('已经是最后一个')
        }
      } else {
        this.$message('请先进行标注')
      }
    },
    getValue (arr) {
      this.axios
        .post('getValue/' + arr[0] + '/' + arr[1])
        .then(res => {
          this.primary(parseInt(res.data))
        })
        .catch(error => {
          console.log(error)
        })
    },
    submit () {
      this.$confirm('此操作将提交全部，且不能被修改, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.axios.post('submit').then(res => {
          this.getTask()
          this.$message({
            message: '提交成功',
            type: 'success'
          })
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消'
        })
      })
    },
    getImage (value, id) {
      this.axios
        .post('open/' + value)
        .then(res => {
          if (id === '1') {
            this.image1 = res.data
          } else {
            this.image2 = res.data
          }

        })
        .catch(error => {
          console.log(error)
        })
    },
    getSize () {
      this.axios
        .post('page_list')
        .then(res => {
          this.size = res.data
          if (this.size === 2) {
            this.nextName = '提交'
          }
          if (res.data > 1) {
            this.disableValue = true
            for (let i = 1; i <= res.data; i++) {
              const item = {value: i, label: i}
              this.options1.push(item)
            }
            this.options2 = JSON.parse(JSON.stringify(this.options1))
          }

        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  created () {
    this.getTask()
    this.min = (window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight) - 34
    this.getSize()
  }
}
</script>
<style>
  .exam {
    border-width: 1px;
    border-color: black;
    border-style: double;
  }
</style>
