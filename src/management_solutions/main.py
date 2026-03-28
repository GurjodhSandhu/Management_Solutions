from management_solutions.models.Truck import truck
from management_solutions.utils.Truck_util import get_truck_input
from management_solutions.utils.Truck_util import new_truck

#testing code:
truck1 = new_truck(get_truck_input())
if truck1 == None :
    print("try again")
    truck1 = new_truck(get_truck_input())
if truck1 != None:
    print(truck1.year)
