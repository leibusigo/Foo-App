import { Button, Grid, Input, Swiper, Tabs, Toast } from 'antd-mobile'
import { SwiperRef } from 'antd-mobile/es/components/swiper'
import { useEffect, useMemo, useCallback, useRef, useState } from 'react'

import styles from './index.module.scss'
import LoadingModal from '../../../components/LoadingModal'
import useBasic from '../../../hooks/useBasic'
import useDebounce from '../../../hooks/useDebounce'
import classNames from 'classnames'

export default function Home() {
  const swiperRef = useRef<SwiperRef>(null)
  const [activeIndex, setActiveIndex] = useState(0)
  const [speakValue, setSpeakValue] = useState('')
  const [walkValue, setWalkValue] = useState('0.1')
  // 控制加载modal显示
  const [loadingVisible, setModalVisible] = useState(false)
  // 控制加载按钮显示
  const [buttonVisible, setButtonVisible] = useState(false)
  // 控制设置输入框显示隐藏
  const [inputVisible, setInputVisible] = useState(false)
  const { basicLoaded, speak, wake, stop } = useBasic()
  const { debounce } = useDebounce()

  // 提交说话
  const submitSpeak = useCallback(() => {
    debounce(() => {
      setButtonVisible(false)
      speak(speakValue)
      setModalVisible(true)
      setSpeakValue('')
    }, 1000)
  }, [debounce, speak, speakValue])

  const tabItems = useMemo(
    () => [
      { key: 'func1', title: '控制方式一' },
      { key: 'func2', title: '控制方式二' },
    ],
    []
  )

  const controlButtons = useMemo(
    () => [
      {
        key: 'left-front',
        content: '左上前进',
        onClick: () => {},
      },
      { key: 'front', content: '正向前进', onClick: () => {} },
      {
        key: 'right-front',
        content: '右上前进',
        style: 'right',
        onClick: () => {},
      },
      { key: 'left', content: '左向前进', onClick: () => {} },
      {
        key: 'center',
        content: '行走遥控',
        onClick: () => {},
      },
      { key: 'right', content: '右向前进', onClick: () => {} },
      {
        key: 'left-back',
        content: '左下前进',
        style: 'left',
        onClick: () => {},
      },
      { key: 'back', content: '反向前进', onClick: () => {} },
      {
        key: 'right-back',
        content: '右下前进',
        onClick: () => {},
      },
    ],
    []
  )

  const basicControl = useMemo(() => {
    return (
      <>
        <Grid.Item className={styles.content_grid_title} span={6}>
          <span>切换Nao状态</span>
        </Grid.Item>
        <Grid.Item className={styles.content_grid_button} span={3}>
          <Button
            onClick={() => {
              debounce(() => {
                setButtonVisible(false)
                wake()
                setModalVisible(true)
              }, 1000)
            }}
            block
            color="primary"
          >
            唤醒
          </Button>
        </Grid.Item>
        <Grid.Item className={styles.content_grid_button} span={3}>
          <Button
            onClick={() => {
              debounce(() => {
                setButtonVisible(false)
                stop()
                setModalVisible(true)
              }, 1000)
            }}
            block
            color="primary"
          >
            待机
          </Button>
        </Grid.Item>
      </>
    )
  }, [debounce, stop, wake])

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
          <Grid columns={6} className={styles.content}>
            {basicControl}
            <Grid.Item className={styles.content_grid_title} span={6}>
              <span>Nao基本控制</span>
            </Grid.Item>
            <Grid.Item
              className={classNames(styles.set_grid, styles.set_left)}
              span={2}
            >
              <span>当前行走距离:</span>
            </Grid.Item>
            <Grid.Item
              className={classNames(styles.set_grid, styles.set_value)}
              span={2}
            >
              {inputVisible ? (
                <Input
                  value={walkValue}
                  onChange={val => {
                    setWalkValue(val)
                  }}
                  onEnterPress={() => {
                    setInputVisible(false)
                  }}
                  autoFocus
                  placeholder="请输入"
                ></Input>
              ) : (
                <span>{walkValue}</span>
              )}
              <span className={styles.unit}>m</span>
            </Grid.Item>
            <Grid.Item
              className={classNames(styles.set_grid, styles.set_right)}
              span={2}
            >
              <Button
                onClick={() => {
                  setInputVisible(!inputVisible)
                }}
                block
                color={inputVisible ? 'default' : 'primary'}
              >
                {inputVisible ? '确定' : '设置'}
              </Button>
            </Grid.Item>
            {controlButtons.map(item => (
              <Grid.Item
                key={item.key}
                className={classNames(
                  styles.content_grid_button,
                  styles.control_button
                )}
                span={2}
              >
                <Button
                  className={styles.walk_button}
                  onClick={item.onClick}
                  color={item.key === 'center' ? 'primary' : 'default'}
                  block
                >
                  {item.content}
                </Button>
              </Grid.Item>
            ))}
          </Grid>
        </Swiper.Item>
        <Swiper.Item>
          <Grid columns={6} className={styles.content}>
            {basicControl}
          </Grid>
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
