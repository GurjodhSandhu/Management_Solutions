from utils import Truck_util
from utils import driver_util
from database import truck_repository
from database import driver_repository

while True:
    print("""\n\n\nSelect option from below
1.add truck 
2.add driver
3.list trucks
4.list drivers
5.assign driver to truck
6.unassign driver from truck 
7.unassign truck from driver
8.exit
----------

""")

    option = input("select option:")
    if option == "1": #add truck
        truck = Truck_util.create_truck(Truck_util.get_truck_input()) #gets truck inputs from user creates truck object
        if truck == None:
            print("\n\nFailed to add truck: Try again")
            continue
        truck_repository.add_truck(**truck.to_dict())
        print("successfully added truck to database")

    elif option == "2":
        driver_input = driver_util.get_driver_input()
        driver = driver_util.create_driver(driver_input)
        if driver == None:
            print("\n\nfailed to create driver: try again")
            continue
        driver_repository.add_driver(**driver.to_dict())
        print("succesfully added driver to database")

    elif option == "3":
        try:
            truck_repository.list_all_trucks()
        except:
            print("failed to print all trucks")
        print("succesfully printed all trucks")

    elif option == "4":
        print()
    elif option == "5":
        print()
    elif option == "6":
        print()
    elif option == "7":
        print()
    elif option == "8":
        break



