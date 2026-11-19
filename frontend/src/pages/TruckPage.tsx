import TruckTable from '../features/trucks/components/TruckTable'
import TruckInputForm from '../features/trucks/components/TruckInputForm'
import { useTrucks } from '../features/trucks/hooks'

function TruckPage() {
  const { data, isLoading, error } = useTrucks()

  // Only the table depends on the fetch. The form renders regardless,
  // so a slow or failed list request never hides it.
  return (
    <div>
      <h1>Trucks</h1>

      {isLoading && <p>Loading trucks…</p>}
      {error && <p role="alert">Couldn't load trucks: {error.message}</p>}
      {data && <TruckTable trucks={data.results} />}

      <h2>Add a truck</h2>
      <TruckInputForm />

    </div>
  )
}

export default TruckPage