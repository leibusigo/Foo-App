import Lottie from 'lottie-react'
import { Button, DotLoading, Modal } from 'antd-mobile'

import styles from './index.module.scss'
import loadingAnimation from '../../assets/images/RobotLoading.json'

interface Props {
  visible: boolean
  // 是否显示急停按钮
  stopButton?: boolean
  onToggleVisible: () => void
  // 急停事件
  onStop?: () => void
}

export default function LoadingModal({ visible, onToggleVisible }: Props) {
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
            <div className={styles.stop}>
              <Button
                className={styles.stop_button}
                block
                onClick={onToggleVisible}
                color="danger"
              >
                终止运行
              </Button>
            </div>
          </div>
        }
      />
    </>
  )
}
