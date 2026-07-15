from utils import Truck_util
from database import truck_repository
from utils.exceptions import ValidationError
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
        print()
    elif option == "3":
        print()
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



