<template>
  <el-row class="warp">
    <el-col :span="24" class="warp-breadcrum">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }"><b>首页</b></el-breadcrumb-item>
        <el-breadcrumb-item>学生列表</el-breadcrumb-item>
      </el-breadcrumb>
    </el-col>

    <el-col :span="24" class="warp-main" v-loading="loading" element-loading-text="拼命加载中">
      <!--工具条-->
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" :model="filters">
          <el-form-item>
            <el-input v-model="filters.name" placeholder="学生姓名" @keyup.enter.native="handleSearch"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" v-on:click="handleSearch">查询</el-button>
          </el-form-item>
          <el-form-item>
            <el-input v-model="filters.uid" placeholder="学生学号" @keyup.enter.native="uidSearch"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" v-on:click="uidSearch">查询</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="showAddDialog">新增</el-button>
          </el-form-item>
        </el-form>
      </el-col>

      <!--列表-->
      <el-table :data="students" highlight-current-row @selection-change="selsChange"
                style="width: 100%;">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column type="index" width="60"></el-table-column>
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="[授课教师信息]">
                <span>{{ props.row.studentInfo }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="uid" label="学号" sortable></el-table-column>
        <el-table-column prop="name" label="姓名" sortable></el-table-column>
        <el-table-column prop="nickname" label="昵称" sortable></el-table-column>    
        <el-table-column prop="sex" label="性别" sortable></el-table-column>
        <el-table-column prop="urgent_contactor" label="紧急联系人" ></el-table-column>
        <el-table-column prop="urgent_mobile" label="紧急联系人手机" ></el-table-column>
        <el-table-column prop="birthday" label="生日" ></el-table-column>
        <el-table-column prop="education" label="学历" ></el-table-column>
        <el-table-column prop="image_url" label="头像" ></el-table-column>
        <el-table-column prop="mentor_id" label="授课教师" ></el-table-column>
        <el-table-column prop="c_time" label="创建时间" width="120" sortable></el-table-column>
        <el-table-column label="操作" width="150">
          <template slot-scope="scope">
            <el-button size="small" @click="showEditDialog(scope.$index,scope.row)">编辑</el-button>
            <el-button type="danger" @click="delStudent(scope.$index,scope.row)" size="small">删除</el-button>
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
          <el-form-item label="学号" prop="uid" >
            <el-input v-model="editForm.uid" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="姓名" prop="name" >
            <el-input v-model="editForm.name" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="性别" prop="sex" >
            <el-input v-model="editForm.sex" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>          
          <el-form-item label="紧急联系人" prop="urgent_contactor" >
            <el-input v-model="editForm.urgent_contactor" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="紧急联系人手机" prop="urgent_mobile" auto-complete="off" >
            <el-input v-model="editForm.urgent_mobile" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="生日" prop="birthday" auto-complete="off" >
            <el-input v-model="editForm.birthday" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="学历" prop="education" auto-complete="off" >
            <el-input v-model="editForm.education" auto-complete="off"></el-input>
          </el-form-item>          
          <el-form-item label="头像" prop="image_url" auto-complete="off" :disabled="true">
            <el-input v-model="editForm.image_url" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="授课教师" prop="mentor_id" auto-complete="off" :disabled="true">
            <el-input v-model="editForm.mentor_id" auto-complete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="editFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="editSubmit">提交</el-button>
        </div>
      </el-dialog>

      <!--新增学生界面-->
      <el-dialog title="新增学生" :visible.sync ="addFormVisible" :close-on-click-modal="false">
        <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
          <el-row>
            <el-col :span="8">
                <el-form-item label="学号" prop="uid">
                  <el-input v-model="addForm.uid" auto-complete="off"></el-input>
                </el-form-item>
            </el-col>
            <el-col :span="8">
                <el-form-item label="姓名" prop="name">
                  <el-input v-model="addForm.name" auto-complete="off"></el-input>
                </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="昵称" prop="nickname">
                <el-input v-model="addForm.nickname" auto-complete="off"></el-input>
              </el-form-item>   
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="8">
              <el-form-item label="性别" prop="sex">
                <el-input v-model="addForm.sex" auto-complete="off"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="生日" prop="birthday" auto-complete="off" >
                <el-input v-model="addForm.birthday" auto-complete="off"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="学历" prop="education" auto-complete="off" >
                 <el-input v-model="addForm.education" auto-complete="off"></el-input>
              </el-form-item> 
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
                <el-form-item label="紧急联系人" prop="urgent_contactor" >
                  <el-input v-model="addForm.urgent_contactor" auto-complete="off"></el-input>
                </el-form-item>
            </el-col>
            <el-col :span="12">
                <el-form-item label="紧急联系人手机" prop="urgent_mobile" auto-complete="off" >
                  <el-input v-model="addForm.urgent_mobile" auto-complete="off"></el-input>
                </el-form-item>
            </el-col>
          </el-row>         
          <el-form-item label="头像" prop="image_url" auto-complete="off" :disabled="true">
            <el-input v-model="addForm.image_url" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="授课教师" prop="mentor_id" auto-complete="off" :disabled="true">
            <el-input v-model="addForm.mentor_id" auto-complete="off"></el-input>
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
  import API from '../../api/api_student';

  export default{
    data(){
      return {
        filters: {
          name: '',
          uid: ''
        },
        students: [],
        total: 0,
        page: 1,
        limit: 10,
        loading: false,
        sels: [], //列表选中列

        //编辑相关数据
        editFormVisible: false,//编辑界面是否显示
        editFormRules: {
          name: [
            {required: true, message: '请输入学生姓名', trigger: 'blur'}
          ]
        },
        editForm: {
          uid: '',
          name: '',
          nickname: '',
          sex: '',
          urgent_contactor: '',
          urgent_mobile: '',
          birthday: '',
          education: '',
          image_url: '',
          mentor_id: ''
        },

        //新增相关数据
        addFormVisible: false,//新增界面是否显示
        addLoading: false,
        addFormRules: {
          name: [
            {required: true, message: '请输入姓名', trigger: 'blur'}
          ],
          nickname: [
            {required: true, message: '请输入昵称', trigger: 'blur'}
          ],         
          uid: [
            {required: true, message: '请输入学号', trigger: 'blur'}
          ]          
        },
        addForm: {
          uid: '',
          name: '',
          nickname: '',
          sex: '',
          urgent_contactor: '',
          urgent_mobile: '',
          birthday: '',
          education: '',
          image_url: '',
          mentor_id: ''
        }
      }
    },
    methods: {
      handleCurrentChange(val) {
        this.page = val;
        this.search();
      },

      uidSearch(){
        this.total = 0;
        this.page = 1;
        if (this.filters.uid === '') {
          this.search();
        } else {
          this.SearchByUid();
        }
      },
      SearchByUid(){
        let that = this;
        that.loading = true;
        that.page = 1;
        that.total = 0;
        let param = that.filters.uid;
        API.findById(param).then(function (result) {
          that.loading = false;
          if (result && result.students) {
            if (result.students.length > 0) {
               that.students = result.students;
               that.total = result.students.length;
            } else{
               that.$message.error({showClose: true, message: '查询不到该学生信息, 请确认学号！', duration: 5000});
            }
          }
          that.filters.uid = '';

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
          console.log("receive get all students result")
          console.log(result)
          if (result && result.students) {
            if (result.students.length > 0) {
               that.total = result.total;
               that.students = result.students;
            } else{
               that.$message.error({showClose: true, message: '查询不到学生信息', duration: 5000});
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
      delStudent: function (index, row) {
        let that = this;
        this.$confirm('确认删除该记录吗?', '提示', {type: 'warning'}).then(() => {
          that.loading = true;
          API.remove(row.uid).then(function (result) {
            that.loading = false;
            if (result && parseInt(result.errcode) === 0) {
              that.$message.success({showClose: true, message: '删除成功', duration: 2000});
            } else{
              that.$message.success({showClose: true, message: '删除失败，请重试', duration: 2000});
            }
            that.filters.name = '';
            that.filters.uid = '';
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
            API.update(para.uid, para).then(function (result) {
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
          uid: '',
          name: '',
          nickname: '',
          sex: '',
          urgent_contactor: '',
          urgent_mobile: '',
          birthday: '',
          education: '',
          image_url: '',
          mentor_id: ''
        };
      },
      //新增
      addSubmit: function () {
        let that = this;
        this.$refs.addForm.validate((valid) => {
          if (valid) {
            that.loading = true;
            let para = Object.assign({}, this.addForm);
            API.add(para).then(function (result) {
              that.loading = false;
              if (result && parseInt(result.errcode) === 0) {
                that.$message.success({showClose: true, message: '添加老师信息成功', duration: 2000});
                that.$refs['addForm'].resetFields();
                that.addFormVisible = false;
                that.search();
              } else {
                that.$message.error({showClose: true, message: '添加学生信息失败', duration: 2000});
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
        let uids = this.sels.map(item => item.uid).toString();
        let that = this;
        this.$confirm('确认删除选中记录吗？', '提示', {
          type: 'warning'
        }).then(() => {
          that.loading = true;
          API.removeBatch(uids).then(function (result) {
            that.loading = false;
            if (result && parseInt(result.errcode) === 0) {
              that.$message.success({showClose: true, message: '删除成功', duration: 1500});
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
