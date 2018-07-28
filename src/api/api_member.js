/**
 * Created by liqiang on 2018/05/30.
 * 会员相关api
 */
import * as API from './'

export default {

  //查询获取member列表(通过page分页)
  findList: params => {
    return API.GET('/api/v1/members', params)
  },

  //查询获取单个会员信息
  findById: id => {
    return API.GET(`/api/v1/members/${id}`)
  },

  add: params => {
    return API.POST(`/api/v1/members`, params)
  },
  update: (id, params) => {
    return API.PUT(`/api/v1/members/${id}`, params)
  },

  //单个删除会员
  remove: id => {
    return API.DELETE(`/api/v1/members/${id}`)
  },

  //批量删除，传ids数组
  removeBatch: (ids) => {
    return API.DELETE(`/api/v1/members/batch/${ids}`)
  }

}
