/**
 * Created by liqiang on 2018/06/10.
 * 教师相关api
 */
import * as API from './'

export default {

  //查询获取member列表(通过page分页)
  findList: params => {
    return API.GET('/api/v1/teachers', params)
  },

  //查询获取一条book信息
  findById: id => {
    return API.GET(`/api/v1/teachers/${id}`)
  },

  add: params => {
    return API.POST(`/api/v1/teachers`, params)
  },
  update: (id, params) => {
    return API.PUT(`/api/v1/teachers/${id}`, params)
  },

  //单个删除book
  remove: id => {
    return API.DELETE(`/api/v1/teachers/${id}`)
  },

  //批量删除，传ids数组
  removeBatch: (ids) => {
    return API.DELETE(`/api/v1/teachers/batch/${ids}`)
  }

}
