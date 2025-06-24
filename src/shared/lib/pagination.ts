interface BasePaginatedData<T> {
  results: T[]
}

interface PageNumberPaginatedData<T> extends BasePaginatedData<T> {
  count: number
  next: number | null
  previous: number | null
}

interface CursorPaginatedData<T> extends BasePaginatedData<T> {
  next: string | null
  previous: string | null
}

interface PageNumberPaginationParamsDto {
  page: number
  page_size: number
}

interface PageNumberPaginationParams {
  page: number
  pageSize: number
}

interface CursorPaginationParamsDto {
  cursor?: string
  page_size: number
}
interface CursorPaginationParams {
  cursor?: string
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

function mapCursorPaginationParamsToDto(
  obj: CursorPaginationParams,
): CursorPaginationParamsDto {
  return {
    cursor: obj.cursor,
    page_size: obj.pageSize,
  }
}

export {
  mapCursorPaginationParamsToDto,
  mapPageNumberPaginationParamsDto,
  mapPageNumberPaginationParamsToDto,
}
export type {
  CursorPaginatedData,
  CursorPaginationParams,
  PageNumberPaginatedData,
  PageNumberPaginationParams,
  PageNumberPaginationParamsDto,CursorPaginationParamsDto
}
