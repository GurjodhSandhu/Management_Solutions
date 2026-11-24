export type DriverStatus = 'AV' | 'UNAV'

// What the API returns.
export interface Driver {
  id: number
  driver_name: string
  driver_licensenumber?: string | null
  driver_status?: DriverStatus
  truck?: string | null
  truck_id?: number | null

}

// What the client is allowed to send when creating a driver.
// No `id` (server assigns it) and no `truck_status` (read-only in your serializer,
// the backend decides it). Optional fields are omitted when left blank.
export interface DriverInput {
  driver_name: string
  driver_licensenumber?: string
  driver_status?: DriverStatus
  truck_id?: string

}

// Display labels for the codes the backend uses. Mirrors Driver.driverstatus in Django.
export const DRIVER_STATUS_LABELS: Record<DriverStatus, string> = {
  AV: 'AVAILABLE',
  UNAV: 'UNAVAILABLE',
}

export type DriverPatch = {
  [K in keyof DriverInput]?: DriverInput[K] | null
}