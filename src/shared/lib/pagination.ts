interface BasePaginatedData<T> {
  results: T[]
}

interface PageNumberPaginatedData<T> extends BasePaginatedData<T> {
  count: number
  next: number | null
  previous: number | null
}

interface PageNumberPaginationParamsDto {
  page: number
  page_size: number
}

interface PageNumberPaginationParams {
  page: number
  pageSize: number
}

function mapPageNumberPaginationParamsDto(
  dto: PageNumberPaginationParamsDto,
): PageNumberPaginationParams {
  return {
    page: dto.page,
    pageSize: dto.page_size,
  }
}

function mapPageNumberPaginationParamsToDto(
  obj: PageNumberPaginationParams,
): PageNumberPaginationParamsDto {
  return {
    page: obj.page,
    page_size: obj.pageSize,
  }
}

export {
  mapPageNumberPaginationParamsDto,
  mapPageNumberPaginationParamsToDto,
}
export type {
  PageNumberPaginatedData,
  PageNumberPaginationParams,
  PageNumberPaginationParamsDto,
}
