/**
 * Created by liqiang on 20180615.
 * 学生家长关系表相关api
 */
import * as API from './'

export default {

  findList: params => {
    return API.GET('/api/v1/studentGuards', params)
  },

  findByMemberId: id => {
    return API.GET(`/api/v1/studentGuards/memberid/${id}`)
  },

  GetStudentByMemmobile: id => {
    return API.GET(`/api/v1/studentGuards/memmobile/${id}`)
  },  

  add: params => {
    return API.POST(`/api/v1/studentGuards`, params)
  },
  // 根据member id 更新记录
  updateByMemberID: (id, params) => {
    return API.PUT(`/api/v1/studentGuards/memberid/${id}`, params)
  },

  // 根据student id 更新记录
  updateByStudentID: (id, params) => {
    return API.PUT(`/api/v1/studentGuards/studentid/${id}`, params)
  },

  remove: id => {
    return API.DELETE(`/api/v1/studentGuards/${id}`)
  },

  //批量删除，传ids数组
  removeBatch: (ids) => {
    return API.DELETE(`/api/v1/studentGuards/batch/${ids}`)
  }

}
