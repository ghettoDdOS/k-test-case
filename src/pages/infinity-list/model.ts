import type { DataEntry } from '@/entities/data-entry'

import { makeAutoObservable, runInAction } from 'mobx'

import { getCursorPaginatedDataEntryList } from '@/entities/data-entry/api'
import { LRUCache } from '@/shared/lib/cache'

class DataEntryCursorPaginatedStore {
  private cache: LRUCache<DataEntry[]>

  pageSize: number = 300
  cursor?: string
  loading: boolean = true

  nextCursor: string | null = null
  previousCursor: string | null = null

  constructor() {
    makeAutoObservable(this)
    this.cache = new LRUCache(3)
  }

  get data() {
    return this.cache.get(this.cursor ?? 'initial')
  }

  async fetchPage(
    cursor?: string,
  ) {
    if (this.cache.has(cursor ?? 'initial')) {
      runInAction(() => {
        this.cursor = cursor
      })
      return
    }
    this.loading = true
    try {
      const result = await getCursorPaginatedDataEntryList({
        params: {
          pageSize: this.pageSize,
          cursor,
        },
      })
      runInAction(() => {
        this.cache.set(cursor ?? 'initial', result.results)
        this.cursor = cursor ?? 'initial'
        this.nextCursor = result.next
        this.previousCursor = result.previous
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

export { DataEntryCursorPaginatedStore }
