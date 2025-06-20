import { createRoot } from 'react-dom/client'

import App from '@/app'

import '@ant-design/v5-patch-for-react-19'

const rootEl = document.getElementById('root')!

const root = createRoot(rootEl)

root.render(<App />)
