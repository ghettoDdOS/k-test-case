interface RequestOptions {}

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

function joinUrl(base: string, path: string) {
  if (!base.endsWith('/') && !path.startsWith('/')) {
    return `${base}/${path}`
  }
  if (base.endsWith('/') && path.startsWith('/')) {
    return base + path.slice(1)
  }
  return base + path
}

function createApiClient(options: ApiClientOptions = {}): ApiClient {
  const { baseUrl } = options

  const resolveUrl = (url: string) => {
    if (baseUrl != null)
      return joinUrl(baseUrl, url)
    return url
  }

  const request = async <T>(url: string) => {
    const response = await fetch(resolveUrl(url))
    if (!response.ok)
      throw new ApiError(response)
    const data = response.json()
    return data as T
  }

  return {
    get: async url => request(url),
  }
}

const api = createApiClient({
  baseUrl: '/api',
})

export default api
export type { RequestOptions }
export { ApiError }
