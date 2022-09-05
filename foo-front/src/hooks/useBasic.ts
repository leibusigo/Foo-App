import { Toast } from 'antd-mobile'
import { useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import * as basicServices from '../services/basicAciton'

export default function useBasic() {
  // 异常
  const [basicError, setBasicError] = useState('')
  // 加载
  const [basicLoaded, setBasicLoaded] = useState(false)
  const navigate = useNavigate()

  const connect = useCallback(
    async (ip: string) => {
      try {
        setBasicError('')
        setBasicLoaded(false)
        const { code } = await basicServices.connect(ip)
        if (code === 0) {
          navigate('/')
          Toast.show('连接成功')
        }
      } catch (error: any) {
        if (error.request.status === 500) {
          Toast.show('ip地址错误或网络异常，请重新连接')
        }

        setBasicError(error.message)
      } finally {
        setBasicLoaded(true)
      }
    },
    [navigate]
  )

  return {
    basicError,
    basicLoaded,
    connect,
  }
}
