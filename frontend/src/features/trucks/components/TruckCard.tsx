import type { Truck } from "../types"

function TruckCard({ truck }: { truck: Truck })
{
return <div className="truck-card">
    <h3>{truck.vin}</h3>
    <p>{truck.id}</p>
    <p>{truck.brand}</p>
    <p>{truck.truck_status}</p>
    <p>{truck.truck_location}</p>
    <p>truck.make</p>
    <p>truck.year</p>
    <p>truck.mileage</p>

</div>
}

export default TruckCard;