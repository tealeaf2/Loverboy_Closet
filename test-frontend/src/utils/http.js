// basic axios wrapping

import axios from "axios"

const httpInstane= axios.create({
    baseURL:'http://127.0.0.1:5000',
    timeout: 5000
})


// axios请求拦截器
httpInstane.interceptors.request.use(config => {
    return config
  }, e => Promise.reject(e))
  
// axios响应式拦截器
httpInstane.interceptors.response.use(res => res.data, e => {
    return Promise.reject(e)
})
  

export default httpInstane