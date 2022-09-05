import { Button } from 'antd-mobile'
import { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'

// import styles from './index.module.scss'
import LoadingModal from '../../components/LoadingModal'

export default function Main() {
  const navigate = useNavigate()
  // 控制加载modal显示
  const [loadingVisible, setModalVisible] = useState(false)

  const loadingModal = useMemo(() => {
    return (
      <>
        <LoadingModal
          visible={loadingVisible}
          onToggleVisible={() => {
            setModalVisible(false)
          }}
        />
      </>
    )
  }, [loadingVisible])

  return (
    <div>
      {loadingModal}
      Main
      <Button
        onClick={() => {
          setModalVisible(true)
        }}
      >
        modal
      </Button>
      <Button
        onClick={() => {
          navigate('/login')
        }}
      >
        login
      </Button>
    </div>
  )
}
