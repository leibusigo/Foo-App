import request from '../libs/request'
import { ApiResp } from '../types/models'

// 建立连接
export async function connect(ip: string) {
  const { data } = await request.get<ApiResp>(
    `/py27/basic/connect?${new URLSearchParams('ip=' + ip)}`
  )

  return data
}

// 建立连接
export async function info() {
  const { data } = await request.get<ApiResp>('/py27/basic/info')

  return data
}

// 说话
export async function speak(value: string) {
  const { data } = await request.post<ApiResp>('/py27/basic/speak', { value })

  return data
}

// 唤醒
export async function wake() {
  const { data } = await request.get<ApiResp>('/py27/basic/wake')

  return data
}

// 停止
export async function stop() {
  const { data } = await request.get<ApiResp>('/py27/basic/stop')

  return data
}
