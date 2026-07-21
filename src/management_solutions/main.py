from utils import Truck_util
from utils import driver_util
from database import truck_repository
from database import driver_repository
from models.Truck import truck
while True:
    print("""\n\n\nSelect option from below
1.add truck 
2.add driver
3.list trucks
4.list drivers
5.update truck info
6.unassign driver from truck 
7.unassign truck from driver
8.assign driver to truck
9.exit
----------

""")
    test_truck = truck(None,"12345678910234567","ford","shelby","2001","20000","ab632s")
    option = input("select option:")
    if option == "1": #add truck
        print(Truck_util.add_truck(test_truck))
    elif option == "2":
        driver_input = driver_util.get_driver_input()
        driver = driver_util.create_driver(driver_input)
        if driver == None:
            print("\n\nfailed to create driver: try again")
            continue
        driver_repository.add_driver(**driver.to_dict())
        print("succesfully added driver to database")

    elif option == "3":
        Truck_util.list_trucks()

    elif option == "4":
        try:
            driver_repository.list_all_drivers()
        except:
            print("failed to print all drivers")
        print("succesfully printed all drivers")

    elif option == "5":
        truck_id = int(input("input truck id: "))
        Truck_util.update_trucks(truck_id,test_truck)

    elif option == "6":
        driver = driver_util.create_driver(driver_util.get_driver_input())
        driver_id = int(input("input driver id: "))
        try:
            driver_repository.update_driver(driver_id,**driver.to_dict())
        except ValueError as e:
            print(e)
    elif option == "7":
        try:
            print(driver_repository.retrieve_driver("1"))
        except ValueError as e:
            print(e)
    elif option == "7":
        print()
    elif option == "9":
        break



