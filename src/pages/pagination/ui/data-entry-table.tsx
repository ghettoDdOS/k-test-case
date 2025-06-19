import type { TableColumnsType, TableProps } from 'antd'
import type { FC } from 'react'

import type { DataEntry } from '@/app/entities/data-entry'

import { Table } from 'antd'
import { useState } from 'react'

import { formatDateTime } from '@/shared/lib/date'

import { DataEntryPageNumberPaginatedStore } from '../model'

const columns: TableColumnsType<DataEntry> = [
  {
    title: 'ID',
    dataIndex: 'id',
  },
  {
    title: 'Наименование',
    dataIndex: 'name',
  },
  {
    title: 'Код страны',
    dataIndex: 'country',
  },
  {
    title: 'Версия',
    dataIndex: 'version',
  },
  {
    title: 'Кол-во',
    dataIndex: 'count',
  },
  {
    title: 'Дата создания',
    dataIndex: 'createdAt',
    render: (value: Date) => {
      return formatDateTime(value)
    },
  },
  {
    title: 'Родитель (ID)',
    dataIndex: 'parent',
  },
]

const DataEntryTable: FC = () => {
  const [store] = useState(() => new DataEntryPageNumberPaginatedStore())

  const handleTableChange: TableProps<DataEntry>['onChange']
  = (pagination) => {
    if (pagination.current != null)
      store.setPage(pagination.current)
    if (pagination.pageSize != null)
      store.setPageSize(pagination.pageSize)
  }

  return (
    <Table
      dataSource={store.data}
      columns={columns}
      rowKey={row => row.id}
      loading={store.loading}
      pagination={{
        current: store.page,
        pageSize: store.pageSize,
        total: store.count,
      }}
      expandable={{
        expandedRowRender: row => <p>{row.desc}</p>,
      }}
      onChange={handleTableChange}
    />
  )
}

export default DataEntryTable
