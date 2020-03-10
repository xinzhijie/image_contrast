<template>
<el-row class="tac">

    <el-col style="text-align: center"  :span="5">
      <el-row>
        <el-col style="text-align: center" :span="18">
          <el-scrollbar wrap-class="scrollbar-wrapper">
            <div style="text-align: center;float: left;width: 100%" :style="{'height':min+'px'}">
<!--              <div >-->
<!--                <router-link style="width: 150px;background-color: grey;color: white" tag="el-button" to='/upload'>数据上传</router-link>-->
<!--              </div>-->
              <div style="margin-top: 10px">
                <router-link style="width: 150px;background-color: grey;color: white" tag="el-button" to='/contrast'>数据对比</router-link>
              </div>
              <div style="margin-top: 10px">
                <router-link style="width: 150px;background-color: grey;color: white" tag="el-button" to='/download'>数据下载</router-link>
              </div>
            </div>
          </el-scrollbar>
        </el-col>
        <el-col :span="4">
          <div  style="float: left;text-align: center" :style="{'height':min+'px'}" class="link-right"></div>
        </el-col>
      </el-row>
    </el-col>

  <el-col :span="18">
    <router-view></router-view>
  </el-col>
</el-row>
</template>
<script>
export default {
  data() {
    return {
      min: ''
    }
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
    download() {
      window.location.href = '/download'
    }
  },
  created() {
    this.min = (window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight) - 34
  }
}
</script>
<style>
  .link-right {
    border-right: solid gray 1px;
  }
</style>
