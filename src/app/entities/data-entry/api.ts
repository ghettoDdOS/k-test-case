import type { DataEntryDto } from './model'

import api from '@/shared/api'

import { mapDataEntryDto } from './model'

async function getDataEntryList() {
  return api.get<DataEntryDto[]>('data-entry/')
    .then(data => data.map(mapDataEntryDto))
}

export { getDataEntryList }
