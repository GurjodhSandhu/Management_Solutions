from management_solutions.models.Truck import truck
from management_solutions.utils.Truck_util import get_truck_input
from management_solutions.utils.Truck_util import create_truck
from management_solutions.utils.driver_util import create_driver
from management_solutions.utils.driver_util import get_driver_input
from management_solutions.services.Driver_truck_services import assign_driver_to_truck
from management_solutions.services.Driver_truck_services import unassign_truck_from_driver

#testing code:
truck15 = create_truck({"truck_id": 10})
driver15 = create_driver({"driver_id": 15, "driver_name": "greg", "assigned_truck_id": 1})
driver16 = create_driver({"driver_id": 16, "driver_name": "gregery"})

drivers = {driver15.driver_id: driver15, driver16.driver_id: driver16} #dictionary of drivers
truckers = {truck15.truck_id: truck15} #key is truck_id which correlates to a object

print(assign_driver_to_truck(15,10,truckers,drivers))
print(drivers.get(15).assigned_truck_id)
print(assign_driver_to_truck(16,10,truckers,drivers))
print(drivers.get(15).assigned_truck_id)

print(unassign_truck_from_driver(15,truckers,drivers))
print(unassign_truck_from_driver(16,truckers,drivers))

