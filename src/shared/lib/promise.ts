import { useEffect, useRef, useState } from 'react'

type PromiseStatus = 'pending' | 'fulfilled' | 'rejected'

function useAsyncData<T>(queryFn: () => Promise<T>) {
  const promiseRef = useRef<() => Promise<T>>(queryFn)

  const [data, setData] = useState<T>()
  const [error, setError] = useState<unknown>()
  const [status, setStatus] = useState<PromiseStatus>()

  useEffect(() => {
    const invoke = async () => {
      try {
        setStatus('pending')
        const data = await promiseRef.current()

        setStatus('fulfilled')
        setData(data)
      }
      catch (error) {
        console.error(error)
        setStatus('rejected')
        setError(error)
      }
    }

    void invoke()
  }, [])

  return {
    data,
    error,
    isLoading: status === 'pending',
    isError: status === 'rejected',
    isSuccess: status === 'fulfilled',
  }
}

export { useAsyncData }
