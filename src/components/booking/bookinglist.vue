<template>
  <el-row class="warp">
    <el-col :span="24" class="warp-breadcrum">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }"><b>首页</b></el-breadcrumb-item>
        <el-breadcrumb-item>预约列表</el-breadcrumb-item>
      </el-breadcrumb>
    </el-col>

    <el-col :span="24" class="warp-main" v-loading="loading" element-loading-text="拼命加载中">
      <!--工具条-->
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" :model="filters">
          <el-form-item>
            <el-input v-model="filters.name" placeholder="姓名" ></el-input>
          </el-form-item>
          <el-form-item>
            <el-input v-model="filters.date" placeholder="2018-07-01" ></el-input>
          </el-form-item>
          <el-form-item >
            <el-select v-model="filters.status" placeholder="请选择预约状态">
              <el-option label="预约待确认" value="0"></el-option>
              <el-option label="已确认" value="1"></el-option>
              <el-option label="已调整" value="2"></el-option>
              <el-option label="已取消" value="3"></el-option>
            </el-select>
          </el-form-item>


          <el-form-item>
            <el-button type="primary" v-on:click="handleSearch">查询</el-button>
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="showAddDialog">新增</el-button>
          </el-form-item>
        
        </el-form>
      </el-col>

      <!--列表-->
      <el-table :data="teachers" highlight-current-row @selection-change="selsChange"
                style="width: 100%;">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column type="index" width="60"></el-table-column>

        <el-table-column type="expand" >
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-row :gutter="15">
                <el-col :span="10">
                  <el-form-item label="昵称">
                    <span>{{ props.row.nickname }}</span>
                  </el-form-item>   
                  <el-form-item label="生日">
                    <span>{{ props.row.birthday}}</span>
                  </el-form-item>                         
                  <el-form-item label="邮箱">
                    <span>{{ props.row.email }}</span>
                  </el-form-item>
                </el-col>
            </el-row>
            </el-form>
          </template>
        </el-table-column>   

        <el-table-column prop="pkgname" label="套餐名称" sortable></el-table-column>
        <el-table-column prop="stdname" label="学生姓名" sortable></el-table-column>
        <el-table-column prop="memname" label="会员姓名" sortable></el-table-column>
        <el-table-column prop="teachername" label="教师姓名" sortable></el-table-column>
   
        <el-table-column prop="is_adjusted" label="已调课" :formatter="formatAdjust" sortable></el-table-column>
        <el-table-column prop="resertype" label="预约类型" ></el-table-column>
        <el-table-column prop="bookingdate" label="预约日期" ></el-table-column>
        <el-table-column prop="bookingtime" label="预约时段" ></el-table-column>
        <el-table-column prop="status" label="当前状态" :formatter="formatStatus" ></el-table-column>

        <el-table-column label="操作" width="150">
          <template slot-scope="scope">
            <el-button size="small" @click="showEditDialog(scope.$index,scope.row)">调整</el-button>
            <el-button type="danger" @click="delTeacher(scope.$index,scope.row)" size="small">确认</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!--工具条-->
      <el-col :span="24" class="toolbar">
        <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="10" :total="total"
                       style="float:right;">
        </el-pagination>
      </el-col>

      <el-dialog title="编辑" :visible.sync ="editFormVisible" :close-on-click-modal="false">
        <el-form :model="editForm" label-width="100px" :rules="editFormRules" ref="editForm">
          <el-form-item label="昵称" prop="nickname" >
            <el-input v-model="editForm.nickname" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="姓名" prop="name" >
            <el-input v-model="editForm.name" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="性别" >
            <el-select v-model="editForm.sex" placeholder="请选择性别">
              <el-option label="男" value="1"></el-option>
              <el-option label="女" value="2"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="密码" prop="password" >
            <el-input v-model="editForm.password" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="权限" prop="options" auto-complete="off" >
            <el-input v-model="editForm.options" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="手机" prop="mobile" auto-complete="off" >
            <el-input v-model="editForm.mobile" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="类别" prop="type" auto-complete="off" >
            <el-input v-model="editForm.type" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="级别" prop="level" auto-complete="off" >
            <el-input v-model="editForm.type" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="地址" prop="address" auto-complete="off" :disabled="true">
            <el-input v-model="editForm.address" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="线下店" prop="school_id" auto-complete="off" :disabled="true">
            <el-input v-model="editForm.school_id" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="头像" prop="image_url" auto-complete="off" :disabled="true">
            <el-input v-model="editForm.image_url" auto-complete="off"></el-input>
          </el-form-item>
        </el-form>        <div slot="footer" class="dialog-footer">
          <el-button @click.native="editFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="editSubmit">提交</el-button>
        </div>
      </el-dialog>

      <!--新增界面-->
      <el-dialog title="新建预约" :visible.sync ="addFormVisible" :close-on-click-modal="false">
        <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
          <el-row>
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
            <el-col :span="8">
              <el-form-item label="权限" prop="options">
                <el-input v-model="addForm.options" auto-complete="off"></el-input>
              </el-form-item>      
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="8">
              <el-form-item label="密码" prop="password">
                <el-input v-model="addForm.password" auto-complete="off"></el-input>
              </el-form-item>  
            </el-col>
            <el-col :span="10">
              <el-form-item label="手机号" prop="mobile">
                <el-input v-model="addForm.mobile" auto-complete="off"></el-input>
              </el-form-item>  
            </el-col>          
            <el-col :span="6">
              <el-form-item label="性别">
                <el-select v-model="addForm.sex" placeholder="请选择性别">
                  <el-option label="男" value="1"></el-option>
                  <el-option label="女" value="2"></el-option>
                </el-select>
              </el-form-item> 
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="10">
              <el-form-item label="类别" prop="type">
                <el-input v-model="addForm.type" auto-complete="off"></el-input>
              </el-form-item>  
            </el-col>          
            <el-col :span="10">
              <el-form-item label="级别" prop="level">
                <el-input v-model="addForm.level" auto-complete="off"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="8">
              <el-form-item label="省份" prop="province">
                <el-input v-model="addForm.province" auto-complete="off"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="城市" prop="city">
                <el-input v-model="addForm.city" auto-complete="off"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="国家" prop="country">
                <el-input v-model="addForm.country" auto-complete="off"></el-input>
              </el-form-item>  
            </el-col>
          </el-row>                
          <el-form-item label="地址" prop="address">
            <el-input v-model="addForm.address" auto-complete="off"></el-input>
          </el-form-item>
          <el-row>
            <el-col :span="8">
              <el-form-item label="邮箱" prop="email">
                <el-input v-model="addForm.email" auto-complete="off"></el-input>
              </el-form-item>   
            </el-col>
            <el-col :span="8">       
              <el-form-item label="生日" prop="birthday" >
                <el-input v-model="addForm.birthday" placeholder="1970-01-01" auto-complete="off"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="学历" prop="education">
                <el-input v-model="addForm.education" auto-complete="off"></el-input>
              </el-form-item> 
            </el-col> 
          </el-row>        
          <el-form-item label="线下店" prop="school_id">
            <el-input v-model="addForm.school_id" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="头像" prop="image_url">
            <el-input v-model="addForm.image_url" auto-complete="off"></el-input>
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

