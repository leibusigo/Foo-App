import { useCallback, useState } from 'react'

export default function useDebounce() {
  const [first, setFrist] = useState(false)

  const debounce = useCallback(
    (fn: () => void, delay: number) => {
      if (!first) {
        setFrist(true)
        fn()
        setTimeout(() => {
          setFrist(false)
        }, delay)
      }
    },
    [first]
  )

  return {
    debounce,
  }
}
