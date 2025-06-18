import type { FC } from 'react'

import { StrictMode } from 'react'

import DefaultLayout from './layouts/default'
import AppProviders from './providers'
import Router from './router'

import 'antd/dist/reset.css'

const App: FC = () => {
  return (
    <StrictMode>
      <AppProviders>
        <DefaultLayout>
          <Router />
        </DefaultLayout>
      </AppProviders>
    </StrictMode>
  )
}

export default App
