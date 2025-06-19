import type { DependencyList } from 'react'

import { runInAction } from 'mobx'
import { useLocalObservable } from 'mobx-react-lite'
import { useCallback, useEffect, useRef, useState } from 'react'

type PromiseStatus = 'pending' | 'fulfilled' | 'rejected'

interface QueryFnOptions {
  signal: AbortSignal
}
type QueryFn<T> = (options: QueryFnOptions) => Promise<T>

interface UseAsyncDataOptions<T> {
  onSuccess?: (data: T) => void | Promise<void>
  onError?: (error: unknown) => void | Promise<void>
}

function useAsyncData<T>(
  queryFn: QueryFn<T>,
  deps: DependencyList,
  options: UseAsyncDataOptions<T> = {},
) {
  const { onSuccess, onError } = options

  const queryFnRef = useRef<QueryFn<T>>(queryFn)
  const successHandlerRef = useRef(onSuccess)
  const errorHandlerRef = useRef(onError)

  queryFnRef.current = queryFn
  successHandlerRef.current = onSuccess
  errorHandlerRef.current = onError

  const [data, setData] = useState<T>()
  const [error, setError] = useState<unknown>()
  const [status, setStatus] = useState<PromiseStatus>()

  const handleOnStart = useCallback(() => {
    setStatus('pending')
  }, [])
  const handleSuccess = useCallback((data: T) => {
    setStatus('fulfilled')
    setData(data)
    void successHandlerRef.current?.(data)
  }, [])
  const handleError = useCallback((error: unknown) => {
    console.error(error)
    setStatus('rejected')
    setError(error)
    void errorHandlerRef.current?.(error)
  }, [])

  useEffect(() => {
    const controller = new AbortController()

    const invoke = async () => {
      try {
        handleOnStart()
        const data = await queryFnRef.current({ signal: controller.signal })
        handleSuccess(data)
      }
      catch (error) {
        handleError(error)
      }
    }

    void invoke()

    return () => {
      controller.abort()
    }
  }, [...deps, handleOnStart, handleSuccess, handleError])

  return {
    data,
    error,
    isLoading: status === 'pending',
    isError: status === 'rejected',
    isSuccess: status === 'fulfilled',
  }
}

interface Query<T = unknown> {
  data?: T
  status: PromiseStatus
}
interface UseQueryOptions<T> {
  queryFn: () => Promise<T>
}

function useQuery<T = unknown>({ queryFn }: UseQueryOptions<T>) {
  return useLocalObservable<Query<T>>(() => ({
    data: undefined,
    status: 'fulfilled',
    async run() {
      this.status = 'pending'
      try {
        const data = await queryFn()
        runInAction(() => {
          this.data = data
          this.status = 'fulfilled'
        })
      }
      catch (error) {
        console.error(error)
        runInAction(() => {
          this.status = 'rejected'
        })
      }
    },
  }))
}

export { useAsyncData, useQuery }
