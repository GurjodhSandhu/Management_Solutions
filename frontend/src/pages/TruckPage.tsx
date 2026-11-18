import TruckTable from '../features/trucks/components/TruckTable'
import { useTrucks } from '../features/trucks/hooks'
import TruckInputForm from "../features/trucks/components/TruckInputForm.tsx";

function TruckPage() {
    const { data, isLoading, error } = useTrucks()
    if (isLoading) return <p>Loading...</p>
    if (error) return <p>Failed to load trucks: {error.message}</p>

    return (
        <div>
            <h1>table</h1>
        <TruckTable trucks={data?.results ?? []} />
        <br/>
            <h2>input</h2>
            <TruckInputForm/>


    </div>
    )
}

export default TruckPage
