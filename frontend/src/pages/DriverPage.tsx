import { useState } from 'react'
import DriverTable from '../features/drivers/components/DriverTable'
import DriverInputForm from '../features/drivers/components/DriverInputForm'
import DriverUpdateForm from '../features/drivers/components/DriverUpdateForm'
import { useDrivers, useDeleteDriver } from '../features/drivers/hooks'
import type {Driver} from "../features/drivers/types.ts";

function DriverPage() {
  const { data, isLoading, error } = useDrivers()
  const deleteTruck = useDeleteDriver()

  function handleDelete(driver: Driver) {
    if (!window.confirm(`Delete driver ${driver.driver_name}?`)) return
    deleteTruck.mutate(driver.id, {
      onSuccess: () => {
        if (editingId === driver.id) setEditingId(null) // close the edit form if it was open on this truck
      },
    })
  }

  // when the list refreshes after a save. Looking it up from the list keeps it current.
  const [editingId, setEditingId] = useState<number | null>(null)
  const editingDriver = data?.results.find((driver) => driver.id === editingId) ?? null

  function closeEditor() {
    setEditingId(null)
  }

  return (
    <div>
      <h1>Drivers</h1>

      {isLoading && <p>Loading drivers…</p>}
      {error && <p role="alert">Couldn't load drivers: {error.message}</p>}
      {data && (
        <DriverTable drivers={data.results} onEdit={(driver) => setEditingId(driver.id)} onDelete={handleDelete} />
      )}

      {editingDriver ? (
        <>
          <h2>Edit driver</h2>
          {/* key makes React rebuild the form with the right values when you switch trucks */}
          <DriverUpdateForm
            key={editingDriver.id}
            driver={editingDriver}
            onDone={closeEditor}
            onCancel={closeEditor}
          />
        </>
      ) : (
        <>


          <h2>Add a Driver</h2>
          <DriverInputForm />
        </>
      )}
    </div>
  )
}

export default DriverPage