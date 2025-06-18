import type { FC } from 'react'

import type { Route } from '@/shared/lib/router'

import { Button, Flex, Spin, Typography } from 'antd'
import { lazy } from 'react'

import { Router, useRouter } from '@/shared/lib/router'

const { Title, Paragraph } = Typography

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
    <Flex vertical align="center">
      <Title>404</Title>
      <Paragraph>Страница не найдена</Paragraph>
      <Button onClick={() => { navigate('/') }}>На главную</Button>
    </Flex>
  )
}

const AppRouter: FC = () => {
  return (
    <Router
      routes={routes}
      loading={<Spin fullscreen />}
      fallback={NotFoundPage}
    />
  )
}

export default AppRouter
