import { useState } from 'react'
import { useRoutes } from 'react-router-dom'

// 导入路由表
import { StoreProvider } from '../../hooks/store'
import routerConfig from '../../routers'
import { IRobotInfo } from '../../types/models'

export default function App() {
  const element = useRoutes(routerConfig)
  const [robotInfo, setRobotInfo] = useState<IRobotInfo>({
    battery: '',
    status: '',
  })
  const [imageVisible, setImageVisible] = useState(false)

  return (
    <StoreProvider
      value={{
        robotInfo,
        setRobotInfo,
        imageVisible,
        setImageVisible,
      }}
    >
      {element}
    </StoreProvider>
  )
}
