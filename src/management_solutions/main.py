from management_solutions.models.Truck import truck
from management_solutions.utils.Truck_util import get_truck_input
from management_solutions.utils.Truck_util import create_truck
from management_solutions.utils.driver_util import create_driver
from management_solutions.utils.driver_util import get_driver_input

#testing code:
truck15 = create_truck({"assigned_driver_id": 15})
driver15 = create_driver({"driver_id": 15, "driver_name": "greg"})
driver = {driver15.driver_id: driver15} #dictionary of drivers
print(truck15.assigned_driver_id)
print(driver.get(truck15.assigned_driver_id).driver_name)
