type FilterOperationSuffix = 'eq' | 'lt' | 'gt' | 'icontains'

type FilteringParamsDto<T = unknown> = Record<
`${Extract<keyof T, string>}__${FilterOperationSuffix}`,
  string | undefined
>
type FilteringParams<T = unknown> = Record<
`${Extract<keyof T, string>}${Capitalize<FilterOperationSuffix>}`,
  string | undefined
>

export type { FilteringParams, FilteringParamsDto }
