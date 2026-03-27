from management_solutions.models.Truck import truck
from management_solutions.utils.Truck_util import get_truck_input

print("test")
kwarg = get_truck_input()
truck1 = truck(**kwarg)
print(truck1.year)
