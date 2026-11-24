import { Providers } from './providers'
import TruckPage from '../pages/TruckPage'
import DriverPage from '../pages/DriverPage'

function App() {
  return (
    <Providers>
        
      <TruckPage />
        <DriverPage />
    </Providers>
  )
}

export default App