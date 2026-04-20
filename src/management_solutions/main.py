from management_solutions.models.Truck import truck
from management_solutions.utils.Truck_util import get_truck_input
from management_solutions.utils.Truck_util import create_truck
from management_solutions.utils.driver_util import create_driver
from management_solutions.utils.driver_util import get_driver_input
from management_solutions.services.Driver_truck_services import assign_driver_to_truck
from management_solutions.services.Driver_truck_services import unassign_truck_from_driver

#testing code:
try:
    truck15 = create_truck({"truck_id": 10,"year": 2000})
    truck15.mileage = 2105
    truck15.remove_mileage()
except ValueError as e:
    print(e)

driver15 = create_driver({"driver_id": 15, "driver_name": "greg", "assigned_truck_id": 1})
driver16 = create_driver({"driver_id": 16, "driver_name": "gregery"})
