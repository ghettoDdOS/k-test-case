import type { MenuProps } from 'antd'
import type { FC, PropsWithChildren } from 'react'

import { Layout, Menu } from 'antd'

import { useRouter } from '@/shared/lib/router'

import styles from './default.module.css'

const { Header, Content } = Layout

const links: MenuProps['items'] = [
  {
    key: '/',
    label: 'Пагинация',
  },
  {
    key: '/infinity-list',
    label: 'Бесконечный список',
  },
]

const DefaultLayout: FC<PropsWithChildren> = ({ children }) => {
  const { location, navigate } = useRouter()

  const handleSelect: MenuProps['onSelect'] = ({ key }) => {
    navigate(key)
  }

  return (
    <Layout className={styles.root}>
      <Header>
        <Menu
          selectedKeys={[location]}
          onSelect={handleSelect}
          theme="dark"
          mode="horizontal"
          items={links}
        />
      </Header>
      <Content>
        {children}
      </Content>
    </Layout>
  )
}

export default DefaultLayout
