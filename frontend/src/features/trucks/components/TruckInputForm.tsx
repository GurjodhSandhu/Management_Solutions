import { useState } from 'react'
import { useCreateTruck } from '../hooks'

function TruckInputForm() {
  const createTruck = useCreateTruck()

  const [vin, setVin] = useState('')
  const [brand, setBrand] = useState('')
  const [make, setMake] = useState('')
  const [plate, setPlate] = useState('')

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()

    createTruck.mutate({
      vin,
      brand,
      make,
      plate,
      truck_status: 'AV',
      truck_location: 'IT',
    })
  }

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>VIN</label>
        <input
          value={vin}
          onChange={(e) => setVin(e.target.value)}
        />
      </div>

      <div>
        <label>Brand</label>
        <input
          value={brand}
          onChange={(e) => setBrand(e.target.value)}
        />
      </div>

      <div>
        <label>Make</label>
        <input
          value={make}
          onChange={(e) => setMake(e.target.value)}
        />
      </div>

      <div>
        <label>Plate</label>
        <input
          value={plate}
          onChange={(e) => setPlate(e.target.value)}
        />
      </div>

      <button
        type="submit"
        disabled={createTruck.isPending}
      >
        {createTruck.isPending ? 'Saving...' : 'Create Truck'}
      </button>

     {createTruck.error && (
    <p>{createTruck.error.message}</p>
)}
    </form>
  )
}

export default TruckInputForm
