import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {createDriver, getDriver, updateDriver, deleteDriver} from './api'

export function useDrivers() {
  return useQuery({
    queryKey: ['drivers'],
    queryFn: getDriver,
  })
}

export function useCreateDriver() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: createDriver,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['drivers'] })
    },
  })
}

export function useUpdateDriver() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: updateDriver,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['drivers'] })
    },
  })
}
export function useDeleteDriver() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: deleteDriver,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['drivers'] })
    },
  })
}