/**
 * Created by liqiang on 2018/07/18.
 * 套餐相关api
 */
import * as API from './'

export default {

  //查询获取套餐列表(通过page分页)
  findList: params => {
    return API.GET('/api/v1/courses', params)
  },

  //查询获取一个套餐信息
  findById: id => {
    return API.GET(`/api/v1/courses/${id}`)
  },

  add: params => {
    return API.POST(`/api/v1/courses`, params)
  },
  update: (id, params) => {
    return API.PUT(`/api/v1/courses/${id}`, params)
  },

  //单个删除course
  remove: id => {
    return API.DELETE(`/api/v1/courses/${id}`)
  },

  //批量删除，传ids数组
  removeBatch: (ids) => {
    return API.DELETE(`/api/v1/courses/batch/${ids}`)
  }

}
