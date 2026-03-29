from management_solutions.models.Truck import truck
from management_solutions.utils.Truck_util import get_truck_input
from management_solutions.utils.Truck_util import new_truck

#testing code:
#truck1 = new_truck(get_truck_input())

testDictionary = {"vin":"12345678901234567","brand": "volvo","make": "vnl","year": 2126,"mileage": -1150,"plate": "2xe5m3"}
TruckTest = new_truck(testDictionary)

trucktest1 = truck()

if TruckTest is not None:
    print(TruckTest.vin)


#if truck1 == None :
    #print("try again")
    #truck1 = new_truck(get_truck_input())
#if truck1 != None:
    #print(truck1.vin, truck1.mileage)
