import { useQuery } from '@tanstack/react-query'
import { getTrucks } from './api'

export function useTrucks() {
  return useQuery({
    queryKey: ['trucks'],
    queryFn: getTrucks,
  })
}