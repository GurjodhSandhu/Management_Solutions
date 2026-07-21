from utils import Truck_util
from utils import driver_util
from database import truck_repository
from database import driver_repository
from models.Truck import truck
from models.Driver import driver
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
    test_truck = truck(None,"12345678910234567","ford","shelby","2001",20000,"ab632s")
    test_driver = driver(None,None,"bob","9723")
    option = input("select option:")
    if option == "1": #add truck to database
        print(Truck_util.add_truck(test_truck))

    elif option == "2": #add driver to database
        driver_util.add_driver(test_driver)

    elif option == "3": #list all trucks
        Truck_util.list_trucks()

    elif option == "4": #list all drivers
       driver_util.list_drivers()

    elif option == "5": #update a truck in database via a changes dictionary
        test_truck = Truck_util.get_truck(14)
        test_truck.add_mileage(6000)
        changes = {"mileage": test_truck.mileage}
        Truck_util.update_trucks(test_truck.truck_id,changes)
        Truck_util.list_trucks()

    elif option == "6": #upload driver changes into database
        test_driver = driver_util.get_driver(2)
        test_driver.driver_name = "name"
        changes = {"driver_name": test_driver.driver_name}
        driver_util.update_drivers(test_driver.driver_id,changes)
        driver_util.list_drivers()

    elif option == "7":
        print()
    elif option == "8":
        print()
    elif option == "9":
        break



