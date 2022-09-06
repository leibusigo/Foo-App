import { Toast } from 'antd-mobile'
import { useState, useCallback, useContext, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import * as basicServices from '../services/basicAciton'
import { context } from './store'

export default function useBasic() {
  // 异常
  const [basicError, setBasicError] = useState('')
  // 加载
  const [basicLoaded, setBasicLoaded] = useState(false)
  const [first, setFrist] = useState(false)
  const { setRobotInfo } = useContext(context)
  const navigate = useNavigate()

  // 连接
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
        switch (error.request.status) {
          case 500:
            Toast.show('ip地址错误或网络异常，请重新连接')
            break
          case 504:
            Toast.show('服务器异常，请检查是否开启服务器')
            break
          default:
            break
        }

        setBasicError(error.message)
      } finally {
        setBasicLoaded(true)
      }
    },
    [navigate]
  )

  // 连接
  const info = useCallback(async () => {
    try {
      setBasicError('')
      setBasicLoaded(false)
      const { code, data } = await basicServices.info()
      if (code === 0) {
        setRobotInfo(data)
      }
    } catch (error: any) {
      if (error.request.status === 500) {
        Toast.show('ip地址错误或网络异常，请重新连接')
      }

      setBasicError(error.message)
    } finally {
      setBasicLoaded(true)
    }
  }, [setRobotInfo])

  // 说话
  const speak = useCallback(async (value: string) => {
    try {
      setBasicError('')
      setBasicLoaded(false)
      await basicServices.speak(value)
    } catch (error: any) {
      Toast.show(error.message)
      setBasicError(error.message)
    } finally {
      setBasicLoaded(true)
    }
  }, [])

  // 行走
  const walk = useCallback(async (distance: string, angle: string) => {
    try {
      setBasicError('')
      setBasicLoaded(false)
      if (
        parseFloat(distance) < 0 ||
        distance.trim() === '' ||
        parseFloat(angle) < -Math.PI ||
        parseFloat(angle) > Math.PI
      ) {
        Toast.show('参数不能为空，距离不能小于0，角度必须在-1派到1派之间')
      } else {
        await basicServices.walk(distance, angle)
      }
    } catch (error: any) {
      Toast.show(error.message)
      setBasicError(error.message)
    } finally {
      setBasicLoaded(true)
    }
  }, [])

  // 唤醒
  const wake = useCallback(async () => {
    try {
      setBasicError('')
      setBasicLoaded(false)
      await basicServices.wake()
    } catch (error: any) {
      Toast.show(error.message)
      setBasicError(error.message)
    } finally {
      setBasicLoaded(true)
    }
  }, [])

  // 停止
  const stop = useCallback(async () => {
    try {
      setBasicError('')
      setBasicLoaded(false)
      await basicServices.stop()
    } catch (error: any) {
      Toast.show(error.message)
      setBasicError(error.message)
    } finally {
      setBasicLoaded(true)
    }
  }, [])

  useEffect(() => {
    if (!first) {
      setFrist(true)
      info()
    }
  }, [first, info])

  return {
    basicError,
    basicLoaded,
    connect,
    speak,
    wake,
    stop,
    walk,
  }
}
