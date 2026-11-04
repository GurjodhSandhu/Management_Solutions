export interface Truck {

  id: number
  vin: string
  brand?: string | null
  make?: string | null
  plate?: string | null
  year?: number | null
  mileage?: number | null
  truck_status?: 'IR'| 'AV' | 'UNAV' | 'OOS'
  truck_location?: 'IT'|'AT'|'AD'|'OR'

}