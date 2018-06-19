<template>
  <el-row class="warp">
    <el-col :span="24" class="warp-breadcrum">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }"><b>首页</b></el-breadcrumb-item>
        <el-breadcrumb-item>会员列表</el-breadcrumb-item>
      </el-breadcrumb>
    </el-col>

    <el-col :span="24" class="warp-main" v-loading="loading" element-loading-text="拼命加载中">
      <!--工具条-->
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" :model="filters">
          <el-form-item>
            <el-input v-model="filters.name" placeholder="会员姓名" @keyup.enter.native="handleSearch"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" v-on:click="handleSearch">查询</el-button>
          </el-form-item>
          <el-form-item>
            <el-input v-model="filters.mobile" placeholder="手机号" @keyup.enter.native="mobileSearch"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" v-on:click="mobileSearch">查询</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="showAddDialog">新增</el-button>
          </el-form-item>
        </el-form>
      </el-col>

      <!--列表-->
      <el-table :data="members" highlight-current-row @selection-change="selsChange"
                style="width: 100%;">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column type="index" width="60"></el-table-column>
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="[关联学生信息]">
                <span>{{ props.row.studentInfo }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="nickname" label="会员昵称" sortable></el-table-column>
        <el-table-column prop="name" label="会员名" sortable></el-table-column>
        <el-table-column prop="sex" label="性别" sortable></el-table-column>
        <el-table-column prop="address" label="地址" sortable></el-table-column>
        <el-table-column prop="memtype" label="会员级别" sortable></el-table-column>
        <el-table-column prop="mobile" label="手机" ></el-table-column>
        <el-table-column prop="email" label="邮箱" ></el-table-column>
        <el-table-column prop="birthday" label="生日" ></el-table-column>
        <el-table-column prop="education" label="学历" ></el-table-column>
        <el-table-column prop="industry" label="行业" ></el-table-column>
        <el-table-column prop="background" label="背景" ></el-table-column>
        <el-table-column prop="createtime" label="创建时间" width="120" sortable></el-table-column>
        <el-table-column prop="changetime" label="修改时间" width="120" sortable></el-table-column>
        <el-table-column prop="balance" label="余额" ></el-table-column>        
        <el-table-column label="操作" width="150">
          <template slot-scope="scope">
            <el-button size="small" @click="showEditDialog(scope.$index,scope.row)">编辑</el-button>
            <el-button type="danger" @click="delMember(scope.$index,scope.row)" size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!--工具条-->
      <el-col :span="24" class="toolbar">
        <el-button type="danger" @click="batchDeleteMember" :disabled="this.sels.length===0">批量删除</el-button>
        <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="10" :total="total"
                       style="float:right;">
        </el-pagination>
      </el-col>

      <el-dialog title="编辑" :visible.sync ="editFormVisible" :close-on-click-modal="false">
        <el-form :model="editForm" label-width="100px" :rules="editFormRules" ref="editForm">
          <el-form-item label="会员昵称" prop="nickname">
            <el-input v-model="editForm.nickname" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="会员名" prop="name" >
            <el-input v-model="editForm.name" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>

          <el-form-item label="地址" prop="address" auto-complete="off" :disabled="true">
            <el-input v-model="editForm.address" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="会员级别" prop="memtype" auto-complete="off" :disabled="true">
            <el-input v-model="editForm.memtype" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="手机" prop="mobile" auto-complete="off" :disabled="true">
            <el-input v-model="editForm.mobile" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="邮箱" prop="email" auto-complete="off" :disabled="true">
            <el-input v-model="editForm.email" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="余额" prop="balance" auto-complete="off" :disabled="true">
            <el-input v-model="editForm.balance" auto-complete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="editFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="editSubmit">提交</el-button>
        </div>
      </el-dialog>

      <!--新增界面-->
      <el-dialog title="新增" :visible.sync ="addFormVisible" :close-on-click-modal="false">
        <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
          <el-form-item label="会员昵称" prop="nickname">
            <el-input v-model="addForm.nickname" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="会员名" prop="name">
            <el-input v-model="addForm.name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="性别" prop="sex">
            <el-input v-model="addForm.sex" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="地址" prop="address">
            <el-input v-model="addForm.address" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="会员级别" prop="memtype">
            <el-input v-model="addForm.memtype" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="手机号" prop="mobile">
            <el-input v-model="addForm.mobile" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="addForm.email" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="生日" prop="birthday">
            <el-input v-model="addForm.birthday" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="学历" prop="education">
            <el-input v-model="addForm.education" auto-complete="off"></el-input>
          </el-form-item>          
          <el-form-item label="行业" prop="industry">
            <el-input v-model="addForm.industry" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="背景" prop="background">
            <el-input v-model="addForm.background" auto-complete="off"></el-input>
          </el-form-item>  
          <el-form-item label="余额" prop="balance">
            <el-input v-model="addForm.balance" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="线下店" prop="school_id">
            <el-input v-model="addForm.school_id" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="邀请者" prop="inviter_id">
            <el-input v-model="addForm.inviter_id" auto-complete="off"></el-input>
          </el-form-item>          
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="addFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
        </div>
      </el-dialog>

    </el-col>
  </el-row>
</template>
<script>
  import util from '../../common/util'
  import API from '../../api/api_member';

  export default{
    data(){
      return {
        filters: {
          name: '',
          mobile: ''
        },
        members: [],
        total: 0,
        page: 1,
        limit: 10,
        loading: false,
        sels: [], //列表选中列

        //编辑相关数据
        editFormVisible: false,//编辑界面是否显示
        editFormRules: {
          name: [
            {required: true, message: '请输入会员姓名', trigger: 'blur'}
          ]
        },
        editForm: {
          nickname: '',
          name: '',
          address: '',
          memtype: '',
          mobile: '',
          email: '',
          balance: ''
        },

        //新增相关数据
        addFormVisible: false,//新增界面是否显示
        addLoading: false,
        addFormRules: {
          name: [
            {required: true, message: '请输入会员姓名', trigger: 'blur'}
          ],
          nickname: [
            {required: true, message: '请输入会员昵称', trigger: 'blur'}
          ],
          balance: [
            {required: true, message: '请输入充值金额', trigger: 'blur'}
          ],          
          mobile: [
            {required: true, message: '请输入手机号', trigger: 'blur'}
          ]          
        },
        addForm: {
          nickname: '',
          name: '',
          sex: '',
          address: '',
          memtype: '',
          mobile: '',
          email: '',
          birthday: '',
          education: '',
          industry: '',
          background: '',
          balance: '',
          school_id: '',
          inviter_id: ''
        }
      }
    },
    methods: {
      handleCurrentChange(val) {
        this.page = val;
        console.log("val is: ");
        console.log(val)
        this.search();
      },

      mobileSearch(){
        console.log("mobile search");
        if (this.filters.mobile === '') {
          this.total = 0;
          this.page = 1;
          this.search();
        } else {
          this.total = 0;
          this.page = 1;
          this.SearchByMobile();
        }
      },
      SearchByMobile(){
        let that = this;
        that.loading = true;
        that.page = 1;
        that.total = 0;
        let param = that.filters.mobile;
        API.findById(param).then(function (result) {
          that.loading = false;
          if (result && result.members) {
            if (result.members.length > 0) {
               that.members = result.members;
               that.total = result.members.length;
            } else{
               that.$message.error({showClose: true, message: '查询不到该会员信息, 请确认手机号码！', duration: 5000});
            }
          }
          that.filters.mobile = '';

        }, function (err) {
          that.loading = false;
          that.$message.error({showClose: true, message: err.toString(), duration: 2000});
        }).catch(function (error) {
          that.loading = false;
          console.log(error);
          that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
        });

      },

      handleSearch(){
        this.total = 0;
        this.page = 1;
        this.search();
      },
      search(){
        let that = this;
        let params = {
          page: that.page,
          limit: 10,
          name: that.filters.name
        };

        that.loading = true;
        API.findList(params).then(function (result) {
          that.loading = false;
          console.log("receive get all members result")
          console.log(result)
          if (result && result.members) {
            if (result.members.length > 0) {
               that.total = result.total;
               that.members = result.members;
            } else{
               that.$message.error({showClose: true, message: '查询不到该会员信息', duration: 5000});
            }
          }

        }, function (err) {
          that.loading = false;
          that.$message.error({showClose: true, message: err.toString(), duration: 2000});
        }).catch(function (error) {
          that.loading = false;
          console.log(error);
          that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
        });
      },
      selsChange: function (sels) {
        this.sels = sels;
      },
      //删除
      delMember: function (index, row) {
        let that = this;
        this.$confirm('确认删除该记录吗?', '提示', {type: 'warning'}).then(() => {
          that.loading = true;
          console.log("row.nickname is");
          console.log(row.nickname);
          API.remove(row.nickname).then(function (result) {
            that.loading = false;
            console.log('result is ');
            console.log(result);
            if (result && parseInt(result.errcode) === 0) {
              that.$message.success({showClose: true, message: '删除成功', duration: 2000});
            } else{
              that.$message.success({showClose: true, message: '删除失败，请重试', duration: 2000});
            }
            that.filters.name = '';
            that.filters.mobile = '';
            that.search();       

          }, function (err) {
            that.loading = false;
            that.$message.error({showClose: true, message: err.toString(), duration: 2000});
          }).catch(function (error) {
            that.loading = false;
            console.log(error);
            that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
          });
        }).catch(() => {
        });
      },
      //显示编辑界面
      showEditDialog: function (index, row) {
        this.editFormVisible = true;
        this.editForm = Object.assign({}, row);
      },
      //编辑
      editSubmit: function () {
        let that = this;
        this.$refs.editForm.validate((valid) => {
          if (valid) {
            this.loading = true;
            let para = Object.assign({}, this.editForm);
            console.log("para.nickname is ");
            console.log(para);
            API.update(para.nickname, para).then(function (result) {
              that.loading = false;
              if (result && parseInt(result.errcode) === 0) {
                that.$message.success({showClose: true, message: '修改成功', duration: 4000});
                that.$refs['editForm'].resetFields();
                that.editFormVisible = false;
                that.search();
              } else {
                that.$message.error({showClose: true, message: '修改失败', duration: 2000});
              }
            }, function (err) {
              that.loading = false;
              that.$message.error({showClose: true, message: err.toString(), duration: 2000});
            }).catch(function (error) {
              that.loading = false;
              console.log(error);
              that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
            });
          }
        });
      },
      showAddDialog: function () {
        this.addFormVisible = true;
        this.addForm = {
          nickname: '',
          name: '',
          sex: '',
          address: '',
          memtype: '',
          mobile: '',
          email: '',
          birthday: '',
          education: '',
          industry: '',
          background: '',
          balance: '',
          school_id: '',
          inviter_id: ''
        };
      },
      //新增
      addSubmit: function () {
        let that = this;
        this.$refs.addForm.validate((valid) => {
          if (valid) {
            that.loading = true;
            let para = Object.assign({}, this.addForm);
            para.createtime = new Date().toLocaleDateString();
            para.changetime = new Date().toLocaleDateString();
            console.log("create time is ");
            console.log(para.createtime);
            API.add(para).then(function (result) {
              that.loading = false;
              if (result && parseInt(result.errcode) === 0) {
                that.$message.success({showClose: true, message: '创建新会员成功', duration: 2000});
                that.$refs['addForm'].resetFields();
                that.addFormVisible = false;
                that.search();
              } else {
                that.$message.error({showClose: true, message: '创建新会员失败', duration: 2000});
              }
            }, function (err) {
              that.loading = false;
              that.$message.error({showClose: true, message: err.toString(), duration: 2000});
            }).catch(function (error) {
              that.loading = false;
              console.log(error);
              that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
            });

          }
        });
      },
      //批量删除
      batchDeleteMember: function () {
        //let ids = this.sels.map(item => item.id).toString();
        let nicknames = this.sels.map(item => item.nickname).toString();
        let that = this;
        this.$confirm('确认删除选中记录吗？', '提示', {
          type: 'warning'
        }).then(() => {
          that.loading = true;
          API.removeBatch(nicknames).then(function (result) {
            that.loading = false;
            if (result && parseInt(result.errcode) === 0) {
              that.$message.success({showClose: true, message: '删除成功', duration: 1500});
              that.filters.name = '';
              that.filters.mobile = '';
              that.search();
            }
          }, function (err) {
            that.loading = false;
            that.$message.error({showClose: true, message: err.toString(), duration: 2000});
          }).catch(function (error) {
            that.loading = false;
            console.log(error);
            that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
          });
        }).catch(() => {

        });
      }
    },
    mounted() {
      this.handleSearch()
    }
  }
</script>

<style>
  .demo-table-expand label {
    font-weight: bold;
  }
</style>
