import type { FC, PropsWithChildren } from 'react'

import { App, ConfigProvider } from 'antd'
import ruRU from 'antd/locale/ru_RU'

const AntdConfigProvider: FC<PropsWithChildren> = ({ children }) => {
  return (
    <ConfigProvider locale={ruRU}>
      <App>{children}</App>
    </ConfigProvider>
  )
}

export default AntdConfigProvider
