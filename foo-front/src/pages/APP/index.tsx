// import { useState } from 'react'
import { useRoutes } from 'react-router-dom'

// 导入路由表
// import { StoreProvider } from '../../hooks/store'
import routerConfig from '../../routers'

export default function App() {
  const element = useRoutes(routerConfig)

  return (
    // <StoreProvider
    //   value={{

    //   }}
    // >
    <>{element}</>
    // </StoreProvider>
  )
}
