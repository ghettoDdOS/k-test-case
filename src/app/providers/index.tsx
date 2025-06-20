import type { FC, PropsWithChildren } from 'react'

import AntdConfigProvider from './antd-config'

const AppProviders: FC<PropsWithChildren> = ({ children }) => {
  return (
    <AntdConfigProvider>
      {children}
    </AntdConfigProvider>
  )
}

export default AppProviders
