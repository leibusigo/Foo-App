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
  const { algorithmStatus, algorithmLoaded, epoch, startTracking } =
    useAlgorithm()
  const { stop } = useBasic()
  const { debounce } = useDebounce()

  // useEffect(() => {
  //   if (algorithmLoaded) {
  //     setLodingVisible(false)
  //   }
  // }, [algorithmLoaded])

  // const imgUrl = useMemo(() => {
  //   if (algorithmStatus === '没有目标类别物品') {
  //     return `/img/epoch${epoch}/origin.jpg`
  //   } else if (algorithmStatus === '') {
  //     return '/img/default.png'
  //   } else {
  //     return `/img/epoch${epoch}/cut.jpg`
  //   }
  // }, [algorithmStatus, epoch])
  const imgUrl = useMemo(() => {
    return '/img/default.png'
  }, [])

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
          <h3>{algorithmStatus}</h3>
          <Button
            className={styles.stop}
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
      <div className={styles.ai_title}>Nao特定目标跟踪算法</div>
      <Button
        onClick={() => {
          setTrackModalVisible(true)
          startTracking(1)
        }}
        block
        color="primary"
      >
        启动跟踪算法
      </Button>
    </div>
  )
}
