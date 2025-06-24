import type { DataEntry } from '@/entities/data-entry'
import type { PageNumberPaginatedDataEntryListParams } from '@/entities/data-entry/api'
import type { FilteringParams } from '@/shared/lib/filters'
import type { OrderingParams } from '@/shared/lib/ordering'
import type { PageNumberPaginationParams } from '@/shared/lib/pagination'

import { makeAutoObservable, runInAction } from 'mobx'

import { getPageNumberPaginatedDataEntryList } from '@/entities/data-entry'
import { LRUCache } from '@/shared/lib/cache'

function makeKey(input: unknown): string {
  return JSON.stringify(input)
}

class DataEntryPageNumberPaginatedStore {
  private cache: LRUCache<DataEntry[]>
  private currentCacheKey?: string

  count: number = 0
  loading: boolean = true

  constructor() {
    makeAutoObservable(this)
    this.cache = new LRUCache(3)
  }

  get data() {
    if (this.currentCacheKey == null)
      return
    return this.cache.get(this.currentCacheKey)
  }

  async fetchPage(
    pagination: PageNumberPaginationParams,
    ordering?: OrderingParams,
    filters?: Partial<FilteringParams<DataEntry>>,
  ) {
    const params: PageNumberPaginatedDataEntryListParams = {
      ...pagination,
      ...ordering,
      ...filters,
    }
    const cacheKey = makeKey(params)
    if (this.cache.has(cacheKey)) {
      runInAction(() => {
        this.currentCacheKey = cacheKey
      })
      return
    }
    this.loading = true
    try {
      const result = await getPageNumberPaginatedDataEntryList({
        params,
      })
      runInAction(() => {
        this.cache.set(cacheKey, result.results)
        this.count = result.count
        this.currentCacheKey = cacheKey
      })
    }
    catch (error) {
      console.error(error)
    }
    finally {
      runInAction(() => {
        this.loading = false
      })
    }
  }
}

export { DataEntryPageNumberPaginatedStore }
