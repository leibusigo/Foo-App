import request from '../libs/request'
import { ApiResp } from '../types/models'

// 建立连接
export async function connect(ip: string) {
  const { data } = await request.get<ApiResp>(
    `/py27/basic/connect?${new URLSearchParams('ip=' + ip)}`
  )

  return data
}
