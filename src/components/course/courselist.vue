<template>
  <el-row class="warp">
    <el-col :span="24" class="warp-breadcrum">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }"><b>首页</b></el-breadcrumb-item>
        <el-breadcrumb-item>套餐列表</el-breadcrumb-item>
      </el-breadcrumb>
    </el-col>

    <el-col :span="24" class="warp-main" v-loading="loading" element-loading-text="拼命加载中">
      <!--工具条-->
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" :model="filters">
          <el-form-item>
            <el-input v-model="filters.name" placeholder="套餐名字" @keyup.enter.native="handleSearch"></el-input>
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
      <el-table :data="courses" highlight-current-row @selection-change="selsChange"
                style="width: 100%;">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column type="index" width="60"></el-table-column>
        <el-table-column type="expand" >
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="套餐介绍">
                <span>{{ props.row.description }}</span>
              </el-form-item>    
            </el-form>
          </template>
        </el-table-column> 
        <el-table-column prop="name" label="套餐名称" sortable></el-table-column>
        <el-table-column prop="category" label="套餐类别" :formatter="formatCategory" sortable></el-table-column>
        <el-table-column prop="age" label="适龄岁数" sortable></el-table-column>   
        <el-table-column prop="scope" label="适用区域" :formatter="formatScope" sortable></el-table-column>
        <el-table-column prop="director" label="负责人" ></el-table-column>
        <el-table-column prop="lesson_times" label="上课次数"  ></el-table-column>
        <el-table-column prop="expiretime" label="到期时间" ></el-table-column>
        <el-table-column prop="status" label="状态" :formatter="formatStatus" ></el-table-column>
        <el-table-column prop="repeats" label="上课频率" :formatter="formatRepeats"></el-table-column>
        <el-table-column prop="createtime" label="创建时间" ></el-table-column>

        <el-table-column label="操作" width="250">
          <template slot-scope="scope">
            <el-button size="small" @click="showLessonDialog(scope.$index,scope.row)">关联课程</el-button>
            <el-button size="small" @click="showTeacherDialog(scope.$index,scope.row)">关联教师</el-button>
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


      <el-dialog title="关联课程" :visible.sync ="corLessonFormVisible" :close-on-click-modal="false">
        <el-form :model="corLessonEditForm" label-width="100px"  ref="corLessonEditForm">
          <el-form-item label="套餐名字" prop="name" >
            <el-input v-model="corLessonEditForm.name" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>
          <el-row>
            <el-col :span="16">
              <el-form-item >
                <el-input v-model="corLessonEditForm.filtername" placeholder="请输入待关联课程名称"  @keyup.enter.native="corLessonSearch">
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item>
                <el-button type="primary" v-on:click="corLessonSearch">查询</el-button>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="16">
              <el-select v-model="corLessonoption" clearable placeholder="请选择待课程" no-data-text="请先查询课程">
                <el-option v-for="item in corLessonOptions" :key="item.value" :label="item.label" :value="item.value">
                  <span style="float: left">{{ item.label }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">{{ item.coursename }}</span>
                </el-option>
              </el-select>        
            </el-col>              
            <el-col :span="8">
              <el-form-item>
                <el-button type="primary" v-on:click="corLessonAdd">添加</el-button>
              </el-form-item>
            </el-col>            
          </el-row>     
        </el-form>      
        <el-table :data="corLessonEditForm.GridData">
          <el-table-column property="lessonname" label="课程姓名" ></el-table-column>
          <el-table-column property="duration" label="上课时长" ></el-table-column>
          <el-table-column property="version" label="版本"></el-table-column>
          <el-table-column label="操作" width="80">
             <template slot-scope="scope1">
               <el-button size="small" @click="corLessonDel(scope1.$index,scope1.row)">删除</el-button>
             </template>
          </el-table-column>
        </el-table>         
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="corLessonFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="corLessonEditSubmit">提交</el-button>
        </div>
      </el-dialog>




      <el-dialog title="关联教师" :visible.sync ="corTeacherFormVisible" :close-on-click-modal="false">
        <el-form :model="corTeacherEditForm" label-width="100px"  ref="corTeacherEditForm">
          <el-form-item label="套餐名字" prop="name" >
            <el-input v-model="corTeacherEditForm.name" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>
          <el-row>
            <el-col :span="16">
              <el-form-item >
                <el-input v-model="corTeacherEditForm.filtername" placeholder="请输入待关联教师姓名"  @keyup.enter.native="corTeacherSearch">
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item>
                <el-button type="primary" v-on:click="corTeacherSearch">查询</el-button>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="16">
              <el-select v-model="corTeacheroption" clearable placeholder="请选择待关联教师" no-data-text="请先查询教师">
                <el-option v-for="item in corTeacherOptions" :key="item.value" :label="item.label" :value="item.value">
                  <span style="float: left">{{ item.label }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">{{ item.mobile }}</span>
                </el-option>
              </el-select>        
            </el-col>              
            <el-col :span="8">
              <el-form-item>
                <el-button type="primary" v-on:click="corTeacherAdd">添加</el-button>
              </el-form-item>
            </el-col>            
          </el-row>     
        </el-form>      
        <el-table :data="corTeacherEditForm.GridData">
          <el-table-column property="teacher_name" label="教师姓名" ></el-table-column>
          <el-table-column property="teacher_mobile" label="手机号" ></el-table-column>
          <el-table-column label="操作" width="80">
             <template slot-scope="scope1">
               <el-button size="small" @click="corTeacherDel(scope1.$index,scope1.row)">删除</el-button>
             </template>
          </el-table-column>
        </el-table>         
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="corTeacherFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="corTeacherEditSubmit">提交</el-button>
        </div>
      </el-dialog>









      <el-dialog title="编辑" :visible.sync ="editFormVisible" :close-on-click-modal="false">
        <el-form :model="editForm" label-width="100px" :rules="editFormRules" ref="editForm">
          <el-form-item label="套餐名称" prop="name" >
            <el-input v-model="editForm.name" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="适龄" prop="age" >
            <el-input v-model="editForm.age" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="套餐类别" >
            <el-select v-model="editForm.category" placeholder="请选择类别">
              <el-option label="益智类" value="1"></el-option>
              <el-option label="动手类" value="2"></el-option>
              <el-option label="性格培养" value="3"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="适用区域" prop="scope" >
            <el-input v-model="editForm.scope" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="价格" prop="price" auto-complete="off" >
            <el-input v-model="editForm.price" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="负责人" prop="director" auto-complete="off" >
            <el-input v-model="editForm.director" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="到期时间" prop="expiretime" auto-complete="off" >
            <el-input v-model="editForm.expiretime" auto-complete="off"></el-input>
          </el-form-item>

          <el-form-item label="时效" >
            <el-select v-model="editForm.status" placeholder="请选择时效">
              <el-option label="过期" value="0"></el-option>
              <el-option label="在用" value="1"></el-option>
              <el-option label="正在制作" value="2"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="上课频率" >
            <el-select v-model="editForm.repeats" placeholder="请选择上课频率">
              <el-option label="一周一次" value="1"></el-option>
              <el-option label="一周两次" value="2"></el-option>
              <el-option label="一周三次" value="3"></el-option>
              <el-option label="一月一次" value="4"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="套餐介绍" prop="level" auto-complete="off" >
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
            <el-col :span="8">
              <el-form-item label="套餐名字" prop="name">
                <el-input v-model="addForm.name" auto-complete="off"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="套餐类别">
                <el-select v-model="addForm.category" placeholder="请选择套餐类别">
                  <el-option label="益智类" value="1"></el-option>
                  <el-option label="动手类" value="2"></el-option>
                  <el-option label="性格培养" value="3"></el-option>
                </el-select>
              </el-form-item>
            </el-col>

            <el-col :span="8">
              <el-form-item label="适用区域" prop="scope">
                  <el-select v-model="addForm.scope" placeholder="请选择适用区域">
                  <el-option label="公开" value="0"></el-option>
                  <el-option label="机构特色" value="1"></el-option>
                </el-select>
              </el-form-item>  
            </el-col>


          </el-row>
          <el-row>            
            <el-col :span="8">
              <el-form-item label="适用年龄" prop="age">
                <el-input v-model="addForm.age" auto-complete="off"></el-input>
              </el-form-item>      
            </el-col>

            <el-col :span="8">
              <el-form-item label="状态" prop="status">
                  <el-select v-model="addForm.status" placeholder="请选择状态">
                  <el-option label="过期" value="0"></el-option>
                  <el-option label="在用" value="1"></el-option>
                  <el-option label="正在制作" value="3"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="上课频率" prop="repeats">
                <el-select v-model="addForm.repeats" placeholder="请选择上课频率">
                  <el-option label="一周一次" value="0"></el-option>
                  <el-option label="一周两次" value="1"></el-option>
                  <el-option label="一周三次" value="3"></el-option>
                  <el-option label="一月一次" value="11"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="8">
              <el-form-item label="上课次数" prop="lesson_times">
                <el-input v-model="addForm.lesson_times" auto-complete="off"></el-input>
              </el-form-item>  
            </el-col>          
            <el-col :span="8">
              <el-form-item label="到期时间" prop="expiretime">
                <el-input v-model="addForm.expiretime" auto-complete="off"></el-input>
              </el-form-item>
            </el-col>


            <el-col :span="8">
              <el-form-item label="负责人" prop="director">
                <el-input v-model="addForm.director" auto-complete="off"></el-input>
              </el-form-item>  
            </el-col>   

          </el-row>
          <el-row>       
            <el-col :span="8">
              <el-form-item label="价格" prop="price">
                <el-input v-model="addForm.price" auto-complete="off"></el-input>
              </el-form-item>  
            </el-col>  
            <el-col :span="16">
              <el-form-item label="素材url" prop="media_url">
                <el-input v-model="addForm.media_url" auto-complete="off"></el-input>
              </el-form-item>  
            </el-col>
          </el-row>                
          <el-form-item label="套餐描述" prop="description">
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
  import API from '../../api/api_course';
  import APILESSON from '../../api/api_lesson';
  import APITEACHER from '../../api/api_teacher';
  import APICOURSETEACHER from '../../api/api_courseteacher';
  

  export default{
    data(){
      return {
        filters: {
          name: ''
        },
        courses: [],
        total: 0,
        page: 1,
        limit: 10,
        loading: false,
        sels: [], //列表选中列

        //关联课程相关数据
        corLessonFormVisible: false,//关联学生界面是否显示
        corLessonEditForm: {
          course_id:"",
          name: '',
          filtername: '',
          GridData: []
        },
        corLessonoption: [],
        corLessonOptions: [],

        //关联教师相关数据
        corTeacherFormVisible: false,//关联学生界面是否显示
        corTeacherEditForm: {
          course_id:"",
          name: '',
          filtername: '',
          GridData: []
        },
        corTeacheroption: [],
        corTeacherOptions: [],


        //编辑相关数据
        editFormVisible: false,//编辑界面是否显示
        editFormRules: {
          name: [
            {required: true, message: '请输入教师姓名', trigger: 'blur'}
          ]
        },
        editForm: {
          name: '',
          age: '',
          category: '',
          scope: '',
          price: '',
          director: '',
          expiretime: '',
          status: '',
          repeats: '',
          description:''
        },

        //新增相关数据
        addFormVisible: false,//新增界面是否显示
        addLoading: false,
        addFormRules: {
          name: [
            {required: true, message: '请输入套餐名字', trigger: 'blur'}
          ]        
        },
        addForm: {
          name: '',
          category: '',
          age: '',
          scope: '',
          director: '',
          lesson_times: '',
          expiretime: '',
          status: '',          
          repeats: '',
          media_url:'',
          description: ''
        }
      }
    },
    methods: {

      formatCategory(row, column){
        return row.category == 1 ? "益智类" : row.category == 2 ? "动手类" : "性格培养";
      },

      formatScope(row, column){
        return row.scope == 0 ? "公开" : "机构特殊";
      },

      formatStatus(row, column){
        return row.status == 0 ? "过期" : row.status == 1 ? "在用" : "正在制作";
      },

      formatRepeats(row, column){
        return row.repeats == 1 ? "一周一次" : row.repeats == 2 ? "一周两次" : row.repeats == 3 ? "一周三次" :  "一月一次";
      },      

      handleCurrentChange(val) {
        this.page = val;
        console.log("val is: ");
        console.log(val)
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
          name: that.filters.name
        };

        that.loading = true;
        API.findList(params).then(function (result) {
          that.loading = false;
          console.log("receive get all courses result")
          console.log(result)
          if (result && result.courses) {
            if (result.courses.length > 0) {
               that.total = result.total;
               that.courses = result.courses;
            
            } else{
               that.$message.error({showClose: true, message: '查询不到套餐信息', duration: 5000});
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
          console.log("row.name is");
          console.log(row.name);
          API.remove(row.name).then(function (result) {
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
            console.log("para.name is ");
            console.log(para);
            API.update(para.name, para).then(function (result) {
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
          name: '',
          category: '',
          age: '',
          scope: '',
          director: '',
          lesson_times: '',
          expiretime: '',
          status: '',          
          repeats: '',
          media_url:'',
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
                that.$message.success({showClose: true, message: '添加套餐信息成功', duration: 2000});
                that.$refs['addForm'].resetFields();
                that.addFormVisible = false;
                that.search();
              } else {
                that.$message.error({showClose: true, message: '添加套餐信息失败', duration: 2000});
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
        let nicknames = this.sels.map(item => item.name).toString();
        let that = this;
        this.$confirm('确认删除选中记录吗？', '提示', {
          type: 'warning'
        }).then(() => {
          that.loading = true;
          API.removeBatch(nicknames).then(function (result) {
            that.loading = false;
            if (result && parseInt(result.errcode) === 0) {
              that.$message.success({showClose: true, message: '删除成功', duration: 2500});
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
      },
      // 关联课程相关
      showLessonDialog: function (index, row) {
        let that = this;
        that.corLessonFormVisible = true;
        that.corLessonEditForm.GridData = [];
        //that.corStdeditForm.studentIds = [];
        that.corLessonEditForm.filtername = "";
        let course = Object.assign({}, row);
        that.corLessonEditForm.name = course.name;
        that.corLessonEditForm.course_id = course.id;
        console.log(row.lessonInfo);
        that.corLessonEditForm.GridData = row.lessonInfo;
      },

      corLessonSearch(){
        let that = this;
        let params = that.corLessonEditForm.filtername;
        console.log(params);
        that.corLessonOptions = [];
        APILESSON.GetByName(params).then(function (result) {
          if (result && result.lessons) {
            if (result.lessons.length > 0) {
                console.log("corLessonSearch");
                console.log(result.lessons);
                for(var j=0;j<result.lessons.length;j++){
                  that.corLessonOptions.push({'value':result.lessons[j].id, 'label':result.lessons[j].lessonname, 'coursename':result.lessons[j].coursename});
                }
            } else{
               that.$message.error({showClose: true, message: '查询不到课程信息', duration: 5000});
            }
          }

        }, function (err) {
          that.$message.error({showClose: true, message: err.toString(), duration: 2000});
        }).catch(function (error) {
          console.log(error);
          that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
        });        

      },

      corLessonAdd(){
        let that = this;
        let param = that.corlessonoption;
        
        console.log('corlessonAdd');
        console.log(that.corLessonoption);

        APILESSON.findById(that.corLessonoption).then(function (result) {
          console.log(result);
          if (result && result.lesson) {
              
            var isKeyExist = 0;
            for(var j=0;j<that.corLessonEditForm.GridData.length;j++){
              if (that.corLessonoption == that.corLessonEditForm.GridData[j]['id']){
                isKeyExist = 1;
                break;
              }
            }
            if (isKeyExist == 0){
              that.corLessonEditForm.GridData.push({'id':result.lesson['id'],'lessonname': result.lesson['lessonname'] ,'duration':result.lesson['duration'] ,'version':result.lesson['version']});
            }
  
          } else{
               that.$message.error({showClose: true, message: '查询不到课程信息', duration: 5000});
            }

        }, function (err) {
          that.$message.error({showClose: true, message: err.toString(), duration: 2000});
        }).catch(function (error) {
          console.log(error);
          that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
        });   
        
      },

      corLessonEditSubmit: function () {
        let that = this;
        that.loading = true;
        //let para = Object.assign({}, that.corLessonEditForm.GridData);
        console.log("corLessonEditForm");
        //console.log(para);
        console.log(that.corLessonEditForm.GridData);

        var corlessonids = [];
        for(var i=0;i<that.corLessonEditForm.GridData.length;i++){
          console.log(that.corLessonEditForm.GridData[i]);
          corlessonids.push(that.corLessonEditForm.GridData[i]['id']);
        }

        let params = {
          corLessonids: corlessonids
        };

        APILESSON.updateCourseId(that.corLessonEditForm.course_id, params).then(function (result) {
              that.loading = false;
              if (result && parseInt(result.errcode) === 0) {
                that.$message.success({showClose: true, message: '修改成功', duration: 4000});
                //that.$refs['editForm'].resetFields();
                that.corLessonFormVisible = false;
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

        that.corLessonFormVisible = false;
        that.corlessonOptions = [] ;
        that.corLessonoption = "";
      },
      corLessonDel: function (index, row) {
        console.log("showStdGuardEditDialog");
        console.log(index);
        console.log(row);
        console.log(row.id);
        console.log(this.corLessonEditForm.GridData);
        let indexflag = -1;
        for(var i=0; i<this.corLessonEditForm.GridData.length; i++){
          //console.log(this.corStdeditForm.GridData[i].id);
          if (this.corLessonEditForm.GridData[i].id == row.id){
            indexflag = i;               
          }
        }
        console.log(indexflag);
        this.corLessonEditForm.GridData.splice(indexflag,1);
      },

      // 关联教师相关
      showTeacherDialog: function (index, row) {
        let that = this;
        that.corTeacherFormVisible = true;
        that.corTeacherEditForm.GridData = [];
        that.corTeacherEditForm.filtername = "";
        let course = Object.assign({}, row);
        that.corTeacherEditForm.name = course.name;
        that.corTeacherEditForm.course_id = course.id;
        console.log(row);
        that.corTeacherEditForm.GridData = row.teacherInfo;
      },

      corTeacherSearch(){
        let that = this;
        let params = that.corTeacherEditForm.filtername;
        console.log(params);
        that.corTeacherOptions = [];
        APITEACHER.GetTeacherInfoByName(params).then(function (result) {
          if (result && result.teacherinfos) {
            if (result.teacherinfos.length > 0) {
                console.log("corTeacherSearch");
                console.log(result.teacherinfos);
                for(var j=0;j<result.teacherinfos.length;j++){
                  that.corTeacherOptions.push({'value':result.teacherinfos[j].id, 'label':result.teacherinfos[j].name, 'mobile':result.teacherinfos[j].mobile});
                }
            } else{
               that.$message.error({showClose: true, message: '查询不到教师信息', duration: 5000});
            }
          }

        }, function (err) {
          that.$message.error({showClose: true, message: err.toString(), duration: 2000});
        }).catch(function (error) {
          console.log(error);
          that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
        });        

      },

      corTeacherAdd(){
        let that = this;
        let param = that.corTeacheroption;
        
        console.log('corteacherAdd');
        console.log(that.corTeacherEditForm.GridData);

        APITEACHER.findById(that.corTeacheroption).then(function (result) {
          console.log(result);
          if (result && result.teacher) {
              
            var isKeyExist = 0;
            for(var j=0;j<that.corTeacherEditForm.GridData.length;j++){
              if (that.corTeacheroption == that.corTeacherEditForm.GridData[j]['id']){
                isKeyExist = 1;
                break;
              }
            }
            if (isKeyExist == 0){
              that.corTeacherEditForm.GridData.push({'teacher_id':result.teacher['id'],'teacher_name': result.teacher['name'] ,'teacher_mobile':result.teacher['mobile'] });
            }
  
          } else{
               that.$message.error({showClose: true, message: '查询不到教师信息', duration: 5000});
            }

        }, function (err) {
          that.$message.error({showClose: true, message: err.toString(), duration: 2000});
        }).catch(function (error) {
          console.log(error);
          that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
        });   
        
      },

      corTeacherEditSubmit: function () {
        let that = this;
        that.loading = true;
        //let para = Object.assign({}, that.corTeacherEditForm.GridData);
        console.log("corTeacherEditForm");
        //console.log(para);
        console.log(that.corTeacherEditForm.GridData);

        var corteachers = [];
        for(var i=0;i<that.corTeacherEditForm.GridData.length;i++){
          console.log(that.corTeacherEditForm.GridData[i]);
          corteachers.push({'teacher_id':that.corTeacherEditForm.GridData[i]['teacher_id'],'teacher_name':that.corTeacherEditForm.GridData[i]['teacher_name'],'teacher_mobile':that.corTeacherEditForm.GridData[i]['teacher_mobile']});
        }

        let params = {
          corTeachers: corteachers
        };

        APICOURSETEACHER.update(that.corTeacherEditForm.course_id, params).then(function (result) {
              that.loading = false;
              if (result && parseInt(result.errcode) === 0) {
                that.$message.success({showClose: true, message: '修改成功', duration: 4000});
                //that.$refs['editForm'].resetFields();
                that.corTeacherFormVisible = false;
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

        that.corTeacherFormVisible = false;
        that.corteacherOptions = [] ;
        that.corTeacheroption = "";
      },
      corTeacherDel: function (index, row) {
        let indexflag = -1;
        for(var i=0; i<this.corTeacherEditForm.GridData.length; i++){
          if (this.corTeacherEditForm.GridData[i].id == row.id){
            indexflag = i;               
          }
        }
        console.log(indexflag);
        this.corTeacherEditForm.GridData.splice(indexflag,1);
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
