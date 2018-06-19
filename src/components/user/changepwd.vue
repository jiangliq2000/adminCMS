<template>
  <el-row class="warp">
    <el-col :span="24" class="warp-breadcrum" >
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }"><b>首页</b></el-breadcrumb-item>
        <el-breadcrumb-item>设置</el-breadcrumb-item>
        <el-breadcrumb-item>修改密码</el-breadcrumb-item>
      </el-breadcrumb>
    </el-col>

    <el-col :span="24" class="warp-main">
      <el-form ref="form" :model="form" label-width="120px">
        <el-form-item label="原密码">
          <el-input v-model="form.oldPwd"></el-input>
        </el-form-item>
        <el-form-item label="新密码">
          <el-input v-model="form.newPwd"></el-input>
        </el-form-item>
        <el-form-item label="确认新密码">
          <el-input v-model="form.confirmPwd"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="default" @click="handleChangepwd">提交</el-button>
        </el-form-item>
      </el-form>
    </el-col>
  </el-row>
</template>
<script>
  import API from '../../api/api_user';
  export default{
    data(){
      return {
        form: {
          oldPwd: '',
          newPwd: '',
          confirmPwd: ''
        }
      }
    },
    methods: {
      handleChangepwd() {
        let that = this;
        //this.$message({message:"此功能暂时未开发",duration:1500});
        if (that.form.newPwd !== that.form.confirmPwd) {
           that.$message({message: '两次输入的新密码不一致，请重新输入', type: 'error'});
        }
        else{
          let userInfo = sessionStorage.getItem('access-user');

          if (userInfo) {
             userInfo = JSON.parse(userInfo);
          }
          let para = {
            username: userInfo,
            oldpwd: that.form.oldPwd,
            newpwd: that.form.newPwd
          }  

          API.changePassword(para).then(function (result) {
            //this.loading = false;
            if (result && parseInt(result.errcode) === 0) {
              //修改成功
              that.$message.success({showClose: true, message: '修改成功, 5秒后将退出，请重新登录', duration: 5000});
              sessionStorage.removeItem('access-user');
              sessionStorage.removeItem('token');
              that.$router.go('/login'); //用go刷新       
            } else {
              that.$message.error({showClose: true, message: result.errmsg, duration: 2000});
            }
          }, function (err) {
            //this.loading = false;
            that.$message.error({showClose: true, message: err.toString(), duration: 2000});
          }).catch(function (error) {
            //this.loading = false;
            console.log(error);
            that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
          });

        }
      }
    }
  }
</script>
