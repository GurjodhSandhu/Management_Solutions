import type { Paginated } from '../../lib/types.ts'
import type {Truck, TruckInput, TruckPatch} from './types.ts'
import { apiClient } from "../../lib/apiClient.ts";

export function getTrucks() {
  return apiClient<Paginated<Truck>>('/api/trucks/')
}

export function createTruck(data: TruckInput) {
  return apiClient<Truck>('/api/trucks/', { method: 'POST', body: data })
}

export function updateTruck({ id, data }: { id: number; data: TruckPatch }) {
  return apiClient<Truck>(`/api/trucks/${id}/`, { method: 'PATCH', body: data })
}