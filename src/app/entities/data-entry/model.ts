interface DataEntryDto {
  readonly id: number
  name: string
  version: string
  desc: string
  country: number
  count: number
  parent: number
  created_at: string
}

interface DataEntry {
  readonly id: number
  name: string
  version: string
  desc: string
  country: number
  count: number
  parent: number
  createdAt: Date
}

function mapDataEntryDto(dto: DataEntryDto): DataEntry {
  return {
    id: dto.id,
    name: dto.name,
    version: dto.version,
    desc: dto.desc,
    country: dto.country,
    count: dto.count,
    parent: dto.parent,
    createdAt: new Date(dto.created_at),
  }
}

export { mapDataEntryDto }
export type { DataEntry, DataEntryDto }
