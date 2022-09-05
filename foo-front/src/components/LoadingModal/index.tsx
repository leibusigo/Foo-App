import Lottie from 'lottie-react'
import { Button, DotLoading, Modal } from 'antd-mobile'

import styles from './index.module.scss'
import loadingAnimation from '../../assets/images/RobotLoading.json'

interface Props {
  visible: boolean
  // 是否显示急停按钮
  stopButton?: boolean
  // 急停事件
  onStop?: () => void
}

export default function LoadingModal({ visible, stopButton, onStop }: Props) {
  return (
    <>
      <Modal
        visible={visible}
        content={
          <div className={styles.modal_content}>
            <Lottie
              animationData={loadingAnimation}
              loop={true}
              className={styles.loading_animation}
            />
            <div className={styles.loading_word}>
              <span>代码执行中</span>
              <DotLoading />
            </div>
            {stopButton && (
              <div className={styles.stop}>
                <Button
                  className={styles.stop_button}
                  block
                  onClick={onStop}
                  color="danger"
                >
                  终止运行
                </Button>
              </div>
            )}
          </div>
        }
      />
    </>
  )
}
