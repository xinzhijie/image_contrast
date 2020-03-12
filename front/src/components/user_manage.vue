<template>
  <div style="margin: 50px">
    <el-scrollbar wrap-class="scrollbar-wrapper">
      <el-table
        :style="{'height':min+'px'}"
        border
        :data="tableData"
        style="width: 100%;">
        <el-table-column
          align="center"
          label="账号"
          width="180">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.username }}</span>
          </template>
        </el-table-column>
        <el-table-column
          align="center"
          label="密码"
        >
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.password }}</span>
          </template>
        </el-table-column>
      </el-table>
    </el-scrollbar>
  </div>
</template>

<script>
export default {
  data () {
    return {
      min: '',
      tableData: []
    }
  },
  methods: {},
  created () {
    this.min = (window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight) - 200
    this.axios
      .get('/getUsers')
      .then(res => {
        this.tableData = res.data
      })
  }
}
</script>
