import { createContext } from 'react'

import { IRobotInfo } from '../types/models'

interface IContext {
  // 机器人信息
  robotInfo: IRobotInfo
  setRobotInfo: (robotInfo: IRobotInfo) => void
}

// 创建context对象
const context = createContext<IContext>({
  robotInfo: {
    battery: '',
    status: '',
  },
  setRobotInfo: () => {},
})

// 创建生产者
const StoreProvider = context.Provider

export { context, StoreProvider }
