import { useCallback, useState } from 'react'
import * as algorithmServices from '../services/algorithmAction'

export default function useAlgorithm() {
  // 异常
  const [algorithmError, setAlgorithmError] = useState('')
  // 加载
  const [algorithmLoaded, setAlgorithmLoaded] = useState(false)
  const [algorithmStatus, setAlgorithmStatus] = useState('')

  const startTracking = useCallback(async (epoch: number) => {
    try {
      setAlgorithmError('')
      setAlgorithmLoaded(false)
      const { code, data } = await algorithmServices.startTracking(
        String(epoch)
      )
      if (code === 0) {
        setAlgorithmStatus(data)
      }
    } catch (error: any) {
      setAlgorithmError(error.message)
    } finally {
      setAlgorithmLoaded(true)
    }
  }, [])

  return {
    algorithmError,
    algorithmLoaded,
    algorithmStatus,
    startTracking,
  }
}
