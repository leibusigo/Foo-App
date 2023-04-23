import request from '../libs/request'
import { ApiResp } from '../types/models'

// 开始跟踪接口
export async function startTracking(isFirst:boolean) {
  const { data } = await request.get<ApiResp>(
    `/py27/algorithm/startTracking?${new URLSearchParams('isFirst=' + isFirst)}`
  )

  return data
}

// 循环跟踪接口
export async function loopTracking(epoch: string) {
  const { data } = await request.get<ApiResp>(
    `/py27/algorithm/loopTracking?${new URLSearchParams('epoch=' + epoch)}`
  )

  return data
}

// 测距跟踪接口
export async function rangeTracking() {
  const { data } = await request.get<ApiResp>('/py27/algorithm/rangeTracking')

  return data
}

// 结束跟踪接口
export async function stopTracking(value: string) {
  const { data } = await request.get<ApiResp>(
    `/py27/algorithm/stopTracking?${new URLSearchParams('value=' + value)}`
  )

  return data
}
