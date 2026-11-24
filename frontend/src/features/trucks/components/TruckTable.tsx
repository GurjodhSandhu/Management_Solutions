import type { Truck } from "../types"

interface TruckTableProps {
  trucks: Truck[]
  onEdit: (truck: Truck) => void // the table only reports the click; the page decides what happens
    onDelete: (truck: Truck) => void
}

function TruckTable({ trucks, onEdit, onDelete }: TruckTableProps) {
 if (trucks.length === 0) {
    return <p>No trucks yet</p>
  }
    return (
        <table>
            <thead>
            <tr>
                <th>VIN</th>
                <th>Brand</th>
                <th>Status</th>
                <th>Make</th>
                <th>location</th>
                <th>Plate</th>
                <th>Mileage</th>

            </tr>
            </thead>
            <tbody>
            {trucks.map((truck) => (
                <tr key={truck.id}>
                    <td>{truck.vin?? '-'}</td>
                    <td>{truck.brand ?? '-'}</td>
                    <td>{truck.truck_status ?? '-' }</td>
                    <td>{truck.make ?? '-'}</td>
                    <td>{truck.truck_location ?? '-' }</td>
                    <td>{truck.plate ?? '-'}</td>
                    <td>{truck.mileage ?? '-'}</td>
                    <td>
              <button type="button" onClick={() => onEdit(truck)}>
                Edit
              </button>
                        <button type="button" onClick={() => onDelete(truck)}>
                Delete
              </button>

                    </td>
                </tr>
            ))}

            </tbody>
        </table>

    )
}


export default TruckTable;