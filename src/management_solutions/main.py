from management_solutions.models.Truck import truck
from management_solutions.utils.Truck_util import get_truck_input
from management_solutions.utils.Truck_util import create_truck

#testing code:
#truck1 = new_truck(get_truck_input())

testDictionary = {"vin":"1234678901234567","brand": "volvo","make": "vnl","year": 2126,"mileage": -1150,"plate": "2xe5m3"}
TruckTest = create_truck(testDictionary)

trucktest1 = truck()
trucktest2 = get_truck_input()
