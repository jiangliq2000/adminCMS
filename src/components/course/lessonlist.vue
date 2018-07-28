<template>
  <el-row class="warp">
    <el-col :span="24" class="warp-breadcrum">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }"><b>首页</b></el-breadcrumb-item>
        <el-breadcrumb-item>课程列表</el-breadcrumb-item>
      </el-breadcrumb>
    </el-col>

    <el-col :span="24" class="warp-main" v-loading="loading" element-loading-text="拼命加载中">
      <!--工具条-->
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" :model="filters">
          <el-form-item>
            <el-input v-model="filters.lessonname" placeholder="课程名字" @keyup.enter.native="handleSearch"></el-input>
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
      <el-table :data="lessons" highlight-current-row @selection-change="selsChange"
                style="width: 100%;">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column type="index" width="60"></el-table-column>
        <el-table-column type="expand" >
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="课程介绍">
                <span>{{ props.row.description }}</span>
              </el-form-item>    
            </el-form>
          </template>
        </el-table-column> 
        <el-table-column prop="lessonname" label="课程名称" sortable></el-table-column>
        <el-table-column prop="abilities" label="能力" width="120" sortable></el-table-column>
        <el-table-column prop="duration" label="上课时长" sortable></el-table-column>  
        <!-- 
        <el-table-column prop="homework" label="亲子任务" width="120" sortable></el-table-column>
      -->
        <el-table-column prop="material_id" label="素材" ></el-table-column>
        <el-table-column prop="version" label="版本"  ></el-table-column>
        <el-table-column prop="sequence" label="排课顺序" ></el-table-column>
        <el-table-column prop="createtime" label="创建时间" ></el-table-column>

        <el-table-column label="操作" width="150">
          <template slot-scope="scope">
            <el-button size="small" @click="showEditDialog(scope.$index,scope.row)">编辑</el-button>
            <el-button type="danger" @click="delTeacher(scope.$index,scope.row)" size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!--工具条-->
      <el-col :span="24" class="toolbar">
        <el-button type="danger" @click="batchDeleteTeacher" :disabled="this.sels.length===0">批量删除</el-button>
        <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="10" :total="total"
                       style="float:right;">
        </el-pagination>
      </el-col>

      <el-dialog title="编辑" :visible.sync ="editFormVisible" :close-on-click-modal="false">
        <el-form :model="editForm" label-width="100px" :rules="editFormRules" ref="editForm">
          <el-form-item label="课程名称" prop="lessonname" >
            <el-input v-model="editForm.lessonname" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="能力" prop="abilities" >
            <el-input v-model="editForm.abilities" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="上课时长" prop="duration" >
            <el-input v-model="editForm.duration" auto-complete="off"></el-input>
          </el-form-item>
          <!--
          <el-form-item label="亲子任务" prop="homework" auto-complete="off" >
            <el-input v-model="editForm.homework" auto-complete="off"></el-input>
          </el-form-item>
        -->
          <el-form-item label="素材" prop="material_id" auto-complete="off" >
            <el-input v-model="editForm.material_id" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="版本" prop="version" auto-complete="off" >
            <el-input v-model="editForm.version" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="排课顺序" prop="sequence" auto-complete="off" >
            <el-input v-model="editForm.sequence" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="课程描述" prop="description" auto-complete="off" >
            <el-input v-model="editForm.description" auto-complete="off"></el-input>
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
          <el-row>
            <el-col :span="10">
              <el-form-item label="课程名字" prop="lessonname">
                <el-input v-model="addForm.lessonname" auto-complete="off"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="10">
              <el-form-item label="上课时长" prop="duration">
                <el-input v-model="addForm.duration" auto-complete="off"></el-input>
              </el-form-item>  
            </el-col>
         

          </el-row>
          <el-row>    
            <el-col :span="10">
              <el-form-item label="排课顺序" prop="sequence">
                <el-input v-model="addForm.sequence" auto-complete="off"></el-input>
              </el-form-item>  
            </el-col>

            <el-col :span="10">
              <el-form-item label="版本" prop="version">
                <el-input v-model="addForm.version" auto-complete="off"></el-input>
              </el-form-item>      
            </el-col>   

          </el-row>

          <el-form-item label="能力" prop="abilities">
             <el-input v-model="addForm.abilities" auto-complete="off"></el-input>
          </el-form-item>  
  
          <el-form-item label="素材" prop="material_id">
            <el-input v-model="addForm.material_id" auto-complete="off"></el-input>
          </el-form-item>  
          <!--
          <el-form-item label="亲子任务" prop="homework">
            <el-input v-model="addForm.homework" auto-complete="off"></el-input>
          </el-form-item>              
          -->
          <el-form-item label="课程描述" prop="description">
            <el-input v-model="addForm.description" auto-complete="off"></el-input>
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
  import API from '../../api/api_lesson';

  export default{
    data(){
      return {
        filters: {
          lessonname: ''
        },
        lessons: [],
        total: 0,
        page: 1,
        limit: 10,
        loading: false,
        sels: [], //列表选中列

        //编辑相关数据
        editFormVisible: false,//编辑界面是否显示
        editFormRules: {
          lessonname: [
            {required: true, message: '请输入教师姓名', trigger: 'blur'}
          ]
        },
        editForm: {
          lessonname: '',
          abilities: '',
          duration: '',
          homework: '',
          material_id: '',
          version: '',
          sequence: '',
          description: ''
        },

        //新增相关数据
        addFormVisible: false,//新增界面是否显示
        addLoading: false,
        addFormRules: {
          lessonname: [
            {required: true, message: '请输入课程名字', trigger: 'blur'}
          ]        
        },
        addForm: {
          lessonname: '',
          abilities: '',
          duration: '',
          version: '',
          sequence: '',
          material_id: '',
          homework: '',
          description: ''
        }
      }
    },
    methods: {

      handleCurrentChange(val) {
        this.page = val;
        this.search();
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
          lessonname: that.filters.lessonname
        };

        that.loading = true;
        API.findList(params).then(function (result) {
          that.loading = false;
          if (result && result.lessons) {
            if (result.lessons.length > 0) {
               that.total = result.total;
               that.lessons = result.lessons;            
            } else{
               that.$message.error({showClose: true, message: '查询不到课程信息', duration: 5000});
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
          console.log("row.lessonname is");
          console.log(row.lessonname);
          API.remove(row.lessonname).then(function (result) {
            that.loading = false;
            console.log('result is ');
            console.log(result);
            if (result && parseInt(result.errcode) === 0) {
              that.$message.success({showClose: true, message: '删除成功', duration: 2000});
            } else{
              that.$message.success({showClose: true, message: '删除失败，请重试', duration: 2000});
            }
            that.filters.lessonname = '';
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
            API.update(para.lessonname, para).then(function (result) {
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
          lessonname: '',
          abilities: '',
          duration: '',
          version: '',
          sequence: '',
          material_id: '',
          homework: '',
          description: ''
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
                that.$message.success({showClose: true, message: '添加课程信息成功', duration: 2000});
                that.$refs['addForm'].resetFields();
                that.addFormVisible = false;
                that.search();
              } else {
                that.$message.error({showClose: true, message: '添加课程信息失败', duration: 2000});
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
      batchDeleteTeacher: function () {
        //let ids = this.sels.map(item => item.id).toString();
        let nicknames = this.sels.map(item => item.lessonname).toString();
        let that = this;
        this.$confirm('确认删除选中记录吗？', '提示', {
          type: 'warning'
        }).then(() => {
          that.loading = true;
          API.removeBatch(nicknames).then(function (result) {
            that.loading = false;
            if (result && parseInt(result.errcode) === 0) {
              that.$message.success({showClose: true, message: '删除成功', duration: 2500});
              that.filters.lessonname = '';          
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
