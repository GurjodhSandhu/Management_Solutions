from service import truck_service
from service import driver_service
from models.truck import Truck
from models.driver import Driver
while True:
    print("""\n\n\nSelect option from below
1.add truck 
2.add driver
3.list trucks
4.list drivers
5.update truck info
6.update driver info
7.
8.
9.exit
----------

""")
    #test_truck = truck(None,"12345678910234567","ford","shelby","2001",20000,"ab632s")
    test_driver = Driver(driver_name = "newpydantic", driver_licensenumber= "9723")
    test_truck = Truck(vin="1234asdfqwer12345", brand="Volvo", make="DB4F", year=2020, mileage=1500,plate="V2A3D2")

    option = input("select option:")
    if option == "1": #add truck to database
        print(truck_service.add_truck(test_truck))

    elif option == "2": #add driver to database
        print(driver_service.add_driver(test_driver))

    elif option == "3": #list all trucks
        truck_service.list_trucks()

    elif option == "4": #list all drivers
        try:
            driver_service.list_drivers()
        except Exception as e:
            print(e)

    elif option == "5": #update a truck in database via a changes dictionary
        try:
            test_truck = truck_service.get_truck(17)
            test_truck.add_mileage(6000)
            truck_service.update_trucks(test_truck.truck_id, test_truck.model_dump(exclude={"truck_id", "assigned_driver_id"}))
            truck_service.list_trucks()
        except Exception as e:
            print(e)

    elif option == "6": #upload driver changes into database
        try:
            test_driver = driver_service.get_driver()
            test_driver.driver_name = "what"
            driver_service.update_drivers(test_driver.driver_id, test_driver.model_dump(exclude={"driver_id", "assigned_truck_id"}))
            driver_service.list_drivers()
        except Exception as e:
            print(e)



    elif option == "7":
        print()
    elif option == "8":
        print()
    elif option == "9":
        break



