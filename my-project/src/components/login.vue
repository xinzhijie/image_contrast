<template>
  <div>
  <div class="pannel" v-if="isIn">
    <div class="pannel-inner">
      <el-row>
        <el-col :span="1" :offset="24" style="color:rgba(0, 0, 0, 0.2);">
           &nbsp;
<!--          <i class="el-icon-close" v-on:click="close_sign" style="cursor:pointer;"></i>-->
        </el-col>
      </el-row>
      <div class="pannel-header">
        <span v-on:click="sign_in" style="cursor:pointer;color:#409eff;">登陆</span>·
        <span v-on:click="sign_up" style="cursor:pointer;">注册 </span></div>
      <el-input v-model="username_login" placeholder="用户名" style="margin-bottom: 5px;"></el-input>
      <el-input type="password" v-model="password_login" placeholder="密码"></el-input>
      <el-button type="primary" v-on:click="login()" size="medium" style="width: 100%; margin-top: 17px;">登陆</el-button>
    </div>
  </div>
  <!-- 注册框 -->
  <div class="pannel" v-if="isUp">
    <div class="pannel-inner">
      <el-row>
        <el-col :span="1" :offset="24" style="color:rgba(0, 0, 0, 0.2);">
          &nbsp;
<!--          <i class="el-icon-close" v-on:click="close_sign" style="cursor:pointer;"></i>-->
        </el-col>
      </el-row>
      <div class="pannel-header"><span v-on:click="sign_in" style="cursor:pointer;">登陆</span>·
        <span v-on:click="sign_up" style="cursor:pointer;color:#409eff;">注册 </span></div>
      <el-input v-model="username_registry" placeholder="用户名" style="margin-bottom: 5px;"></el-input>
      <el-input type="password" v-model="password_registry" placeholder="密码" style="margin-bottom: 5px;"></el-input>
      <el-input type="password" v-model="password_review" placeholder="请再次输入密码"></el-input>
      <el-button type="primary" @click="registry()" size="medium" style="width: 100%; margin-top: 17px;">注册</el-button>
    </div>
  </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      isUp: false,
      isIn: true,
      username_login: '',
      password_login: '',
      username_registry: '',
      password_registry: '',
      password_review: ''
    }
  },
  methods: {
    sign_in(){
      this.isUp = false
      this.isIn = true
    },
    sign_up(){
      this.isIn = false
      this.isUp = true
    },
    login() {
      const param = {'username': this.username_login, 'password': this.password_login}
      const that = this
      this.axios.post('login', param)
        .then(function (res) {
          if (res.data.status === 'ok') {
            sessionStorage.setItem('role', res.data.role)
            sessionStorage.setItem('accessToken', res.data.session)
            if (parseInt(res.data.role) === 10) {
              that.$router.push({path: '/adminIndex'})
            } else {
              that.$router.push({path: '/'})
            }

          } else {
            that.$message('账号或密码错误')
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    registry() {
      const param = {'username': this.username_registry, 'password': this.password_registry}
      this.$http
        .post('registry', param)
        .then(res => {
          if (res.data.status === 'ok') {
            this.$message('注册成功')
          } else {
            this.$message('注册失败有相同的用户名')
          }
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  created() {
    this.min = (window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight) - 34
  }
}
</script>
<style>
  .pannel {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    z-index: 1502;
    background-color: white;
  }
  .pannel-inner {
    position: absolute;
    background-color: white;
    left: 40%;
    top: 30%;
    width: 20%;
    /* border: solid #409eff 1px; */
    padding: 0 17px 17px 17px;
    font-size: 18px;
  }
  .pannel-header {
    margin-bottom: 7px;
    text-align: center;
  }
</style>
