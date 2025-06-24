import { joinUrl } from './lib/url'

type QueryParamValue = number | string | number[] | string[] | undefined
type QueryParams = Record<string, QueryParamValue>
interface RequestOptions {
  params?: QueryParams
  signal?: AbortSignal
}

interface ApiClient {
  get: <T>(url: string, options?: RequestOptions) => Promise<T>
}

interface ApiClientOptions {
  baseUrl?: string
}

class ApiError extends Error {
  constructor(response: Response) {
    super(response.statusText)
    this.name = 'ApiError'
  }
}

function stripUndefined(obj: object) {
  const copy: Record<string, unknown> = { ...obj }
  for (const [k, v] of Object.entries(copy)) {
    if (v === undefined)
      delete copy[k]
  }
  return copy
}

function serializeQueryParams(params: QueryParams): string {
  const serializedParams = Object.entries(
    stripUndefined(params),
  ).flatMap(([key, value]) => {
    if (Array.isArray(value))
      return value.map(v => [key, String(v)])
    return [[key, String(value)]]
  })
  return new URLSearchParams(serializedParams).toString()
}

function createApiClient(options: ApiClientOptions = {}): ApiClient {
  const { baseUrl } = options

  const resolveUrl = (url: string, params?: QueryParams) => {
    let resolvedUrl = url
    if (baseUrl != null)
      resolvedUrl = joinUrl(baseUrl, url)

    if (params) {
      resolvedUrl += `?${serializeQueryParams(params)}`
    }

    return resolvedUrl
  }

  const request = async <T>(url: string, options: RequestOptions = {}) => {
    const { params, signal } = options

    const response = await fetch(resolveUrl(url, params), { signal })
    if (!response.ok)
      throw new ApiError(response)
    const data = response.json()
    return data as T
  }

  return {
    get: async (url, options) => request(url, options),
  }
}

const api = createApiClient({
  baseUrl: '/api',
})

export default api
export type { QueryParams, RequestOptions }
export { ApiError }
