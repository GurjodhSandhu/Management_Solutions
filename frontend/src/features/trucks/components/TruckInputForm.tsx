import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useCreateTruck } from '../hooks'
import { ApiError } from '../../../lib/apiClient'
import { TRUCK_LOCATION_LABELS } from '../types'
import type { TruckInput, TruckLocation } from '../types'

/* ---------- 1. Validation rules (mirror core/models/truck.py) ---------- */
// Browser inputs always give you strings, so every field is a string here.
// We convert to numbers once, in toTruckInput(), right before sending.

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

const defaultValues: TruckFormValues = {
  vin: '',
  brand: '',
  make: '',
  plate: '',
  year: '',
  mileage: '',
  truck_location: 'AT', // matches the model default: new trucks start at the depot
}

/* ---------- 2. Describe the text inputs as data, not copy-pasted JSX ---------- */
// Adding a field later = adding one line here (plus one line in the schema).

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

/* ---------- 3. Form values -> API payload ---------- */
// Blank optional fields are omitted entirely (undefined is dropped by JSON.stringify),
// instead of being sent as "" and stored as empty strings.

function toTruckInput(values: TruckFormValues): TruckInput {
  return {
    vin: values.vin,
    brand: values.brand || undefined,
    make: values.make || undefined,
    plate: values.plate || undefined,
    year: values.year === '' ? undefined : Number(values.year),
    mileage: values.mileage === '' ? undefined : Number(values.mileage),
    truck_location: values.truck_location,
  }
}

/* ---------- 4. The component ---------- */

function TruckInputForm() {
  const createTruck = useCreateTruck()

  const {
    register,
    handleSubmit,
    reset,
    setError,
    formState: { errors },
  } = useForm<TruckFormValues>({
    resolver: zodResolver(truckFormSchema),
    defaultValues,
  })

  function onSubmit(values: TruckFormValues) {
    createTruck.mutate(toTruckInput(values), {
      onSuccess: () => reset(defaultValues),
      onError: (error) => {
        // The server is the final authority (e.g. rules we can't check in the browser).
        // Put its field messages next to the matching inputs.
        if (!(error instanceof ApiError)) return
        for (const name of FIELD_NAMES) {
          const message = error.fieldErrors[name]
          if (message) setError(name, { type: 'server', message })
        }
      },
    })
  }

  // Show a form-level message only when the error isn't already shown on a field
  // (network down, 403, 429, 500, non-field validation errors...).
  const serverError = createTruck.error
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

      <button type="submit" disabled={createTruck.isPending}>
        {createTruck.isPending ? 'Saving…' : 'Create truck'}
      </button>

      {serverError && !hasFieldErrors && <p role="alert">{serverError.message}</p>}
      {createTruck.isSuccess && <p role="status">Truck created.</p>}
    </form>
  )
}

export default TruckInputForm
