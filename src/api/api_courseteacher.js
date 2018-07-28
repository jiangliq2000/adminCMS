/**
 * Created by liqiang on 2018/07/25.
 * 套餐教师相关api
 */
import * as API from './'

export default {


  update: (cid, params) => {
    return API.PUT(`/api/v1/courseteachers/${cid}`, params)
  }

}
