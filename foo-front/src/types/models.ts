export interface ApiResp<T = any> {
  code: number
  message: string
  data: T
}

export interface IRobotInfo {
  battery: string
  status: string
}
