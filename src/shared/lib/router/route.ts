import type { FC } from 'react'

interface Route {
  path: string
  component: FC
}

const routeMatch = (path: string) => (route: Route) => route.path === path

export { routeMatch }
export type { Route }