<style>
  .demo-table-expand {
    font-size: 0;
  }
  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
</style>

<script>
  import util from '../../common/util'
  import API from '../../api/api_teacher';

  export default{
    data(){
      return {
        filters: {
          name: '',
          mobile: ''
        },
        teachers: [],
        total: 0,
        page: 1,
        limit: 10,
        loading: false,
        sels: [], //列表选中列

        //编辑相关数据
        editFormVisible: false,//编辑界面是否显示
        editFormRules: {
          name: [
            {required: true, message: '请输入教师姓名', trigger: 'blur'}
          ]
        },
        editForm: {
          nickname: '',
          name: '',
          sex: '',
          password: '',
          options: '',
          mobile: '',
          address: '',
          school_id: '',
          image_url: '',
          type: '',
          level:'',
          effectivetime:''
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
          mobile: [
            {required: true, message: '请输入手机号', trigger: 'blur'}
          ]          
        },
        addForm: {
          name: '',
          password: '',
          options: '',
          nickname: '',
          sex: '',
          province: '',
          city: '',
          country: '',
          address: '',          
          mobile: '',
          email: '',
          birthday: '',
          education: '',
          school_id: '',
          image_url: '',
          type: '',
          level: '',
          effectivetime: ''
        }
      }
    },
    methods: {
      formatAdjust(row, column){
        return row.status == 0 ? "否" : "是";
      },      
      formatStatus(row, column){
        return row.status == 0 ? "预约待确认" : row.status == 1 ? "已确认" : row.status == 2 ? "已调整" : "已取消";
      },            
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
        API.findByMobile(param).then(function (result) {
          that.loading = false;
          if (result && result.teachers) {
            if (result.teachers.length > 0) {
               that.teachers = result.teachers;
               that.total = result.teachers.length;
            } else{
               that.$message.error({showClose: true, message: '查询不到该教师信息, 请确认手机号码！', duration: 5000});
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
          console.log("receive get all teachers result")
          console.log(result)
          if (result && result.teachers) {
            if (result.teachers.length > 0) {
               that.total = result.total;
               that.teachers = result.teachers;
              //replace sex prop
              that.teachers.forEach((teacher, index) => {
                if (teacher.sex == '1'){
                  teacher.sex = '男'
                }else{
                  teacher.sex = '女'
                }
                if (teacher.type == '1'){
                  teacher.type = '线下店'
                }else{
                  teacher.type = '非线下店'
                }

              });                
            } else{
               that.$message.error({showClose: true, message: '查询不到教师信息', duration: 5000});
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
      delTeacher: function (index, row) {
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
          password: '',
          sex: '',
          province: '',
          city: '',
          country: '',
          address: '',
          options: '',
          mobile: '',
          birthday: '',
          education: '',
          school_id: '',
          image_url: ''
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
                that.$message.error({showClose: true, message: '添加老师信息失败', duration: 2000});
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
