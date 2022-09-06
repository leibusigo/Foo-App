import React from 'react'
import Lottie from 'lottie-react'
import { Button } from 'antd-mobile'

import styles from './index.module.scss'
import NotFoundAnimation from '../../assets/images/NotFound.json'
import { useNavigate } from 'react-router-dom'

export default function NotFound() {
  const navigate = useNavigate()

  return (
    <div className={styles.main}>
      <Lottie
        animationData={NotFoundAnimation}
        loop={true}
        className={styles.notFound_animation}
      />
      <Button
        onClick={() => {
          navigate('/login')
        }}
        color="primary"
      >
        尝试重新连接
      </Button>
    </div>
  )
}
