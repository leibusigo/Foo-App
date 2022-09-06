import { Toast } from 'antd-mobile'
import axios from 'axios'

const whiteList = ['/login']

const instance = axios.create({
  baseURL: '/api',
  validateStatus: status => status < 500,
})

instance.interceptors.response.use(
  res => {
    if (
      res.data.code === 40001 &&
      whiteList.indexOf(window.location.pathname) === -1
    ) {
      window.location.href = '/login'
    } else if (res.data.code !== 0 && res.data.code !== 40001) {
      Toast.show(res.data.message)
    }

    return res
  },
  err => {
    // if (whiteList.indexOf(window.location.pathname) === -1) {
    //   window.location.href = '/notFound'
    // }

    return Promise.reject(err)
  }
)

export default instance
