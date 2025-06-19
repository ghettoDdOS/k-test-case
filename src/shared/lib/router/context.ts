import { createContext, use } from 'react'

interface RouterContextValue {
  location: string
  navigate: (path: string) => void
}

const RouterContext = createContext<RouterContextValue | null>(null)

function useRouter() {
  const api = use(RouterContext)
  if (api === null) {
    throw new Error('`useRouter` must be called in `Router` context.')
  }
  return api
}

export { RouterContext, useRouter }
export type { RouterContextValue }
