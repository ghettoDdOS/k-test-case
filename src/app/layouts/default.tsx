import type { MenuProps } from 'antd'
import type { FC, PropsWithChildren } from 'react'

import { Layout, Menu } from 'antd'
import { useState } from 'react'

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
  const [selectedKeys, setSelectedKeys] = useState<string[]>([window.location.pathname])

  const handleSelect: MenuProps['onSelect'] = ({ key }) => {
    setSelectedKeys([key])
    window.history.pushState({}, '', key)
  }

  return (
    <Layout>
      <Header>
        <Menu
          selectedKeys={selectedKeys}
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
