/**
 * Created by liqiang on 2018/07/21.
 * 课程相关api
 */
import * as API from './'

export default {

  //查询获取课程列表(通过page分页)
  findList: params => {
    return API.GET('/api/v1/lessons', params)
  },

  //查询获取一个课程信息
  GetByName: name => {
    return API.GET(`/api/v1/lessons/${name}`)
  },

    //查询获取一个课程信息
  findById: id => {
    return API.GET(`/api/v1/lessons/id/${id}`)
  },

  add: params => {
    return API.POST(`/api/v1/lessons`, params)
  },
  update: (id, params) => {
    return API.PUT(`/api/v1/lessons/${id}`, params)
  },
  updateCourseId: (id, params) => {
    return API.PUT(`/api/v1/lessons/courseid/${id}`, params)
  },

  //单个删除lesson
  remove: id => {
    return API.DELETE(`/api/v1/lessons/${id}`)
  },

  //批量删除，传ids数组
  removeBatch: (ids) => {
    return API.DELETE(`/api/v1/lessons/batch/${ids}`)
  }

}
