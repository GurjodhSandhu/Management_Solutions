from management_solutions.models.Truck import truck
from management_solutions.utils.Truck_util import get_truck_input
from management_solutions.utils.Truck_util import new_truck

print("test")

kwarg = get_truck_input() #dictionary with information on truck is created from user inputs
truck1 = new_truck(kwarg) #method is used to create the new object

print(truck1.year)



input("again?:")
