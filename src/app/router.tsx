import type { FC } from 'react'

import type { Route } from '@/shared/lib/router'

import { Button, Result, Spin } from 'antd'
import { lazy } from 'react'

import { Router, useRouter } from '@/shared/lib/router'

import DefaultLayout from './layouts/default'

const routes: Route[] = [
  {
    path: '/',
    component: lazy(async () => import('@/pages/pagination')),
  },
  {
    path: '/infinity-list',
    component: lazy(async () => import('@/pages/infinity-list')),
  },
]

const NotFoundPage: FC = () => {
  const { navigate } = useRouter()

  return (
    <Result
      style={{ marginBlock: 'auto' }}
      status="404"
      title="404"
      subTitle="Страница не найдена."
      extra={<Button type="primary" onClick={() => { navigate('/') }}>На главную</Button>}
    />

  )
}

const AppRouter: FC = () => {
  return (
    <Router
      routes={routes}
      loading={<Spin fullscreen />}
      fallback={NotFoundPage}
      layout={DefaultLayout}
    />
  )
}

export default AppRouter
