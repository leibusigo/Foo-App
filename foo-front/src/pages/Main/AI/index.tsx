import { Button, Image } from 'antd-mobile'
import { useEffect, useMemo, useState } from 'react'

import useAlgorithm from '../../../hooks/useAlgorithm'
import styles from './index.module.scss'
import useBasic from '../../../hooks/useBasic'
import useDebounce from '../../../hooks/useDebounce'
import AlgorithmModal from '../../../components/AlgorithmModal'

export default function AI() {
  const [trackModalVisible, setTrackModalVisible] = useState(false)
  // 控制加载按钮显示
  // const [loadingVisible, setLodingVisible] = useState(false)
  const { algorithmStatus, algorithmLoaded, startTracking } = useAlgorithm()
  const { stop } = useBasic()
  const [epoch] = useState(1)
  const { debounce } = useDebounce()

  // useEffect(() => {
  //   if (algorithmLoaded) {
  //     setLodingVisible(false)
  //   }
  // }, [algorithmLoaded])

  const imgUrl = useMemo(() => `/img/epoch${epoch}/origin.jpg`, [epoch])

  const trackingProcess = useMemo(() => {
    return (
      <AlgorithmModal visible={trackModalVisible}>
        <div className={styles.modal}>
          <Image src={require('../../../assets' + imgUrl)} fit="fill" />
          <h1>{algorithmStatus}</h1>
          <Button
            onClick={() => {
              debounce(() => {
                stop()
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
  }, [algorithmStatus, debounce, imgUrl, stop, trackModalVisible])

  return (
    <div className={styles.main}>
      {trackingProcess}
      <div className={styles.ai_title}>Nao自动跟踪算法</div>
      <Button
        onClick={() => {
          setTrackModalVisible(true)
          startTracking(epoch)
        }}
        block
        color="primary"
      >
        启动跟踪算法
      </Button>
    </div>
  )
}
