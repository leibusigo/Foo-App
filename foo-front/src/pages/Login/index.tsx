import { useEffect, useState } from 'react'
import { Button, Form, Grid, Input } from 'antd-mobile'

import styles from './index.module.scss'
import { ReactComponent as LogoIcon } from '../../assets/images/LogoIcon.svg'
import LoadingModal from '../../components/LoadingModal'
import useBasic from '../../hooks/useBasic'

export default function Login() {
  // 控制加载modal显示
  const [loadingVisible, setModalVisible] = useState(false)

  const { basicLoaded, connect } = useBasic()

  useEffect(() => {
    if (basicLoaded) {
      setModalVisible(false)
    }
  }, [basicLoaded])

  return (
    <div className={styles.content}>
      <LoadingModal visible={loadingVisible} />
      <Grid columns={1} gap={10} className={styles.main}>
        <Grid.Item className={styles.logo}>
          <LogoIcon className={styles.logo_icon} />
        </Grid.Item>
        <Grid.Item className={styles.title_gird}>
          <h1 className={styles.title}>Foo App</h1>
        </Grid.Item>
        <Grid.Item className={styles.slogan_gird}>
          <span className={styles.slogan}>—— 随心所欲控制Nao机器人</span>
        </Grid.Item>
        <Grid.Item className={styles.form_gird}>
          <Form
            name="form"
            layout="horizontal"
            onFinish={vals => {
              connect(vals.ip)
              setModalVisible(true)
            }}
            footer={
              <div className={styles.form_footer}>
                <Button
                  className={styles.submit}
                  block
                  type="submit"
                  size="middle"
                >
                  连接
                </Button>
              </div>
            }
          >
            <Form.Item
              name="ip"
              label="ip地址"
              rules={[
                { required: true },
                {
                  pattern:
                    /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/,
                  message: '请输入正确的ip地址',
                },
              ]}
            >
              <Input placeholder="请输入ip地址" />
            </Form.Item>
          </Form>
        </Grid.Item>
      </Grid>
    </div>
  )
}
