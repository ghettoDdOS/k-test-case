import type { DataEntry, DataEntryDto } from './model'
import type { QueryParams } from '@/shared/api'
import type { FilteringParams, FilteringParamsDto } from '@/shared/lib/filters'
import type { OrderingParams } from '@/shared/lib/ordering'
import type {
  CursorPaginatedData,
  CursorPaginationParams,
  CursorPaginationParamsDto,
  PageNumberPaginatedData,
  PageNumberPaginationParams,
  PageNumberPaginationParamsDto,
} from '@/shared/lib/pagination'

import api from '@/shared/api'
import { mapCursorPaginationParamsToDto, mapPageNumberPaginationParamsToDto } from '@/shared/lib/pagination'

import { mapDataEntryDto } from './model'

interface PageNumberPaginatedDataEntryListParamsDto
  extends PageNumberPaginationParamsDto,
  Partial<FilteringParamsDto<DataEntryDto>>, OrderingParams, QueryParams {}

interface PageNumberPaginatedDataEntryListParams
  extends PageNumberPaginationParams,
  Partial<FilteringParams<DataEntry>>, OrderingParams {}

const dataEntryKeyMap: Partial<Record<keyof DataEntry, keyof DataEntryDto>> = {
  createdAt: 'created_at',
}

function mapDataEntryKeyToDtoKey(key: string): keyof DataEntryDto {
  if (key in dataEntryKeyMap) {
    return dataEntryKeyMap[key] as keyof DataEntryDto
  }
  return key as keyof DataEntryDto
}

function mapPageNumberPaginatedDataEntryListParamsToDto(
  {
    nameIcontains,
    countryEq,
    ordering,

    ...paginationParams
  }: PageNumberPaginatedDataEntryListParams,
): PageNumberPaginatedDataEntryListParamsDto {
  return {
    ...mapPageNumberPaginationParamsToDto(paginationParams),
    name__icontains: nameIcontains,
    country__eq: countryEq,
    ordering,
  }
}

interface PageNumberPaginatedDataEntryListParams
  extends PageNumberPaginationParams,
  Partial<FilteringParams<DataEntry>>, OrderingParams {}

interface PageNumberPaginatedDataEntryListOptions {
  params: PageNumberPaginatedDataEntryListParams
  signal?: AbortSignal
}

async function getPageNumberPaginatedDataEntryList(
  options: PageNumberPaginatedDataEntryListOptions,
) {
  const { params, ...requestOptions } = options
  return api.get<PageNumberPaginatedData<DataEntryDto>>(
    'data-entry/page-number-paginated',
    {
      ...requestOptions,
      params: mapPageNumberPaginatedDataEntryListParamsToDto(params),
    },
  )
    .then(data => ({
      ...data,
      results: data.results.map(mapDataEntryDto),
    }))
}

interface CursorDataEntryListParamsDto
  extends CursorPaginationParamsDto, QueryParams {}

interface CursorDataEntryListParams
  extends CursorPaginationParams {}

function mapCursorPaginatedDataEntryListParamsToDto(
  {
    ...paginationParams
  }: CursorDataEntryListParams,
): CursorDataEntryListParamsDto {
  return {
    ...mapCursorPaginationParamsToDto(paginationParams),
  }
}

interface CursorDataEntryListOptions {
  params: CursorDataEntryListParams
  signal?: AbortSignal
}

async function getCursorPaginatedDataEntryList(
  options: CursorDataEntryListOptions,
) {
  const { params, ...requestOptions } = options
  return api.get<CursorPaginatedData<DataEntryDto>>(
    'data-entry/cursor-paginated',
    {
      ...requestOptions,
      params: mapCursorPaginatedDataEntryListParamsToDto(params),
    },
  )
    .then(data => ({
      ...data,
      results: data.results.map(mapDataEntryDto),
    }))
}

export {
  getCursorPaginatedDataEntryList,
  getPageNumberPaginatedDataEntryList,
  mapDataEntryKeyToDtoKey,
}
export type {
  PageNumberPaginatedDataEntryListOptions,
  PageNumberPaginatedDataEntryListParams,
}
