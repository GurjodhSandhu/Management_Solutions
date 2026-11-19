export type TruckStatus = 'IR' | 'AV' | 'UNAV' | 'OOS'
export type TruckLocation = 'IT' | 'AT' | 'AD' | 'OR'

// What the API returns.
export interface Truck {
  id: number
  vin: string
  brand?: string | null
  make?: string | null
  plate?: string | null
  year?: number | null
  mileage?: number | null
  truck_status?: TruckStatus
  truck_location?: TruckLocation
}

// What the client is allowed to send when creating a truck.
// No `id` (server assigns it) and no `truck_status` (read-only in your serializer,
// the backend decides it). Optional fields are omitted when left blank.
export interface TruckInput {
  vin: string
  brand?: string
  make?: string
  plate?: string
  year?: number
  mileage?: number
  truck_location?: TruckLocation
}

// Display labels for the codes the backend uses. Mirrors Truck.TruckLocation in Django.
export const TRUCK_LOCATION_LABELS: Record<TruckLocation, string> = {
  AT: 'At depot',
  IT: 'In transit',
  OR: 'On route',
  AD: 'Arrived at destination',
}

export type TruckPatch = {
  [K in keyof TruckInput]?: TruckInput[K] | null
}