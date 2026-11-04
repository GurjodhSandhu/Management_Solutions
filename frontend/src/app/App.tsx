//import TruckCard from '../features/trucks/components/TruckCard';
import { mockTruckPage} from "../features/trucks/mockdata.ts";
import TruckList from "../features/trucks/components/TruckList.tsx";
function App() {

  const trucks = mockTruckPage.results
  return <TruckList trucks={trucks} />
}

export default App