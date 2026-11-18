import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { createTruck, getTrucks } from './api'

export function useTrucks() {
  return useQuery({
    queryKey: ['trucks'],
    queryFn: getTrucks,
  })
}

export function useCreateTruck() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: createTruck,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['trucks'] })
    },
  })
}