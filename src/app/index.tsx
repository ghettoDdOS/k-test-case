import type { FC } from 'react'

import { StrictMode } from 'react'

import AppProviders from './providers'
import Router from './router'

import 'antd/dist/reset.css'

const App: FC = () => {
  return (
    <StrictMode>
      <AppProviders>
        <Router />
      </AppProviders>
    </StrictMode>
  )
}

export default App
