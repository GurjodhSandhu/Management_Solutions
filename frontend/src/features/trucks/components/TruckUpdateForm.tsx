import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useUpdateTruck } from '../hooks'
import { ApiError } from '../../../lib/apiClient'
import { TRUCK_LOCATION_LABELS } from '../types'
import type { Truck, TruckPatch, TruckLocation } from '../types'

/* ---------- 1. Validation rules (mirror core/models/truck.py) ---------- */
// Browser inputs always give you strings, so every field is a string here.
// Numbers are converted once, in toTruckPatch(), right before sending.

const optionalText = (max: number) =>
  z.string().trim().max(max, `Use ${max} characters or fewer`)

const optionalInteger = (label: string, min: number, max: number) =>
  z
    .string()
    .trim()
    .refine(
      (v) => v === '' || (/^\d+$/.test(v) && Number(v) >= min && Number(v) <= max),
      `${label} must be a whole number from ${min} to ${max}`,
    )

const truckFormSchema = z.object({
  vin: z.string().trim().length(17, 'VIN must be exactly 17 characters'),
  brand: optionalText(20),
  make: optionalText(20),
  plate: optionalText(10),
  year: optionalInteger('Year', 1900, 2100),
  mileage: optionalInteger('Mileage', 0, 2147483647),
  truck_location: z.enum(['IT', 'AT', 'AD', 'OR']),
})

type TruckFormValues = z.infer<typeof truckFormSchema>
type FieldName = keyof TruckFormValues

const FIELD_NAMES: FieldName[] = [
  'vin',
  'brand',
  'make',
  'plate',
  'year',
  'mileage',
  'truck_location',
]

/* ---------- 2. Text inputs described as data ---------- */

interface TextInputConfig {
  name: Exclude<FieldName, 'truck_location'>
  label: string
  maxLength: number
  required?: boolean
  inputMode?: 'numeric'
}

const TEXT_INPUTS: TextInputConfig[] = [
  { name: 'vin', label: 'VIN', maxLength: 17, required: true },
  { name: 'brand', label: 'Brand', maxLength: 20 },
  { name: 'make', label: 'Make', maxLength: 20 },
  { name: 'plate', label: 'Plate', maxLength: 10 },
  { name: 'year', label: 'Year', maxLength: 4, inputMode: 'numeric' },
  { name: 'mileage', label: 'Mileage', maxLength: 10, inputMode: 'numeric' },
]

const LOCATION_OPTIONS = Object.entries(TRUCK_LOCATION_LABELS) as [TruckLocation, string][]

/* ---------- 3. Conversions ---------- */

// API truck -> form values. Inputs need strings, and null/undefined become ''.
function truckToFormValues(truck: Truck): TruckFormValues {
  return {
    vin: truck.vin ?? '',
    brand: truck.brand ?? '',
    make: truck.make ?? '',
    plate: truck.plate ?? '',
    year: truck.year?.toString() ?? '',
    mileage: truck.mileage?.toString() ?? '',
    truck_location: truck.truck_location ?? 'AT',
  }
}

// Form values -> PATCH body.
// On PATCH, an omitted field means "leave unchanged", so a field the user cleared
// must be sent as null (your model allows null) or the old value would stay.
function toTruckPatch(values: TruckFormValues): TruckPatch {
  return {
    vin: values.vin,
    brand: values.brand || null,
    make: values.make || null,
    plate: values.plate || null,
    year: values.year === '' ? null : Number(values.year),
    mileage: values.mileage === '' ? null : Number(values.mileage),
    truck_location: values.truck_location,
  }
}

/* ---------- 4. The component ---------- */

interface TruckUpdateFormProps {
  truck: Truck
  onDone: () => void // called after a successful save (close the form, etc.)
  onCancel?: () => void
}

// Render with key={truck.id} in the parent so React rebuilds the form
// (and its default values) when a different truck is selected.
function TruckUpdateForm({ truck, onDone, onCancel }: TruckUpdateFormProps) {
  const updateTruck = useUpdateTruck()

  const {
    register,
    handleSubmit,
    setError,
    formState: { errors },
  } = useForm<TruckFormValues>({
    resolver: zodResolver(truckFormSchema),
    defaultValues: truckToFormValues(truck),
  })

  function onSubmit(values: TruckFormValues) {
    updateTruck.mutate(
      { id: truck.id, data: toTruckPatch(values) },
      {
        onSuccess: onDone,
        onError: (error) => {
          // The server is the final authority. Put its field messages next to the inputs.
          if (!(error instanceof ApiError)) return
          for (const name of FIELD_NAMES) {
            const message = error.fieldErrors[name]
            if (message) setError(name, { type: 'server', message })
          }
        },
      },
    )
  }

  // Form-level message only when the error isn't already shown on a field
  // (network down, 403, 429, 500, non-field validation errors...).
  const serverError = updateTruck.error
  const fieldErrors = serverError instanceof ApiError ? serverError.fieldErrors : {}
  const hasFieldErrors = FIELD_NAMES.some((name) => fieldErrors[name])

  return (
    // noValidate: let our messages show instead of the browser's default popups.
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      {TEXT_INPUTS.map(({ name, label, required, ...inputProps }) => (
        <div key={name}>
          <label htmlFor={name}>
            {label}
            {!required && ' (optional)'}
          </label>
          <input
            id={name}
            autoComplete="off"
            aria-required={required}
            aria-invalid={errors[name] ? true : undefined}
            aria-describedby={errors[name] ? `${name}-error` : undefined}
            {...inputProps}
            {...register(name)}
          />
          {errors[name] && (
            <p id={`${name}-error`} role="alert">
              {errors[name]?.message}
            </p>
          )}
        </div>
      ))}

      <div>
        <label htmlFor="truck_location">Location</label>
        <select
          id="truck_location"
          aria-invalid={errors.truck_location ? true : undefined}
          aria-describedby={errors.truck_location ? 'truck_location-error' : undefined}
          {...register('truck_location')}
        >
          {LOCATION_OPTIONS.map(([value, label]) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
        {errors.truck_location && (
          <p id="truck_location-error" role="alert">
            {errors.truck_location.message}
          </p>
        )}
      </div>

      <button type="submit" disabled={updateTruck.isPending}>
        {updateTruck.isPending ? 'Saving…' : 'Save changes'}
      </button>
      {onCancel && (
        <button type="button" onClick={onCancel} disabled={updateTruck.isPending}>
          Cancel
        </button>
      )}

      {serverError && !hasFieldErrors && <p role="alert">{serverError.message}</p>}
    </form>
  )
}

export default TruckUpdateForm
