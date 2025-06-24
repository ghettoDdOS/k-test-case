import type { FC } from 'react'

import { List } from 'antd'
import { useEffect, useRef, useState } from 'react'

import { DataEntryCursorPaginatedStore } from './model'

const InfinityListPage: FC = () => {
  const [store] = useState(() => new DataEntryCursorPaginatedStore())
  const loadMoreRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    void store.fetchPage()
  }, [])

  useEffect(() => {
    const el = loadMoreRef.current
    if (!el)
      return

    const onObserve = (entries: IntersectionObserverEntry[]) => {
      if (entries[0].isIntersecting && store.nextCursor != null && !store.loading) {
        void store.fetchPage(store.nextCursor)
      }
    }

    const observer = new IntersectionObserver(onObserve, { threshold: 0.1 })
    observer.observe(el)
    return () => {
      observer.unobserve(el)
      observer.disconnect()
    }
  }, [])

  return (
    <List
      loadMore={(
        <div
          style={{ width: '100%', height: '100px' }}
          ref={loadMoreRef}
        >
        </div>
      )}
      loading={store.loading}
      dataSource={store.data}
      renderItem={item => (
        <List.Item key={item.id}>
          <List.Item.Meta

            title={item.name}
            description={item.desc}
          />

        </List.Item>
      )}
    />
  )
}

export default InfinityListPage
