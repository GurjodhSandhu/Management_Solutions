import TruckTable from '../features/trucks/components/TruckTable'
import { useTrucks } from '../features/trucks/hooks'

function TruckPage() {
    const { data, isLoading, error } = useTrucks()
    if (isLoading) return <p>Loading...</p>
    if (error) return <p>Failed to load trucks: {error.message}</p>

    return <TruckTable trucks={data?.results ?? []} />
}

export default TruckPage
