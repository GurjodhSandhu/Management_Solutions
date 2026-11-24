import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useCreateDriver } from '../hooks'
import { ApiError } from '../../../lib/apiClient'
import { DRIVER_STATUS_LABELS } from '../types'
import type { DriverInput, DriverStatus } from '../types'


const driverFormSchema = z.object({
  driver_name: z.string(),
  driver_licensenumber: z.string(),
  driver_status: z.enum(['AV','UNAV']),
})

type DriverFormValues = z.infer<typeof driverFormSchema>
type FieldName = keyof DriverFormValues

const FIELD_NAMES: FieldName[] = [
  'driver_name',
  'driver_licensenumber',
  'driver_status',
]

const defaultValues: DriverFormValues = {
  driver_name: '',
  driver_licensenumber: '',
  driver_status: 'AV',
}

/* ---------- 2. Describe the text inputs as data, not copy-pasted JSX ---------- */
// Adding a field later = adding one line here (plus one line in the schema).

interface TextInputConfig {
  name: FieldName
  label: string
}

const TEXT_INPUTS: TextInputConfig[] = [
  { name: 'driver_name', label: 'Driver name'},
  { name: 'driver_licensenumber', label: 'License Number'},

]

const STATUS_OPTIONS = Object.entries(DRIVER_STATUS_LABELS) as [DriverStatus, string][]

/* ---------- 3. Form values -> API payload ---------- */
// Blank optional fields are omitted entirely (undefined is dropped by JSON.stringify),
// instead of being sent as "" and stored as empty strings.

function toDriverInput(values: DriverFormValues): DriverInput {
  return {
    driver_name: values.driver_name,
    driver_licensenumber: values.driver_licensenumber || undefined,
    driver_status: values.driver_status,
  }
}

/* ---------- 4. The component ---------- */

function DriverInputForm() {
  const createDriver = useCreateDriver()

  const {
    register,
    handleSubmit,
    reset,
    setError,
    formState: { errors },
  } = useForm<DriverFormValues>({
    resolver: zodResolver(driverFormSchema),
    defaultValues,
  })

  function onSubmit(values: DriverFormValues) {
    createDriver.mutate(toDriverInput(values), {
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
  const serverError = createDriver.error
  const fieldErrors = serverError instanceof ApiError ? serverError.fieldErrors : {}
  const hasFieldErrors = FIELD_NAMES.some((name) => fieldErrors[name])

  return (
    // noValidate: let our messages show instead of the browser's default popups.
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      {TEXT_INPUTS.map(({ name, label, ...inputProps }) => (
        <div key={name}>
          <label htmlFor={name}>
            {label}
          </label>
          <input
            id={name}
            autoComplete="off"
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
        <label htmlFor="driver_status">Status</label>
        <select
          id="driver_status"
          aria-invalid={errors.driver_status ? true : undefined}
          aria-describedby={errors.driver_status ? 'driver_status-error' : undefined}
          {...register('driver_status')}
        >
          {STATUS_OPTIONS.map(([value, label]) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
        {errors.driver_status && (
          <p id="driver_status-error" role="alert">
            {errors.driver_status.message}
          </p>
        )}
      </div>

      <button type="submit" disabled={createDriver.isPending}>
        {createDriver.isPending ? 'Saving…' : 'Create driver'}
      </button>

      {serverError && !hasFieldErrors && <p role="alert">{serverError.message}</p>}
      {createDriver.isSuccess && <p role="status">Driver created.</p>}
    </form>
  )
}

export default DriverInputForm
