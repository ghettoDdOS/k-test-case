import type { DataEntryDto } from './model'
import type { QueryParams } from '@/shared/api'
import type {
  PageNumberPaginatedData,
  PageNumberPaginationParams,
  PageNumberPaginationParamsDto,
} from '@/shared/lib/pagination'

import api from '@/shared/api'
import { mapPageNumberPaginationParamsToDto } from '@/shared/lib/pagination'

import { mapDataEntryDto } from './model'

interface PageNumberPaginatedDataEntryListParamsDto
  extends PageNumberPaginationParamsDto, QueryParams {}

interface PageNumberPaginatedDataEntryListParams
  extends PageNumberPaginationParams {}

function mapPageNumberPaginatedDataEntryListParamsToDto(
  obj: PageNumberPaginatedDataEntryListParams,
): PageNumberPaginatedDataEntryListParamsDto {
  return {
    ...mapPageNumberPaginationParamsToDto(obj),
  }
}

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

export { getPageNumberPaginatedDataEntryList }
export type { PageNumberPaginatedDataEntryListOptions }
