import type { Paginated } from '../../lib/types.ts'
import type {Driver, DriverInput, DriverPatch} from './types.ts'
import { apiClient } from "../../lib/apiClient.ts";

export function getDriver() {
  return apiClient<Paginated<Driver>>('/api/drivers/')
}

export function createDriver(data: DriverInput) {
  return apiClient<Driver>('/api/drivers/', { method: 'POST', body: data })
}

export function updateDriver({ id, data }: { id: number; data: DriverPatch }) {
  return apiClient<Driver>(`/api/drivers/${id}/`, { method: 'PATCH', body: data })
}

export function deleteDriver(id: number) {
  return apiClient<Driver>(`/api/drivers/${id}/`, { method: 'DELETE' })
}