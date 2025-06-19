import type { DataEntry } from '@/app/entities/data-entry'
import type { PageNumberPaginatedData } from '@/shared/lib/pagination'

import { makeAutoObservable, reaction, runInAction } from 'mobx'

import { getPageNumberPaginatedDataEntryList } from '@/app/entities/data-entry'
import { LRUCache } from '@/shared/lib/cache'

class DataEntryPageNumberPaginatedStore {
  pages: LRUCache<DataEntry[]> = new LRUCache(3)

  page: number = 1
  pageSize: number = 1000

  count: number = 0

  loading: boolean = true

  constructor() {
    makeAutoObservable(this)

    reaction(
      () => this.page,
      (page) => { void this.ensurePageData(page) },
      { fireImmediately: true },
    )
    reaction(
      () => this.pageSize,
      () => {
        this.pages = new LRUCache(3)
        this.page = 1
      },
    )
  }

  get data() {
    return this.pages.get(this.page) ?? []
  }

  async ensurePageData(page: number) {
    if (this.pages.has(page))
      return

    this.loading = true
    try {
      const data = await getPageNumberPaginatedDataEntryList({
        params: {
          page,
          pageSize: this.pageSize,
        },
      })
      runInAction(() => {
        this.setPageData(page, data)
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

  private setPageData(page: number, data: PageNumberPaginatedData<DataEntry>) {
    this.count = data.count
    this.pages.set(page, data.results)
  }

  setPage(page: number) {
    this.page = page
  }

  setPageSize(pageSize: number) {
    this.pageSize = pageSize
  }
}

export { DataEntryPageNumberPaginatedStore }
