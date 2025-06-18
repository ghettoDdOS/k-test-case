import type { TableColumnsType } from 'antd'
import type { FC } from 'react'

import type { DataEntry } from '@/app/entities/data-entry'

import { Table } from 'antd'

import { getDataEntryList } from '@/app/entities/data-entry'
import { formatDateTime } from '@/shared/lib/date'
import { useAsyncData } from '@/shared/lib/promise'

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
  const { data, isLoading } = useAsyncData(async () => getDataEntryList())

  return (
    <Table
      dataSource={data}
      loading={isLoading}
      columns={columns}
      rowKey={row => row.id}
      expandable={{
        expandedRowRender: row => <p>{row.desc}</p>,
      }}
    />
  )
}

export default DataEntryTable
