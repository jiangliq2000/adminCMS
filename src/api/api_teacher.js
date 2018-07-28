/**
 * Created by liqiang on 2018/06/10.
 * 教师相关api
 */
import * as API from './'

export default {

  //查询获取教师列表(通过page分页)
  findList: params => {
    return API.GET('/api/v1/teachers', params)
  },

  //查询获取一条教师信息
  findByMobile: mobile => {
    return API.GET(`/api/v1/teachers/mobile/${mobile}`)
  },


  findById: id => {
    return API.GET(`/api/v1/teachers/id/${id}`)
  },



  //查询获取一条或多条教师信息, 通过模糊匹配查询
  GetTeacherInfoByName: name => {
    return API.GET(`/api/v1/teachers/teacherinfo/${name}`)
  },

  add: params => {
    return API.POST(`/api/v1/teachers`, params)
  },
  update: (id, params) => {
    return API.PUT(`/api/v1/teachers/${id}`, params)
  },

  //单个删除教师
  remove: id => {
    return API.DELETE(`/api/v1/teachers/${id}`)
  },

  //批量删除，传ids数组
  removeBatch: (ids) => {
    return API.DELETE(`/api/v1/teachers/batch/${ids}`)
  }

}
