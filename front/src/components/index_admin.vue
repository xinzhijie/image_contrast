<template>
  <div>
    <el-row style="margin-top: 2px">
      <el-col :span="3">
        <el-scrollbar wrap-class="scrollbar-wrapper">
          <el-menu
            :style="{'height':min+'px'}"
            default-active="2"
            background-color="#545c64"
            class="el-menu-vertical-demo"
            @open="handleOpen"
            @close="handleClose">
            <el-menu-item @click="to('/upload')" index="2">
              <i class="el-icon-menu"></i>
              <span >数据上传</span>
            </el-menu-item>
            <el-menu-item @click="to('/userManage')" index="3">
              <i class="el-icon-document"></i>
              <span >用戶管理</span>
            </el-menu-item>
          </el-menu>
        </el-scrollbar>
      </el-col>
      <el-col :span="21">
        <el-row style="height: 40px">
          <span @click="loginOut()" style="line-height: 40px;float: right;margin-right: 10px;cursor:pointer">退出登录</span>
        </el-row>
        <hr>
        <router-view></router-view>
      </el-col>
    </el-row>
  </div>
</template>
<script>
export default {
  data () {
    return {
      min: ''
    }
  },
  methods: {
    loginOut(){
      this.$router.push({ path: 'login' })
    },
    to (path) {
      this.$router.push({ path: path })
    },
    handleOpen (key, keyPath) {
      console.log(key, keyPath)
    },
    handleClose (key, keyPath) {
      console.log(key, keyPath)
    }
  },
  created () {
    this.min = (window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight) - 17
  }
}
</script>
