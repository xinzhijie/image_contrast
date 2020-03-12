<template>
  <div style="margin: 30px">
    <el-scrollbar :style="{'height':min+'px'}" wrap-class="scrollbar-wrapper">
      <el-table
        :style="{'height':min+'px'}"
        border
        :data="tableData"
        style="width: 100%">
        <el-table-column
          align="center"
          label="日期"
          width="180">
          <template slot-scope="scope">
            <i class="el-icon-time"></i>
            <span style="margin-left: 10px">{{ scope.row.create_time | timeString }}</span>
          </template>
        </el-table-column>
        <el-table-column
          align="center"
          label="标注数量"
          width="180">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.size }}</span>
          </template>
        </el-table-column>
        <el-table-column align="center" label="操作">

          <template slot-scope="scope">
            <el-button
              size="mini"
              @click="download(scope.$index, scope.row)">标注下载
            </el-button>
            <el-button
              size="mini"
              @click="downloadResult(scope.$index, scope.row)">结果下载
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-scrollbar>
  </div>
</template>

<script>
export default {
  filters: {
    timeString: function (time) {
      const now = new Date(parseInt(time) * 1000)
      const year = now.getFullYear()
      const month = now.getMonth() + 1
      const date = now.getDate()
      const hour = now.getHours()
      const minute = now.getMinutes()
      const second = now.getSeconds()
      return year + '-' + month + '-' + date + ' ' + hour + ':' + minute + ':' + second
    }
  },
  data () {
    return {
      min: '',
      tableData: []
    }
  },
  methods: {
    downloadResult (index, row) {
      window.location.href = 'download/' + row.folder_name + '/result.xlsx'
    },
    download (index, row) {
      window.location.href = 'download/' + row.folder_name + '/data.xlsx'
    },
    handleDelete (index, row) {
      console.log(index, row)
    }
  },
  created () {
    this.min = (window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight) - 200
    this.axios
      .get('/getTask')
      .then(res => {
        this.tableData = res.data.filter(item => {
          if (item.user_id === sessionStorage.getItem('accessToken') && parseInt(item.status) === 3) {
            return true
          }
        })
      })
  }
}
</script>
<style>
  .el-scrollbar__wrap {
    overflow-x: hidden;
  }
</style>
