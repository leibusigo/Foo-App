import request from '../libs/request'
import { ApiResp } from '../types/models'

// 建立连接
export async function connect(ip: string) {
  const { data } = await request.get<ApiResp>(
    `/py27/basic/connect?${new URLSearchParams('ip=' + ip)}`
  )

  return data
}

// 获取基本信息
export async function info() {
  const { data } = await request.get<ApiResp>('/py27/basic/info')

  return data
}

// 说话
export async function speak(value: string) {
  const { data } = await request.post<ApiResp>('/py27/basic/speak', { value })

  return data
}

// 行走
export async function walk(distance: string, angle: string) {
  const { data } = await request.post<ApiResp>('/py27/basic/walk', {
    distance,
    angle,
  })

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

// 摄像
export async function camera(cameraId: string) {
  const { data } = await request.get<ApiResp>(
    `/py27/basic/camera?${new URLSearchParams('id=' + cameraId)}`
  )

  return data
}
