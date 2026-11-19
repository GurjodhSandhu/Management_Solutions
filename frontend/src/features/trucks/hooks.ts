import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {createTruck, getTrucks, updateTruck, deleteTruck} from './api'

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

export function useUpdateTruck() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: updateTruck,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['trucks'] })
    },
  })
}
export function useDeleteTruck() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: deleteTruck,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['trucks'] })
    },
  })
}