import { NavBar, TabBar } from 'antd-mobile'
import { Outlet, useLocation, useNavigate } from 'react-router-dom'

import styles from './index.module.scss'
import { ReactComponent as LogoIcon } from '../../assets/images/LogoIcon.svg'
import { ReactComponent as ChargeIcon } from '../../assets/images/ChargeIcon.svg'
import { ReactComponent as SuccessIcon } from '../../assets/images/SuccessIcon.svg'
import { ReactComponent as ControLlcon } from '../../assets/images/ControLlcon.svg'
import { ReactComponent as AIcon } from '../../assets/images/AIcon.svg'
import { context } from '../../hooks/store'
import { useContext } from 'react'

export default function Main() {
  const navigate = useNavigate()
  const location = useLocation()
  const { robotInfo } = useContext(context)

  return (
    <main className={styles.main}>
      <NavBar
        backArrow={false}
        left={
          <div className={styles.nav_left}>
            <ChargeIcon style={{ width: '0.4rem', height: '0.4rem' }} />
            <span className={styles.charge}>{robotInfo.battery}%</span>
          </div>
        }
        right={
          <div className={styles.nav_right}>
            <SuccessIcon style={{ width: '0.4rem', height: '0.4rem' }} />
            <span className={styles.status}>已连接</span>
          </div>
        }
        className={styles.nav}
      >
        <LogoIcon style={{ width: '0.7rem', height: '0.7rem' }} />
      </NavBar>
      <div className={styles.content}>
        <Outlet></Outlet>
      </div>
      <TabBar safeArea className={styles.tab_bar} activeKey={location.pathname}>
        <TabBar.Item
          key="/"
          icon={
            <ControLlcon
              style={{ width: '0.5rem', height: '0.5rem' }}
              onClick={() => {
                navigate('/')
              }}
              className={styles.icon}
            />
          }
        />
        <TabBar.Item
          key="/algorithm"
          icon={
            <AIcon
              style={{ width: '0.5rem', height: '0.5rem' }}
              onClick={() => {
                navigate('/algorithm')
              }}
              className={styles.icon}
            />
          }
        />
      </TabBar>
    </main>
  )
}
