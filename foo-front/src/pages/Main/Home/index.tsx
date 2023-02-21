import {
  Button,
  Grid,
  Input,
  Swiper,
  Tabs,
  Toast,
  Image,
  Selector,
  ImageViewer,
} from 'antd-mobile'
import { SwiperRef } from 'antd-mobile/es/components/swiper'
import {
  useEffect,
  useMemo,
  useCallback,
  useRef,
  useState,
  useContext,
} from 'react'
import classNames from 'classnames'

import styles from './index.module.scss'
import LoadingModal from '../../../components/LoadingModal'
import useBasic from '../../../hooks/useBasic'
import useDebounce from '../../../hooks/useDebounce'
import { context } from '../../../hooks/store'

export default function Home() {
  const swiperRef = useRef<SwiperRef>(null)
  const [activeIndex, setActiveIndex] = useState(0)
  const [speakValue, setSpeakValue] = useState('')
  const [walkValue, setWalkValue] = useState('0.1')
  const [cameraId, setCameraId] = useState<string[]>(['0'])
  const { imageVisible, setImageVisible } = useContext(context)
  // 控制加载modal显示
  const [loadingVisible, setLodingVisible] = useState(false)
  // 控制加载按钮显示
  const [buttonVisible, setButtonVisible] = useState(true)
  // 控制设置输入框显示隐藏
  const [inputVisible, setInputVisible] = useState(false)
  // 控制图片查看器
  const [viewerVisible, setViewerVisible] = useState(false)
  const { basicLoaded, speak, wake, stop, walk, camera } = useBasic()
  const { debounce } = useDebounce()

  useEffect(() => {
    if (basicLoaded) {
      setLodingVisible(false)
    }
  }, [basicLoaded])

  // 提交说话
  const submitSpeak = useCallback(() => {
    debounce(async () => {
      setButtonVisible(false)
      speak(speakValue)
      setLodingVisible(true)
      setSpeakValue('')
    }, 1000)
  }, [debounce, speak, speakValue])

  // 行走动作
  const walkAciton = useCallback(
    (angle: string) => {
      debounce(async () => {
        setButtonVisible(true)
        setLodingVisible(true)
        await wake()
        await walk(walkValue, angle)
      }, 1000)
    },
    [debounce, wake, walk, walkValue]
  )

  const tabItems = useMemo(
    () => [
      { key: 'func1', title: '控制模块一' },
      { key: 'func2', title: '控制模块二' },
    ],
    []
  )

  const seletorOption = useMemo(
    () => [
      {
        label: '摄像头一',
        value: '0',
      },
      {
        label: '摄像头二',
        value: '1',
      },
    ],
    []
  )

  const controlButtons = useMemo(
    () => [
      {
        key: 'left-front',
        content: '左上前进',
        onClick: () => {
          walkAciton(`${Math.PI / 4}`)
        },
      },
      {
        key: 'front',
        content: '正向前进',
        onClick: () => {
          walkAciton('0')
        },
      },
      {
        key: 'right-front',
        content: '右上前进',
        style: 'right',
        onClick: () => {
          walkAciton(`${-(Math.PI / 4)}`)
        },
      },
      {
        key: 'left',
        content: '左向前进',
        onClick: () => {
          walkAciton(`${Math.PI / 2}`)
        },
      },
      {
        key: 'center',
        content: '行走遥控',
        onClick: () => {},
      },
      {
        key: 'right',
        content: '右向前进',
        onClick: () => {
          walkAciton(`${-(Math.PI / 2)}`)
        },
      },
      {
        key: 'left-back',
        content: '左下前进',
        style: 'left',
        onClick: () => {
          walkAciton(`${(3 * Math.PI) / 4}`)
        },
      },
      {
        key: 'back',
        content: '反向前进',
        onClick: () => {
          walkAciton(`${Math.PI}`)
        },
      },
      {
        key: 'right-back',
        content: '右下前进',
        onClick: () => {
          walkAciton(`${-((3 * Math.PI) / 4)}`)
        },
      },
    ],
    [walkAciton]
  )

  const imgUrl = useMemo(
    () => (imageVisible ? '/img/shot_cut.jpg' : '/img/default.png'),
    [imageVisible]
  )

  return (
    <div>
      <LoadingModal
        visible={loadingVisible}
        stopButton={buttonVisible}
        onStop={() => {
          debounce(() => {
            stop()
            setLodingVisible(false)
          }, 1000)
        }}
      />
      <ImageViewer
        image={require('../../../assets' + imgUrl)}
        visible={viewerVisible}
        onClose={() => {
          setViewerVisible(false)
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
            <Grid.Item className={styles.content_grid_title} span={6}>
              <span>切换Nao状态</span>
            </Grid.Item>
            <Grid.Item className={styles.content_grid_button} span={3}>
              <Button
                onClick={() => {
                  debounce(() => {
                    setButtonVisible(false)
                    wake()
                    setLodingVisible(true)
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
                    setLodingVisible(true)
                  }, 1000)
                }}
                block
                color="primary"
              >
                待机
              </Button>
            </Grid.Item>
            <Grid.Item className={styles.content_grid_title} span={6}>
              <span>Nao行走控制</span>
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
                    if (val.trim() !== '' && isNaN(parseFloat(val))) {
                      Toast.show('请输入数字')
                    } else {
                      setWalkValue(val)
                    }
                  }}
                  onEnterPress={() => {
                    setInputVisible(false)
                  }}
                  autoFocus
                  placeholder="请输入"
                />
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
            <Grid.Item className={styles.content_grid_title} span={6}>
              <span>Nao拍摄控制</span>
            </Grid.Item>
            <Grid.Item className={styles.image_grid} span={6}>
              <Image
                className={styles.shot_img}
                onClick={() => {
                  setViewerVisible(true)
                }}
                src={require('../../../assets' + imgUrl)}
                fit="fill"
              />
            </Grid.Item>
            <Grid.Item span={6}>
              <Selector
                className={styles.single_seletor}
                columns={2}
                options={seletorOption}
                defaultValue={cameraId}
                onChange={value => {
                  setCameraId(value)
                }}
              />
            </Grid.Item>
            <Grid.Item span={6} className={styles.shot_button}>
              <Button
                onClick={async () => {
                  setButtonVisible(false)
                  setLodingVisible(true)
                  await camera(cameraId[0])
                  setImageVisible(true)
                }}
                block
                color="primary"
              >
                拍摄
              </Button>
            </Grid.Item>
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
