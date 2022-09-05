import { Button, Input, Swiper, Tabs, Toast } from 'antd-mobile'
import { SwiperRef } from 'antd-mobile/es/components/swiper'
import { useEffect, useMemo, useCallback, useRef, useState } from 'react'

import styles from './index.module.scss'
import LoadingModal from '../../../components/LoadingModal'
import useBasic from '../../../hooks/useBasic'

export default function Home() {
  const swiperRef = useRef<SwiperRef>(null)
  const [activeIndex, setActiveIndex] = useState(1)
  const [speakValue, setSpeakValue] = useState('')
  // 控制加载modal显示
  const [loadingVisible, setModalVisible] = useState(false)
  // 控制加载按钮显示
  const [buttonVisible, setButtonVisible] = useState(false)
  // 设置防抖标志
  const [debounce, setDebounce] = useState(false)
  const { basicLoaded, speak } = useBasic()
  // 提交说话
  const submitSpeak = useCallback(() => {
    if (!debounce) {
      setDebounce(true)
      setButtonVisible(false)
      speak(speakValue)
      setModalVisible(true)
      setSpeakValue('')
      setTimeout(() => {
        setDebounce(false)
      }, 500)
    }
  }, [debounce, speak, speakValue])

  const tabItems = useMemo(
    () => [
      { key: 'func1', title: '控制方式一' },
      { key: 'func2', title: '控制方式二' },
    ],
    []
  )

  useEffect(() => {
    if (basicLoaded) {
      setModalVisible(false)
    }
  }, [basicLoaded])

  return (
    <div>
      <LoadingModal
        visible={loadingVisible}
        stopButton={buttonVisible}
        onStop={() => {
          setModalVisible(false)
        }}
      />
      <Tabs
        activeKey={tabItems[activeIndex].key}
        onChange={key => {
          const index = tabItems.findIndex(item => item.key === key)
          setActiveIndex(index)
          swiperRef.current?.swipeTo(index)
        }}
      >
        {tabItems.map(item => (
          <Tabs.Tab title={item.title} key={item.key} />
        ))}
      </Tabs>
      <Swiper
        direction="horizontal"
        loop
        indicator={() => null}
        ref={swiperRef}
        defaultIndex={activeIndex}
        onIndexChange={index => {
          setActiveIndex(index)
        }}
      >
        <Swiper.Item>
          <div className={styles.content}>菠萝</div>
        </Swiper.Item>
        <Swiper.Item>
          <div className={styles.content}>西红柿</div>
        </Swiper.Item>
      </Swiper>
      <div className={styles.speak_block}>
        <div className={styles.speak_input}>
          <Input
            placeholder="输入你想让Nao说的话"
            value={speakValue}
            onChange={val => {
              setSpeakValue(val)
            }}
            onEnterPress={() => {
              if (speakValue.trim() !== '') {
                submitSpeak()
              } else {
                Toast.show('输入不能为空')
              }
            }}
          />
        </div>
        <Button
          onClick={() => {
            if (speakValue.trim() !== '') {
              submitSpeak()
            } else {
              Toast.show('输入不能为空')
            }
          }}
          color="primary"
          className={styles.speak_button}
        >
          说话
        </Button>
      </div>
    </div>
  )
}
