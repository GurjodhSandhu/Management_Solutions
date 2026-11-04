import type { Truck } from "../types"
//import { mockTruckPage} from ".../features/trucks/mockdata.ts";
//import TruckCard from "./TruckCard.tsx";

function TruckList({ trucks }: {trucks: Truck[]}) {
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
            </tr>
            </thead>
            <tbody>
            {trucks.map((truck) => (
                <tr key={truck.id}>
                    <td>{truck.vin}</td>
                    <td>{truck.brand ?? '-'}</td>
                    <td>{truck.truck_status}</td>
                </tr>



            ))}

            </tbody>


        </table>






    )

}


export default TruckList;