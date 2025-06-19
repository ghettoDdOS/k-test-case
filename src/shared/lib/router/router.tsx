import type { FC, PropsWithChildren, ReactNode } from 'react'

import type { RouterContextValue } from './context'
import type { Route } from './route'

import { Suspense, useCallback, useEffect, useMemo, useState } from 'react'

import { RouterContext } from './context'
import { routeMatch } from './route'

interface RouterProps {
  routes: Route[]
  loading: ReactNode
  fallback: FC
  layout: FC<PropsWithChildren>
}

const Router: FC<RouterProps> = ({ routes, fallback, loading, layout: Layout }) => {
  const [path, setPath] = useState(window.location.pathname)

  const Route = useMemo(() => {
    return routes.find(routeMatch(path))?.component ?? fallback
  }, [path, fallback, routes])

  const navigate = useCallback((path: string) => {
    window.history.pushState({}, '', path)
    setPath(window.location.pathname)
  }, [])

  useEffect(() => {
    const handlePopState = () => {
      setPath(window.location.pathname)
    }

    window.addEventListener('popstate', handlePopState)
    return () => {
      window.removeEventListener('popstate', handlePopState)
    }
  }, [])

  const api = useMemo<RouterContextValue>(
    () => ({ location: path, navigate }),
    [path, navigate],
  )

  return (
    <RouterContext value={api}>
      <Layout>
        <Suspense fallback={loading}>
          <Route />
        </Suspense>
      </Layout>
    </RouterContext>
  )
}

export default Router
export type { RouterProps }
