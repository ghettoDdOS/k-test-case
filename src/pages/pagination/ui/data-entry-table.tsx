import type { InputRef, TableColumnsType, TableColumnType, TableProps } from 'antd'
import type { FC } from 'react'

import type { DataEntry } from '@/entities/data-entry'

import { CloseOutlined, SearchOutlined } from '@ant-design/icons'
import { Button, Flex, Input, Table } from 'antd'
import { useEffect, useRef, useState } from 'react'

import { mapDataEntryKeyToDtoKey } from '@/entities/data-entry/api'
import { formatDateTime } from '@/shared/lib/date'

import { DataEntryPageNumberPaginatedStore } from '../model'

const DataEntryTable: FC = () => {
  const [store] = useState(() => new DataEntryPageNumberPaginatedStore())

  const searchInput = useRef<InputRef>(null)

  const getColumnSearchProps = (): TableColumnType<DataEntry> => ({
    filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters, close }) => (
      <Flex gap={8} align="center" style={{ padding: 8 }} onKeyDown={e => e.stopPropagation()}>

        <Input
          ref={searchInput}
          size="small"
          placeholder="Поиск"
          value={selectedKeys[0]}
          onChange={e => setSelectedKeys(e.target.value ? [e.target.value] : [])}
          onPressEnter={() => confirm()}
          allowClear
          onClear={() => clearFilters && clearFilters({ confirm: true })}
        />
        <Button
          type="primary"
          onClick={() => confirm()}
          icon={<SearchOutlined />}
          size="small"
        >
          Искать
        </Button>
        <Button type="text" size="small" icon={<CloseOutlined />} onClick={() => close()} />
      </Flex>
    ),
    filterIcon: (filtered: boolean) => (
      <SearchOutlined style={{ color: filtered ? '#1677ff' : undefined }} />
    ),
    filterDropdownProps: {
      onOpenChange(open) {
        if (open) {
          setTimeout(() => searchInput.current?.select(), 100)
        }
      },
    },
  })

  const columns: TableColumnsType<DataEntry> = [
    {
      title: 'ID',
      dataIndex: 'id',
      sorter: { multiple: 1 },

    },
    {
      title: 'Наименование',
      dataIndex: 'name',
      sorter: { multiple: 2 },
      ...getColumnSearchProps(),

    },
    {
      title: 'Код страны',
      dataIndex: 'country',
      sorter: { multiple: 3 },
      ...getColumnSearchProps(),

    },
    {
      title: 'Версия',
      dataIndex: 'version',
      sorter: { multiple: 4 },

    },
    {
      title: 'Кол-во',
      dataIndex: 'count',
      sorter: { multiple: 5 },

    },
    {
      title: 'Дата создания',
      dataIndex: 'createdAt',
      render: (value: Date) => {
        return formatDateTime(value)
      },
      sorter: { multiple: 6 },

    },
    {
      title: 'Родитель (ID)',
      dataIndex: 'parent',
      sorter: { multiple: 7 },
    },
  ]

  const handleTableChange: TableProps<DataEntry>['onChange']
  = (pagination, filters, sorter) => {
    const sorterCols = Array.isArray(sorter) ? sorter : [sorter]
    const ordering = sorterCols.map(
      (col) => {
        if (col.field === undefined)
          return undefined
        const field = mapDataEntryKeyToDtoKey(col.field.toString())
        return col.order === 'descend'
          ? `-${field}`
          : col.order === 'ascend' ? field : undefined
      },
    ).filter(Boolean) as string[]

    if (pagination.current != null && pagination.pageSize != null) {
      void store.fetchPage({
        page: pagination.current,
        pageSize: pagination.pageSize,

      }, {
        ordering: ordering.length ? ordering : undefined,
      }, {
        nameIcontains: filters?.name?.[0] as string,
        countryEq: filters?.country?.[0] as string,
      })
    }
  }

  useEffect(() => {
    void store.fetchPage({ page: 1, pageSize: 10 })
  }, [store])

  return (
    <Table
      dataSource={store.data}
      columns={columns}
      rowKey={row => row.id}
      loading={store.loading}

      pagination={{
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
