import { Toast } from 'antd-mobile'
import axios from 'axios'

const instance = axios.create({
  baseURL: '/api',
  validateStatus: status => status < 500,
})

instance.interceptors.response.use(res => {
  if (res.data.code !== 0) {
    Toast.show(res.data.message)
  }

  return res
})

export default instance
