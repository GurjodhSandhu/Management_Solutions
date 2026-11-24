import { useState } from 'react'
import TruckTable from '../features/trucks/components/TruckTable'
import TruckInputForm from '../features/trucks/components/TruckInputForm'
import TruckUpdateForm from '../features/trucks/components/TruckUpdateForm'
import { useTrucks, useDeleteTruck } from '../features/trucks/hooks'
import type {Truck} from "../features/trucks/types.ts";

function TruckPage() {
  const { data, isLoading, error } = useTrucks()
  const deleteTruck = useDeleteTruck()

  function handleDelete(truck: Truck) {
    if (!window.confirm(`Delete truck ${truck.vin ?? truck.id}?`)) return
    deleteTruck.mutate(truck.id, {
      onSuccess: () => {
        if (editingId === truck.id) setEditingId(null) // close the edit form if it was open on this truck
      },
    })
  }

  // when the list refreshes after a save. Looking it up from the list keeps it current.
  const [editingId, setEditingId] = useState<number | null>(null)
  const editingTruck = data?.results.find((truck) => truck.id === editingId) ?? null

  function closeEditor() {
    setEditingId(null)
  }

  return (
    <div>
      <h1>Trucks</h1>

      {isLoading && <p>Loading trucks…</p>}
      {error && <p role="alert">Couldn't load trucks: {error.message}</p>}
      {data && (
        <TruckTable trucks={data.results} onEdit={(truck) => setEditingId(truck.id)} onDelete={handleDelete} />
      )}

      {editingTruck ? (
        <>
          <h2>Edit truck</h2>
          {/* key makes React rebuild the form with the right values when you switch trucks */}
          <TruckUpdateForm
            key={editingTruck.id}
            truck={editingTruck}
            onDone={closeEditor}
            onCancel={closeEditor}
          />
        </>
      ) : (
        <>


          <h2>Add a truck</h2>
          <TruckInputForm />
        </>
      )}
    </div>
  )
}

export default TruckPage