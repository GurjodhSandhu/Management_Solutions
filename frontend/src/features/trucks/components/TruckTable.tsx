import type { Truck } from "../types"
//import { mockTruckPage} from ".../features/trucks/mockdata.ts";
//import TruckCard from "./TruckCard.tsx";

function TruckTable({ trucks }: {trucks: Truck[]}) {
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
                    <td>{truck.vin}</td>
                    <td>{truck.brand ?? '-'}</td>
                    <td>{truck.truck_status}</td>
                    <td>{truck.make}</td>
                    <td>{truck.truck_location}</td>
                    <td>{truck.plate}</td>
                    <td>{truck.mileage}</td>
                </tr>
            ))}

            </tbody>
        </table>






    )

}


export default TruckTable;