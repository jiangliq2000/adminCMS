/**
 * Created by liqiang on 20180615.
 * 学生相关api
 */
import * as API from './'

export default {

  //查询获取学生列表(通过page分页)
  findList: params => {
    return API.GET('/api/v1/students', params)
  },

  //查询获取一个学生信息
  findById: id => {
    return API.GET(`/api/v1/students/${id}`)
  },


  //获取一个学生信息根据学生记录的id
  findBySid: sid => {
    return API.GET(`/api/v1/students/stdinfo/id/${sid}`)
  },


  //查询获取关联学生信息
  findByName: name => {
    return API.GET(`/api/v1/students/stdinfo/${name}`)
  },


  add: params => {
    return API.POST(`/api/v1/students`, params)
  },
  update: (id, params) => {
    return API.PUT(`/api/v1/students/${id}`, params)
  },

  //单个删除book
  remove: id => {
    return API.DELETE(`/api/v1/students/${id}`)
  },

  //批量删除，传ids数组
  removeBatch: (ids) => {
    return API.DELETE(`/api/v1/students/batch/${ids}`)
  }

}
