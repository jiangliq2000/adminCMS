/**
 * Created by jerry on 2017/6/9.
 */
import axios from 'axios'
import {bus} from '../bus.js'

axios.defaults.withCredentials = true;
// axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;
// axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';//配置请求头



//添加一个请求拦截器
axios.interceptors.request.use(config => {

    // 下面会说在什么时候存储 token
    if (sessionStorage.getItem('token')) {   
        config.headers.Authorization = "JWT " + sessionStorage.getItem('token');
    }
    return config;
},error =>{
    console.log(error);
    alert("错误的传参", 'fail');
    return Promise.reject(error);
});


/*
// 添加一个响应拦截器
axios.interceptors.response.use(function (response) {
  if (response.data && response.data.status_code) {
    if (parseInt(response.data.status_code) === 401) {
      //未登录
      bus.$emit('goto', '/login')
    }
  }

  return response;
}, function (error) {
  // Do something with response error
  return Promise.reject(error);
});

*/

// 添加一个响应拦截器
axios.interceptors.response.use(function (response) {
  if (response.data && response.data.errcode) {
    if (parseInt(response.data.errcode) === 40001) {
      //未登录
      bus.$emit('goto', '/login')
    }
  }

  return response;
}, function (error) {
  // Do something with response error

  if (error.response) {
      switch (error.response.status) {
          case 401:
              // 401 清除token信息并跳转到登录页面
              if (sessionStorage.getItem('access-user')){
                  alert("token 已经过期，请重新登录！");
              }
              
              sessionStorage.removeItem('token');  
              sessionStorage.removeItem('access-user');
              location.href = '/#/login';
      }
  }  
  return Promise.reject(error);
});

//基地址
let base = '';  //接口代理地址参见：config/index.js中的proxyTable配置

//通用方法
export const POST = (url, params) => {
  return axios.post(`${base}${url}`, params).then(res => res.data)
}

export const GET = (url, params) => {
  return axios.get(`${base}${url}`, {params: params}).then(res => res.data)
}

export const PUT = (url, params) => {
  return axios.put(`${base}${url}`, params).then(res => res.data)
}

export const DELETE = (url, params) => {
  return axios.delete(`${base}${url}`, {params: params}).then(res => res.data)
}

export const PATCH = (url, params) => {
  return axios.patch(`${base}${url}`, params).then(res => res.data)
}
