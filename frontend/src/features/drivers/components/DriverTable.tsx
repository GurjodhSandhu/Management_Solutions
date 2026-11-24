import type { Driver } from "../types"

interface DriverTableProps {
  drivers: Driver[]
  onEdit: (driver: Driver) => void // the table only reports the click; the page decides what happens
    onDelete: (driver: Driver) => void
}

function DriverTable({ drivers, onEdit, onDelete }: DriverTableProps) {
 if (drivers.length === 0) {
    return <p>No trucks yet</p>
  }
    return (
        <table>
            <thead>
            <tr>
                <th>name</th>
                <th>licensenumber</th>
                <th>status</th>
                <th>truck</th>


            </tr>
            </thead>
            <tbody>
            {drivers.map((driver) => (
                <tr key={driver.id}>
                    <td>{driver.driver_name?? '-'}</td>
                    <td>{driver.driver_licensenumber?? '-'}</td>
                    <td>{driver.driver_status?? '-'}</td>
                    <td>{driver.truck_id?? '-'}</td>
                    <td>
              <button type="button" onClick={() => onEdit(driver)}>
                Edit
              </button>
                        <button type="button" onClick={() => onDelete(driver)}>
                Delete
              </button>

                    </td>
                </tr>

            ))}

            </tbody>
        </table>

    )
}


export default DriverTable;