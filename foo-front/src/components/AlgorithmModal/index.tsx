import classNames from 'classnames'
import { PropsWithChildren } from 'react'
import styles from './index.module.scss'

interface Props {
  visible: boolean
}

export default function AlgorithmModal({
  children,
  visible,
}: PropsWithChildren<Props>) {
  return (
    <div className={classNames(styles.main, { [styles.visible]: visible })}>
      {children}
    </div>
  )
}
