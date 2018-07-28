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
         @expand-change="expandChange" style="width: 100%;">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column type="index" width="60"></el-table-column>
        <el-table-column type="expand" prop='studentInfo'>
          <template slot-scope="props">
            <el-table stripe :data="props.row.studentInfo" label="关联学生信息">
              <el-table-column prop="name" label="学生姓名" width="170">
              </el-table-column>
              <el-table-column prop="uid" label="学号" width="170">
              </el-table-column>
              <el-table-column prop="nickname" label="昵称" width="150">
              </el-table-column>
              <el-table-column prop="sex" label="性别" width="150">
              </el-table-column>
              <el-table-column prop="birthday" label="生日" width="150">
              </el-table-column>                            
              <el-table-column prop="urgent_contactor" label="紧急联系人" width="200">
              </el-table-column>
            </el-table>
          </template>
        </el-table-column>
        <el-table-column prop="nickname" label="会员昵称" sortable></el-table-column>
        <el-table-column prop="name" label="会员名" sortable></el-table-column>
        <el-table-column prop="sex" label="性别" sortable></el-table-column>
        <el-table-column prop="province" label="省份" sortable></el-table-column>
        <el-table-column prop="city" label="城市" sortable></el-table-column>
        <el-table-column prop="country" label="国家" sortable></el-table-column>
        <el-table-column prop="address" label="地址" sortable></el-table-column>
        <el-table-column prop="wxunionid" label="微信id" sortable></el-table-column>
        <el-table-column prop="memtype" label="会员级别" sortable></el-table-column>
        <el-table-column prop="mobile" label="手机" ></el-table-column>
        <el-table-column prop="email" label="邮箱" ></el-table-column>
        <el-table-column prop="birthday" label="生日" ></el-table-column>
        <el-table-column prop="education" label="学历" ></el-table-column>
        <el-table-column prop="industry" label="行业" ></el-table-column>
        <el-table-column prop="background" label="背景" ></el-table-column>
        <el-table-column prop="createtime" label="创建时间" width="120" sortable></el-table-column>
        <el-table-column prop="changetime" label="修改时间" width="120" sortable></el-table-column>
        <el-table-column prop="emailVerified" label="email绑定" sortable></el-table-column>
        <el-table-column prop="lastloginip" label="最后登录ip" ></el-table-column> 
        <el-table-column prop="lastdevice" label="最后登录设备" ></el-table-column> 
        <el-table-column prop="lastlogintime" label="最后登录时间" ></el-table-column> 
        <el-table-column prop="balance" label="余额" ></el-table-column>        
        <el-table-column prop="school_id" label="线下店" ></el-table-column>      
        <el-table-column prop="inviter_id" label="邀请者" ></el-table-column>      
        <el-table-column label="操作" width="240">
          <template slot-scope="scope">
            <el-button size="small" @click="showStdDialog(scope.$index,scope.row)">关联学生</el-button>
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

      <el-dialog title="关联学生" :visible.sync ="corStdFormVisible" :close-on-click-modal="false">
        <el-form :model="corStdeditForm" label-width="100px"  ref="corStdeditForm">
          <el-form-item label="会员名" prop="name" >
            <el-input v-model="corStdeditForm.name" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>
          <el-row>
            <el-col :span="16">
              <el-form-item >
                <el-input v-model="corStdeditForm.filtername" placeholder="请输入待关联学生姓名" @keyup.enter.native="corStdSearch">
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item>
                <el-button type="primary" v-on:click="corStdSearch">查询</el-button>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="8">
              <!--
              <el-select  v-model="corStdoption"  multiple  filterable remote reserve-keyword
                placeholder="请输入待关联学生姓名" :remote-method="remoteMethod" :loading="loading">
                <el-option v-for="item in corStdOptions" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
              </el-select>  
              -->

              <el-select v-model="corStdoption" placeholder="请选择待关联学生">
                <!--
                <el-option
                  v-for="item in corStdOptions" :key="item.value" :label="item.label" :value="item.value">
                  <span style="float: left">{{ item.label }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
                </el-option>
                 -->
                <el-option v-for="item in corStdOptions" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
              </el-select>  
            
            </el-col>              
            <el-col :span="8">
              <el-form-item label="学生关系">
                <el-select v-model="corStdeditForm.relation" placeholder="学生关系">
                  <el-option label="母亲" value="1"></el-option>
                  <el-option label="父亲" value="2"></el-option>
                  <el-option label="爷爷" value="3"></el-option>
                  <el-option label="奶奶" value="4"></el-option>
                  <el-option label="外公" value="5"></el-option>
                  <el-option label="外婆" value="6"></el-option>          
                  <el-option label="其他" value="7"></el-option>
                </el-select>
              </el-form-item>     
            </el-col>
            <el-col :span="8">
              <el-form-item label="关注点" prop="focus" >
                <el-input v-model="corStdeditForm.focus" auto-complete="off" ></el-input>
              </el-form-item>      
            </el-col>
          </el-row>     
          <!--       
          <el-form-item>
            <template>
              <el-transfer :titles="['未关联学生', '已关联学生']" v-model="corStdeditForm.studentIds" 
              :data="corStdeditForm.data">
              </el-transfer>
            </template>
          </el-form-item>
        -->
        </el-form>      
        <el-table :data="gridData">
          <el-table-column property="name" label="学生姓名" ></el-table-column>
          <el-table-column property="uid" label="学号" ></el-table-column>
          <el-table-column property="relationship" label="关系"></el-table-column>
          <el-table-column property="focus" label="关注点"></el-table-column>
          <el-table-column label="操作" width="80">
             <template slot-scope="scope1">
               <el-button size="small" @click="showStdGuardEditDialog(scope1.$index,scope1.row)">编辑</el-button>
             </template>
          </el-table-column>
        </el-table>         
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="corStdFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="corStdeditSubmit">提交</el-button>
        </div>
      </el-dialog>

      <el-dialog title="编辑" :visible.sync ="StdGuardEditFormVisible" :close-on-click-modal="false">
        <el-form :model="StdGuardEditForm" label-width="100px"  ref="StdGuardEditForm">
          <el-form-item label="姓名" prop="name">
            <el-input v-model="StdGuardEditForm.name" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="学号" prop="uid" >
            <el-input v-model="StdGuardEditForm.uid" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="关系" prop="relationship" auto-complete="off">
            <el-input v-model="StdGuardEditForm.relationship" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="关注点" prop="focus" auto-complete="off" >
            <el-input v-model="StdGuardEditForm.focus" auto-complete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="StdGuardEditFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="StdGuardEditSubmit">提交</el-button>
        </div>
      </el-dialog>


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
      <el-dialog title="新增会员" :visible.sync ="addFormVisible" :close-on-click-modal="false">

      <el-tabs v-model="editableTabsValue" type="card" :before-leave="beforeLevaeTab" editable @edit="handleTabsEdit" @tab-click="clickTab">
        <el-tab-pane label="会员信息" name="member">
          <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
          <el-row>
            <el-col :span="7">
              <el-form-item label="会员昵称" prop="nickname">
                <el-input v-model="addForm.nickname" auto-complete="off"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="7">
              <el-form-item label="会员名" prop="name">
                <el-input v-model="addForm.name" auto-complete="off"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="5">
              <el-form-item label="性别">
                <el-select v-model="addForm.sex" placeholder="性别">
                  <el-option label="男" value="1"></el-option>
                  <el-option label="女" value="2"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="5">
              <el-form-item label="会员级别" >
                <el-select v-model="addForm.memtype" placeholder="会员级别">
                  <el-option label="非付费会员" value="0"></el-option>
                  <el-option label="普通会员" value="1"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="地址" prop="address">
            <el-input v-model="addForm.address" auto-complete="off"></el-input>
          </el-form-item>

          <el-row>
            <el-col :span="8">
              <el-form-item label="省份" prop="province">
                <el-input v-model="addForm.province" auto-complete="off"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="城市" prop="city" auto-complete="off" >
                <el-input v-model="addForm.city" auto-complete="off"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="国家" prop="country" auto-complete="off" >
                 <el-input v-model="addForm.country" auto-complete="off"></el-input>
              </el-form-item> 
            </el-col>          
          </el-row>

          <el-row>
            <el-col :span="8">
              <el-form-item label="手机号" prop="mobile">
                <el-input v-model="addForm.mobile" auto-complete="off"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="邮箱" prop="email">
                <el-input v-model="addForm.email" auto-complete="off"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
               <el-form-item label="生日" prop="birthday">
                 <el-input v-model="addForm.birthday" placeholder="1980-01-01" auto-complete="off"></el-input>
               </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="8">
               <el-form-item label="学历" prop="education">
                 <el-input v-model="addForm.education" auto-complete="off"></el-input>
               </el-form-item>
            </el-col>
            <el-col :span="8">          
               <el-form-item label="行业" prop="industry">
                 <el-input v-model="addForm.industry" auto-complete="off"></el-input>
               </el-form-item>
            </el-col>
            <el-col :span="8">
               <el-form-item label="背景" prop="background">
                 <el-input v-model="addForm.background" auto-complete="off"></el-input>
               </el-form-item>
            </el-col>
          </el-row>  
          <el-form-item label="余额" prop="balance">
            <el-input v-model="addForm.balance" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="线下店" prop="school_id">
            <el-input v-model="addForm.school_id" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="邀请者" prop="inviter_id">
            <el-input v-model="addForm.inviter_id" auto-complete="off"></el-input>
          </el-form-item>    
          <el-form-item label="学生关系">
            <el-select v-model="relation" placeholder="学生关系">
              <el-option label="母亲" value="1"></el-option>
              <el-option label="父亲" value="2"></el-option>
              <el-option label="爷爷" value="3"></el-option>
              <el-option label="奶奶" value="4"></el-option>
              <el-option label="外公" value="5"></el-option>
              <el-option label="外婆" value="6"></el-option>          
              <el-option label="其他" value="7"></el-option>
            </el-select>
          </el-form-item>

          </el-form>

        </el-tab-pane>
        <el-tab-pane :key="item.name" v-for="(item, index) in editableTabs" :label="item.title" :name="item.name">
          <el-form :model="item.addStudentForm" label-width="100px" :rules="addStudentFormRules" ref="addStudentForm">
            <el-row>
              <el-col :span="8">
                  <el-form-item label="学号" prop="uid">
                    <el-input v-model="item.addStudentForm.uid" auto-complete="off"></el-input>
                  </el-form-item>
              </el-col>
              <el-col :span="8">
                  <el-form-item label="姓名" prop="name">
                    <el-input v-model="item.addStudentForm.name" auto-complete="off"></el-input>
                  </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="昵称" prop="nickname">
                  <el-input v-model="item.addStudentForm.nickname" auto-complete="off"></el-input>
                </el-form-item>   
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="8">
              <el-form-item label="性别">
                <el-select v-model="item.addStudentForm.sex" placeholder="请选择性别">
                  <el-option label="男" value="1"></el-option>
                  <el-option label="女" value="2"></el-option>
                </el-select>
              </el-form-item> 
              </el-col>
              <el-col :span="8">
                <el-form-item label="生日" prop="birthday" auto-complete="off" >
                  <el-input v-model="item.addStudentForm.birthday" auto-complete="off"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="学历" prop="education" auto-complete="off" >
                   <el-input v-model="item.addStudentForm.education" auto-complete="off"></el-input>
                </el-form-item> 
              </el-col>
            </el-row>

            <el-row>
              <el-col :span="8">
                <el-form-item label="省份" prop="province">
                  <el-input v-model="item.addStudentForm.province" auto-complete="off"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="城市" prop="city" auto-complete="off" >
                  <el-input v-model="item.addStudentForm.city" auto-complete="off"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="国家" prop="country" auto-complete="off" >
                   <el-input v-model="item.addStudentForm.country" auto-complete="off"></el-input>
                </el-form-item> 
              </el-col>          
            </el-row>
            <el-row>
              <el-col :span="12">
                  <el-form-item label="紧急联系人" prop="urgent_contactor" >
                    <el-input v-model="item.addStudentForm.urgent_contactor" auto-complete="off"></el-input>
                  </el-form-item>
              </el-col>
              <el-col :span="12">
                  <el-form-item label="联系人手机" prop="urgent_mobile" auto-complete="off" >
                    <el-input v-model="item.addStudentForm.urgent_mobile" auto-complete="off"></el-input>
                  </el-form-item>
              </el-col>
            </el-row>         
            <el-form-item label="头像" prop="image_url" auto-complete="off" :disabled="true">
              <el-input v-model="item.addStudentForm.image_url" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="授课教师" prop="mentor_id" auto-complete="off" :disabled="true">
              <el-input v-model="item.addStudentForm.mentor_id" auto-complete="off"></el-input>
            </el-form-item>  
          </el-form>      
  
        </el-tab-pane>
      </el-tabs>
        <div slot="footer" class="dialog-footer">
          <!-- el-button @click.native="addFormVisible = false">取消</el-button -->
          <el-button @click.native="addCancel">取消</el-button>
          <el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
        </div>
      </el-dialog>

    </el-col>
  </el-row>
</template>
<script>
  import util from '../../common/util'
  import API from '../../api/api_member';
  import APISTD from '../../api/api_student';
  import APISTDGARD from '../../api/api_studentGuard';
  export default{
    data(){
      return {
        filters: {
          name: '',
          mobile: ''
        },
        gridData: [
        { name: '1111',
          uid: '0001',
          relationship: '1',
          focus: '1'
        }
        ],
        members: [],
        total: 0,
        page: 1,
        limit: 10,
        loading: false,
        sels: [], //列表选中列

        //关联学生相关数据
        corStdFormVisible: false,//关联学生界面是否显示
        corStdeditForm: {
          memid:'',
          name: '',
          filtername: '',
          relationship:'',
          studentIds: [],
          data: []
        },
        corStdoption: [],
        corStdOptions: [],
        StdGuardEditFormVisible: false,
        StdGuardEditForm: {
          name: '',
          uid: '',
          relationship: '',
          focus: ''
        },        
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
        addStudentFormRules: {
          name: [
            {required: true, message: '请输入学生姓名', trigger: 'blur'}
          ],
          uid: [
            {required: true, message: '请输入学生昵称', trigger: 'blur'}
          ]  
        },

        addForm: {
          nickname: '',
          name: '',
          sex: '',
          address: '',
          province: '',
          city: '',
          country: '',
          wxunionid: '',          
          memtype: '',
          mobile: '',
          email: '',
          birthday: '',
          education: '',
          industry: '',
          background: '',
          emailVerified:'',
          balance: '',
          school_id: '',
          inviter_id: '',
          studentInfo:''
        },
        relation:'',
        stdguard:'',

        editableTabsValue: 'member',
        removeIndex: '',
        leaveTab: false,
        editableTabs: [{
          title: '学生 1',
          name: 'student1',
          addStudentForm: {
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
        }],
        tabIndex: 1
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

      remoteMethod(query) {
        let that = this;
        if (query !== '') {
          this.loading = true;
          setTimeout(() => {
            this.loading = false;
            /*
            this.corStdOptions = this.list.filter(item => {
              return item.label.toLowerCase()
                .indexOf(query.toLowerCase()) > -1;
            });
            */
            let params = query;
            console.log(params);
            APISTD.findByName(params).then(function (result) {
              if (result && result.stdinfos) {
                if (result.stdinfos.length > 0) {
                    console.log("remoteMethod");
                    console.log(result.stdinfos);
                    that.corStdOptions = result.stdinfos;
                    /*
                    for(var i=0;i<result.stdinfos.length;i++){
                      that.corStdeditForm.data.push(result.stdinfos[i]);       
                    }
                    */
                } else{
                   that.$message.error({showClose: true, message: '查询不到学生信息', duration: 5000});
                }
              }
    
            }, function (err) {
              that.$message.error({showClose: true, message: err.toString(), duration: 2000});
            }).catch(function (error) {
              console.log(error);
              that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
            });    
    

          }, 200);
        } else {
          this.corStdOptions = [];
        }
      },

      corStdSearch(){
        console.log("get corelation student");
        let that = this;
        let params = that.corStdeditForm.filtername;
        console.log(params);
        APISTD.findByName(params).then(function (result) {
          if (result && result.stdinfos) {
            if (result.stdinfos.length > 0) {
                console.log("corstdSearch");
                console.log(result.stdinfos);
                that.corStdOptions = result.stdinfos;
                /*
                for(var i=0;i<result.stdinfos.length;i++){
                  var isKeyExist = 0;
                  for(var j=0;j<that.corStdeditForm.data.length;j++){
                    if (result.stdinfos[i].key == that.corStdeditForm.data[i].key){
                      isKeyExist = 1;
                      break;
                    }
                  }
                  if (isKeyExist == 0){
                    that.corStdeditForm.data.push(result.stdinfos[i]);       
                  }
                }
                */
            } else{
               that.$message.error({showClose: true, message: '查询不到学生信息', duration: 5000});
            }
          }

        }, function (err) {
          that.$message.error({showClose: true, message: err.toString(), duration: 2000});
        }).catch(function (error) {
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
              //replace sex prop
              that.members.forEach((member, index) => {
                if (member.sex == '1'){
                  member.sex = '男'
                }else{
                  member.sex = '女'
                }
                if (member.memtype == '0'){
                  member.memtype = '非付费会员'
                }else{
                  member.memtype = '普通会员'
                }

                member.studentInfo.forEach((std, index) => {
                  if (std.sex == '1'){
                    std.sex = '男'
                  }else{
                    std.sex = '女'
                  }
                });

              });  

              console.log("result.member is ");
              console.log(result.members);
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
      showStdDialog: function (index, row) {
        let that = this;
        that.corStdFormVisible = true;
        that.corStdeditForm.data = [];
        that.corStdeditForm.studentIds = [];
        that.corStdeditForm.filtername = "";

        let member = Object.assign({}, row);
        that.corStdeditForm.name = member.name;
        that.corStdeditForm.memid = member.id;
        //that.corStdeditForm.relationship = "";

        for(var i=0;i<member.studentInfo.length;i++){
          let value = member.studentInfo[i]['name'] + '(' + member.studentInfo[i]['uid'] +')';
          that.corStdeditForm.data.push({key:member.studentInfo[i]['id'],label:value});
          that.corStdeditForm.studentIds.push(member.studentInfo[i]['id']);
        }
      },
      //编辑
      corStdeditSubmit: function () {
        let that = this;
        that.loading = true;
        let para = Object.assign({}, that.corStdeditForm);
        console.log(para);
        console.log(para.studentIds);

        let params = {
          //focus: 2,
          relationship: 1,
          studentIds: that.corStdeditForm.studentIds
        };

        APISTDGARD.updateByMemberID(that.corStdeditForm.memid, params).then(function (result) {
              that.loading = false;
              if (result && parseInt(result.errcode) === 0) {
                that.$message.success({showClose: true, message: '修改成功', duration: 4000});
                //that.$refs['editForm'].resetFields();
                that.corStdFormVisible = false;
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
        that.corStdFormVisible = false;
      },
      // 关联学生编辑
      showStdGuardEditDialog: function (index, row) {
        console.log("showStdGuardEditDialog");
        this.StdGuardEditFormVisible = true;
        this.StdGuardEditForm = Object.assign({}, row);
      },

      StdGuardEditSubmit: function () {
        let that = this;

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
      //新增会员和学生
      addSubmit: function () {
        let that = this;
        that.loading = true;
        let validFailCount = 0;
    
        // check member validate
        that.$refs.addForm.validate((valid) => {
          if (!valid) {
            validFailCount++;
          }
        });
 
        // check student validate
        let tabs = this.editableTabs;
        tabs.forEach((tab, index) => {
          this.$refs.addStudentForm[index].validate((valid) => {
            if (!valid) {
              validFailCount++;
            }
          });
        });  
        console.log("valid flag is ");
   
        
        if (validFailCount == 0) {
          console.log("valid is pass");
          // get studentguard data 
          let studentids = [];
          this.editableTabs.forEach((tab, index) => {   
          studentids.push(tab.addStudentForm.uid);
          });
          console.log("student id is:");
          console.log(studentids);
          console.log("realtion is:");
          console.log(this.relation);
          //let mobile = this.addForm.mobile;
          //let relation = this.relation;

          let stdguard = {
            memmobile: this.addForm.mobile,
            relationship: this.relation,
            studentids: studentids           
          }

          this.stdguard = Object.assign({}, stdguard);

        
          this.addStudent();
          //this.addMember();
          //this.addStdGuard(stdguard);
 

          that.loading = false;
          // clear studentids list
          //this.studentids = [];
          that.search();
        }else{
          console.log("valid is failed.");
          that.$message.error({showClose: true, message: '请输入必填字符后重新提交', duration: 2000});

        }

      },

      // 新增会员取消
      addCancel: function() {
        console.log("add member is cancel");
        let that = this;
        this.addFormVisible = false;        
        this.editableTabsValue = 'member';
        this.tabIndex = 1 ;
        this.editableTabs = [{ title: '学生 1',
                                     name: 'student1',
                                     addStudentForm: {
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
                                   }] ;

        this.$refs['addForm'].resetFields();  
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
      },
      addMember: function () {
        let that = this;
        let para = Object.assign({}, this.addForm);
        API.add(para).then(function (result) {
          that.loading = false;
          if (result && parseInt(result.errcode) === 0) {
            that.$message.success({showClose: true, message: '创建新会员成功', duration: 5000});
            that.addStdGuard();
            that.$refs['addForm'].resetFields();
            that.addFormVisible = false;
            that.search();
          } else {
            that.$message.error({showClose: true, message: '创建新会员失败', duration: 2000});
          }
        }, function (err) {
          //that.loading = false;
          that.$message.error({showClose: true, message: err.toString(), duration: 2000});
        }).catch(function (error) {
          //that.loading = false;
          console.log(error);
          that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
        });  
      },

      addStudent: function () {
        let that = this;
        let tabs = this.editableTabs;
        tabs.forEach((tab, index) => {
          let para = Object.assign({}, tab.addStudentForm);
          APISTD.add(para).then(function (result) {
            if (result && parseInt(result.errcode) === 0) {
              that.$message.success({showClose: true, message: '创建新学生成功', duration: 5000});
              that.addMember();
            } else {
              that.$message.error({showClose: true, message: '创建新学生失败', duration: 2000});
            }
          }, function (err) {
            //that.loading = false;
            that.$message.error({showClose: true, message: err.toString(), duration: 2000});
          }).catch(function (error) {
            //that.loading = false;
            console.log(error);
            that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
          });
        });
      },

      addStdGuard: function () {
        let that = this;
        /*
        let para = {
          realtion: that.realtion,
          mobile: that.addForm.mobile,
          studentids: that.studentids
        };
        */
        let para = that.stdguard;
        console.log(para);      
        APISTDGARD.add(para).then(function (result) {
          if (result && parseInt(result.errcode) === 0) {
            that.$message.success({showClose: true, message: '关联学生成功', duration: 5000});
          } else {
            that.$message.error({showClose: true, message: '关联学生失败', duration: 2000});
          }
        }, function (err) {
          //that.loading = false;
          that.$message.error({showClose: true, message: err.toString(), duration: 2000});
        }).catch(function (error) {
          //that.loading = false;
          console.log(error);
          that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
        });
      },


      beforeLevaeTab() {
        console.log("validInput function");
        console.log(this.editableTabsValue);
        if (this.editableTabsValue == 'member'){
          
          this.$refs.addForm.validate((valid) => {
            if (valid) {
              this.leaveTab = true;
              //return true;
            }
            else{
              console.log("valid is failed");
              this.leaveTab = false;
              //return false;
            }
          });
          console.log(this.leaveTab);
          //return this.leaveTab;          
        }
        else {
          
          let tabs = this.editableTabs;
          tabs.forEach((tab, index) => {
            if (tab.name === this.editableTabsValue) {
              console.log("currentTab");
              console.log(this.editableTabsValue);
              console.log(this.$refs.addStudentForm.length);
              console.log("index is: ");
              console.log(index);
              this.$refs.addStudentForm[index].validate((valid) => {
                if (valid) {
                  this.leaveTab = true;
                  //return true;
                }
                else{
                  console.log("valid is failed");
                  this.leaveTab = false;
                  //return false;
                }
              });
              
            }
         });       
         
       }
       return this.leaveTab; 
      },

      expandChange(row, expandedRows){
        let that = this;
        console.log('row is');
        console.log(row);
        console.log(expandedRows);
        let arr = Array.from(row.studentInfo);
        console.log(arr);
        row.studentInfo = arr;
        /*
        APISTDGARD.GetStudentByMemmobile(row.mobile).then(function (result) {
          if (result && parseInt(result.errcode) === 0) {
            //that.$message.success({showClose: true, message: '关联学生成功', duration: 5000});
          } else {
            that.$message.error({showClose: true, message: '获取关联学生信息失败，请重试', duration: 2000});
          }
        }, function (err) {
          that.$message.error({showClose: true, message: err.toString(), duration: 2000});
        }).catch(function (error) {
          console.log(error);
          that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
        });
        */

      },


      clickTab(tab, event) {
        console.log('click tab');
        console.log(tab, event);


      },

      handleTabsEdit(targetName, action) {
        if (action === 'add') {
          let newTabName = ++this.tabIndex + '';
          console.log(newTabName);
          this.editableTabs.push({
            title: '学生 '+ newTabName,
            name: newTabName,
            addStudentForm: {
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
          });
          //this.editableTabsValue = newTabName;
        }
        if (action === 'remove') {
          console.log("remove tab");
          let tabs = this.editableTabs;
          let activeName = this.editableTabsValue;

          if (activeName === targetName) {
            tabs.forEach((tab, index) => {
              if (tab.name === targetName) {
                let nextTab = tabs[index + 1] || tabs[index - 1];
                if (nextTab) {
                  activeName = nextTab.name;
                }
                console.log("clear validatae");
                console.log(targetName);
                console.log(index);
                this.removeIndex = index;
                this.$refs.addStudentForm[index].resetFields();

              }
            });
          }
          tabs.splice(this.removeIndex, 1);
          if (tabs.length == 1) {
            this.editableTabsValue = 'member' ;
          }
          else{
            this.editableTabsValue = activeName;
          }
          
          //this.editableTabs = tabs.filter(tab => tab.name !== targetName);
        }
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
