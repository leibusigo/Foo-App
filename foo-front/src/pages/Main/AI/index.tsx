import { Button, Image } from 'antd-mobile'
import { useEffect, useMemo, useState } from 'react'

import useAlgorithm from '../../../hooks/useAlgorithm'
import styles from './index.module.scss'
import useDebounce from '../../../hooks/useDebounce'
import AlgorithmModal from '../../../components/AlgorithmModal'

export default function AI() {
  const [trackModalVisible, setTrackModalVisible] = useState(false)
  const {
    algorithmStatus,
    setAlgorithmStatus,
    epoch,
    startTracking,
    stopTracking,
  } = useAlgorithm()
  const { debounce } = useDebounce()

  useEffect(() => {
    if (algorithmStatus === '未检测到目标') {
      setTimeout(() => {
        setTrackModalVisible(false)
      }, 3000)
    }
  }, [algorithmStatus])

  const imgUrl = useMemo(() => {
    if (algorithmStatus === '没有目标类别物品') {
      return `/img/epoch${epoch}/origin.jpg`
    } else if (algorithmStatus === '算法运行中') {
      return '/img/default.png'
    } else {
      return `/img/epoch${epoch}/cut.jpg`
    }
  }, [algorithmStatus, epoch])

  const trackingProcess = useMemo(() => {
    return (
      <AlgorithmModal visible={trackModalVisible}>
        <h1 className={styles.modal_title}>Nao特定目标跟踪算法</h1>
        <div className={styles.modal}>
          <div className={styles.img_container}>
            <Image
              className={styles.img}
              src={require('../../../assets' + imgUrl)}
              fit="contain"
            />
          </div>
          <h2 className={styles.algorithm_status}>
            当前算法状态：
            <br />
            <br />
            {algorithmStatus}
          </h2>
          {algorithmStatus === 'ocr识别到特定目标物品' && (
            <Button
              className={styles.continue}
              onClick={() => {
                debounce(() => {
                  startTracking(1, false)
                }, 1000)
                setAlgorithmStatus('算法运行中')
              }}
              color="success"
            >
              继续检测
            </Button>
          )}
          <Button
            className={styles.stop}
            onClick={() => {
              debounce(() => {
                stopTracking('完成跟踪')
                setTrackModalVisible(false)
              }, 1000)
            }}
            color="danger"
          >
            终止运行
          </Button>
        </div>
      </AlgorithmModal>
    )
  }, [
    algorithmStatus,
    debounce,
    imgUrl,
    setAlgorithmStatus,
    startTracking,
    stopTracking,
    trackModalVisible,
  ])

  return (
    <div className={styles.main}>
      {trackingProcess}
      <div className={styles.ai_title}>Nao特定目标跟踪算法</div>
      <Button
        onClick={() => {
          setTrackModalVisible(true)
          startTracking(1)
          setAlgorithmStatus('算法运行中')
        }}
        block
        color="primary"
      >
        启动跟踪算法
      </Button>
    </div>
  )
}
