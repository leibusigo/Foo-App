import { useCallback, useState } from 'react'
import * as algorithmServices from '../services/algorithmAction'

export default function useAlgorithm() {
  // 异常
  const [algorithmError, setAlgorithmError] = useState('')
  // 加载
  const [algorithmLoaded, setAlgorithmLoaded] = useState(false)
  const [algorithmStatus, setAlgorithmStatus] = useState('')
  const [epoch, setEpoch] = useState(1)

  // const [turn, setTurn] = useState(1)

  const loopTracking = useCallback(async (epoch: number) => {
    try {
      setAlgorithmError('')
      setAlgorithmLoaded(false)
      const { code, data } = await algorithmServices.loopTracking(String(epoch))
      if (code === 0) {
        setAlgorithmStatus(data)
        return data
      }
      return ''
    } catch (error: any) {
      setAlgorithmError(error.message)
      return ''
    } finally {
      setAlgorithmLoaded(true)
    }
  }, [])

  const rangeTracking = useCallback(async () => {
    try {
      setAlgorithmError('')
      setAlgorithmLoaded(false)
      await algorithmServices.rangeTracking()
    } catch (error: any) {
      setAlgorithmError(error.message)
    } finally {
      setAlgorithmLoaded(true)
    }
  }, [])

  const stopTracking = useCallback(async (value: string) => {
    try {
      setAlgorithmError('')
      setAlgorithmLoaded(false)
      await algorithmServices.stopTracking(value)
    } catch (error: any) {
      setAlgorithmError(error.message)
    } finally {
      setAlgorithmLoaded(true)
    }
  }, [])

  // 开始跟踪
  const startTracking = useCallback(
    async (epoch: number) => {
      try {
        setAlgorithmError('')
        setAlgorithmLoaded(false)
        const { code, data } = await algorithmServices.startTracking(
          String(epoch)
        )
        if (code === 0) {
          setAlgorithmStatus(data)
          if (data !== 'ocr识别到特定目标物品') {
            while (1) {
              const res = await loopTracking(epoch + 1)
              setEpoch(epoch + 1)
              if (res === 'ocr识别到特定目标物品') {
                await rangeTracking()
                break
              } else if (res === '未检测到目标') {
                await stopTracking(res)
                break
              }
            }
          } else {
            await rangeTracking()
            setEpoch(epoch + 1)
          }
        }
      } catch (error: any) {
        setAlgorithmError(error.message)
      } finally {
        setAlgorithmLoaded(true)
      }
    },
    [loopTracking, rangeTracking, stopTracking]
  )

  return {
    epoch,
    algorithmError,
    algorithmLoaded,
    algorithmStatus,
    startTracking,
  }
}
